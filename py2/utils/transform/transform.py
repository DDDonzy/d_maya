import maya.cmds as cmds
import maya.api.OpenMaya as om
from py2.utils.generateUniqueName import generateUniqueName
from py2.utils.createAssets import createAssets, assetBindAttr

RAD_TO_DEG = 57.29577951308232     # 180.0 / pi
DEG_TO_RAD = 0.017453292519943295  # pi / 180.0


class UNIT_CONVERT():
    mm = 10.0
    cm = 1.0
    m = 0.01

    def __init__(self, unit=None):
        if unit is None:
            unit = cmds.currentUnit(q=1)
        if unit not in ["mm", "cm", "m"]:
            raise ValueError("Invalid axis. Choose from 'mm', 'cm', or 'm'.")

    def __new__(cls, unit=None):
        if unit is None:
            unit = cmds.currentUnit(q=1)
        return getattr(UNIT_CONVERT, unit)


def get_offsetMatrix(child_world_matrix, parent_world_matrix):
    child_local_matrix = child_world_matrix * parent_world_matrix.inverse()
    return child_local_matrix


def get_relativesMatrix(matrix, referenceMatrix):
    relativesMatrix = matrix * referenceMatrix.inverse()
    return relativesMatrix


def get_localMatrix(obj):
    mSel = om.MSelectionList()
    mSel.add(obj)
    return om.MFnTransform(mSel.getDagPath(0)).transformation().asMatrix()


def get_worldMatrix(obj):
    mSel = om.MSelectionList()
    mSel.add(obj)
    return mSel.getDagPath(0).inclusiveMatrix()


def get_parentMatrix(obj):
    mSel = om.MSelectionList()
    mSel.add(obj)
    return mSel.getDagPath(0).exclusiveMatrix()


def set_localMatrix(obj, matrix):
    if cmds.objExists("{}.jointOrient".format(obj)):
        try:
            cmds.setAttr("{}.jointOrient".format(obj), 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(matrix))


def set_worldMatrix(obj, matrix):
    mSel = om.MSelectionList()
    mSel.add(obj)
    local_matrix = matrix * mSel.getDagPath(0).exclusiveMatrixInverse()
    if cmds.objExists("{}.jointOrient".format(obj)):
        try:
            cmds.setAttr("{}.jointOrient".format(obj), 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(local_matrix))


def matrix_to_trs(matrix, rotateOrder=0):
    mTransformation = om.MTransformationMatrix(matrix)
    translate = mTransformation.translation(1) * UNIT_CONVERT()
    euler_radians = mTransformation.rotation()
    euler_radians.reorderIt(rotateOrder)
    euler_angle = [RAD_TO_DEG * radians for radians in [euler_radians.x, euler_radians.y, euler_radians.z]]
    scale = mTransformation.scale(1)
    outputList = [translate[0], translate[1], translate[2],
                  euler_angle[0], euler_angle[1], euler_angle[2],
                  scale[0], scale[1], scale[2]]
    return outputList


def trs_to_matrix(trs, rotateOrder=0):
    mTransformation = om.MTransformationMatrix()
    translate = om.MVector(trs[0], trs[1], trs[2]) / UNIT_CONVERT()
    euler_radians = om.MEulerRotation([DEG_TO_RAD * angle for angle in trs[3:6]], rotateOrder)
    scale = om.MVector(trs[6], trs[7], trs[8])
    mTransformation.setTranslation(translate, 1)
    mTransformation.setRotation(euler_radians)
    mTransformation.setScale(scale, 1)
    return mTransformation.asMatrix()


def get_trs(obj):
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    trs = []
    for attr in attrs:
        trs.append(cmds.getAttr("{}.{}".format(obj, attr)))
    return trs


def set_trs(obj, trs):
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    for i, attr in enumerate(attrs):
        try:
            cmds.setAttr("{}.{}".format(obj, attr), trs[i])
        except Exception as e:
            om.MGlobal.displayWarning(str(e))


