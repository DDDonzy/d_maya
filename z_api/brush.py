import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds
from enum import Enum


class ButtonType(Enum):
    LeftButton = 64
    MiddleButton = 128


class BlendShapeBrushContext(omui.MPxContext):
    kToolName = "customBlendShapeBrush"

    def __init__(self):
        omui.MPxContext.__init__(self)
        self.setTitleString("Custom BlendShape Brush")

    def toolOnSetup(self, event: omui.MEvent, *args, **kwargs):
        self.setHelpString("拖拽鼠标绘制BlendShape权重")

    def doPress(self, event: omui.MEvent, *args, **kwargs):
        self.debutEvent(event)

    def doDrag(self, event, drawMgr, context, *args, **kwargs):
        self.debutEvent(event)

    def doRelease(self, event: omui.MEvent, *args, **kwargs):
        self.debutEvent(event)

    def debutEvent(self, event: omui.MEvent):
        button = ButtonType(event.mouseButton())
        pos = event.position
        ctrl = event.isModifierControl()
        shift = event.isModifierShift()
        print(button, pos, " - CTRL:", ctrl, " - SHIFT:", shift)


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
