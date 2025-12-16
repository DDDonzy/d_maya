import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import sys


def maya_useNewAPI():
    pass


kPluginNodeName = "curveIntegrator"
kPluginNodeId = om.MTypeId(0x0007F7F8)


class CurveIntegratorNode(om.MPxNode):
    aInputCurve = None
    aSpeedCurve = None
    aStartFrame = None
    aOutput = None

    def __init__(self):
        om.MPxNode.__init__(self)

    def setDependentsDirty(self, plug, plugArray):
        print("Dependents dirty for plug: ", plug.name())
        print("Affected plugs: ", [p.name() for p in plugArray])

    def compute(self, plug, data):
        if plug != self.aOutput:
            return

        start_frame = data.inputValue(self.aStartFrame).asTime().value  # 起始帧
        current_time = oma.MAnimControl.currentTime().value  # 当前帧
        # 获取连接的动画曲线
        fn_input_curve: oma.MFnAnimCurve = self.get_connected_anim_curve(self.aInputCurve)
        fn_speed_curve: oma.MFnAnimCurve = self.get_connected_anim_curve(self.aSpeedCurve)
        # 处理未连接情况
        if fn_input_curve is None:
            data.outputValue(self.aOutput).setFloat(0.0)
            data.setClean(plug)
            return

        # 计算
        accumulated_pos = 0.0  # 积分结果

        start_f_int = int(start_frame)  # 起始帧整数
        curr_f_int = int(current_time)  # 当前帧整数

        prev_input_val = fn_input_curve.evaluate(om.MTime(start_f_int))  # 上一帧输入值

        # 循环积分
        for t in range(start_f_int + 1, curr_f_int + 1):
            curr_input_val = fn_input_curve.evaluate(om.MTime(t))  # 当前帧输入值
            if fn_speed_curve:
                speed_val = fn_speed_curve.evaluate(om.MTime(t))  # 当前帧速度值
            else:
                speed_val = 1.0
            delta = curr_input_val - prev_input_val  # 输入值变化量
            accumulated_pos += delta * speed_val  # 积分计算
            prev_input_val = curr_input_val  # 更新上一帧输入值

        initial_offset = fn_input_curve.evaluate(om.MTime(start_frame))  # 起始帧初始偏移
        final_result = initial_offset + accumulated_pos  # 最终结果

        out_handle = data.outputValue(self.aOutput)
        out_handle.setFloat(final_result)
        data.setClean(plug)

    def get_connected_anim_curve(self, attr_obj) -> oma.MFnAnimCurve:
        this_node = self.thisMObject()
        plug = om.MPlug(this_node, attr_obj)
        if not plug.isConnected:
            return None
        sources = plug.sourceWithConversion()
        if sources.isNull:
            return None
        source_node = sources.node()
        if source_node.hasFn(om.MFn.kAnimCurve):
            return oma.MFnAnimCurve(source_node)
        return None

    @classmethod
    def creator(cls):
        return CurveIntegratorNode()

    @classmethod
    def initialize(cls):
        nAttr = om.MFnNumericAttribute()
        uAttr = om.MFnUnitAttribute()

        cls.aInputCurve = nAttr.create("inputCurve", "inC", om.MFnNumericData.kFloat, 0.0)
        nAttr.readable = False
        nAttr.storable = False

        cls.aSpeedCurve = nAttr.create("speedCurve", "spC", om.MFnNumericData.kFloat, 0.0)
        nAttr.readable = False
        nAttr.keyable = True

        cls.aStartFrame = uAttr.create("startFrame", "sf", om.MFnUnitAttribute.kTime, 0.0)
        uAttr.keyable = True
        uAttr.storable = True

        cls.aOutput = nAttr.create("output", "out", om.MFnNumericData.kFloat, 0.0)
        nAttr.writable = False
        nAttr.storable = False

        cls.addAttribute(cls.aInputCurve)
        cls.addAttribute(cls.aSpeedCurve)
        cls.addAttribute(cls.aStartFrame)
        cls.addAttribute(cls.aOutput)

        cls.attributeAffects(cls.aInputCurve, cls.aOutput)
        cls.attributeAffects(cls.aSpeedCurve, cls.aOutput)
        cls.attributeAffects(cls.aStartFrame, cls.aOutput)


def initializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject, "GeminiUser", "2.1", "Any")
    try:
        mplugin.registerNode(kPluginNodeName, kPluginNodeId, CurveIntegratorNode.creator, CurveIntegratorNode.initialize)
    except:
        sys.stderr.write("Failed to register node: " + kPluginNodeName)
        raise


def uninitializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        sys.stderr.write("Failed to deregister node: " + kPluginNodeName)
        raise