def create_decomposeMatrix(name, translate=True, rotate=True, scale=True, shear=True):

    hasJointOrient = cmds.objExists("{}.jointOrient".format(name))

    node_decom = cmds.createNode("decomposeMatrix", name="{}_decomposeMatrix".format(name))
    node_mult = cmds.createNode("multMatrix", name="{}_getLocalMatrix_multMatrix".format(name))
    node_matrixInverse = cmds.createNode("inverseMatrix", name="{}_inverseRelativesSpaceMatrix_multMatrix".format(name))
    _assets_nodeList = [node_decom, node_mult, node_matrixInverse]
    _bindAttr = {
        "inputMatrix": "{}.matrixIn[0]".format(node_mult),
        "inputRotateOrder": "{}.inputRotateOrder".format(node_decom),
        "inputRelativeSpaceMatrix": "{}.inputMatrix".format(node_matrixInverse),
        "outputTranslate": "{}.outputTranslate".format(node_decom),
        "outputRotate": "{}.outputRotate".format(node_decom),
        # "outputQuat": "{}.outputQuat".format(node_decom),
        "outputScale": "{}.outputScale".format(node_decom),
        "outputShear": "{}.outputShear".format(node_decom)
    }

    # Internal connects
    cmds.connectAttr("{}.outputMatrix".format(node_matrixInverse), "{}.matrixIn[1]".format(node_mult))
    cmds.connectAttr("{}.matrixSum".format(node_mult), "{}.inputMatrix".format(node_decom))

    if hasJointOrient:
        node_euler_to_quat = cmds.createNode("eulerToQuat", name="{}_eulerToQuat".format(name))
        node_invert_quat = cmds.createNode("quatInvert", name="{}_invertQuat".format(name))
        node_prod_quat = cmds.createNode("quatProd", name="{}_prodQuat".format(name))
        node_quat_to_euler = cmds.createNode("quatToEuler", name="{}_quatToEuler".format(name))

        cmds.connectAttr("{}.inputRotateOrder".format(node_decom), "{}.inputRotateOrder".format(node_euler_to_quat))
        cmds.connectAttr("{}.inputRotateOrder".format(node_decom), "{}.inputRotateOrder".format(node_quat_to_euler))
        cmds.connectAttr("{}.outputQuat".format(node_decom), "{}.input1Quat".format(node_prod_quat))
        cmds.connectAttr("{}.outputQuat".format(node_euler_to_quat), "{}.inputQuat".format(node_invert_quat))
        cmds.connectAttr("{}.outputQuat".format(node_invert_quat), "{}.input2Quat".format(node_prod_quat))
        cmds.connectAttr("{}.outputQuat".format(node_prod_quat), "{}.inputQuat".format(node_quat_to_euler))

        _assets_nodeList.extend([node_euler_to_quat, node_invert_quat, node_prod_quat, node_quat_to_euler])

        _bindAttr.update({
            "inputJointOrient": "{}.inputRotate".format(node_euler_to_quat),
            # "outputQuat": "{}.outputQuat".format(node_prod_quat)
            "outputRotate": "{}.outputRotate".format(node_quat_to_euler)
        })

    # assets
    _assets = createAssets(name="{}_decomMatrix".format(name), assetsType="DecomposeMatrix", addNode=_assets_nodeList)
    assetBindAttr(_assets, _bindAttr)

    # External connects
    if cmds.objExists(name):
        if cmds.objExists("{}.jointOrient".format(name)):
            cmds.connectAttr("{}.jointOrient".format(name), "{}.inputJointOrient".format(_assets))  # in jointOrient
        cmds.connectAttr("{}.parentMatrix[0]".format(name), "{}.inputRelativeSpaceMatrix".format(_assets))  # input relatives space matrix
        cmds.connectAttr("{}.rotateOrder".format(name), "{}.inputRotateOrder".format(_assets))  # in rotateOrder
        if translate:
            cmds.connectAttr("{}.outputTranslate".format(_assets), "{}.translate".format(name))  # out translate
        if scale:
            cmds.connectAttr("{}.outputScale".format(_assets), "{}.scale".format(name))  # out scale
        if shear:
            cmds.connectAttr("{}.outputShear".format(_assets), "{}.shear".format(name))  # out shear
        if rotate:
            cmds.connectAttr("{}.outputRotate".format(_assets), "{}.rotate".format(name))  # out rotate
            # cmds.connectAttr("{}.outputQuat".format(_assets), "{}.rotateQuaternion".format(name))  # out rotate

    return _assets


