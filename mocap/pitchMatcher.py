import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
from maya import cmds

from pathlib import Path

__all__ = [
    "pitchMatcher",
    "install",
]


def maya_useNewAPI():
    pass


kPluginNodeName = "pitchMatcher"
kPluginNodeId = om.MTypeId(0x0007F7F8)


class _PitchMatcher(om.MPxNode):
    aInputCurve = None
    aSpeedCurve = None
    aStartFrame = None
    aOutput = None

    def __init__(self):
        om.MPxNode.__init__(self)

    def calculate_simulation(
        self,
        fn_input: oma.MFnAnimCurve,
        fn_speed: oma.MFnAnimCurve | None,
        start_frame: int,
        current_frame: int,
    ) -> float:
        """
        计算输入曲线在指定帧区间的积分结果。
        Args:
            fn_input (oma.MFnAnimCurve): 输入动画曲线的函数集。
            fn_speed (oma.MFnAnimCurve | None): 速度动画曲线的函数集；若为 None，则速度视为 1.0。
            start_frame (int): 起始帧（包含）。
            current_frame (int): 当前帧（包含）。
        Returns:
            float: 从起始帧到当前帧的积分累积结果。
        """
        if fn_input is None:
            return 0.0
        accumulated_pos = 0.0
        prev_input_val = fn_input.evaluate(om.MTime(start_frame))
        for t in range(start_frame + 1, current_frame + 1):
            m_time = om.MTime(t)
            curr_input_val = fn_input.evaluate(m_time)
            if fn_speed:
                speed_val = fn_speed.evaluate(m_time)
            else:
                speed_val = 1.0
            accumulated_pos += (curr_input_val - prev_input_val) * speed_val
            prev_input_val = curr_input_val
        initial_offset = fn_input.evaluate(om.MTime(start_frame))
        return initial_offset + accumulated_pos

    def get_input_fn(self, logical_index: int) -> oma.MFnAnimCurve:
        """
        根据逻辑索引获取输入曲线的函数集。
        Args:
            logical_index (int): 输入属性数组元素的逻辑索引。
        Returns:
            oma.MFnAnimCurve: 连接到该元素的动画曲线函数集；若未连接则可能返回 None。
        """
        attr_plug = om.MPlug(self.thisMObject(), self.aInputCurve)
        element_plug = attr_plug.elementByLogicalIndex(logical_index)
        return self.get_connected_anim_curve(element_plug)

    def get_connected_anim_curve(self, plug: om.MPlug) -> oma.MFnAnimCurve:
        """获取与给定 Plug 相连的动画曲线函数集。
        Args:
            plug (om.MPlug): 需要解析其输入连接的属性 Plug。
        Returns:
            oma.MFnAnimCurve: 若 plug 的源节点为动画曲线则返回其函数集；若未连接或源类型不匹配则返回 None。
        """
        if not plug.isConnected:
            return None
        sources = plug.sourceWithConversion()
        if sources.isNull:
            return None
        source_node = sources.node()
        if source_node.hasFn(om.MFn.kAnimCurve):
            return oma.MFnAnimCurve(source_node)
        return None

    def compute(self, plug: om.MPlug, data: om.MDataBlock):
        if plug.attribute() != self.aOutput:
            return

        start_frame_val = data.inputValue(self.aStartFrame).asTime().value
        current_time_val = oma.MAnimControl.currentTime().value
        start_frame = int(start_frame_val)
        current_frame = int(current_time_val)
        speed_plug = om.MPlug(self.thisMObject(), self.aSpeedCurve)
        fn_speed_curve = self.get_connected_anim_curve(speed_plug)

        if plug.isElement():
            # call single
            index = plug.logicalIndex()
            fn_input = self.get_input_fn(index)
            result = self.calculate_simulation(fn_input, fn_speed_curve, start_frame, current_frame)
            out_handle = data.outputValue(plug)
            out_handle.setFloat(result)
            data.setClean(plug)

        else:
            # cal all
            input_array_handle = data.inputArrayValue(self.aInputCurve)
            output_array_handle = data.outputArrayValue(self.aOutput)
            builder = output_array_handle.builder()

            for i in range(len(input_array_handle)):
                input_array_handle.jumpToElement(i)
                index = input_array_handle.elementIndex()

                fn_input = self.get_input_fn(index)

                result = self.calculate_simulation(fn_input, fn_speed_curve, start_frame, current_frame)

                out_element = builder.addElement(index)
                out_element.setFloat(result)

            output_array_handle.set(builder)
            output_array_handle.setAllClean()

    @classmethod
    def creator(cls):
        return _PitchMatcher()

    @classmethod
    def initialize(cls):
        nAttr = om.MFnNumericAttribute()
        uAttr = om.MFnUnitAttribute()

        cls.aInputCurve = nAttr.create("inputCurve", "inC", om.MFnNumericData.kFloat, 0.0)
        nAttr.readable = False
        nAttr.storable = False
        nAttr.array = True
        nAttr.indexMatters = True
        nAttr.disconnectBehavior = om.MFnAttribute.kDelete

        cls.aSpeedCurve = nAttr.create("speedCurve", "spC", om.MFnNumericData.kFloat, 0.0)
        nAttr.readable = False
        nAttr.keyable = True

        cls.aStartFrame = uAttr.create("startFrame", "sf", om.MFnUnitAttribute.kTime, 0.0)
        uAttr.keyable = True
        uAttr.storable = True

        cls.aOutput = nAttr.create("output", "out", om.MFnNumericData.kFloat, 0.0)
        nAttr.writable = False
        nAttr.storable = False
        nAttr.array = True
        nAttr.usesArrayDataBuilder = True

        cls.addAttribute(cls.aInputCurve)
        cls.addAttribute(cls.aSpeedCurve)
        cls.addAttribute(cls.aStartFrame)
        cls.addAttribute(cls.aOutput)

        cls.attributeAffects(cls.aInputCurve, cls.aOutput)
        cls.attributeAffects(cls.aSpeedCurve, cls.aOutput)
        cls.attributeAffects(cls.aStartFrame, cls.aOutput)


def initializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject, "Donzy", "1.0", "Any")
    try:
        mplugin.registerNode(kPluginNodeName, kPluginNodeId, _PitchMatcher.creator, _PitchMatcher.initialize)
    except:
        om.MGlobal.displayError("Failed to register node: " + kPluginNodeName)
        raise


def uninitializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        om.MGlobal.displayError("Failed to deregister node: " + kPluginNodeName)
        raise


def install():
    cmds.loadPlugin(__file__.replace(".pyc", ".py"), quiet=True)


def pitchMatcher(*args, **kwargs):
    if not cmds.pluginInfo(Path(__file__).stem, query=True, loaded=True):
        install()
    node = cmds.createNode("pitchMatcher", *args, **kwargs)
    return node
