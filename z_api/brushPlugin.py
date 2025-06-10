import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr
import maya.cmds as cmds
from enum import Enum


class ButtonType(Enum):
    LeftButton = 64
    MiddleButton = 128


def getActiveMesh() -> om.MFnMesh:
    mSel: om.MSelectionList = om.MGlobal.getActiveSelectionList()
    try:
        mDag: om.MDagPath = mSel.getDagPath(0)
        fnMesh: om.MFnMesh = om.MFnMesh(mDag)
        return fnMesh
    except:
        return None


class BlendShapeBrushContext(omui.MPxContext):
    kToolName = "customBlendShapeBrush"

    def __init__(self):
        omui.MPxContext.__init__(self)
        self.setTitleString("Custom BlendShape Brush")
        print(f"INIT: {BlendShapeBrushContext.kToolName}")

    def toolOnSetup(self, event: omui.MEvent, *args, **kwargs):
        fnMesh = getActiveMesh()

        print("Into brush.")
        print(f"mesh:{fnMesh.fullPathName() if fnMesh else 'None'}")

    def toolOffSetup(self):
        print("Out of brush.")

    def doHold(self, event, drawMgr, context, *args, **kwargs):
        print("Hold the brush.")

    def doPtrMoved(self, event, drawMgr:omr.MUIDrawManager, context):

        # 2. 开始绘制。所有 MUIDrawManager 的操作都应在此范围内
        drawMgr.beginDrawable()

        # 3. 设置绘制颜色
        # drawMgr.setColor(self.brush_color)

        # 4. 绘制圆环
        #    参数：圆心，法线，半径，是否填充
        # drawMgr.circle(om.MPoint(0,0,0), om.MVector(0,0,1), 10, False)
        drawMgr.circle2d(om.MPoint(event.position),100,100,True)

        # 5. 结束绘制
        drawMgr.endDrawable()

    def doPress(self, event: omui.MEvent, *args, **kwargs):
        self.debutEvent(event)
        hit_point = self.getHitPointOnMesh(event)
        if hit_point:
            # 创建一个定位器来显示撞击点
            locator_name = "hitPoint_debug_locator"
            if not cmds.objExists(locator_name):
                locator_name = cmds.spaceLocator(name=locator_name)[0]
            cmds.xform(locator_name, translation=(hit_point.x, hit_point.y, hit_point.z), worldSpace=True)

    def doDrag(self, event, drawMgr, context, *args, **kwargs):
        self.debutEvent(event)

    def doRelease(self, event: omui.MEvent, *args, **kwargs):
        self.debutEvent(event)

    def debutEvent(self, event: omui.MEvent):
        button = ButtonType(event.mouseButton())
        pos = event.position
        ctrl = event.isModifierControl()
        shift = event.isModifierShift()
        modify = event.isModifierKeyRelease()
        print(button, pos, " - CTRL:", ctrl, " - SHIFT:", shift, f"--{modify}")

    def getHitPointOnMesh(self, event: omui.MEvent) -> om.MPoint:

        # 1. 获取目标网格
        fnMesh = getActiveMesh()
        if not fnMesh:
            return None

        # 2. 从事件中获取2D屏幕坐标
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

        # 5. 在世界空间中执行射线-网格相交测试
        intersection_result = fnMesh.closestIntersection(
            om.MFloatPoint(ray_source),       # 参数1: 射线源点
            om.MFloatVector(ray_direction),   # 参数2: 射线方向
            om.MSpace.kWorld,                 # 参数3: 所在空间
            100000,                         # 参数4: 最大距离
            False                             # 参数5: 是否测试双方向
        )
        if intersection_result:
            print(intersection_result)
            hit_point = intersection_result[0]
            return om.MPoint(hit_point)

        return None


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