def create_relativesMatrix(name=""):
    node_multMatrix = cmds.createNode("multMatrix", name="{}_getRelativesMatrix_multMatrix".format(name))
    node_inverseMatrix = cmds.createNode("inverseMatrix", name="{}_getRelativesMatrix_inverseMatrix".format(name))
    cmds.connectAttr("{}.outputMatrix".format(node_inverseMatrix), "{}.matrixIn[1]".format(node_multMatrix))

    _assets_nodeList = [node_multMatrix, node_inverseMatrix]
    _bindAttr = {
        "inputMatrix": "{}.matrixIn[0]".format(node_multMatrix),
        "inputRelativeMatrix": "{}.inputMatrix".format(node_inverseMatrix),
        "outputMatrix": "{}.matrixSum".format(node_multMatrix)
    }

    _assets = createAssets("{}_getRelativesMatrix".format(name), addNode=_assets_nodeList)
    assetBindAttr(_assets, _bindAttr)


def matrixConstraint(*args,  **kwargs):

    _info_name = "matrixConstraintInfo"

    def _create_matrixConstraint(source_obj, target_object, keep_offset=True):

        hasJointOrient = cmds.objExists("{}.jointOrient".format(target_object))
        offset_matrix = get_offsetMatrix(get_worldMatrix(target_object), get_worldMatrix(source_obj))
        node_multMatrix = cmds.createNode("multMatrix", name="{}_MM_matrixConstraint".format(target_object))
        node_decom = create_decomposeMatrix(name=target_object, translate=translate, rotate=rotate, scale=scale, shear=shear)
        _add_nodeList = [node_multMatrix, node_decom]
        _bindAttr = {
            "inputOffsetMatrix": "{}.matrixIn[0]".format(node_multMatrix),
            "inputControllerMatrix": "{}.matrixIn[1]".format(node_multMatrix),
            "inputRotateOrder": "{}.inputRotateOrder".format(node_decom),
            "inputRelativeSpaceMatrix": "{}.inputRelativeSpaceMatrix".format(node_decom),
            "outputTranslate": "{}.outputTranslate".format(node_decom),
            "outputRotate": "{}.outputRotate".format(node_decom),
            # "outputQuat": "{}.outputQuat".format(node_decom),
            "outputScale": "{}.outputScale".format(node_decom),
            "outputShear": "{}.outputShear".format(node_decom)
        }
        if hasJointOrient:
            _bindAttr.update({"inputTargetJointOrient": "{}.inputJointOrient".format(node_decom)})
        _assets = generateUniqueName("{}_matrixConstraint".format(target_object))
        _assets = createAssets(name=_assets, assetsType="MatrixConstraint", addNode=_add_nodeList)
        assetBindAttr(_assets, _bindAttr)

        # Internal connects
        cmds.connectAttr("{}.matrixSum".format(node_multMatrix), "{}.inputMatrix".format(node_decom))

        # External connects
        if keep_offset:
            cmds.setAttr("{}.inputOffsetMatrix".format(_assets), offset_matrix, type="matrix")
        cmds.connectAttr("{}.worldMatrix[0]".format(source_obj), "{}.inputControllerMatrix".format(_assets))

        # Add info
        if cmds.objExists("{}.{}".format(target_object, _info_name)):
            cmds.deleteAttr("{}.{}".format(target_object, _info_name))

        # Matrix constraint attr
        cmds.addAttr(_assets, ln=_info_name, at="message")
        cmds.addAttr(target_object, ln=_info_name, at="message", pxy="{}.{}".format(_assets, _info_name))

        return _assets

    def _query_matrixConstraint(obj):
        dict_info = {}
        _assets = None
        target_obj = None
        if not cmds.objExists("{}.{}".format(obj, _info_name)):
            return dict_info
        if cmds.objectType(obj) == "container":
            _assets = obj
            target_obj_list = cmds.listConnections("{}.{}".format(_assets, _info_name), s=0, d=1)
            if target_obj_list:
                target_obj = target_obj_list[0]
        else:
            target_obj = obj
            _assets_list = cmds.listConnections("{}.{}".format(target_obj, _info_name), s=1, d=0)
            if _assets_list:
                _assets = _assets_list[0]
        controller_obj = cmds.listConnections("{}.inputControllerMatrix".format(_assets), s=1, d=0)[0]
        dict_info.update({controller_obj: target_obj})
        return dict_info

    maintainOffset = kwargs.get("mo", True) and kwargs.get("maintainOffset", True)
    query = kwargs.get("q", False) or kwargs.get("query", False)
    q_source = kwargs.get("s", True)
    if not q_source:
        q_source = kwargs.get("source", False)
    q_target = kwargs.get("t", True)
    if not q_target:
        q_target = kwargs.get("target", False)
    translate=kwargs.get("translate")
    rotate=kwargs.get("rotate")
    scale=kwargs.get("scale")
    shear=kwargs.get("shear")

    # Do functions
    if query:
        if args:
            obj = args[0]
        else:
            obj = cmds.ls(sl=1)
            obj = obj[0]
        return _query_matrixConstraint(obj)

    if not query:
        if not args:
            args = cmds.ls(sl=1)
        source_obj = args[0]
        target_object = args[1:]
        _assets_list = []
        for target in target_object:
            _assets = _create_matrixConstraint(source_obj, target, maintainOffset)
            _assets_list.append(_assets)
        return _assets_list


