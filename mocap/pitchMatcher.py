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
    aInput = None
    aSpeed = None
    aStartFrame = None
    aOutput = None

    def __init__(self):
        om.MPxNode.__init__(self)

    def calculate_simulation(
        self,
        fn_input: oma.MFnAnimCurve,
        start_frame: int,
        current_frame: int,
        fn_speed: oma.MFnAnimCurve | float = 1.0,
    ) -> float:
        """
        计算输入曲线在指定帧区间的积分结果。
        Args:
            fn_input (oma.MFnAnimCurve): 输入动画曲线的函数集。
            fn_speed (oma.MFnAnimCurve | float): 速度动画曲线的函数集，默认值为 1.0。
            start_frame (int): 起始帧（包含）。
            current_frame (int): 当前帧（包含）。
        Returns:
            float: 从起始帧到当前帧的积分累积结果。
        """
        if fn_input is None:
            return 0.0
        time_unit = om.MTime.uiUnit()
        accumulated_pos = 0.0
        prev_input_val = fn_input.evaluate(om.MTime(start_frame, time_unit))
        for t in range(start_frame + 1, current_frame + 1):
            m_time = om.MTime(t, time_unit)
            curr_input_val = fn_input.evaluate(m_time)
            if isinstance(fn_speed, oma.MFnAnimCurve):
                speed_val = fn_speed.evaluate(m_time)
            elif isinstance(fn_speed, (int, float)):
                speed_val = fn_speed
            else:
                speed_val = 1.0
            accumulated_pos += (curr_input_val - prev_input_val) * speed_val
            prev_input_val = curr_input_val
        initial_offset = fn_input.evaluate(om.MTime(start_frame, time_unit))
        return initial_offset + accumulated_pos

    def get_input_fn(self, logical_index: int) -> oma.MFnAnimCurve:
        """
        根据逻辑索引获取输入曲线的函数集。
        Args:
            logical_index (int): 输入属性数组元素的逻辑索引。
        Returns:
            oma.MFnAnimCurve: 连接到该元素的动画曲线函数集；若未连接则可能返回 None。
        """
        attr_plug = om.MPlug(self.thisMObject(), self.aInput)
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

        start_frame_val = data.inputValue(self.aStartFrame).asFloat()
        current_time_val = oma.MAnimControl.currentTime().value
        start_frame = int(start_frame_val)
        current_frame = int(current_time_val)
        speed_plug = om.MPlug(self.thisMObject(), self.aSpeed)
        fn_speed_curve = self.get_connected_anim_curve(speed_plug)
        if not fn_speed_curve:
            fn_speed_curve = data.inputValue(self.aSpeed).asFloat()

        if plug.isElement:
            # call single
            index = plug.logicalIndex()
            fn_input = self.get_input_fn(index)
            result = self.calculate_simulation(fn_input, start_frame, current_frame, fn_speed_curve)
            out_handle = data.outputValue(plug)
            out_handle.setFloat(result)
            data.setClean(plug)

        else:
            # cal all
            input_array_handle: om.MArrayDataHandle = data.inputArrayValue(self.aInput)
            output_array_handle = data.outputArrayValue(self.aOutput)
            builder = output_array_handle.builder()

            for i in range(len(input_array_handle)):
                input_array_handle.jumpToPhysicalElement(i)
                index = input_array_handle.elementLogicalIndex()
                fn_input = self.get_input_fn(index)

                result = self.calculate_simulation(fn_input, start_frame, current_frame, fn_speed_curve)

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

        cls.aInput = nAttr.create("input", "i", om.MFnNumericData.kFloat, 0.0)
        nAttr.readable = False
        nAttr.storable = True
        nAttr.array = True
        nAttr.indexMatters = True
        nAttr.disconnectBehavior = om.MFnAttribute.kDelete

        cls.aSpeed = nAttr.create("speed", "s", om.MFnNumericData.kFloat, 1.0)
        nAttr.readable = False
        nAttr.keyable = True

        cls.aStartFrame = nAttr.create("startFrame", "sf", om.MFnNumericData.kFloat, 0.0)
        nAttr.keyable = True
        nAttr.storable = True

        cls.aOutput = nAttr.create("output", "o", om.MFnNumericData.kFloat, 0.0)
        nAttr.writable = False
        nAttr.storable = True
        nAttr.array = True
        nAttr.usesArrayDataBuilder = True

        cls.addAttribute(cls.aInput)
        cls.addAttribute(cls.aSpeed)
        cls.addAttribute(cls.aStartFrame)
        cls.addAttribute(cls.aOutput)

        cls.attributeAffects(cls.aInput, cls.aOutput)
        cls.attributeAffects(cls.aSpeed, cls.aOutput)
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


def createPitchMatcherNode(*args, **kwargs):
    if not cmds.pluginInfo(Path(__file__).stem, query=True, loaded=True):
        install()
    node = cmds.createNode("pitchMatcher", *args, **kwargs)
    return node


def pitchMatcher():
    attrs = ["*:IKLeg_R.tx", "*:IKLeg_L.tx", "*:RootX_M.tx"]
    node = createPitchMatcherNode()

    for i, x in enumerate(attrs):
        p = cmds.listConnections(x, p=1) or []
        cmds.connectAttr(p[0], f"{node}.input[{i}]")
        cmds.connectAttr(f"{node}.output[{i}]", x, f=1)


def bakeAnimation():
    attrs = ["*:IKLeg_R.tx", "*:IKLeg_L.tx", "*:RootX_M.tx"]
    timeRange = (oma.MAnimControl.animationStartTime().value, oma.MAnimControl.animationEndTime().value)
    cmds.bakeResults(
        attrs,
        t=timeRange,
        sb=1,
        simulation=1,
    )
