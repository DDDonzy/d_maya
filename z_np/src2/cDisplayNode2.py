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

    points_size = 4.0
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
        self.renderStatus = False
        self.shape_class.refresh_plug.asInt()

        cSkin = self.shape_class.cSkin

        if not cSkin or cSkin.DATA.rawPoints_output is None:
            return

        # 在这里统一读取 UI 最新属性，并同步给后端黑板！
        self.shape_class.sync_ui_state_to_blackboard()

        # 1. 获取并快照拓扑
        _cache = self._get_gpu_index_buffers(cSkin)
        if _cache:
            (
                self._cached_solid_mgr,
                self._cached_wire_mgr,
                self._cached_point_mgr,
                self._cached_vertex_count,
            ) = _cache

        # 💥 修复 1：把丢失的坐标和笔刷状态快照加回来！
        self._cached_raw_points_mgr = cSkin.DATA.rawPoints_output
        self._cached_hit_state = cSkin.DATA.brush_hit_state

        # 从黑板拿到原汁原味的 2D 数据和原始索引
        weights2D_mgr, target_idx, is_mask = cSkin.DATA.active_paint_target
        
        # 抓取本帧负载 (1D权重、状态、颜色参数)
        self._cached_weights_1d = None
        if weights2D_mgr is not None and weights2D_mgr.view is not None:
            mv_2d = weights2D_mgr.view

            # 获取列数 (即 influences_count，如果是遮罩则为 1)
            cols = mv_2d.shape[1] if len(mv_2d.shape) > 1 else 1

            # 越界保护
            safe_idx = max(0, min(target_idx, cols - 1))
            mv_1d_flat = mv_2d.cast("B").cast("f")
            self._cached_weights_1d = mv_1d_flat[safe_idx::cols]

        # 3. 抓取其他状态
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


        self.renderStatus = True

    def populateGeometry(self, requirements, renderItems, data):
        """显存推送总控：3倍顶点克隆架构！"""
        if not self.renderStatus:
            return

        N = self._cached_vertex_count

        # 1. 填充顶点要求 (位置, 颜色) -> 注意，内部会自动申请 3 倍显存 (3 * N)
        for req in requirements.vertexRequirements():
            if req.semantic == omr.MGeometry.kPosition:
                self._fill_position_buffer(data.createVertexBuffer(req), N)

            elif req.semantic == omr.MGeometry.kColor:
                self._fill_color_buffer(data.createVertexBuffer(req), N)

        # 2. 填充拓扑索引 (面, 线, 笔刷点)
        for item in renderItems:
            if item.name() == "WeightSolidItem" and self._cached_solid_mgr:
                # 面用第 0 ~ N 区间，偏移量为 0
                self._commit_index_buffer_with_offset(data, item, self._cached_solid_mgr, 0)

            elif item.name() == "WeightWireItem" and self._cached_wire_mgr:
                # 线用第 N ~ 2N 区间，偏移量为 N
                self._commit_index_buffer_with_offset(data, item, self._cached_wire_mgr, N)

            elif item.name() == "BrushDebugPoints":
                # 点用第 2N ~ 3N 区间，偏移量为 2N
                self._fill_brush_points_buffer(data, item, N)

    # --------------------------------------------------------------------------
    # 🛠️ 拆分出来的独立车间函数 (直接读取自身快照，清爽至极)
    # --------------------------------------------------------------------------
    def _fill_position_buffer(self, v_buf, N: int):
        points_mgr = self._cached_raw_points_mgr
        if not v_buf or not points_mgr or not points_mgr.ptr_addr:
            return

        # 💥 降维打击：强行申请 3 倍的显存空间！
        v_addr = v_buf.acquire(N * 3, True)

        # 将原坐标原封不动地连续拷贝 3 次
        ctypes.memmove(v_addr, points_mgr.ptr_addr, N * 12)  # 给面
        ctypes.memmove(v_addr + N * 12, points_mgr.ptr_addr, N * 12)  # 给线
        ctypes.memmove(v_addr + N * 24, points_mgr.ptr_addr, N * 12)  # 给点

        v_buf.commit(v_addr)

    def _fill_color_buffer(self, c_buf, N: int):
        if not c_buf:
            return

        c_addr = c_buf.acquire(N * 3, True)
        color_view = CMemoryManager.from_ptr(c_addr, "f", (N * 3, 4)).view

        # ==========================================
        # 🎨 1. 面 (0 ~ N): 视图层自主决定采用何种色彩策略！
        # ==========================================
        if self._cached_weights_1d is not None:
            if self._cached_paintMask:
                # 遮罩插值
                cColor.render_gradient(self._cached_weights_1d, color_view[0:N], self._cached_c_mask_remapA, self._cached_c_mask_remapB)
            elif self._cached_render_mode == 1:
                # 黑白插值
                cColor.render_gradient(self._cached_weights_1d, color_view[0:N], self._cached_c_weights_remapA, self._cached_c_weights_remapB)
            else:
                # 默认冷暖色
                cColor.render_heatmap(self._cached_weights_1d, color_view[0:N])
        else:
            # 没抓到数据，报警纯蓝
            cColor.render_fill(color_view[0:N], (0.0, 0.0, 1.0, 1.0))

        # ==========================================
        # 🎨 2. 线 (N ~ 2N): 一键填充线框色
        # ==========================================
        
        cColor.render_fill(color_view[N : 2 * N], self._cached_c_wire)

        # ==========================================
        # 🎨 3. 点 (2N ~ 3N): 一键填充红点色
        # ==========================================
        hit_state = self._cached_hit_state
        if hit_state and hit_state.hit_count > 0:
            cColor.render_brush_gradient(
                color_view[2 * N : 3 * N],         # 正确的点显存切片
                hit_state.hit_indices_mgr.view,    # 命中 ID
                hit_state.hit_weights_mgr.view,    # 衰减权重
                hit_state.hit_count,               # 真实命中数量
                self._cached_c_brush_remapA,       
                self._cached_c_brush_remapB,       
            )

        c_buf.commit(c_addr)

    def _fill_brush_points_buffer(self, data, item, N: int):
        hit_state = self._cached_hit_state
        if not hit_state or hit_state.hit_count <= 0:
            return

        hit_count = hit_state.hit_count
        i_buf = data.createIndexBuffer(omr.MGeometry.kUnsignedInt32)
        if i_buf:
            i_addr = i_buf.acquire(hit_count, True)

            # 获取底层的视图
            hit_indices_view = hit_state.hit_indices_mgr.view

            # 创建一个临时的数组，加上 2N 的偏移量！
            # (因为点的数据存放在 2N ~ 3N 之间)
            offset_array = (ctypes.c_uint32 * hit_count)()
            for i in range(hit_count):
                offset_array[i] = hit_indices_view[i] + (2 * N)

            ctypes.memmove(i_addr, ctypes.addressof(offset_array), hit_count * 4)
            i_buf.commit(i_addr)
            item.associateWithIndexBuffer(i_buf)

    def _commit_index_buffer_with_offset(self, data, item, mgr: CMemoryManager, offset: int):
        """支持自定义偏移量的通用索引装载器"""
        if not mgr or mgr.view is None:
            return

        num_indices = mgr.view.nbytes // 4
        i_buf = data.createIndexBuffer(omr.MGeometry.kUnsignedInt32)
        if i_buf:
            i_addr = i_buf.acquire(num_indices, True)

            # 如果不需要偏移(面的情况)，直接内存硬拷贝，速度极快
            if offset == 0:
                ctypes.memmove(i_addr, mgr.ptr_addr, num_indices * 4)
            # 如果需要偏移(线的情况)，循环加上偏移量
            else:
                idx_view = mgr.view
                offset_array = (ctypes.c_uint32 * num_indices)()
                for i in range(num_indices):
                    offset_array[i] = idx_view[i] + offset
                ctypes.memmove(i_addr, ctypes.addressof(offset_array), num_indices * 4)

            i_buf.commit(i_addr)
            item.associateWithIndexBuffer(i_buf)

    def _get_gpu_index_buffers(self, cSkin: "CythonSkinDeformer"):
        """
        🛠️ GPU 索引缓冲生成器: 极简模式
        纯函数逻辑，不产生副作用，直接返回组装好的内存管理器。
        返回: tuple(solid_mgr, wire_mgr, point_mgr, N) 或 None
        """
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

        # B. 点：生成基础索引
        new_point_mgr = CMemoryManager.from_list(list(range(N)), "i")

        # 光明正大地返回！
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
    aRefresh = None

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
            if not self.refresh_plug.isConnected:
                return None

            connected_plugs = self.refresh_plug.connectedTo(True, False)
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
        if plug == self.refresh_plug:
            # 只要连接一断开，立刻清空缓存，绝不给野指针留下任何可乘之机！
            self._cached_cSkin = None

        return super(WeightPreviewShape, self).connectionBroken(plug, otherPlug, asSrc)

    def postConstructor(self):
        self.mObj = self.thisMObject()
        self.layer_plug = om.MPlug(self.mObj, self.aLayer)
        self.mask_plug = om.MPlug(self.mObj, self.aMask)
        self.influence_plug = om.MPlug(self.mObj, self.aInfluence)
        self.refresh_plug = om.MPlug(self.mObj, self.aRefresh)

    def setDependentsDirty(self, plug, plugArray):
        # 1. 视口刷新通知 (纯粹的脏传播)
        attr = plug.attribute()
        if attr in (self.aRefresh, self.aLayer, self.aMask, self.aInfluence):
            omr.MRenderer.setGeometryDrawDirty(self.thisMObject(), True)

        return super(WeightPreviewShape, self).setDependentsDirty(plug, plugArray)

    def postEvaluation(self, context, evaluationNode, evalType):
        omr.MRenderer.setGeometryDrawDirty(self.thisMObject(), True)
        super(WeightPreviewShape, self).postEvaluation(context, evaluationNode, evalType)

    def preEvaluation(self, context, evaluationNode):
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

        WeightPreviewShape.aRefresh = nAttr.create("refresh", "rf", om.MFnNumericData.kInt, 0)
        nAttr.storable = False
        nAttr.hidden = True
        nAttr.keyable = False
        WeightPreviewShape.addAttribute(WeightPreviewShape.aRefresh)

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
