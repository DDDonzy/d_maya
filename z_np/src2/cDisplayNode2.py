from typing import TYPE_CHECKING
import ctypes

import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr

# 💥 顶级导入：光明正大的单向依赖，彻底告别循环引用！

from . import cBoundingBoxCython
from .cMemoryView import CMemoryManager
from ._cRegistry2 import SkinRegistry
from z_np.src2 import cColorCython as cColor
from . import _profile


if TYPE_CHECKING:
    from .cSkinDeform2 import CythonSkinDeformer
    # from typing import Callable


def maya_useNewAPI():
    pass


NODE_NAME = "WeightPreviewShape"
NODE_ID = om.MTypeId(0x80005)
DRAW_CLASSIFICATION = "drawdb/geometry/WeightPreview"
DRAW_REGISTRAR = "WeightPreviewShapeRegistrar"


# ==============================================================================
# 🎨 视口渲染器 (View): 绝对变“瞎”，没有任何私藏，彻底沦为无情的画笔
# ==============================================================================
class WeightGeometryOverride(omr.MPxGeometryOverride):
    RENDER_POINTS = True
    RENDER_LINE = True
    RENDER_POLYGONS = True

    points_size = 1.0
    lines_width = 1.0

    def __init__(self, mObjectShape):
        super(WeightGeometryOverride, self).__init__(mObjectShape)

        self.mObject_shape: om.MObject = mObjectShape
        self.mFnDep_shape: om.MFnDependencyNode = om.MFnDependencyNode(mObjectShape)
        self.shape_class: WeightPreviewShape = self.mFnDep_shape.userNode()

        # 拓扑快照 (仅拓扑改变时更新)
        self._cached_vertex_count = 0
        self._cached_solid_mgr: CMemoryManager = None
        self._cached_wire_mgr: CMemoryManager = None
        self._cached_point_mgr: CMemoryManager = None
        self._indices_initialized: bool = False
        self._last_topo_cache = None

        # 💥 渲染负载快照 (Render Payload) - 每一帧都会硬性刷新
        self._cached_raw_points_mgr = None
        self._cached_weights_view = None
        self._cached_influence_idx = 0
        self._cached_render_func = None
        self._cached_hit_state = None

        self.renderStatus: bool = False
        # 初始化着色器
        shader_mgr = omr.MRenderer.getShaderManager()
        self.cpv_shader = shader_mgr.getStockShader(omr.MShaderManager.k3dCPVSolidShader)

        self.wire_shader = shader_mgr.getStockShader(omr.MShaderManager.k3dCPVThickLineShader)
        self.wire_shader.setParameter("lineWidth", [WeightGeometryOverride.lines_width, WeightGeometryOverride.lines_width])

        self.point_shader = shader_mgr.getStockShader(omr.MShaderManager.k3dCPVFatPointShader)
        self.point_shader.setParameter("pointSize", [WeightGeometryOverride.points_size, WeightGeometryOverride.points_size])

    def updateDG(self):
        with _profile.MicroProfiler(target_runs=100, enable=False) as prof:
            self.renderStatus = False
            cSkin = self.shape_class.cSkin

            if not cSkin or cSkin.DATA.rawPoints_output is None:
                return
            
            if not self.shape_class or self.shape_class.deformMesh_plug is None:
                return 
            prof.step("updateDG:---------预处理")
            self.shape_class.deformMesh_plug.asMObject() # 更新数据
            prof.step("updateDG:---------更新模型")

            # 在这里统一读取 UI 最新属性，并同步给后端黑板！
            self.shape_class.sync_ui_state_to_blackboard()

            # region Topology
            _cache = self._get_topology_index_buffers(cSkin)
            if _cache:
                (
                    self._cached_solid_mgr,
                    self._cached_wire_mgr,
                    self._cached_point_mgr,
                    self._cached_vertex_count,
                ) = _cache
                # 💥 核心拦截器：对比缓存的内存地址，如果换了，说明拓扑变了！
                if self._last_topo_cache is not _cache:
                    self._indices_initialized = False # 锁解开，允许重新向显卡装载索引
                    self._last_topo_cache = _cache
            # endregion
            prof.step("updateDG:---------更新模型结构")
            self._cached_raw_points_mgr = cSkin.DATA.rawPoints_output
            # region Color
            weights2D_mgr, target_idx, is_mask = cSkin.DATA.active_paint_target
            self._cached_weights_1d = None
            if weights2D_mgr is not None and weights2D_mgr.view is not None:
                mv_2d = weights2D_mgr.view
                # 获取列数 (即 influences_count，如果是遮罩则为 1)
                cols = mv_2d.shape[1] if len(mv_2d.shape) > 1 else 1
                # 越界保护
                safe_idx = max(0, min(target_idx, cols - 1))
                mv_1d_flat = mv_2d.cast("B").cast("f")
                self._cached_weights_1d = mv_1d_flat[safe_idx::cols]
            self._cached_paintMask = is_mask
            self._cached_render_mode = cSkin.DATA.render_mode
            self._cached_c_wire = cSkin.DATA.color_wire
            self._cached_c_point = cSkin.DATA.color_point
            self._cached_c_mask_remapA = cSkin.DATA.color_mask_remapA
            self._cached_c_mask_remapB = cSkin.DATA.color_mask_remapB
            self._cached_c_weights_remapA = cSkin.DATA.color_weights_remapA
            self._cached_c_weights_remapB = cSkin.DATA.color_weights_remapB
            self._cached_c_brush_remapA = cSkin.DATA.color_brush_remapA
            self._cached_c_brush_remapB = cSkin.DATA.color_brush_remapB
            # endregion
            # Brush DATA
            self._cached_hit_state = cSkin.DATA.brush_hit_state
            self.renderStatus = True
            prof.step("updateDG:---------准备数据结束")

    def populateGeometry(self, requirements, renderItems, data):
        """
        由于显示色是根据顶点来进行渐变的，
        我们无法让点，边，线显示不同颜色
        所以我们申请了三分点的数据放在内存中
        -----------------
        0-1,第一份点数据,填充模型点位置信息              填充颜色A
        1-2,第二份点数据,同上填充和上面一模一样的位置信息,填充颜色B
        2-3,第三份点数据,同上填充和上面一模一样的位置信息,填充颜色C
        -----------------
        然后需要让模型显示出 面，边，点，
        需要申请新的缓存，用来填充模型结构
        比如 绘制 `面`
        [[0,1,2], # face1,三个点的index
            [1,2,3], # face2,三个点的index
            [2,3,4]] # face3,三个点的index
        显卡会去 `kPosition` 填充的数据中寻找这些点，绘制出面
        并且使用 `kColor` 中的颜色来渲染面的颜色
        当我绘制 边的时候
        我可以用第二遍填充的点数据来绘制，只要填充的index对应第二遍填充的index
        比如 绘制 `边`
        [[10,11], # face1,三个点的index
            [11,12], # face2,三个点的index
            [12,13]] # face3,三个点的index
        这样显卡会在`kPosition`中寻找对应的index，
        并且使用 `kColor` 对应的index颜色来绘制边。
        比如 绘制 `点`同理
        """
        if not self.renderStatus:
            return
        N = self._cached_vertex_count
        points_mgr = self._cached_raw_points_mgr

        # ==========================================
        # 1. 填充顶点缓冲 (位置 & 颜色)
        # ==========================================
        for req in requirements.vertexRequirements():
            if req.semantic == omr.MGeometry.kPosition:
                # """ `POINTS` """
                if points_mgr and points_mgr.ptr_addr:
                    vtx_buf = data.createVertexBuffer(req)
                    vtx_addr = vtx_buf.acquire(N * 3, True)
                    if vtx_addr:
                        # """
                        # 默认申请 `acquire(N,True)` 返回`[x,y,z] * N`的缓存空间, 类型是`float`
                        # 我们需要 `面，点，边` 颜色不同,  所以申请三倍的空间 `N*3`,
                        # MAYA会给我们一个 `[x,y,z] * N*3` 的缓存空间。
                        # """
                        # fmt:off
                        # 连续三次硬拷贝 (面、线、点共用同一套坐标)
                        stride = N * 12 # len([x,y,z]) * N * 4 bytes
                        #               Target Addr              Source Addr                Length
                        ctypes.memmove( vtx_addr              ,    points_mgr.ptr_addr,       stride )
                        ctypes.memmove( vtx_addr + stride     ,    points_mgr.ptr_addr,       stride )
                        ctypes.memmove( vtx_addr + stride * 2 ,    points_mgr.ptr_addr,       stride )
                        vtx_buf.commit( vtx_addr )

                        # fmt:on
            # ==========================================
            # 🎨 填充顶点缓冲 (颜色)
            # ==========================================
            elif req.semantic == omr.MGeometry.kColor:
                # """ `Color` """
                color_buf = data.createVertexBuffer(req)
                color_addr = color_buf.acquire(N * 3, True)
                if color_addr:
                    # 使用 `CMemoryManager` 快速映射显存
                    color_view = CMemoryManager.from_ptr(color_addr, "f", (N * 3, 4)).view
                    # ==================================
                    # 🎨  面颜色 (0~N): 权重梯度
                    # ==================================
                    if self._cached_weights_1d is not None:
                        # Mask Mode
                        if self._cached_paintMask:
                            cColor.render_gradient(self._cached_weights_1d, color_view[0:N], self._cached_c_mask_remapA, self._cached_c_mask_remapB)
                        # Alpha Mode
                        elif self._cached_render_mode == 1:
                            cColor.render_gradient(self._cached_weights_1d, color_view[0:N], self._cached_c_weights_remapA, self._cached_c_weights_remapB)
                        # heatmap Mode
                        else:
                            cColor.render_heatmap(self._cached_weights_1d, color_view[0:N])
                    # None Weights color
                    else:
                        cColor.render_fill(color_view[0:N], (0.0, 0.0, 1.0, 1.0))

                    # ==================================
                    # 🎨 线颜色 (N~2N)
                    # ==================================
                    cColor.render_fill(color_view[N : 2 * N], self._cached_c_wire)

                    # ==================================
                    # 🎨 笔刷点颜色 (2N~3N)
                    # ==================================
                    hit_state = self._cached_hit_state
                    if hit_state and hit_state.hit_count > 0:
                        cColor.render_brush_gradient(
                            color_view[2 * N : 3 * N],
                            hit_state.hit_indices_mgr.view,
                            hit_state.hit_weights_mgr.view,
                            hit_state.hit_count,
                            self._cached_c_brush_remapA,
                            self._cached_c_brush_remapB,
                        )
                    color_buf.commit(color_addr)

        # ==========================================
        #  填充topology缓冲 (index偏移)
        # ==========================================
        for item in renderItems:
            item_name = item.name()

            # --- 面索引 (0 偏移) ---
            if item_name == "WeightSolidItem" and self._cached_solid_mgr:
                if not self._indices_initialized:  # 💥 拦截！只有拓扑改变时才拷贝！
                    mgr = self._cached_solid_mgr
                    num_indices = mgr.view.nbytes // 4
                    i_buf = data.createIndexBuffer(omr.MGeometry.kUnsignedInt32)
                    i_addr = i_buf.acquire(num_indices, True)
                    if i_addr:
                        ctypes.memmove(i_addr, mgr.ptr_addr, num_indices * 4)
                        i_buf.commit(i_addr)
                        item.associateWithIndexBuffer(i_buf)
            # --- 线索引 (N 偏移) ---
            elif item_name == "WeightWireItem" and self._cached_wire_mgr:
                if not self._indices_initialized:  # 💥 拦截！彻底释放 PCIe 带宽！
                    mgr = self._cached_wire_mgr
                    num_indices = mgr.view.nbytes // 4
                    i_buf = data.createIndexBuffer(omr.MGeometry.kUnsignedInt32)
                    i_addr = i_buf.acquire(num_indices, True)
                    if i_addr:
                        cColor.offset_indices_direct(mgr.ptr_addr, int(i_addr), num_indices, N)
                        i_buf.commit(i_addr)
                        item.associateWithIndexBuffer(i_buf)

            # --- 笔刷点索引 (2N 偏移) ---
            elif item_name == "BrushDebugPoints":
                hit_state = self._cached_hit_state
                hit_count = hit_state.hit_count
                if hit_state and (hit_count > 0):
                    # 💥 笔刷是动态追踪的，它的索引必须每一帧更新，这个不能锁！
                    i_buf = data.createIndexBuffer(omr.MGeometry.kUnsignedInt32)
                    i_addr = i_buf.acquire(hit_count, True)
                    if i_addr:
                        cColor.offset_indices_direct(
                            hit_state.hit_indices_mgr.ptr_addr,
                            int(i_addr),
                            hit_count,
                            2 * N,
                        )
                        i_buf.commit(i_addr)
                        item.associateWithIndexBuffer(i_buf)
        self._indices_initialized = True

    def _get_topology_index_buffers(self, cSkin: "CythonSkinDeformer"):
        N = cSkin.DATA.vertex_count
        if N == 0 or getattr(cSkin.DATA, "tri_indices_2D", None) is None:
            return None

        # 缓存命中, 直接把老数据原样扔回去
        if (self._cached_vertex_count == N) and (self._cached_solid_mgr is not None):
            return (
                self._cached_solid_mgr,
                self._cached_wire_mgr,
                self._cached_point_mgr,
                self._cached_vertex_count,
            )

        new_solid_mgr = cSkin.DATA.tri_indices_2D
        new_wire_mgr = cSkin.DATA.base_edge_indices

        new_point_mgr = CMemoryManager.from_list(list(range(N)), "i")

        return new_solid_mgr, new_wire_mgr, new_point_mgr, N

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
        if WeightGeometryOverride.RENDER_POLYGONS:
            self._setup_render_item(renderItems, "WeightSolidItem", omr.MGeometry.kTriangles, self.cpv_shader)

        if WeightGeometryOverride.RENDER_LINE:
            self._setup_render_item(renderItems, "WeightWireItem", omr.MGeometry.kLines, self.wire_shader, omr.MRenderItem.sActiveWireDepthPriority)

        if WeightGeometryOverride.RENDER_POINTS:
            self._setup_render_item(renderItems, "BrushDebugPoints", omr.MGeometry.kPoints, self.point_shader, omr.MRenderItem.sActivePointDepthPriority)
            idx = renderItems.indexOf("BrushDebugPoints")
            if idx >= 0:
                item = renderItems[idx]
                cSkin = self.shape_class.cSkin
                hit_state = cSkin.DATA.brush_hit_state if cSkin else None
                item.enable(hit_state is not None and hit_state.hit_count > 0)

    def cleanUp(self):
        pass

    @staticmethod
    def creator(obj):
        return WeightGeometryOverride(obj)

    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices


