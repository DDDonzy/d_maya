from maya import cmds
from maya.api import OpenMaya as om
from typing import List


class CurveData(om.MFnNurbsCurve):
    """
    B-样条曲线数据类
    继承自 Maya OpenMaya 的 MFnNurbsCurve，提供 B-样条曲线的创建和操作功能
    """

    def __init__(self, controlPoints, degree):
        """
        初始化 B-样条曲线

        Args:
            controlPoints (list): 控制点列表，每个点为 MPoint 对象
            degree (int): 曲线的度数（阶数-1）
        """
        super().__init__()

        # 创建 NURBS 曲线数据对象
        self.data = om.MFnNurbsCurveData().create()
        self._knots = self.generateKnots(controlPoints, degree)
        # 创建 NURBS 曲线
        # 注意：传入的节点向量需要去掉首尾重复的节点
        self.create(
            controlPoints,
            self._knots[1:-1],  # 去掉首尾重复节点
            degree,
            om.MFnNurbsCurve.kOpen,  # 开放型曲线
            False,  # 不是理性曲线
            True,  # 三维曲线
            self.data,
        )

    def build(self):
        """
        重建曲线
        使用当前的控制点位置和参数重新创建曲线
        """
        cv = cmds.createNode("transform", name="bSplineCurve")
        sel: om.MSelectionList = om.MGlobal.getSelectionListByName(cv)
        self.create(
            self.cvPositions(om.MFn.kWorld),  # 获取世界坐标系下的控制点
            self.knots(),  # 当前节点向量
            self.degree,  # 当前度数
            self.form,  # 当前形式（开放/封闭）
            False,
            True,
            sel.getDependNode(0),
        )
        for x in cmds.listRelatives(cv, shapes=1) or []:
            cmds.rename(x, f"{cv}Shape")
        return cv

    def t_length(self, t=1.0):
        """
        根据参数 t 获取曲线长度

        Args:
            t (float): 参数值，范围 [0, 1]

        Returns:
            float: 从曲线起点到参数 t 位置的弧长
        """
        return self.findLengthFromParam(t)

    def parameter(self, length=0):
        """
        根据长度获取对应的parameter参数值

        Args:
            length (float): 从曲线起点开始的长度

        Returns:
            float: 对应的参数值 t
        """
        return self.findParamFromLength(length)

    def get_tWeights(self, t):
        """
        获取参数 t 处所有控制点的基函数权重

        Args:
            t (float): 参数值

        Returns:
            list: 每个控制点对应的基函数值列表
        """
        return [self.basisFunction(i, t, self.degree) for i in range(len(self.cvPositions()))]

    def generateKnots(self, controlPoints, degree):
        """
        为 B-样条曲线生成均匀分布的节点向量

        Args:
            controlPoints (list): 控制点列表
            degree (int): 曲线度数

        Returns:
            list: 节点向量，首尾重复度数次

        Note:
            对于度数为 d 的 B-样条曲线，需要 n+d+1 个节点值
            其中 n 是控制点数量
        """
        d = degree
        count = len(controlPoints)

        # 起始节点：重复度数次的 0.0
        knots = [0.0] * d
        # 内部节点：均匀分布的参数值
        knots += [i / (count - d) for i in range(count - d + 1)]
        # 结束节点：重复度数次的 1.0
        knots += [1.0] * d
        return knots

    def basisFunction(self, i, t, d):
        """
        计算 B-样条基函数值 (Cox-de Boor 递归公式)

        Args:
            i (int): 基函数索引
            t (float): 参数值
            d (int): 度数

        Returns:
            float: 基函数 N_{i,d}(t) 的值

        Note:
            使用 Cox-de Boor 递归公式：
            - 当 d=0 时，N_{i,0}(t) = 1 if t_i <= t < t_{i+1}, else 0
            - 当 d>0 时，N_{i,d}(t) = (t-t_i)/(t_{i+d}-t_i) * N_{i,d-1}(t) +
                                     (t_{i+d+1}-t)/(t_{i+d+1}-t_{i+1}) * N_{i+1,d-1}(t)
        """
        knots = self._knots

        # 递归终止条件：0度基函数
        if d == 0:
            # 特殊处理边界情况：t=1时包含右端点
            if (knots[i] <= t < knots[i + 1]) or (t == 1 and knots[i] <= t <= knots[i + 1]):
                return 1
            else:
                return 0
        else:
            # 递归计算：Cox-de Boor 公式
            denom1 = knots[i + d] - knots[i]
            denom2 = knots[i + d + 1] - knots[i + 1]

            # 第一项：避免除零错误
            term1 = 0.0 if denom1 == 0.0 else (t - knots[i]) / denom1 * self.basisFunction(i, t, d - 1)

            # 第二项：避免除零错误
            term2 = 0.0 if denom2 == 0.0 else (knots[i + d + 1] - t) / denom2 * self.basisFunction(i + 1, t, d - 1)

            return term1 + term2