def parentspaceConstraint(*args, **kwargs):
    parentspace_attrName = "parentSpace"
    _info_name = "parentspaceConstraint"

    def _pre_parentspace(target_obj):
        localMatrix = get_localMatrix(target_obj)

        # Create choice nodes
        node_choseControllerMatrix = cmds.createNode("choice", name="{}_controller_choice".format(target_obj))
        node_choseOffsetMatrix = cmds.createNode("choice", name="{}_offset_choice".format(target_obj))

        # Create multMatrix node for world matrix calculation
        node_calWorldMatrix = cmds.createNode("multMatrix", name="{}_parentSpace_multMatrix".format(target_obj))
        cmds.connectAttr("{}.output".format(node_choseOffsetMatrix), "{}.matrixIn[0]".format(node_calWorldMatrix))
        cmds.connectAttr("{}.output".format(node_choseControllerMatrix), "{}.matrixIn[1]".format(node_calWorldMatrix))

        # Create decomposeMatrix node for translating, rotating, scaling, and shearing
        node_decom = create_decomposeMatrix("{}".format(target_obj), translate=translate, rotate=rotate, scale=scale, shear=shear)
        cmds.connectAttr("{}.matrixSum".format(node_calWorldMatrix), "{}.inputMatrix".format(node_decom))

        _add_nodeList = [node_decom, node_choseOffsetMatrix, node_choseControllerMatrix, node_calWorldMatrix]
        _bindAttr = {
            "inputRotateOrder": "{}.inputRotateOrder".format(node_decom),
            "inputRelativeSpaceMatrix": "{}.inputRelativeSpaceMatrix".format(node_decom),
            "outputTranslate": "{}.outputTranslate".format(node_decom),
            "outputRotate": "{}.outputRotate".format(node_decom),
            "outputScale": "{}.outputScale".format(node_decom),
            "outputShear": "{}.outputShear".format(node_decom)
        }

        # Create assets and bind attributes
        _assets = createAssets(name=generateUniqueName("{}_parentspace".format(target_obj)),
                               assetsType="ParentspaceAssets",
                               addNode=_add_nodeList)
        assetBindAttr(_assets, _bindAttr)

        # Add parentspace switch attribute
        cmds.addAttr(_assets, ln=parentspace_attrName, at="enum", en="Parent", k=1)
        cmds.connectAttr("{}.{}".format(_assets, parentspace_attrName), "{}.selector".format(node_choseControllerMatrix))
        cmds.connectAttr("{}.{}".format(_assets, parentspace_attrName), "{}.selector".format(node_choseOffsetMatrix))

        # Add matrices
        cmds.addAttr(_assets, ln="controllerMatrix", at="matrix", m=1)
        cmds.addAttr(_assets, ln="offsetMatrix", at="matrix", m=1)
        cmds.connectAttr("{}.controllerMatrix[0]".format(_assets), "{}.input[0]".format(node_choseControllerMatrix))
        cmds.connectAttr("{}.offsetMatrix[0]".format(_assets), "{}.input[0]".format(node_choseOffsetMatrix))

        # Set parent matrix * base local matrix
        cmds.setAttr("{}.offsetMatrix[0]".format(_assets), localMatrix, type="matrix")
        cmds.connectAttr("{}.parentMatrix[0]".format(target_obj), "{}.controllerMatrix[0]".format(_assets))

        # Add parentspace attribute to target object
        if cmds.objExists("{}.{}".format(target_obj, parentspace_attrName)):
            cmds.deleteAttr("{}.{}".format(target_obj, parentspace_attrName))
        cmds.addAttr(target_obj, ln=parentspace_attrName, k=1, pxy="{}.{}".format(_assets, parentspace_attrName))

        # Add message info to target object
        cmds.addAttr(_assets, ln=_info_name, at="message")
        if cmds.objExists("{}.{}".format(target_obj, _info_name)):
            cmds.deleteAttr("{}.{}".format(target_obj, _info_name))
        cmds.addAttr(target_obj, ln=_info_name, at="message", pxy="{}.{}".format(_assets, _info_name))

        return _assets

    def _add_parentspace(controllerObj, targetObj, niceName=None):
        # Get parentspace assets
        if not cmds.objExists("{}.{}".format(targetObj, _info_name)):
            _assets = _pre_parentspace(targetObj)

        _assets = cmds.listConnections("{}.{}".format(targetObj, _info_name), s=1, d=0)[0]
        if not _assets:
            raise RuntimeError("Cannot find parentspace constraint node!")

        # Set nice name for enum
        if not niceName:
            niceName = controllerObj
        enum_str = cmds.addAttr("{}.{}".format(targetObj, parentspace_attrName), q=1, en=1)
        nice_name_list = enum_str.split(":")
        nice_name_list.append(niceName)
        enum_str = ":".join(nice_name_list)
        parent_indices = len(nice_name_list) - 1

        # Update parentspace enum
        cmds.addAttr("{}.{}".format(targetObj, parentspace_attrName), e=1, en=enum_str)
        cmds.addAttr("{}.{}".format(_assets, parentspace_attrName), e=1, en=enum_str)

        # Set offset matrix and controller matrix to chosen nodes
        offset_matrix = get_offsetMatrix(get_worldMatrix(targetObj), get_worldMatrix(controllerObj))
        cmds.setAttr("{}.offsetMatrix[{}]".format(_assets, parent_indices), offset_matrix, type="matrix")
        cmds.connectAttr("{}.worldMatrix[0]".format(controllerObj), "{}.controllerMatrix[{}]".format(_assets, parent_indices))

        # Update chosen node input data
        controller_chose = cmds.listConnections("{}.controllerMatrix[0]".format(_assets), p=0, d=1, s=0)[0]
        offset_chose = cmds.listConnections("{}.offsetMatrix[0]".format(_assets), p=0, d=1, s=0)[0]
        cmds.connectAttr("{}.controllerMatrix[{}]".format(_assets, parent_indices), "{}.input[{}]".format(controller_chose, parent_indices))
        cmds.connectAttr("{}.offsetMatrix[{}]".format(_assets, parent_indices), "{}.input[{}]".format(offset_chose, parent_indices))

    # Main function logic
    
    translate=kwargs.get("translate")
    rotate=kwargs.get("rotate")
    scale=kwargs.get("scale")
    shear=kwargs.get("shear")
    
    if len(args) == 0:
        sel = cmds.ls(sl=1)
        if len(sel) < 2:
            om.MGlobal.displayError("Please select at least two objects.")
            return
        control_obj_list = cmds.ls(sl=1)[:-1]
        target_obj = cmds.ls(sl=1)[-1]
    else:
        control_obj_list = []
        control_obj_list.extend(args[:-1])
        target_obj = args[-1]

    for control_obj in control_obj_list:
        _add_parentspace(control_obj, target_obj, **kwargs)


