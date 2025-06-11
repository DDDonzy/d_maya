import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr
import maya.cmds as cmds
from enum import Enum
import time
from functools import partial, wraps


class ButtonType(Enum):
    LeftButton = 64
    MiddleButton = 128


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"Function: '{func.__name__}' Runtimes: {duration:.6f} sec")

        return result

    return wrapper


def debutEvent(event: omui.MEvent):
    button = ButtonType(event.mouseButton())
    pos = event.position
    ctrl = event.isModifierControl()
    shift = event.isModifierShift()
    modify = event.isModifierKeyRelease()
    print(button, pos, " - CTRL:", ctrl, " - SHIFT:", shift, f"--{modify}")


def getActiveMesh() -> om.MFnMesh:
    mSel: om.MSelectionList = om.MGlobal.getActiveSelectionList()
    try:
        mDag: om.MDagPath = mSel.getDagPath(0)
        fnMesh: om.MFnMesh = om.MFnMesh(mDag)
        return fnMesh
    except:
        return None


def getRaySourceAndDirection(event: omui.MEvent):
    pos = event.position
    x_pos, y_pos = pos[0], pos[1]

    # 3. 获取当前激活的3D视图
    view = omui.M3dView.active3dView()
    if not view:
        return None

    # 4. 将2D屏幕坐标转换为3D射线
    ray_source = om.MPoint()
    ray_direction = om.MVector()
    view.viewToWorld(x_pos, y_pos, ray_source, ray_direction)
    return ray_source, ray_direction


def get_normal_from_intersection(fnMesh: om.MFnMesh, intersection_result: tuple) -> om.MVector:

    if not intersection_result:
        return None

    # intersection_result 元组的第三个元素 (索引为2) 就是被击中面片的ID
    hit_face_index = intersection_result[2]

    try:
        # 使用面片ID来查询该面的法线
        hit_normal = fnMesh.getPolygonNormal(hit_face_index, om.MSpace.kWorld)
        return hit_normal
    except Exception as e:
        print(f"无法获取面法线 (Could not get face normal) for face {hit_face_index}: {e}")
        return None


class BlendShapeBrushContext(omui.MPxContext):
    kToolName = "customBlendShapeBrush"

    def __init__(self):
        omui.MPxContext.__init__(self)
        self.mesh = None
        self.intersection = None
        self.setTitleString("Custom BlendShape Brush")
        print(f"INIT: {BlendShapeBrushContext.kToolName}")

    @timeit
    def toolOnSetup(self, event: omui.MEvent, *args, **kwargs):
        self.mesh = getActiveMesh()
        self.intersection = self.mesh.autoUniformGridParams()
        self.setCursor(omui.MCursor.kPencilCursor)

        print("Into brush.")
        print(f"mesh:{self.mesh.fullPathName() if self.mesh else 'None'}")

    def toolOffSetup(self):
        self.mesh = None
        self.intersection = None
        self.setCursor(omui.MCursor.kDefaultCursor)
        print("Out of brush.")

    def doHold(self, event, drawMgr, context, *args, **kwargs):
        print("Hold the brush.")

    @timeit
    def doPtrMoved(self, event, drawMgr: omr.MUIDrawManager, context):

        if not self.mesh or not self.intersection:
            return

        ray_source, ray_direction = getRaySourceAndDirection(event)
        if not ray_source or not ray_direction:
            return

        hit_info = self.mesh.closestIntersection(om.MFloatPoint(ray_source),       # 参数1: 射线源点
                                                 om.MFloatVector(ray_direction),   # 参数2: 射线方向
                                                 om.MSpace.kWorld,                 # 参数3: 所在空间
                                                 100000,                           # 参数4: 最大距离
                                                 False,                            # 参数5: 是否测试双方向
                                                 accelParams=self.intersection)
        if hit_info:
            hit_position = om.MPoint(hit_info[0])  
            hit_normal = self.mesh.getPolygonNormal(hit_info[2], om.MSpace.kWorld)

            drawMgr.beginDrawable()
            drawMgr.setColor(om.MColor((1.0, 0.0, 0.0))) 
            drawMgr.circle(hit_position, hit_normal, 0.5, False)
            drawMgr.setPointSize(10)
            drawMgr.point(hit_position)
            
            drawMgr.endDrawable()
        else:
            pass

    def doPress(self, event: omui.MEvent, *args, **kwargs):
        debutEvent(event)

    def doDrag(self, event, drawMgr, context, *args, **kwargs):
        debutEvent(event)

    def doRelease(self, event: omui.MEvent, *args, **kwargs):
        debutEvent(event)


class BlendShapeBrushContextCmd(omui.MPxContextCommand):
    kCmdName = "customBlendShapeBrush"

    def __init__(self):
        omui.MPxContextCommand.__init__(self)

    @staticmethod
    def creator():
        return BlendShapeBrushContextCmd()

    def makeObj(self):
        return BlendShapeBrushContext()

    def appendSyntax(self):
        pass


def maya_useNewAPI():
    pass


def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerContextCommand(
            BlendShapeBrushContextCmd.kCmdName,
            BlendShapeBrushContextCmd.creator
        )
        print(f"INSTALL: {BlendShapeBrushContextCmd.kCmdName}")
    except:
        om.MGlobal.displayError(f"ERROR-INSTALL: {BlendShapeBrushContextCmd.kCmdName}")


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterContextCommand(BlendShapeBrushContextCmd.kCmdName)
        print(f"UNINSTALL: {BlendShapeBrushContextCmd.kCmdName}")
    except:
        om.MGlobal.displayError(f"ERROR-UNINSTALL: {BlendShapeBrushContextCmd.kCmdName}")