# ==============================================================================
# 🎛️ 自定义 Shape 节点注册 (Controller/Model 中转): 监听连接，缓存实例，防呆反向同步
# ==============================================================================
class WeightPreviewShape(om.MPxSurfaceShape):
    aLayer = None
    aInfluence = None
    aMask = None
    aInDeformMesh = None

    def __init__(self):
        super(WeightPreviewShape, self).__init__()
        self._boundingBox = om.MBoundingBox(om.MPoint((-10, -10, -10)), om.MPoint((10, 10, 10)))

        # 💥 实例缓存池：再也不用每次去注册表捞了
        self._cached_cSkin = None

    @property
    def cSkin(self) -> "CythonSkinDeformer":
        """
        获取绑定的 cSkin 实例。
        第一次调用时寻址并缓存，后续调用直接返回内存引用！
        """
        if self._cached_cSkin is None:
            if not self.deformMesh_plug.isConnected:
                return None

            connected_plugs = self.deformMesh_plug.connectedTo(True, False)
            if not connected_plugs:
                return None
            mObj_skin = connected_plugs[0].node()

            # 直接使用顶级导入的注册表
            self._cached_cSkin = SkinRegistry.get_instance_by_api2(mObj_skin)
            if self._cached_cSkin and self._cached_cSkin.DATA:
                self._cached_cSkin.DATA.preview_shape_mObj = self.mObj

        return self._cached_cSkin

    def connectionBroken(self, plug, otherPlug, asSrc):
        """💔 Maya 原生事件：当连线被断开时触发"""
        if plug == self.deformMesh_plug:
            # 只要连接一断开，立刻清空缓存，绝不给野指针留下任何可乘之机！
            self._cached_cSkin = None

        return super(WeightPreviewShape, self).connectionBroken(plug, otherPlug, asSrc)

    def postConstructor(self):
        self.mObj = self.thisMObject()
        self.layer_plug = om.MPlug(self.mObj, self.aLayer)
        self.mask_plug = om.MPlug(self.mObj, self.aMask)
        self.influence_plug = om.MPlug(self.mObj, self.aInfluence)
        self.deformMesh_plug = om.MPlug(self.mObj, self.aInDeformMesh)

    def setDependentsDirty(self, plug, plugArray):
        # 1. 视口刷新通知 (纯粹的脏传播)
        attr = plug.attribute()
        if attr in (self.aInDeformMesh, self.aLayer, self.aMask, self.aInfluence):
            omr.MRenderer.setGeometryDrawDirty(self.thisMObject(), True)

        return super(WeightPreviewShape, self).setDependentsDirty(plug, plugArray)

    def postEvaluation(self, context, evaluationNode, evalType):
        omr.MRenderer.setGeometryDrawDirty(self.thisMObject(), True)
        super(WeightPreviewShape, self).postEvaluation(context, evaluationNode, evalType)

    def preEvaluation(self, context, evaluationNode):
        # 💥 只有当我们的核心插头真正发生数据流动时，才通知 VP2 重绘！
        if (evaluationNode.dirtyPlugExists(self.aInDeformMesh) or
            evaluationNode.dirtyPlugExists(self.aLayer) or
            evaluationNode.dirtyPlugExists(self.aInfluence) or
            evaluationNode.dirtyPlugExists(self.aMask)):
            omr.MRenderer.setGeometryDrawDirty(self.thisMObject(), True)
            
        super(WeightPreviewShape, self).preEvaluation(context, evaluationNode)

    def sync_ui_state_to_blackboard(self):
        """
        🧠 [Controller 逻辑] 由前端负责将 UI 最新状态同步给后端黑板！
        """
        cSkin = self.cSkin
        if cSkin and cSkin.DATA:
            cSkin.DATA.paintLayerIndex = self.layer_plug.asInt()
            cSkin.DATA.paintInfluenceIndex = self.influence_plug.asInt()
            cSkin.DATA.paintMask = self.mask_plug.asBool()

    @staticmethod
    def initialize():
        nAttr = om.MFnNumericAttribute()
        WeightPreviewShape.aLayer = nAttr.create("layer", "lyr", om.MFnNumericData.kInt, 0)
        nAttr.storable = True
        nAttr.channelBox = True
        WeightPreviewShape.addAttribute(WeightPreviewShape.aLayer)

        WeightPreviewShape.aMask = nAttr.create("mask", "msk", om.MFnNumericData.kBoolean, False)
        nAttr.storable = True
        nAttr.channelBox = True
        WeightPreviewShape.addAttribute(WeightPreviewShape.aMask)

        WeightPreviewShape.aInfluence = nAttr.create("influence", "ifn", om.MFnNumericData.kInt, 0)
        nAttr.storable = True
        nAttr.channelBox = True
        WeightPreviewShape.addAttribute(WeightPreviewShape.aInfluence)

        tAttr:om.MFnTypedAttribute = om.MFnTypedAttribute()
        WeightPreviewShape.aInDeformMesh = tAttr.create("inDeformMesh", "idm", om.MFnData.kMesh)
        tAttr.hidden = True
        tAttr.storable = False
        WeightPreviewShape.addAttribute(WeightPreviewShape.aInDeformMesh)


    def isBounded(self):
        return True

    def boundingBox(self):
        """
        需要知道物体大小时，才由 Shape 本节点负责请求计算。
        """
        cSkin = self.cSkin

        if cSkin and cSkin.DATA and cSkin.DATA.rawPoints_output:
            boxMin, boxMax = cBoundingBoxCython.compute_bbox_fast(cSkin.DATA.rawPoints_output.view, cSkin.DATA.vertex_count)
            self._boundingBox = om.MBoundingBox(om.MPoint(boxMin), om.MPoint(boxMax))

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