def create_OffsetFK(control_list, offset_list):
    for i, control in enumerate(control_list[:-1]):
        offset = offset_list[i]
        next_offset = offset_list[i + 1]
        next_control = control_list[i + 1]

        node_multMatrix = cmds.createNode("multMatrix", name="{}_multMatrix_offsetFK".format(next_control))
        node_decom = create_decomposeMatrix(name=next_offset)
        _add_nodeList = [node_multMatrix, node_decom]

        # Get offset matrix from 'offset_obj' with 'next offset_obj'
        cmds.connectAttr("{}.parentMatrix[0]".format(next_offset), "{}.matrixIn[0]".format(node_multMatrix))
        cmds.connectAttr("{}.parentInverseMatrix[0]".format(offset), "{}.matrixIn[1]".format(node_multMatrix))

        # Connect controller matrix
        cmds.connectAttr("{}.worldMatrix[0]".format(control), "{}.matrixIn[2]".format(node_multMatrix))

        # Matrix to TRS
        cmds.connectAttr("{}.matrixSum".format(node_multMatrix), "{}.inputMatrix".format(node_decom))

        # Create assets
        _assets = generateUniqueName("{}_offsetFK".format(next_control))
        _assets = createAssets(name=_assets, assetsType="OffsetFK", addNode=_add_nodeList)
