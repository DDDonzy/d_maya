from maya import cmds
from maya.api import OpenMaya as om
from typing import List


class CurveData(om.MFnNurbsCurve):
    def __init__(
        self,
        controlPoints: List[om.MPoint],
        degree: int = 3,
    ):
        """
        Args:
            controlPoints (list): Controls Points Type MPoint
            degree (int): Curve Degree
        """
        super().__init__()

        self.data = om.MFnNurbsCurveData().create()
        self._knots = self.generateKnots(controlPoints, degree)
        self.create(
            controlPoints,
            self._knots[1:-1],
            degree,
            om.MFnNurbsCurve.kOpen,
            False,
            True,
            self.data,
        )

    def build(self):
        cv = cmds.createNode("transform", name="bSplineCurve")
        sel: om.MSelectionList = om.MGlobal.getSelectionListByName(cv)
        self.create(
            self.cvPositions(om.MFn.kWorld),
            self.knots(),
            self.degree,
            self.form,
            False,
            True,
            sel.getDependNode(0),
        )
        for x in cmds.listRelatives(cv, shapes=1) or []:
            cmds.rename(x, f"{cv}Shape")
        return cv

    def get_length_by_parameter(self, parameter=1.0):
        return self.findLengthFromParam(parameter)

    def get_parameter_by_length(self, length=0):
        return self.findParamFromLength(length)

    def get_weights_by_parameter(self, parameter):
        return [self.basisFunction(i, parameter, self.degree) for i in range(len(self.cvPositions()))]

    def generateKnots(self, controlPoints, degree):
        d = degree
        count = len(controlPoints)

        knots = [0.0] * d
        knots += [i / (count - d) for i in range(count - d + 1)]
        knots += [1.0] * d
        return knots

    def basisFunction(self, i, parameter, degree):
        knots = self._knots
        if degree == 0:
            if (knots[i] <= parameter < knots[i + 1]) or (parameter == 1 and knots[i] <= parameter <= knots[i + 1]):
                return 1
            else:
                return 0
        else:
            denom1 = knots[i + degree] - knots[i]
            denom2 = knots[i + degree + 1] - knots[i + 1]
            term1 = 0.0 if denom1 == 0.0 else (parameter - knots[i]) / denom1 * self.basisFunction(i, parameter, degree - 1)
            term2 = 0.0 if denom2 == 0.0 else (knots[i + degree + 1] - parameter) / denom2 * self.basisFunction(i + 1, parameter, degree - 1)
            return term1 + term2


