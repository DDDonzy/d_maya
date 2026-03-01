from typing import TYPE_CHECKING
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr

if TYPE_CHECKING:
    from z_np.src2.cSkinDeform2 import CythonSkinDeformer

from z_np.src2._cRegistry2 import SkinRegistry
from z_np.src2.cBrushCore2 import WeightBrushCore
from z_np.src2 import cRaycast2Cython as cRaycastCython

from m_utils.dag.getHistory import get_history


def maya_useNewAPI():
    pass


class WeightBrushContext(omui.MPxContext):
    brushLine = 2.0
    brushColor = om.MColor((1.0, 0.5, 0.0, 1.0))
    brushPresColor = om.MColor((1.0, 1, 1.0, 1.0))

    def __init__(self):
        super(WeightBrushContext, self).__init__()

        # ==========================================
        # 🧠 核心架构组件
        # ==========================================
        self.core: WeightBrushCore = None  # 数学与逻辑调度大脑
        self.cSkin: "CythonSkinDeformer" = None  # 绑定的变形器实例

        # ==========================================
        # 📦 UI 交互与环境缓存
        # ==========================================
        self._shape_path: str = None
        self.fn_mesh: om.MFnMesh = None  # 用于快速获取法线

        # ==========================================
        # 🖱️ 射线探测缓存
        # ==========================================
        self._view: omui.M3dView = None
        self._ray_source = om.MPoint()
        self._ray_direction = om.MVector()
        self._hit_result = None  
        self._isPressed = False

    # ----------------------------------------------------------------------
    # 生命周期管理 (Setup & Cleanup)
    # ----------------------------------------------------------------------
    def toolOnSetup(self, event):
        """进入工具：纯粹的环境搭建与 Core 引擎点火"""
        try:
            # 1. 解析选择并找到形变节点
            mSel = om.MGlobal.getActiveSelectionList()
            shape_mDag = mSel.getDagPath(0).extendToShape()
            self._shape_path = shape_mDag.fullPathName()
            self.fn_mesh = om.MFnMesh(shape_mDag)
            self.mesh_dag_path = shape_mDag

            skin_node_name = get_history(self._shape_path, type="cSkinDeformer")[0]

            # 💥 2. 使用新版 Registry 安全获取 Python 实例
            mSel_skin = om.MGlobal.getSelectionListByName(skin_node_name)
            mObj_skin = mSel_skin.getDependNode(0)
            self.cSkin = SkinRegistry.get_instance_by_api2(mObj_skin)
            if not self.cSkin:
                raise RuntimeError("无法从注册表获取 cSkinDeformer 实例！")

            # 3. 准备视口
            self._view = omui.M3dView.active3dView()

            # 💥 4. 实例化无状态的 Core 引擎！
            self.core = WeightBrushCore(self.cSkin)
            print("[Brush] 引擎点火成功！内存黑板已挂载！")

        except Exception as e:
            cmds.evalDeferred(lambda: cmds.setToolTo("selectSuperContext"))
            om.MGlobal.displayError(f"笔刷初始化失败: {e}")
            raise

    def toolOffCleanup(self):
        """退出工具：物理销毁 Core 引擎和清理环境"""
        # 完美闭环：通知 Core 进行 teardown
        if self.core:
            self.core.teardown()
            self.core = None
        self.cSkin = None
        self.__init__()

    # ----------------------------------------------------------------------
    # 事件流转 (Events -> Raycast -> Process)
    # ----------------------------------------------------------------------
    def doPress(self, event, drawMgr, context):
        self._shoot_ray_and_process(event, True, drawMgr)

    def doDrag(self, event, drawMgr, context):
        self._shoot_ray_and_process(event, True, drawMgr)

    def doPtrMoved(self, event, drawMgr, context):
        self._shoot_ray_and_process(event, False, drawMgr)

    def doRelease(self, event, drawMgr, context):
        self._isPressed = False

    def _raycast(self, ray_source_MPoint, ray_dir_MVector):
        """💥 对齐最新 cRaycast2Cython，直接接收三维坐标"""
        source_arr = tuple(ray_source_MPoint)[0:3]
        dir_arr = tuple(ray_dir_MVector)

        # 完美接收 6 个参数：成功标志, 空间坐标, 命中的三角面ID, 距离t, 重心坐标u, v
        hit_success, hit_pos, hit_tri, closest_t, u, v = cRaycastCython.raycast(
            source_arr,
            dir_arr,
            self.cSkin.DATA.rawPoints2D_output.view,
            self.cSkin.DATA.tri_indices_2D.view,
        )

        if hit_success:
            # 💥 Python 层彻底告别数学计算，直接查出 Face ID 返回即可！
            hit_face_id = self.cSkin.DATA.tri_to_face_map.view[hit_tri]
            return hit_pos, hit_tri, hit_face_id

        return None

    def _shoot_ray_and_process(self, event, is_pressed, drawMgr):
        """💥 终极调度流水线：完全解耦，各司其职"""
        self._isPressed = is_pressed
        last_hit = self._hit_result

        # 1. 发射射线
        x, y = event.position
        self._view.viewToWorld(x, y, self._ray_source, self._ray_direction)
        # 💥 坐标系纠偏：把射线逆运算进模型自己的局部坐标系里！
        inv_matrix = self.mesh_dag_path.inclusiveMatrixInverse()
        ray_source_obj = self._ray_source * inv_matrix
        ray_dir_obj = self._ray_direction * inv_matrix

        self._hit_result = self._raycast(ray_source_obj, ray_dir_obj)

        # 鼠标移出模型：清空黑板，刷新视口消掉圈圈
        if self._hit_result is None and last_hit is not None:
            if self.core:
                self.core.clear_hit_state()
            self._refresh_viewport()

        if self._hit_result is None:
            return

        # 2. 解包结果
        hit_point_obj, hit_tri, hit_face = self._hit_result
        hit_normal = tuple(self.fn_mesh.getPolygonNormal(hit_face, om.MSpace.kWorld))

        self.core.hit_state.hit_center_normal = hit_normal
        
        # 💥 3. 侦察兵需要真正的局部坐标 hit_point_obj 和真正的三角面 hit_tri！
        self.core.detect_range(hit_point_obj, hit_tri)

        # 4. 炮兵开火
        if is_pressed:
            self.core.apply_weight_math()
            self.cSkin._setDirty()  

        self._refresh_viewport()
        
        # 💥 5. 但是 UI 视口画圈圈，必须乘回世界坐标系！
        hit_point_world = om.MPoint(hit_point_obj) * self.mesh_dag_path.inclusiveMatrix()
        self._draw_brush_cursor(drawMgr, hit_point_world, hit_normal)

    # ----------------------------------------------------------------------
    # 渲染器辅助 (Debug Viewport UI)
    # ----------------------------------------------------------------------
    def _refresh_viewport(self):
        """VP2 视口重绘 (仅刷新视图本身，不牵扯自建节点)"""

        if self.cSkin and self.cSkin.DATA:
            # 1. 从黑板拿到 Shape 的灵魂指针
            shape_mObj = getattr(self.cSkin.DATA, "preview_shape_mObj", None)
            if shape_mObj and not shape_mObj.isNull():
                omr.MRenderer.setGeometryDrawDirty(shape_mObj, True)

        if self._view:
            self._view.refresh(False, False)

    def _draw_brush_cursor(self, drawMgr, hit_point, hit_normal):
        """绘制 3D 笔刷外圈 UI"""
        if not self.core:
            return
        color = self.brushColor if not self._isPressed else self.brushPresColor
        drawMgr.beginDrawable()
        drawMgr.setColor(color)
        drawMgr.setLineWidth(self.brushLine)
        drawMgr.circle(om.MPoint(hit_point), om.MVector(hit_normal), self.core.settings.radius)
        drawMgr.endDrawable()

    def _draw_debug_hit_points(self, drawMgr):
        """
        🚀 命中雷达：直接读取 HitState 黑板！
        验证侦察兵 (detect_range) 算出的 hit_indices 是否正确！
        """
        if not self.core or not self.core.hit_state:
            return

        hit_count = self.core.hit_state.hit_count
        if hit_count == 0:
            return

        indices = self.core.hit_state.hit_indices_mgr.view
        points_2d = self.cSkin.DATA.rawPoints2D_output.view

        pt_array = om.MPointArray()
        for i in range(hit_count):
            v_idx = indices[i]
            pt_array.append(om.MPoint(points_2d[v_idx, 0], points_2d[v_idx, 1], points_2d[v_idx, 2]))

        drawMgr.beginDrawable()
        drawMgr.setDepthPriority(omr.MRenderItem.sActivePointDepthPriority)
        drawMgr.setPointSize(6.0)
        drawMgr.setColor(om.MColor((1.0, 1.0, 0.0, 1.0)))  # 测试黄
        drawMgr.points(pt_array, False)
        drawMgr.endDrawable()


class WeightBrushContextCmd(omui.MPxContextCommand):
    COMMAND_NAME = "cBrushCtx"

    def __init__(self):
        super(WeightBrushContextCmd, self).__init__()

    def makeObj(self):
        return WeightBrushContext()

    @staticmethod
    def creator():
        return WeightBrushContextCmd()
