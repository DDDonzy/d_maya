from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cSkinDeform import CythonSkinDeformer

import ctypes
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr

import maya.OpenMaya as om1  # type:ignore

from . import cBoundingBoxCython
from . import cColorCython
from .cMemoryView import CMemoryManager
from ._cRegistry import GLOBAL_DEFORMER_REGISTRY, GLOBAL_BRUSH_REGISTRY


def maya_useNewAPI():
    pass


NODE_NAME = "WeightPreviewShape"
NODE_ID = om.MTypeId(0x80005)
DRAW_CLASSIFICATION = "drawdb/geometry/WeightPreview"
DRAW_REGISTRAR = "WeightPreviewShapeRegistrar"


class WeightGeometryOverride(omr.MPxGeometryOverride):
    RENDER_POINTS = True
    RENDER_LINE = True
    RENDER_POLYGONS = True

    points_size = 8.0
    lines_width = 1.0

    def __init__(self, mObject):
        super(WeightGeometryOverride, self).__init__(mObject)

        self.mObj: om.MObject = mObject  # GPU渲染的物体，这里是 shape节点的MObject
        self.mFnDep: om.MFnDependencyNode = om.MFnDependencyNode(mObject)  # shape的MFnDep类
        self.shapeClass: WeightPreviewShape = self.mFnDep.userNode()  # shape 自身的python类对象，用于访问方法和属性

        # data
        # 绘制模型的基本数据
        self.verts_count = 0
        self.solid_mgr: CMemoryManager = None
        self.wire_mgr: CMemoryManager = None
        self.point_mgr: CMemoryManager = None
        self.cSkin: CythonSkinDeformer = None  # 变形器自身python类，用于调取变形器自身成员
        self.renderStatus: bool = False  # 渲染状态，用于判断是否可以渲染

        # cache # 用于检测模型布线结构是否有变化
        self.laster_topology_vertex_check = 0

        # region 💥 初始化着色器 (全员 CPV 化)
        shader_mgr = omr.MRenderer.getShaderManager()
        # 1. 实体面
        self.cpv_shader = shader_mgr.getStockShader(omr.MShaderManager.k3dCPVSolidShader)
        # 2. 线框 (换成 CPV 加粗线框，让它能读取后半段颜色)
        self.wire_shader = shader_mgr.getStockShader(omr.MShaderManager.k3dCPVThickLineShader)
        self.wire_shader.setParameter("lineWidth", [self.lines_width, self.lines_width])
        # 3. 点阵 (新增 CPV 胖点着色器)
        self.point_shader = shader_mgr.getStockShader(omr.MShaderManager.k3dCPVFatPointShader)
        self.point_shader.setParameter("pointSize", [self.points_size, self.points_size])
        # endregion

    def _update_cSkinData(self):
        # 通过shape.refresh 查找cSkin节点获取内存数据

        self.cSkin = None
        if self.shapeClass.refresh_plug.isConnected:
            connected_plugs = self.shapeClass.refresh_plug.connectedTo(True, False)
            if len(connected_plugs) < 1:
                return False
            mObj = connected_plugs[0].node()
            hashCode = om.MObjectHandle(mObj).hashCode()
            self.cSkin = GLOBAL_DEFORMER_REGISTRY.get(hashCode, None)
            if self.cSkin is None:
                return False
        return True

    def updateDG(self):
        self.renderStatus = False
        self.shapeClass.refresh_plug.asInt() # 唤醒DG刷新
        self._update_cSkinData()  # 获取Deformer节点数据，数据直接写入 self.skinData
        try:
            fnMesh = self.cSkin.DATA.mFnMesh_output
            self._update_topology_api(fnMesh)  # 检查变形器的输出布线结构是否有变化，如果有变化更新底层数据
        except Exception:
            raise

        try:
            self._cal_color()  # 计算显示颜色，输出到
        except Exception:
            pass
        self.shapeClass._cal_boundingBox(self.cSkin.DATA.output_rawPoints_mgr.view, self.cSkin.DATA.vertex_count)

        self.renderStatus = True

    def populateGeometry(self, requirements, renderItems, data):
        """显存推送车间：数据 x2 架构"""

        if not self.renderStatus:
            return

        # 💥 核心：定义翻倍的顶点数
        N = self.cSkin.DATA.vertex_count
        TOTAL_N = N * 2

        for req in requirements.vertexRequirements():
            # --- 1. 推送坐标 (位置 x2) ---
            if req.semantic == omr.MGeometry.kPosition:
                v_buf = data.createVertexBuffer(req)
                if v_buf:
                    v_addr = v_buf.acquire(TOTAL_N, True)
                    byte_size = N * 12

                    # 填入前半段 (0 ~ N-1) 内存地址 填充为 模型变形点
                    ctypes.memmove(
                        v_addr,
                        self.cSkin.DATA.output_rawPoints_mgr.ptr_addr,
                        byte_size,
                    )
                    # 填入后半段 (N ~ 2N-1) 再次填充为 模型变形点，相当于两份重复数据（用于后面独立的点渲染）
                    ctypes.memmove(
                        v_addr + byte_size,
                        self.cSkin.DATA.output_rawPoints_mgr.ptr_addr,
                        byte_size,
                    )

                    v_buf.commit(v_addr)

            # --- 2. 颜色推送 ---
            elif req.semantic == omr.MGeometry.kColor:
                c_buf = data.createVertexBuffer(req)
                if c_buf:
                    c_addr = c_buf.acquire(TOTAL_N, True)  # 申请2倍内存连续地址
                    # 底色，真实蒙皮权重 (给面和线)
                    gpu_mgr_front = CMemoryManager.from_ptr(c_addr, "f", (N, 4))  # 4个元素(r,g,b,a), [c_addr : c_addr+N*4] 视图为 N列4行
                    # cython 填充内存
                    cColorCython.compute_colors_fast(
                        self.drawWeights.view,
                        gpu_mgr_front.view,
                        self.current_influence,
                        *self.current_color,
                    )
                    # 笔刷与线框上色，后半段显存
                    back_addr = c_addr + (N * 16)  # 后半段内存地址
                    gpu_mgr_back = CMemoryManager.from_ptr(back_addr, "f", (N, 4))  # 4个元素(r,g,b,a), [c_addr+N*4 : c_addr+(N*4)*2]  视图为 N列4行
                    # 极速给线框铺底色 (深灰色 0.1, Alpha必须是 1.0)
                    cColorCython.fill_solid_color(gpu_mgr_back.view, N, 0.1, 0.1, 0.1, 1.0)  # 用cython 填充线框

                    # 给圈中的点和线赋予黄色
                    brush_data = GLOBAL_BRUSH_REGISTRY.get("brush_preview", None)
                    if brush_data and brush_data.get("hit_count", 0) > 0:
                        cColorCython.apply_brush_colors(
                            gpu_mgr_back.view,
                            brush_data["indices_mgr"].view,
                            brush_data["weights_mgr"].view,
                            brush_data["hit_count"],
                        )

        # --- 3. 推送拓扑连线 ---
        for item in renderItems:
            if item.name() == "WeightSolidItem":
                mgr = self.solid_mgr
                if mgr is None or mgr.view is None:
                    continue
                num_indices = len(mgr.view)
                source_addr = mgr.ptr_addr

            elif item.name() == "WeightWireItem":
                mgr = self.wire_mgr
                if mgr is None or mgr.view is None:
                    continue
                num_indices = len(mgr.view)
                source_addr = mgr.ptr_addr

            elif item.name() == "BrushDebugPoints":
                # 💥 动态点阵：没圈中点时直接隐身！
                brush_data = GLOBAL_BRUSH_REGISTRY.get("brush_preview", None)
                hit_count = brush_data.get("hit_count", 0) if brush_data else 0

                if hit_count == 0:
                    continue

                i_buf = data.createIndexBuffer(omr.MGeometry.kUnsignedInt32)
                if i_buf:
                    # 💥 动态申请命中数量的显存空间
                    i_addr = i_buf.acquire(hit_count, True)
                    gpu_idx_mgr = CMemoryManager.from_ptr(i_addr, "I", (hit_count,))

                    # 极速算出偏移后的 ID
                    cColorCython.generate_brush_indices(
                        gpu_idx_mgr.view,
                        brush_data["indices_mgr"].view,
                        N,  # 偏移量是顶点数
                        hit_count,
                    )
                    i_buf.commit(i_addr)
                    item.associateWithIndexBuffer(i_buf)
                continue  # 处理完点阵直接跳出这一轮

            i_buf = data.createIndexBuffer(omr.MGeometry.kUnsignedInt32)
            if i_buf:
                i_addr = i_buf.acquire(num_indices, True)
                ctypes.memmove(i_addr, source_addr, num_indices * 4)
                i_buf.commit(i_addr)
                item.associateWithIndexBuffer(i_buf)

    def _update_topology_api(self, fn_mesh: om1.MFnMesh):
        current_vertex_count = fn_mesh.numVertices()
        if self.verts_count == current_vertex_count:
            return True

        # ==========================================
        # 1. 实体面拓扑 (Solid Indices) -> 读前半段 0 ~ N-1
        # ==========================================
        tri_counts = om1.MIntArray()
        tri_verts = om1.MIntArray()
        fn_mesh.getTriangles(tri_counts, tri_verts)
        self.solid_mgr = CMemoryManager.from_list(list(tri_verts), "I")

        # ==========================================
        # 2. 线框拓扑 (Wire Indices) -> 💥 偏移到后半段 N ~ 2N-1
        # ==========================================
        num_edges = fn_mesh.numEdges()
        num_wire = num_edges * 2

        self.wire_mgr = CMemoryManager.allocate("I", (num_wire,))
        wire_view = self.wire_mgr.view
        util = om1.MScriptUtil()
        edge_ptr = util.asInt2Ptr()
        idx = 0
        offset = current_vertex_count  # 💥 偏移量
        for i in range(num_edges):
            fn_mesh.getEdgeVertices(i, edge_ptr)
            wire_view[idx] = om1.MScriptUtil.getInt2ArrayItem(edge_ptr, 0, 0) + offset
            wire_view[idx + 1] = om1.MScriptUtil.getInt2ArrayItem(edge_ptr, 0, 1) + offset
            idx += 2

        # ==========================================
        # 3. 点拓扑 (Point Indices) -> 偏移到后半段 N ~ 2N-1
        # ==========================================
        # 我们用 CMemoryManager 申请一次，以后都不变了！
        self.point_mgr = CMemoryManager.allocate("I", (current_vertex_count,))
        cColorCython.generate_offset_indices(
            self.point_mgr.view,
            current_vertex_count,  # offset 就是 N
            current_vertex_count,  # count 也是 N
        )

        self.verts_count = current_vertex_count
        return True

    def _cal_color(self):

        layer_idx = self.shapeClass.layer_plug.asInt()
        is_mask = self.shapeClass.mask_plug.asBool()
        inf_idx = self.shapeClass.influence_plug.asInt()
        color = [1, 0, 0, 1]

        _layer = self.cSkin.DATA.weightsLayer.get(layer_idx, None)
        if _layer is None:
            return

        _weights = _layer.weightsHandle
        if is_mask:
            _weights = _layer.maskHandle
            inf_idx = 0
            color = [0, 1, 0, 1]

        # output color
        self.drawWeights = _weights.memory.reshape((self.cSkin.DATA.vertex_count, _weights.length // self.cSkin.DATA.vertex_count))
        self.current_influence = inf_idx
        self.current_color = color
        return True

    # 💥 修改 RenderItem 设置，增加 depth_priority 参数解决闪烁
    def _setup_render_item(self, renderItems, name, geom_type, shader, depth_priority=None):
        idx = renderItems.indexOf(name)
        if idx < 0:
            item = omr.MRenderItem.create(name, omr.MRenderItem.MaterialSceneItem, geom_type)
            renderItems.append(item)
        else:
            item = renderItems[idx]

        item.setDrawMode(omr.MGeometry.kAll)
        item.setShader(shader)
        if depth_priority is not None:
            item.setDepthPriority(depth_priority)
        item.enable(True)

    def updateRenderItems(self, objPath, renderItems):
        # 面
        if WeightGeometryOverride.RENDER_POLYGONS:
            self._setup_render_item(renderItems, "WeightSolidItem", omr.MGeometry.kTriangles, self.cpv_shader)
        # 线 (浮于面上层)
        if WeightGeometryOverride.RENDER_LINE:
            self._setup_render_item(renderItems, "WeightWireItem", omr.MGeometry.kLines, self.wire_shader, omr.MRenderItem.sActiveWireDepthPriority)
        # 点 (浮于最上层)
        if WeightGeometryOverride.RENDER_POINTS:
            self._setup_render_item(renderItems, "BrushDebugPoints", omr.MGeometry.kPoints, self.point_shader, omr.MRenderItem.sActivePointDepthPriority)
            idx = renderItems.indexOf("BrushDebugPoints")
            if idx >= 0:
                item = renderItems[idx]
                brush_data = GLOBAL_BRUSH_REGISTRY.get("brush_preview", None)
                hit_count = brush_data.get("hit_count", 0) if brush_data else 0

                item.enable(hit_count > 0)

    def cleanUp(self):
        pass

    @staticmethod
    def creator(obj):
        return WeightGeometryOverride(obj)

    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices


# ==============================================================================
# 自定义 Shape 节点注册 (下面所有代码均未改动)
# ==============================================================================
class WeightPreviewShape(om.MPxSurfaceShape):
    aInMesh = None
    aLayer = None
    aInfluence = None
    aMask = None
    aRefresh = None

    def __init__(self):
        super(WeightPreviewShape, self).__init__()
        self._boundingBox = om.MBoundingBox(
            om.MPoint((-10, -10, -10)),
            om.MPoint((10, 10, 10)),
        )

    def postConstructor(self):
        """节点创建的时候，直接创建我们常用的对象，避免后续创建浪费性能"""
        self.mObj = self.thisMObject()
        self.layer_plug: om.MPlug = om.MPlug(self.mObj, self.aLayer)
        self.mask_plug: om.MPlug = om.MPlug(self.mObj, self.aMask)
        self.influence_plug: om.MPlug = om.MPlug(self.mObj, self.aInfluence)
        self.refresh_plug: om.MPlug = om.MPlug(self.mObj, self.aRefresh)

    def setDependentsDirty(self, plug, plugArray):
        """设置脏传播"""
        if plug == WeightPreviewShape.aRefresh or plug == WeightPreviewShape.aLayer or plug == WeightPreviewShape.aMask or plug == WeightPreviewShape.aInfluence:
            omr.MRenderer.setGeometryDrawDirty(self.thisMObject(), True)

        return super(WeightPreviewShape, self).setDependentsDirty(plug, plugArray)

    def postEvaluation(self, context, evaluationNode, evalType):
        omr.MRenderer.setGeometryDrawDirty(self.thisMObject(), True)
        super(WeightPreviewShape, self).postEvaluation(context, evaluationNode, evalType)

    def preEvaluation(self, context, evaluationNode):
        omr.MRenderer.setGeometryDrawDirty(self.thisMObject(), True)
        super(WeightPreviewShape, self).preEvaluation(context, evaluationNode)

    @classmethod
    def initialize(cls):
        nAttr: om.MFnNumericAttribute = om.MFnNumericAttribute()

        cls.aLayer = nAttr.create("layer", "lyr", om.MFnNumericData.kInt, 0)
        nAttr.storable = True
        nAttr.keyable = False
        nAttr.channelBox = True
        cls.addAttribute(cls.aLayer)

        cls.aMask = nAttr.create("mask", "msk", om.MFnNumericData.kBoolean, False)
        nAttr.storable = True
        nAttr.keyable = False
        nAttr.channelBox = True
        cls.addAttribute(cls.aMask)

        cls.aInfluence = nAttr.create("influence", "ifn", om.MFnNumericData.kInt, 0)
        nAttr.storable = True
        nAttr.keyable = False
        nAttr.channelBox = True
        cls.addAttribute(cls.aInfluence)

        cls.aRefresh = nAttr.create("refresh", "rf", om.MFnNumericData.kInt, 0)
        nAttr.storable = False
        nAttr.hidden = True
        nAttr.keyable = False
        cls.addAttribute(cls.aRefresh)

    def isBounded(self):
        return True

    def _cal_boundingBox(self, point_view, vertex_count):
        """计算boundingBox,直接写入 `self._boundingBox`，后续GPU渲染通过`MDep.userNode()`来访问这个属性"""
        boxMin, boxMax = cBoundingBoxCython.compute_bbox_fast(
            point_view,
            vertex_count,
        )
        self._boundingBox = om.MBoundingBox(om.MPoint(boxMin), om.MPoint(boxMax))
        return True

    def boundingBox(self):
        return self._boundingBox

    @staticmethod
    def creator():
        return WeightPreviewShape()


class WeightPreviewShapeUI(omui.MPxSurfaceShapeUI):
    def __init__(self):
        super(WeightPreviewShapeUI, self).__init__()

    @staticmethod
    def creator():
        return WeightPreviewShapeUI()