def curveIK(
    controls: List[str],
    secondsNum: int = 30,
    curveDegree: int = 3,
    frontAxis: int = 0,
    uniform: bool = False,
    suffixName: str = "curveIk",
    use_offsetParentMatrix: bool = False,
):
    """
    Create a curve-based IK system where a series of secondary transforms (output objects) follow a curve defined by controllers.

    Args:
        controls (List[str]): A list of control object names that will define the shape of the curve.
        secondsNum (int, optional): Number of secondary transforms (output objects) to generate along the curve. Defaults to 30.
        curveDegree (int, optional): Degree of the generated NURBS curve. 1 is linear, 3 is cubic. Defaults to 3.
        frontAxis (int, optional): Axis on the secondary transforms (output objects) that will point in the direction of the curve tangent. 0=X, 1=Y, 2=Z. Defaults to 0 (X).
        uniform (bool, optional): If True, secondary transforms (output objects) will be evenly distributed along the curve length.
                                 If False, they will be distributed according to the curve parameterization, which may result in uneven distribution,
                                 and the 'stretch' attribute will be locked, the 'positionOffset' attribute will be set to 0, and both features will be disabled.
        suffixName (str, optional): Suffix string used for naming all newly created nodes. Defaults to "curveIk".
        use_offsetParentMatrix (bool, optional): If True, the final calculated matrix will be connected to the secondary transforms' (output objects')
                                                'offsetParentMatrix' attribute, which is a more streamlined connection method. If False,
                                                'decomposeMatrix' nodes will be used to connect to individual translate, rotate and scale attributes. Defaults to False.
    """

    axis = "XYZ"[frontAxis]
    frontVector = [om.MVector(1, 0, 0), om.MVector(0, 1, 0), om.MVector(0, 0, 1)][frontAxis]

    # build root
    root = controls[0]

    # get controls objects positions to MPoint
    controls_mPoint = []
    for x in controls:
        controls_mPoint.append(om.MPoint(cmds.xform(x, ws=1, q=1, t=1)))

    # controls twist
    pickMatrix_root = cmds.createNode("pickMatrix", name=f"{suffixName}_root_pickMatrix", ss=1)
    cmds.setAttr(f"{pickMatrix_root}.useTranslate", 0)
    cmds.setAttr(f"{pickMatrix_root}.useScale", 0)
    cmds.setAttr(f"{pickMatrix_root}.useShear", 0)
    cmds.connectAttr(f"{root}.parentMatrix", f"{pickMatrix_root}.inputMatrix")

    pickMatrix_control_S_list = []
    iter_pickMatrix_control_Rotate = pickMatrix_root
    for idx, _ in enumerate(controls):
        control = controls[idx]

        cmds.addAttr(control, longName="twist", attributeType="double", defaultValue=0, keyable=False)

        # pick only rotate
        pickMatrix_control_Rotate = cmds.createNode("pickMatrix", name=f"{suffixName}_{control}_pickMatrix", ss=1)
        cmds.connectAttr(f"{control}.worldMatrix[0]", f"{pickMatrix_control_Rotate}.inputMatrix")
        cmds.setAttr(f"{pickMatrix_control_Rotate}.useTranslate", 0)
        cmds.setAttr(f"{pickMatrix_control_Rotate}.useScale", 0)
        cmds.setAttr(f"{pickMatrix_control_Rotate}.useShear", 0)

        # relative matrix
        node_multMatrix = cmds.createNode("multMatrix", name=f"{suffixName}_multMatrix", ss=1)
        cmds.connectAttr(f"{pickMatrix_control_Rotate}.outputMatrix", f"{node_multMatrix}.matrixIn[0]")
        inverseMatrix = cmds.createNode("inverseMatrix", name=f"{suffixName}_multMatrix", ss=1)
        cmds.connectAttr(f"{iter_pickMatrix_control_Rotate}.outputMatrix", f"{inverseMatrix}.inputMatrix")
        cmds.connectAttr(f"{inverseMatrix}.outputMatrix", f"{node_multMatrix}.matrixIn[1]")

        # cal twist
        quat_to_euler = cmds.createNode("quatToEuler", name=f"{suffixName}_quatToEuler", ss=1)
        decom_matrix = cmds.createNode("decomposeMatrix", name=f"{suffixName}_decomposeMatrix", ss=1)
        cmds.connectAttr(f"{node_multMatrix}.matrixSum", f"{decom_matrix}.inputMatrix")
        cmds.connectAttr(f"{control}.rotateOrder", f"{decom_matrix}.inputRotateOrder")
        cmds.connectAttr(f"{control}.rotateOrder", f"{quat_to_euler}.inputRotateOrder")
        cmds.connectAttr(f"{decom_matrix}.outputQuatW", f"{quat_to_euler}.inputQuatW")
        cmds.connectAttr(f"{decom_matrix}.outputQuat{axis}", f"{quat_to_euler}.inputQuat{axis}")
        if idx > 0:
            add_twist = cmds.createNode("plusMinusAverage", name=f"{suffixName}_plusMinusAverage", ss=1)
            cmds.connectAttr(f"{quat_to_euler}.outputRotate{axis}", f"{add_twist}.input1D[0]")
            cmds.connectAttr(f"{controls[idx - 1]}.twist", f"{add_twist}.input1D[1]")
            cmds.connectAttr(f"{add_twist}.output1D", f"{control}.twist")
        else:
            cmds.connectAttr(f"{quat_to_euler}.outputRotate{axis}", f"{control}.twist")

        # pick only scale
        pickMatrix_control_S = cmds.createNode("pickMatrix", name=f"{suffixName}_{control}_pickMatrix", ss=1)
        cmds.connectAttr(f"{control}.worldMatrix[0]", f"{pickMatrix_control_S}.inputMatrix")
        cmds.setAttr(f"{pickMatrix_control_S}.useTranslate", 0)
        cmds.setAttr(f"{pickMatrix_control_S}.useRotate", 0)
        pickMatrix_control_S_list.append(pickMatrix_control_S)
        iter_pickMatrix_control_Rotate = pickMatrix_control_Rotate

    # build curve
    cvData: CurveData = CurveData(controls_mPoint, curveDegree)
    cv = cvData.build()
    cv = cmds.rename(cv, f"{suffixName}_curve")
    cvShape = cmds.listRelatives(cv, shapes=1)[0]
    cmds.setAttr(f"{cv}.inheritsTransform", 0)

    # curve logic
    defaultLength = cvData.get_length_by_parameter(1.0)
    cmds.addAttr(cvShape, longName="stretch", attributeType="double", defaultValue=0, min=0, max=1, keyable=True)
    cmds.addAttr(cvShape, longName="positionOffset", attributeType="double", min=0, max=1, keyable=True)
    cmds.addAttr(cvShape, longName="globalScale", attributeType="double", min=1e-6, keyable=False, defaultValue=1.0)
    cmds.addAttr(cvShape, longName="baseLength", attributeType="double", defaultValue=defaultLength, keyable=False)
    cmds.addAttr(cvShape, longName="currentLength", attributeType="double", defaultValue=defaultLength, keyable=False)
    cmds.addAttr(cvShape, longName="lengthScale", attributeType="double", defaultValue=1.0, keyable=False)
    cmds.addAttr(cvShape, longName="outOffset", attributeType="double", min=0, max=1, keyable=False)
    cmds.addAttr(cvShape, longName="contraction", attributeType="double", defaultValue=1.0, max=1, min=1e-6, keyable=True)

    currentLength_attr = f"{cvShape}.currentLength"
    baseLength_attr = f"{cvShape}.baseLength"
    lengthScale_attr = f"{cvShape}.lengthScale"
    stretch_attr = f"{cvShape}.stretch"
    positionOffset_attr = f"{cvShape}.positionOffset"
    contraction_attr = f"{cvShape}.contraction"

    # global scale multiplier
    globalMultiplier = cmds.createNode("multiplyDivide", name=f"{suffixName}_globalScaleMultiplier", ss=1)
    cmds.connectAttr(f"{cvShape}.globalScale", f"{globalMultiplier}.input1X")
    cmds.setAttr(f"{globalMultiplier}.input2X", defaultLength)
    contractionMultiplier = cmds.createNode("multiplyDivide", name=f"{suffixName}_contractionMultiplier", ss=1)
    cmds.connectAttr(contraction_attr, f"{contractionMultiplier}.input1X")
    cmds.connectAttr(f"{globalMultiplier}.outputX", f"{contractionMultiplier}.input2X")
    cmds.connectAttr(f"{contractionMultiplier}.outputX", f"{cvShape}.baseLength")

    # current length
    cvInfo = cmds.createNode("curveInfo", name=f"{suffixName}_curveInfo", ss=1)
    cmds.connectAttr(f"{cvShape}.worldSpace[0]", f"{cvInfo}.inputCurve")
    cmds.connectAttr(f"{cvInfo}.arcLength", currentLength_attr)
    # length scale
    divide = cmds.createNode("multiplyDivide", name=f"{suffixName}_lengthMultiplier", ss=1)
    cmds.connectAttr(currentLength_attr, f"{divide}.input1X")
    cmds.connectAttr(baseLength_attr, f"{divide}.input2X")
    cmds.setAttr(f"{divide}.operation", 2)
    # stretch
    blend = cmds.createNode("blendColors", name=f"{suffixName}_stretchBlend", ss=1)
    cmds.setAttr(f"{blend}.color1R", 1.0)
    cmds.connectAttr(f"{divide}.outputX", f"{blend}.color2R")
    cmds.connectAttr(stretch_attr, f"{blend}.blender")
    cmds.connectAttr(f"{blend}.outputR", lengthScale_attr)
    # max Offset
    maxOffset_divide = cmds.createNode("multiplyDivide", name=f"{suffixName}_maxOffsetDivider", ss=1)
    cmds.setAttr(f"{maxOffset_divide}.operation", 2)
    cmds.setAttr(f"{maxOffset_divide}.input1X", 1.0)
    cmds.connectAttr(lengthScale_attr, f"{maxOffset_divide}.input2X")
    maxOffset_sub = cmds.createNode("plusMinusAverage", name=f"{suffixName}_maxOffsetAdder", ss=1)
    cmds.setAttr(f"{maxOffset_sub}.operation", 2)  # Subtract
    cmds.setAttr(f"{maxOffset_sub}.input1D[0]", 1.0)
    cmds.connectAttr(f"{maxOffset_divide}.outputX", f"{maxOffset_sub}.input1D[1]")

    mult = cmds.createNode("multiplyDivide", name=f"{suffixName}_maxOffsetMultiplier", ss=1)
    cmds.connectAttr(positionOffset_attr, f"{mult}.input1X")
    cmds.connectAttr(f"{maxOffset_sub}.output1D", f"{mult}.input2X")
    cmds.connectAttr(f"{mult}.outputX", f"{cvShape}.outOffset")

    cmds.setAttr(baseLength_attr, lock=True)
    cmds.setAttr(currentLength_attr, lock=True)
    cmds.setAttr(lengthScale_attr, lock=True)
    cmds.setAttr(f"{cvShape}.outOffset", lock=True)

    # build parameters
    parameters = [i / (secondsNum - 1) for i in range(secondsNum)]
    if uniform is False:
        for i, x in enumerate(parameters):
            parameters[i] = cvData.get_parameter_by_length(cvData.get_length_by_parameter(1.0) * x)
        cmds.setAttr(stretch_attr, 1, lock=True, keyable=False)
        cmds.setAttr(positionOffset_attr, 0, lock=True, keyable=False)

    # build motion path
    seconds_list = []
    iter_laster_aim_matrix = None
    for idx, uValue in enumerate(parameters):
        # uValue data
        weights_list = cvData.get_weights_by_parameter(uValue)
        # build output transform
        transform = cmds.createNode("transform", name=f"{suffixName}Output{idx}")
        seconds_list.append(transform)
        # Motion Path
        motionPath = cmds.createNode("motionPath", name=f"{suffixName}_motionPath_{idx}")
        # default uValue
        cmds.addAttr(motionPath, longName="defaultParameter", attributeType="double", defaultValue=uValue, keyable=True)
        cmds.setAttr(f"{motionPath}.defaultParameter", lock=True)
        # motion path attributes
        cmds.setAttr(f"{motionPath}.follow", 0)
        cmds.setAttr(f"{motionPath}.fractionMode", uniform)
        cmds.connectAttr(f"{cvShape}.worldSpace[0]", f"{motionPath}.geometryPath")
        # divide uValue by stretch
        divide = cmds.createNode("multiplyDivide", name=f"{suffixName}_motionPath_{idx}_divider")
        cmds.connectAttr(f"{motionPath}.defaultParameter", f"{divide}.input1X")
        cmds.connectAttr(lengthScale_attr, f"{divide}.input2X")
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
        # out mult matrix
        mult_matrix = cmds.createNode("multMatrix", name=f"{suffixName}_multMatrix_{idx}", ss=1)

        # aim matrix
        compose_matrix = cmds.createNode("composeMatrix", name=f"{suffixName}_composeMatrix_{idx}", ss=1)
        cmds.connectAttr(f"{motionPath}.allCoordinates", f"{compose_matrix}.inputTranslate")

        if iter_laster_aim_matrix:
            # aim source
            decom = cmds.createNode("decomposeMatrix", name=f"{suffixName}_decomposeMatrix_{idx}", ss=1)
            cmds.connectAttr(f"{iter_laster_aim_matrix}.outputMatrix", f"{decom}.inputMatrix")
            cmds.connectAttr(f"{decom}.outputRotate", f"{compose_matrix}.inputRotate")
            # aim target
            pos_matrix = cmds.createNode("composeMatrix", name=f"{suffixName}_composeMatrix_{idx}", ss=1)
            cmds.connectAttr(f"{motionPath}.allCoordinates", f"{pos_matrix}.inputTranslate")
            cmds.connectAttr(f"{pos_matrix}.outputMatrix", f"{iter_laster_aim_matrix}.primary.primaryTargetMatrix")

        aim_matrix = cmds.createNode("aimMatrix", name=f"{suffixName}_aimMatrix{idx}", ss=1)
        cmds.connectAttr(f"{compose_matrix}.outputMatrix", f"{aim_matrix}.inputMatrix")
        if idx == len(parameters) - 1:
            cmds.connectAttr(f"{iter_laster_aim_matrix}.outputMatrix", f"{aim_matrix}.primary.primaryTargetMatrix")
            cmds.setAttr(f"{aim_matrix}.primaryInputAxis", *(frontVector * -1))
        cmds.connectAttr(f"{aim_matrix}.outputMatrix", f"{mult_matrix}.matrixIn[2]")  # pos
        iter_laster_aim_matrix = aim_matrix

        # twist and scale
        compose_matrix_twist = cmds.createNode("composeMatrix", name=f"{suffixName}_composeMatrix_twist_{idx}", ss=1)
        blend_twist = cmds.createNode("blendWeighted", name=f"{suffixName}_blendWeighted_{idx}_twist")
        wtAddMatrix = cmds.createNode("wtAddMatrix", name=f"{suffixName}_wtAddMatrix{idx}", ss=1)
        for w_idx, w in enumerate(weights_list):
            if w == 0:
                continue
            # twist
            cmds.setAttr(f"{blend_twist}.weight[{w_idx}]", w)
            cmds.connectAttr(f"{controls[w_idx]}.twist", f"{blend_twist}.input[{w_idx}]")
            # scale
            cmds.connectAttr(f"{pickMatrix_control_S_list[w_idx]}.outputMatrix", f"{wtAddMatrix}.wtMatrix[{w_idx}].matrixIn")
            cmds.setAttr(f"{wtAddMatrix}.wtMatrix[{w_idx}].weightIn", w)

        cmds.connectAttr(f"{blend_twist}.output", f"{compose_matrix_twist}.inputRotate{axis}")
        cmds.connectAttr(f"{compose_matrix_twist}.outputMatrix", f"{mult_matrix}.matrixIn[1]")
        cmds.connectAttr(f"{wtAddMatrix}.matrixSum", f"{mult_matrix}.matrixIn[0]")

        # output
        if use_offsetParentMatrix:
            cmds.connectAttr(f"{mult_matrix}.matrixSum", f"{transform}.offsetParentMatrix")
        else:
            decompose_matrix = cmds.createNode("decomposeMatrix", name=f"{suffixName}_decomposeMatrix_{idx}", ss=1)
            cmds.connectAttr(f"{mult_matrix}.matrixSum", f"{decompose_matrix}.inputMatrix")
            cmds.connectAttr(f"{decompose_matrix}.outputTranslate", f"{transform}.translate")
            cmds.connectAttr(f"{decompose_matrix}.outputRotate", f"{transform}.rotate")
            cmds.connectAttr(f"{decompose_matrix}.outputScale", f"{transform}.scale")
            cmds.connectAttr(f"{decompose_matrix}.outputShear", f"{transform}.shear")

    # sync attributes
    for x in controls:
        cmds.addAttr(x, longName="stretch", attributeType="double", defaultValue=0, min=0, max=1, keyable=True, pxy=stretch_attr)
        cmds.addAttr(x, longName="positionOffset", attributeType="double", defaultValue=0, min=0, max=1, keyable=True, pxy=positionOffset_attr)
        cmds.addAttr(x, longName="contraction", attributeType="double", defaultValue=1.0, min=1e-6, keyable=True, pxy=contraction_attr)

    return seconds_list, cv


