from typing import TYPE_CHECKING

from z_np.src import cMemoryView


if TYPE_CHECKING:
    from z_np.src.cMemoryView import CMemoryManager
    from z_np.src.cSkinDeform import DeformerData


import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr

from z_np.src.cBrushCore import WeightBrushCore
from z_np.src._cRegistry import GLOBAL_DEFORMER_REGISTRY

from m_utils.dag.getHistory import get_history

from m_utils.time_decorator import time_decorator, time_block

import time
import array
from . import cRaycastCython


def maya_useNewAPI():
    pass


class WeightBrushContext(omui.MPxContext):
    brushLine = 2.0
    brushColor = om.MColor((1.0, 0.5, 0.0, 1.0))
    brushPresColor = om.MColor((1.0, 1, 1.0, 1.0))

    def __init__(self):
        super(WeightBrushContext, self).__init__()
        # mesh data
        self._shape: str = None
        self.fn_mesh: om.MFnMesh = None

        # preview data
        self._overrode_mObj = None
        self._overrode_shape = None
        self._cSkin_node = None
        self._hide_attrs = []

        # memory data
        self._cSkin_data: DeformerData = None
        self._points_mgr: CMemoryManager = None
        self._vertex_count: int = 0
        # brush
        self._view: omui.M3dView = None
        self._mouse_position_x = None
        self._mouse_position_y = None
        self._ray_source = om.MPoint()
        self._ray_direction = om.MVector()
        self._hit_result = None
        # brush status
        self._isPressed = False

    @staticmethod
    def createOverrideShape(cSkin, *args, **kwargs):
        displayNodeType = "WeightPreviewShape"
        preview_shape = cmds.createNode(displayNodeType, ss=1, **kwargs)
        cmds.setAttr(f"{preview_shape}.layer", WeightBrushCore.paintLayerIndex)
        cmds.setAttr(f"{preview_shape}.influence", WeightBrushCore.paintInfluenceIndex)
        cmds.setAttr(f"{preview_shape}.mask", WeightBrushCore.paintMask)
        cmds.connectAttr(f"{cSkin}.refresh", f"{preview_shape}.refresh", force=True)
        return preview_shape

    # region
    def _create_override_shape(self):
        """创建绘制权重节点，并且把数据写入`self._overrode_shape`,`self._hide_attrs`,`self._cSkin_node`"""

        skinNodeType = "cSkinDeformer"
        # --------------- get selection data ------------------
        try:
            mSel: om.MSelectionList = om.MGlobal.getActiveSelectionList()
            shape_mDag: om.MDagPath = mSel.getDagPath(0).extendToShape()
            self._shape = shape_mDag.fullPathName()
            self.fn_mesh = om.MFnMesh(shape_mDag)  # 劫持内存拿到的MFnMesh是 API1.0，这里必须要重新申请一个 API2.0 的 MFnMesh
            _transform = shape_mDag.pop().fullPathName()
        except Exception:
            om.MGlobal.displayError("Please select meshes !")
            raise RuntimeError("Please select meshes !")

        # --------------- get skin data ---------------------
        try:
            self._cSkin_node = get_history(self._shape, type=skinNodeType)[0]

        except Exception:
            om.MGlobal.displayError("Get skin node failed !")
            raise RuntimeError("Get skin node failed !")

        # ---------------- create preview shape ---------------
        try:
            preview_shape = self.createOverrideShape(self._cSkin_node, parent=_transform)
            self._overrode_shape = preview_shape
            self._overrode_mObj: om.MObject = om.MSelectionList().add(preview_shape).getDependNode(0)
        except Exception:
            om.MGlobal.displayError("Create preview shape failed !")
            raise RuntimeError("Create preview shape failed !")

        # -------------- setup display ------------------------
        try:
            _hide_attr = "lodVisibility"
            _baseValue = cmds.getAttr(f"{self._shape}.{_hide_attr}")
            self._hide_attrs.append({
                "name": f"{self._shape}.{_hide_attr}",
                "value": _baseValue,
            })

            cmds.setAttr(f"{self._shape}.{_hide_attr}", 0)
        except Exception:
            om.MGlobal.displayError("Setup display node failed !")
            raise RuntimeError("Setup display node failed !")
        # --------------- build memory view ----------------------
        try:
            mSel = om.MGlobal.getSelectionListByName(self._cSkin_node)
            cSkin_mObjHandle: om.MObjectHandle = om.MObjectHandle(mSel.getDependNode(0))
            self._cSkin_class = GLOBAL_DEFORMER_REGISTRY[cSkin_mObjHandle.hashCode()]
            self._cSkin_data = GLOBAL_DEFORMER_REGISTRY[cSkin_mObjHandle.hashCode()].DATA
            print("成功劫持 cSkin Memory Data: ", self._cSkin_data)
        except Exception:
            om.MGlobal.displayError("Get skin cData failed !")
            raise RuntimeError("Get skin cData failed !")

        # -------------- DEBUG -------------------------
        cmds.setAttr(f"{preview_shape}.mask", 0)  # debug
        return True

    def _delete_override_shape(self):
        """根据`self._overrode_shape`,`self._cSkin_node`,`self._hide_attrs`恢复数据到之前的状态"""
        if self._overrode_shape:
            cmds.delete(self._overrode_shape)
            self._overrode_shape = None
        if self._cSkin_node:
            self._cSkin_node = None
        if self._hide_attrs:
            for attr in self._hide_attrs:
                cmds.setAttr(attr["name"], attr["value"])
            self._hide_attrs.clear()

    def _refresh_viewport(self, topology=True):
        """VP2 视口重绘"""
        if self._overrode_mObj is None:
            return False

        omr.MRenderer.setGeometryDrawDirty(self._overrode_mObj, topology)
        view: omui.M3dView = omui.M3dView.active3dView()
        view.refresh(False, False)
        return True

    def toolOnSetup(self, event):
        """进入工具：获取模型，装配核心引擎的内存池"""
        # test
        self._count = 0
        self._countTime = 0
        try:
            # -----------
            if self._create_override_shape() is not True:
                om.MGlobal.displayError("Init override shape failed !")
                raise RuntimeError("Init override shape failed !")
            print("创建节点成功")
            # ------------ brush
            self._view = omui.M3dView.active3dView()

            WeightBrushCore.clear_preview_registry()
            print("初始化内存成功")
            WeightBrushCore.setup_memory_pool(self._cSkin_class)
            print("申请内存成功")

        except Exception as e:

            def _exit():
                cmds.setToolTo("selectSuperContext")

            cmds.evalDeferred(_exit)
            om.MGlobal.displayError("进入笔刷失败！")
            om.MGlobal.displayError(str(e))
            raise

    def toolOffCleanup(self):
        """退出工具：命令核心引擎销毁指针"""

        self._delete_override_shape()
        # 调度引擎销毁！
        WeightBrushCore.teardown_memory_pool()
        WeightBrushCore.clear_preview_registry()
        self.__init__()

    def doPress(self, event, drawMgr, context):
        self._shoot_ray_and_process(event, True, drawMgr)

    def doDrag(self, event, drawMgr, context):
        self._shoot_ray_and_process(event, True, drawMgr)

    def doPtrMoved(self, event, drawMgr, context):
        self._shoot_ray_and_process(event, False, drawMgr)
        pass

    def doRelease(self, event, drawMgr, context):
        pass

    def _raycast(self, ray_source_MPoint, ray_dir_MVector):
        """
        终极版多线程射线检测：返回 (世界坐标, Maya Face ID)
        """
        # 1. 准备射线数据
        source_arr = tuple(ray_source_MPoint)[0:3]
        dir_arr = tuple(ray_dir_MVector)

        #  Cython Raycast
        hit_success, closest_t, hit_tri, u, v = cRaycastCython.raycast_mesh_core(
            source_arr,
            dir_arr,
            self._cSkin_class.DATA.output_rawPoints_mgr2D.view,
            self._cSkin_class.DATA.tri_indices_2D.view,
        )

        # 4. 结算结果并反查 Face ID
        if hit_success:
            # 计算 3D 击中坐标
            hit_x = source_arr[0] + dir_arr[0] * closest_t
            hit_y = source_arr[1] + dir_arr[1] * closest_t
            hit_z = source_arr[2] + dir_arr[2] * closest_t

            # 💥 O(1) 极速反查真实的 Maya Face ID！
            hit_face_id = self._cSkin_class.DATA.tri_to_face_map.view[hit_tri]

            # 返回格式：(坐标元组), FaceID
            return (hit_x, hit_y, hit_z), hit_face_id

        # 如果打向了空气，坐标返回 None，FaceID 返回 -1
        return None

    def _raycast_by_mouse(self, event):
        self._mouse_position_x, self._mouse_position_y = event.position
        self._view.viewToWorld(self._mouse_position_x, self._mouse_position_y, self._ray_source, self._ray_direction)
        self._hit_result = self._raycast(self._ray_source, self._ray_direction)
        return self._hit_result

    def _draw_brush_cursor(self, event, drawMgr):
        """利用 drawMgr 绘制 3D 笔刷圆圈 UI"""
        if self._hit_result is None:
            return

        hit_point, hit_face = self._hit_result
        hit_normal = self.fn_mesh.getPolygonNormal(hit_face, om.MSpace.kWorld)

        color = self.brushColor if not self._isPressed else self.brushPresColor

        drawMgr.beginDrawable()
        drawMgr.setColor(color)
        drawMgr.setLineWidth(self.brushLine)
        drawMgr.circle(om.MPoint(hit_point), om.MVector(hit_normal), WeightBrushCore.radius)
        drawMgr.endDrawable()

    # endregion

    @time_decorator
    def _shoot_ray_and_process(self, event, is_pressed, drawMgr):
        """💥 调度枢纽：抓取事件 -> 通知核心 -> 刷新画面 -> 执行算法"""
        _laster_hit = self._hit_result
        with time_block("raycast"):
            self._raycast_by_mouse(event)

        if self._hit_result is None and _laster_hit is not None:  # 鼠标离开模型执行一次
            WeightBrushCore.clear_preview_registry()  # 清理残留的预览颜色
            self._refresh_viewport()  # 刷新掉残留画面

        if self._hit_result is None:
            return

        hit_point = self._hit_result[0]
        with time_block("detect_range"):
            WeightBrushCore.detect_range(hit_point)  # 计算影响点的count，idx，weights, 放到预先申请的缓存中

        if is_pressed:  # 如果按下状态
            with time_block("apply_weight_math"):
                WeightBrushCore.apply_weight_math(hit_point)  # 修改权重

            self._cSkin_class._setDirty()  # 设置脏，让maya自动更新

        # 把计算结果的指针，放到全局内存中
        WeightBrushCore.write_preview_registry()  # 把笔刷数据，更新到笔刷全局内存，方便shape 颜色显示和鼠标交互
        # 刷新视图，主要是为了刷新shape节点
        with time_block("refresh_viewport"):
            self._refresh_viewport()
        self._draw_brush_cursor(event, drawMgr)


class WeightBrushContextCmd(omui.MPxContextCommand):
    COMMAND_NAME = "cBrushCtx"

    def __init__(self):
        super(WeightBrushContextCmd, self).__init__()

    def makeObj(self):
        return WeightBrushContext()

    @staticmethod
    def creator():
        return WeightBrushContextCmd()