def addRelativesTwist(control, parentControl, axis="X", suffixName=""):
    """
    Add relatives twist attribute to the control.
    """
    cmds.addAttr(control, longName="relativesTwist", attributeType="double", defaultValue=0, keyable=False)
    cmds.addAttr(control, longName="twist", attributeType="double", defaultValue=0, keyable=False)
    # relative matrix
    node_multMatrix = cmds.createNode("multMatrix", name=f"{suffixName}_multMatrix", ss=1)
    node_inverseMatrix = cmds.createNode("inverseMatrix", name=f"{suffixName}_inverseRelativesMatrix", ss=1)
    cmds.connectAttr(f"{node_inverseMatrix}.outputMatrix", f"{node_multMatrix}.matrixIn[1]")
    # skip scale
    pick_control = cmds.createNode("pickMatrix", name=f"{suffixName}_{control}_pickMatrix", ss=1)
    pick_parentControl = cmds.createNode("pickMatrix", name=f"{suffixName}_{parentControl}_pickMatrix", ss=1)
    cmds.connectAttr(f"{parentControl}.worldMatrix[0]", f"{pick_parentControl}.inputMatrix")
    cmds.connectAttr(f"{control}.worldMatrix[0]", f"{pick_control}.inputMatrix")
    cmds.setAttr(f"{pick_control}.useScale", 0)
    cmds.setAttr(f"{pick_parentControl}.useScale", 0)
    cmds.setAttr(f"{pick_control}.useShear", 0)
    cmds.setAttr(f"{pick_parentControl}.useShear", 0)
    cmds.connectAttr(f"{pick_parentControl}.outputMatrix", f"{node_inverseMatrix}.inputMatrix")
    cmds.connectAttr(f"{pick_control}.outputMatrix", f"{node_multMatrix}.matrixIn[0]")
    # cal twist
    quat_to_euler = cmds.createNode("quatToEuler", name=f"{suffixName}_quatToEuler", ss=1)
    decom_matrix = cmds.createNode("decomposeMatrix", name=f"{suffixName}_decomposeMatrix", ss=1)
    cmds.connectAttr(f"{node_multMatrix}.matrixSum", f"{decom_matrix}.inputMatrix")
    cmds.connectAttr(f"{control}.rotateOrder", f"{decom_matrix}.inputRotateOrder")
    cmds.connectAttr(f"{control}.rotateOrder", f"{quat_to_euler}.inputRotateOrder")
    cmds.connectAttr(f"{decom_matrix}.outputQuatW", f"{quat_to_euler}.inputQuatW")
    cmds.connectAttr(f"{decom_matrix}.outputQuat{axis}", f"{quat_to_euler}.inputQuat{axis}")
    cmds.connectAttr(f"{quat_to_euler}.outputRotate{axis}", f"{control}.twist")