if __name__ == "__main__":
    num = 100
    controlsNum = 10
    controls = []
    for x in range(controlsNum):
        jnt = cmds.createNode("joint", name=f"joint_{x:02d}")
        cmds.setAttr(f"{jnt}.translate", x * 5, 0, 0)
        controls.append(jnt)
    for i, _ in enumerate(controls):
        if i == 0:
            continue
        cmds.parent(controls[i], controls[i - 1])

    transform_list, cv = curveIK(
        controls=controls,
        secondsNum=num,
        curveDegree=3,
        frontAxis=0,
        uniform=True,
        use_offsetParentMatrix=False,
        suffixName="curveIkTest",
    )
    for x in transform_list:
        cube = cmds.polyCube()
        cube_shape = cmds.listRelatives(cube, shapes=1)[0]
        cmds.parent(cube_shape, x, r=1, s=1)
        cmds.delete(cube)
    for i, x in enumerate(transform_list):
        cmds.setAttr(f"{x}.displayLocalAxis", 1)

    for x in controls:
        decom = cmds.createNode("decomposeMatrix", name=f"{x}_decomposeMatrix", ss=1)
        cmds.connectAttr(f"{x}.worldMatrix[0]", f"{decom}.inputMatrix")
        cmds.connectAttr(f"{decom}.outputTranslate", f"{cv}.controlPoints[{controls.index(x)}]")