def curveIK(controls: List[str], secondsNum: int = 30, curveDegree: int = 3, frontAxis: int = 0, upAxis: int = 1, uniform: bool = False, suffixName="curveIk", use_offsetParentMatrix: bool = False):
    """
    创建一个基于曲线的IK系统，其中一系列的次级变换（输出物体）会跟随一条由控制器定义的曲线运动。

    Args:
        controls (List[str]): 一个由控制物体名称组成的列表，这些控制器将定义曲线的形状。
        secondsNum (int, optional): 沿曲线生成的次级变换（输出物体）的数量。默认为 30。
        curveDegree (int, optional): 生成的 NURBS 曲线的阶数。1 是线性，3 是三次。默认为 3。
        frontAxis (int, optional): 次级变换（输出物体）上朝向曲线切线方向的轴向。0=X, 1=Y, 2=Z。默认为 0 (X)。
        upAxis (int, optional): 次级变换（输出物体）的“向上”轴。0=X, 1=Y, 2=Z。默认为 1 (Y)。
        uniform (bool, optional): 如果为 True，次级变换（输出物体）将沿曲线长度均匀分布。
                                  如果为 False，它们将根据曲线的参数化分布，这可能导致分布不均，且 'stretch' 属性将被锁定，且 'positionOffset' 属性将被设置为 0，并且这两个功能失效。
        suffixName (str, optional): 用于命名所有新创建节点的后缀字符串。默认为 "curveIk"。
        use_offsetParentMatrix (bool, optional): 如果为 True，会将最终计算的矩阵连接到次级变换（输出物体）的 'offsetParentMatrix' 属性，
                                                 这是一种更简洁的连接方式。如果为 False，则使用 'decomposeMatrix' 节点分别连接到
                                                 独立的平移、旋转和缩放属性上。默认为 False。
    """

    axis = "XYZ"[frontAxis]
    upVector = [(1, 0, 0), (0, 1, 0), (0, 0, 1)][upAxis]
    seconds_list = []
    # build root
    root = cmds.createNode("transform", name=f"{suffixName}_upRoot")
    cmds.delete(cmds.parentConstraint(controls[0], root))

    # controls positions
    controls_mPoint = []
    for x in controls:
        controls_mPoint.append(om.MPoint(cmds.xform(x, ws=1, q=1, t=1)))

    # controls twist
    iter_laster_control = root
    for idx, _ in enumerate(controls):
        control = controls[idx]
        if idx == 0:
            cmds.addAttr(iter_laster_control, longName="relativesTwist", attributeType="double", defaultValue=0, keyable=False)
            cmds.addAttr(iter_laster_control, longName="twist", attributeType="double", defaultValue=0, keyable=False)
        addRelativesTwist(control, root, axis=axis, suffixName=suffixName)
        iter_laster_control = control

    # build curve
    cvData: CurveData = CurveData(controls_mPoint, curveDegree)
    cv = cvData.build()
    cv = cmds.rename(cv, f"{suffixName}_curve")
    cvShape = cmds.listRelatives(cv, shapes=1)[0]

    # curve logic
    cmds.addAttr(cvShape, longName="stretch", attributeType="double", defaultValue=0, min=0, max=1, keyable=True)
    cmds.addAttr(cvShape, longName="positionOffset", attributeType="double", min=0, max=1, keyable=True)
    cmds.addAttr(cvShape, longName="baseLength", attributeType="double", defaultValue=cvData.t_length(1.0), keyable=False)
    cmds.addAttr(cvShape, longName="currentLength", attributeType="double", defaultValue=cvData.t_length(1.0), keyable=False)
    cmds.addAttr(cvShape, longName="lengthScale", attributeType="double", defaultValue=1.0, keyable=False)
    cmds.addAttr(cvShape, longName="outOffset", attributeType="double", min=0, max=1, keyable=False)

    # length
    cvInfo = cmds.createNode("curveInfo", name=f"{suffixName}_curveInfo")
    cmds.connectAttr(f"{cvShape}.worldSpace[0]", f"{cvInfo}.inputCurve")
    cmds.connectAttr(f"{cvInfo}.arcLength", f"{cvShape}.currentLength")
    # length_attr = f"{cvInfo}.arcLength"
    # length scale
    divide = cmds.createNode("multiplyDivide", name=f"{suffixName}_lengthMultiplier", ss=1, n="lengthDivider")
    cmds.connectAttr(f"{cvShape}.currentLength", f"{divide}.input1X")
    cmds.connectAttr(f"{cvShape}.baseLength", f"{divide}.input2X")
    cmds.setAttr(f"{divide}.operation", 2)
    # length_scale_attr = f"{divide}.outputX"
    # stretch
    blend = cmds.createNode("blendColors", name=f"{suffixName}_stretchBlend", ss=1)
    cmds.setAttr(f"{blend}.color1R", 1.0)
    cmds.connectAttr(f"{divide}.outputX", f"{blend}.color2R")
    cmds.connectAttr(f"{cvShape}.stretch", f"{blend}.blender")
    cmds.connectAttr(f"{blend}.outputR", f"{cvShape}.lengthScale")
    # maxOffset
    maxOffset_divide = cmds.createNode("multiplyDivide", name=f"{suffixName}_maxOffsetDivider", ss=1, n="maxOffsetDivider")
    cmds.setAttr(f"{maxOffset_divide}.operation", 2)
    cmds.setAttr(f"{maxOffset_divide}.input1X", 1.0)
    cmds.connectAttr(f"{cvShape}.lengthScale", f"{maxOffset_divide}.input2X")
    maxOffset_sub = cmds.createNode("plusMinusAverage", name=f"{suffixName}_maxOffsetAdder", ss=1, n="maxOffsetSubtract")
    cmds.setAttr(f"{maxOffset_sub}.operation", 2)  # Subtract
    cmds.setAttr(f"{maxOffset_sub}.input1D[0]", 1.0)
    cmds.connectAttr(f"{maxOffset_divide}.outputX", f"{maxOffset_sub}.input1D[1]")
    # mult = cmds.createNode("multDoubleLinear", name=f"{suffixName}_maxOffsetMultiplier", ss=1)
    # cmds.connectAttr(f"{cvShape}.positionOffset", f"{mult}.input1")
    # cmds.connectAttr(f"{maxOffset_sub}.output1D", f"{mult}.input2")
    # cmds.connectAttr(f"{mult}.output", f"{cvShape}.outOffset")
    mult = cmds.createNode("multiplyDivide", name=f"{suffixName}_maxOffsetMultiplier", ss=1)
    cmds.connectAttr(f"{cvShape}.positionOffset", f"{mult}.input1X")
    cmds.connectAttr(f"{maxOffset_sub}.output1D", f"{mult}.input2X")
    cmds.connectAttr(f"{mult}.outputX", f"{cvShape}.outOffset")

    cmds.setAttr(f"{cvShape}.baseLength", lock=True)
    cmds.setAttr(f"{cvShape}.currentLength", lock=True)
    cmds.setAttr(f"{cvShape}.lengthScale", lock=True)
    cmds.setAttr(f"{cvShape}.outOffset", lock=True)

    # build parameters
    parameters = [i / (secondsNum - 1) for i in range(secondsNum)]
    if uniform is False:
        for i, x in enumerate(parameters):
            parameters[i] = cvData.parameter(cvData.t_length(1.0) * x)
        cmds.setAttr(f"{cvShape}.stretch", 1, lock=True, keyable=False)
        cmds.setAttr(f"{cvShape}.positionOffset", 0, lock=True, keyable=False)

    # build motion path
    iter_laster_up_matrix = f"{root}.worldMatrix[0]"
    for idx, uValue in enumerate(parameters):
        transform = cmds.createNode("transform", name=f"{suffixName}Output{idx}")
        seconds_list.append(transform)
        # -------------------------  DEBUG  -------------------------
        # locShape = cmds.createNode("locator", name=f"{SUFFIX}_joint_{idx}Shape", parent=transform)
        # cmds.setAttr(f"{locShape}.overrideEnabled", 1)  # Set to "No Shape"
        # cmds.setAttr(f"{locShape}.overrideColor", 13)  # Set to "No Shape"
        # cmds.setAttr(f"{locShape}.localScale", 300, 300, 300)
        # cmds.setAttr(f"{transform}.displayLocalAxis", 1)
        # -------------------------  DEBUG  -------------------------

        motionPath = cmds.createNode("motionPath", name=f"{suffixName}_motionPath_{idx}")
        # motion path attributes
        cmds.setAttr(f"{motionPath}.frontAxis", frontAxis)
        cmds.setAttr(f"{motionPath}.upAxis", upAxis)
        cmds.setAttr(f"{motionPath}.worldUpType", 2)
        cmds.setAttr(f"{motionPath}.follow", 1)

        cmds.setAttr(f"{motionPath}.worldUpVector", *upVector, type="double3")
        cmds.setAttr(f"{motionPath}.fractionMode", uniform)

        cmds.connectAttr(iter_laster_up_matrix, f"{motionPath}.worldUpMatrix")
        cmds.connectAttr(f"{cvShape}.worldSpace[0]", f"{motionPath}.geometryPath")

        # default uValue
        cmds.addAttr(motionPath, longName="defaultParameter", attributeType="double", defaultValue=uValue, keyable=True)
        cmds.setAttr(f"{motionPath}.defaultParameter", lock=True)
        # divide uValue by stretch
        divide = cmds.createNode("multiplyDivide", name=f"{suffixName}_motionPath_{idx}_divider")
        cmds.connectAttr(f"{motionPath}.defaultParameter", f"{divide}.input1X")
        cmds.connectAttr(f"{cvShape}.lengthScale", f"{divide}.input2X")
        cmds.setAttr(f"{divide}.operation", 2)
        # offset uValue
        uValue_offset = cmds.createNode("plusMinusAverage", name=f"{suffixName}_offsetUValue_{idx}", ss=1)
        cmds.connectAttr(f"{divide}.outputX", f"{uValue_offset}.input1D[0]")
        cmds.connectAttr(f"{cvShape}.outOffset", f"{uValue_offset}.input1D[1]")
        # unit convert
        unitConvert = cmds.createNode("unitConversion", name=f"{suffixName}_uValueUnitConversion{idx}")
        cmds.connectAttr(f"{uValue_offset}.output1D", f"{unitConvert}.input")
        cmds.setAttr(f"{unitConvert}.conversionFactor", 1.0)
        cmds.connectAttr(f"{unitConvert}.output", f"{motionPath}.uValue")

        # compose matrix
        compose_matrix = cmds.createNode("composeMatrix", name=f"{suffixName}_composeMatrix_{idx}", ss=1)
        cmds.connectAttr(f"{motionPath}.allCoordinates", f"{compose_matrix}.inputTranslate")
        cmds.connectAttr(f"{motionPath}.rotate", f"{compose_matrix}.inputRotate")
        cmds.setAttr(f"{compose_matrix}.inputRotateOrder", 0)  # XYZ
        weights_list = cvData.get_tWeights(uValue)
        # twist
        compose_matrix_twist = cmds.createNode("composeMatrix", name=f"{suffixName}_composeMatrix_twist_{idx}", ss=1)
        blend_twist = cmds.createNode("blendWeighted", name=f"{suffixName}_blendWeighted_{idx}_twist")
        for idx, w in enumerate(weights_list):
            control = controls[idx]
            cmds.setAttr(f"{blend_twist}.weight[{idx}]", w)
            cmds.connectAttr(f"{control}.twist", f"{blend_twist}.input[{idx}]")
        cmds.connectAttr(f"{blend_twist}.output", f"{compose_matrix_twist}.inputRotate{axis}")
        cmds.setAttr(f"{compose_matrix_twist}.inputRotateOrder", 0)  # XYZ
        # scale
        for _axis in "XYZ":
            blend_scale = cmds.createNode("blendWeighted", name=f"{suffixName}_blendWeighted_{idx}_scale{_axis}")
            for idx, w in enumerate(weights_list):
                control = controls[idx]
                cmds.setAttr(f"{blend_scale}.weight[{idx}]", w)
                cmds.connectAttr(f"{control}.scale{_axis}", f"{blend_scale}.input[{idx}]")
            cmds.connectAttr(f"{blend_scale}.output", f"{compose_matrix_twist}.inputScale{_axis}")

        mult_matrix = cmds.createNode("multMatrix", name=f"{suffixName}_multMatrix_{idx}", ss=1)
        cmds.connectAttr(f"{compose_matrix}.outputMatrix", f"{mult_matrix}.matrixIn[1]")
        cmds.connectAttr(f"{compose_matrix_twist}.outputMatrix", f"{mult_matrix}.matrixIn[0]")

        if use_offsetParentMatrix:
            cmds.connectAttr(f"{mult_matrix}.matrixSum", f"{transform}.offsetParentMatrix")
        else:
            decompose_matrix = cmds.createNode("decomposeMatrix", name=f"{suffixName}_decomposeMatrix_{idx}", ss=1)
            cmds.connectAttr(f"{mult_matrix}.matrixSum", f"{decompose_matrix}.inputMatrix")
            cmds.connectAttr(f"{decompose_matrix}.outputTranslate", f"{transform}.translate")
            cmds.connectAttr(f"{decompose_matrix}.outputRotate", f"{transform}.rotate")
            cmds.connectAttr(f"{decompose_matrix}.outputScale", f"{transform}.scale")
            cmds.connectAttr(f"{decompose_matrix}.outputShear", f"{transform}.shear")

        iter_laster_up_matrix = f"{compose_matrix}.outputMatrix"

    return root, seconds_list, cvShape


if __name__ == "__main__":
    controls = []
    for x in range(6):
        loc = cmds.spaceLocator(name=f"control_{x:02d}")[0]
        cmds.setAttr(f"{loc}.translate", x * 5, 0, 0)
        controls.append(loc)

    root, transform_list, cvShape = curveIK(
        controls=controls,
        secondsNum=100,
        curveDegree=3,
        frontAxis=0,
        upAxis=1,
        uniform=True,
        use_offsetParentMatrix=False,
        suffixName="curveIkTest",
    )
    for x in transform_list:
        cube = cmds.polyCube()
        cube_shape = cmds.listRelatives(cube, shapes=1)[0]
        cmds.parent(cube_shape, x, r=1, s=1)
        cmds.delete(cube)

    # driver curve
    for x in controls:
        cmds.connectAttr(f"{x}.translate", f"{cvShape}.controlPoints[{controls.index(x)}]")

