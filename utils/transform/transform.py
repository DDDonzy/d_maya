import maya.cmds as cmds
import maya.api.OpenMaya as om
from utils.generate_unique_name import generate_unique_name
from utils.create_assets import create_assets


class MIRROR_MATRIX():
    x = om.MMatrix([[-1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    y = om.MMatrix([[1, 0, 0, 0],
                    [0, -1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    z = om.MMatrix([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, -1, 0],
                    [0, 0, 0, 1]])

    def __init__(self, axis: str = "x"):
        if axis not in ["x", "y", "z"]:
            raise ValueError("Invalid axis. Choose from 'x', 'y', or 'z'.")

    def __new__(cls, axis: str = "x"):
        return getattr(MIRROR_MATRIX, axis)


class UNIT_CONVERT():
    mm = 10.0
    cm = 1.0
    m = 0.01

    def __init__(self, unit: str = cmds.currentUnit(q=1)):
        if unit not in ["mm", "cm", "m"]:
            raise ValueError("Invalid axis. Choose from 'mm', 'cm', or 'm'.")

    def __new__(cls, unit: str = cmds.currentUnit(q=1)):
        return getattr(UNIT_CONVERT, unit)


def mirror_transform(sour_obj: str,
                     target_obj: str,
                     mirror_axis: str = "x",):
    """flip source object's world space matrix  as target object's world space matrix

    Args:
        sour_obj (str): source transform object
        target_obj (str): target transform object
        mirror_axis (str, optional): mirror axis. Defaults to "x".
    """
    sour_world_matrix = get_world_matrix(sour_obj)
    sour_parent_matrix = get_parent_matrix(sour_obj)
    sour_world_matrix_flip = flip_matrix(sour_world_matrix, mirror_axis)
    sour_parent_matrix_flip = flip_matrix(sour_parent_matrix, mirror_axis)
    target_parent_matrix = get_parent_matrix(target_obj)
    flip_offset_matrix = get_offset_matrix(sour_parent_matrix_flip, target_parent_matrix)
    set_world_matrix(target_obj, flip_offset_matrix * sour_world_matrix_flip)


def flip_matrix(world_matrix: om.MMatrix,
                mirror_axis: str = "x") -> om.MMatrix:
    """flip matrix by mirror matrix

    Args:
        world_matrix (om.MMatrix): input world matrix
        mirror_axis (str, optional): mirror axis x y or z. Defaults to "x".

    Returns:
        om.MMatrix: flip matrix
    """
    mirror_matrix = world_matrix * MIRROR_MATRIX(mirror_axis)
    return mirror_matrix


def get_offset_matrix(child_world_matrix: om.MMatrix,
                      parent_world_matrix: om.MMatrix) -> om.MMatrix:
    """
    get offset matrix
    get local matrix when child in parent space

    Args:
        child_world_matrix (om.MMatrix): child world matrix
        parent_world_matrix (om.MMatrix): parent world matrix

    Returns:
        om.MMatrix: local matrix when child in parent space
    """
    # child_world_matrix = child_local_matrix * parent_world_matrix
    # child_world_matrix * parent_world_matrix.inverse = child_local_matrix
    child_local_matrix = child_world_matrix * parent_world_matrix.inverse()
    return child_local_matrix


def get_local_matrix(obj: str) -> om.MMatrix:
    """get object's local space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: local matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return om.MFnTransform(sel_list.getDagPath(0)).transformation().asMatrix()


def get_world_matrix(obj: str) -> om.MMatrix:
    """get object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: world matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).inclusiveMatrix()


def get_parent_matrix(obj: str) -> om.MMatrix:
    """get object's parent object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: parent object's world space matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).exclusiveMatrix()


def set_local_matrix(obj: str, matrix: om.MMatrix) -> None:
    """set maya object's local as input matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input local matrix
    """
    if cmds.objectType(obj) == "joint":
        try:
            cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(matrix))


def set_world_matrix(obj: str, matrix: om.MMatrix) -> None:
    """ convert world space matrix to local space matrix and as object's local space matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input world space matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    local_matrix = matrix * sel_list.getDagPath(0).exclusiveMatrixInverse()
    if cmds.objectType(obj) == "joint":
        try:
            cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(local_matrix))


def matrix_to_trs(matrix: om.MMatrix, rotateOrder: int = 0) -> list:
    """ convert matrix to maya's translate,rotate and scale

    Args:
        matrix (om.MMatrix): input matrix
        rotateOrder (int, optional): rotate order. Defaults to 0.

    Returns:
        list: [tx,ty.tz,rx,ry,rz,sx,sy,sz]
    """
    om_transformation = om.MTransformationMatrix(matrix)
    translate = om_transformation.translation(1) * UNIT_CONVERT()
    euler_radians = om_transformation.rotation()
    euler_radians.reorderIt(rotateOrder)
    euler_angle = [57.29577951308232*radians for radians in [euler_radians.x, euler_radians.y, euler_radians.z]]
    scale = om_transformation.scale(1)
    outputList = [translate[0], translate[1], translate[2],
                  euler_angle[0], euler_angle[1], euler_angle[2],
                  scale[0], scale[1], scale[2], ]
    return outputList


def trs_to_matrix(trs: list, rotateOrder: int = 0) -> om.MMatrix:
    """convert [tx,ty.tz,rx,ry,rz,sx,sy,sz] to matrix

    Args:
        trs (list): input [tx,ty.tz,rx,ry,rz,sx,sy,sz]
        rotateOrder (int, optional): rotate order. Defaults to 0.

    Returns:
        om.MMatrix: matrix
    """
    om_transformation = om.MTransformationMatrix()
    translate = om.MVector(trs[0], trs[1], trs[2]) / UNIT_CONVERT()
    euler_radians = om.MEulerRotation(*[0.017453292520882225*angle for angle in trs[3:6]], rotateOrder)
    scale = om.MVector(trs[6], trs[7], trs[8])
    om_transformation.setTranslation(translate, 1)
    om_transformation.setRotation(euler_radians)
    om_transformation.setScale(scale, 1)
    return om_transformation.asMatrix()


def get_trs(obj: str) -> list:
    """get maya transform's transformation [tx,ty.tz,rx,ry,rz,sx,sy,sz]

    Args:
        obj (str): _description_

    Returns:
        list: [tx,ty.tz,rx,ry,rz,sx,sy,sz]
    """
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    trs = []
    for attr in attrs:
        trs.append(cmds.getAttr(f"{obj}.{attr}"))
    return trs


def set_trs(obj: str, trs: list) -> None:
    """set maya transform [tx,ty.tz,rx,ry,rz,sx,sy,sz]

    Args:
        obj (str): maya transform object'name
        trs (list): [tx,ty.tz,rx,ry,rz,sx,sy,sz]
    """
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    for i, attr in enumerate(attrs):
        try:
            cmds.setAttr(f"{obj}.{attr}", trs[i])
        except Exception as e:
            om.MGlobal.displayWarning(str(e))


def create_node_fbf(matrix: om.MMatrix = om.MMatrix(), **kwargs) -> str:
    '''
    Create maya node "fourByFourMatrix". And set matrix data

    Return node name
    '''
    matrix_attrs = ["in00", "in01", "in02", "in03",
                    "in10", "in11", "in12", "in13",
                    "in20", "in21", "in22", "in23",
                    "in30", "in31", "in32", "in33"]
    fbf_node = cmds.createNode("fourByFourMatrix", **kwargs)
    for iter_idx, num in enumerate(matrix):
        attr_name = matrix_attrs[iter_idx]
        cmds.setAttr(f"{fbf_node}.{attr_name}", num)
    return fbf_node


def matrixConstraint(*arg,
                     **kwargs) -> str:
    """
    Create a matrix-based constraint node

    Args:
        *arg: Variable length arguments
            - No args: Use current selection, first as source, rest as targets
            - Single arg: Specify source object
            - Multiple args: First as source, rest as targets
        **kwargs: Keyword arguments
            - mo/maintainOffset (bool): Keep offset transforms, default True
            - q/query (bool): Query mode, default False
            - s/source (bool): Query source object, default True
            - t/target (bool): Query target objects, default False

    Returns:
        str: Name of constraint node or query result dictionary
    """

    _info_name = "matrixConstraintInfo"

    def _create_matrix_constraint(source_obj: str,
                                  target_object: str,
                                  keep_offset: bool = True):
        """
        Create matrix constraint between source and target

        Args:
            source_obj: Driver object
            target_object: Driven object
            keep_offset: Maintain offset transforms
        """
        offset_matrix = get_offset_matrix(get_world_matrix(target_object), get_world_matrix(source_obj))
        node_multMatrix = cmds.createNode("multMatrix", name=f"{target_object}_MM_matrixConstraint")
        cmds.addAttr(node_multMatrix, ln="constraintOffsetMatrix", at="matrix")
        if keep_offset:
            cmds.setAttr(f"{node_multMatrix}.constraintOffsetMatrix", offset_matrix, type="matrix")
        cmds.connectAttr(f"{node_multMatrix}.constraintOffsetMatrix",
                         f"{node_multMatrix}.matrixIn[0]")
        cmds.connectAttr(f"{source_obj}.worldMatrix[0]",
                         f"{node_multMatrix}.matrixIn[1]")
        cmds.connectAttr(f"{target_object}.parentInverseMatrix[0]",
                         f"{node_multMatrix}.matrixIn[2]")
        node_decomposeMatrix = cmds.createNode("decomposeMatrix", name=f"{target_object}_DM_matrixConstraint")
        cmds.connectAttr(f"{target_object}.rotateOrder",
                         f"{node_decomposeMatrix}.inputRotateOrder")
        cmds.connectAttr(f"{node_multMatrix}.matrixSum",
                         f"{node_decomposeMatrix}.inputMatrix")
        cmds.connectAttr(f"{node_decomposeMatrix}.outputTranslate",
                         f"{target_object}.translate", f=1)
        cmds.connectAttr(f"{node_decomposeMatrix}.outputRotate",
                         f"{target_object}.rotate", f=1)
        cmds.connectAttr(f"{node_decomposeMatrix}.outputScale",
                         f"{target_object}.scale", f=1)
        cmds.connectAttr(f"{node_decomposeMatrix}.outputShear",
                         f"{target_object}.shear", f=1)
        cmds.connectAttr(f"{node_decomposeMatrix}.outputQuat",
                         f"{target_object}.rotateQuaternion", f=1)
        if cmds.objExists(f"{target_object}.jointOrient"):
            try:
                cmds.setAttr(f"{target_object}.jointOrient", 0, 0, 0)
            except Exception as e:
                om.MGlobal.displayWarning(e)
        # assets box
        all_matrix_assets = create_assets("MatrixConstraint", parent_assets=create_assets("RigAssets"))
        this_matrix_assets_name = generate_unique_name(f"{target_object}_matrixConstraint")
        this_matrix_assets = create_assets(this_matrix_assets_name, parent_assets=all_matrix_assets)
        cmds.container(this_matrix_assets, edit=1,
                       addNode=[node_multMatrix, node_decomposeMatrix])
        cmds.container(this_matrix_assets, edit=True, publishName='offsetMatrix')
        cmds.container(this_matrix_assets, edit=True, bindAttr=[f"{node_multMatrix}.constraintOffsetMatrix", 'offsetMatrix'])
        # add info
        # target attr
        if cmds.objExists(f"{target_object}.{_info_name}"):
            sour_connect_attr = cmds.listConnections(f"{target_object}.{_info_name}", s=1, d=0, p=1)
            if sour_connect_attr:
                for attr in sour_connect_attr:
                    cmds.disconnectAttr(attr, f"{target_object}.{_info_name}")
        else:
            cmds.addAttr(target_object, ln=_info_name, at="message")
        # source attr
        if not cmds.objExists(f"{source_obj}.{_info_name}"):
            cmds.addAttr(source_obj, ln=_info_name, at="message")
        # matrix constraint attr
        cmds.addAttr(this_matrix_assets, ln=_info_name, at="message")
        # connect
        cmds.connectAttr(f"{source_obj}.{_info_name}",
                         f"{this_matrix_assets}.{_info_name}")
        cmds.connectAttr(f"{this_matrix_assets}.{_info_name}",
                         f"{target_object}.{_info_name}")
        return this_matrix_assets

    def _query_matrix_constraint(obj: str,
                                 source: bool,
                                 target: bool):
        """
        Query constraint relationships

        Args:
            obj: Object to query
            source: Query source object
            target: Query target objects

        Returns:
            dict: Constraint relationship dictionary
        """
        dict_info = {}
        if source:
            print("q,s")
            matrix_constraint = cmds.listConnections(f"{obj}.{_info_name}", s=1, d=0)
            if matrix_constraint:
                matrix_constraint = matrix_constraint[0]
                source_obj = cmds.listConnections(f"{matrix_constraint}.{_info_name}", s=1, d=0)
                if source_obj:
                    source_obj = source_obj[0]
                    dict_info.update({source_obj: [obj]})
        if target:
            print("q,t")
            matrix_constraint_list = cmds.listConnections(f"{obj}.{_info_name}", s=0, d=1)
            if matrix_constraint_list:
                target_obj_list = []
                for matrix_constraint in matrix_constraint_list:
                    target_obj = cmds.listConnections(f"{matrix_constraint}.{_info_name}", s=0, d=1)
                    if target_obj:
                        target_obj_list.extend(target_obj)
                dict_info.update({obj: target_obj_list})
        return dict_info

    if len(arg) == 0:
        sel = cmds.ls(sl=1)
        if len(sel) < 2:
            om.MGlobal.displayError("Please select at least two objects.")
            return
        source_obj = cmds.ls(sl=1)[0]
        target_object = cmds.ls(sl=1)[1:]
    elif len(arg) == 1:
        source_obj = arg[0]
    else:
        source_obj = arg[0]
        target_object = []
        target_object.extend(arg[1:])
    maintainOffset = kwargs.get("mo", True) and kwargs.get("maintainOffset", True)
    query = kwargs.get("q", False) or kwargs.get("query", False)
    q_source = kwargs.get("s", True)
    if not q_source:
        q_source = kwargs.get("source", False)
    q_target = kwargs.get("t", True)
    if not q_target:
        q_target = kwargs.get("target", False)

    if query:
        return _query_matrix_constraint(source_obj, q_source, q_target)
    else:
        for target in target_object:
            matrix_constraint = _create_matrix_constraint(source_obj, target, maintainOffset)
        return matrix_constraint


def parentspaceConstraint(*arg,
                          **kwargs):
    """
    Create parent space constraint networks for target object with multiple control objects.

    Usage:
        1. Select multiple controls + one target (last selected)
        2. Or provide objects as arguments (last arg = target)

    Args:
        *arg: Variable length argument list
            - If empty: Uses selected objects (last = target)
            - If provided: Last arg = target, others = controls
        **kwargs: Optional arguments
            - nice_name (str): Custom name for space switch enum
            - translate (bool): Enable translation constraint
            - rotate (bool): Enable rotation constraint  
            - scale (bool): Enable scale constraint
            - shear (bool): Enable shear constraint
    """

    parentspace_attrName = "parentSpace"
    name_info = "parentspaceConstraint"

    def _parentspace_constraint_pre(target_obj):
        """
        Setup initial constraint network and container structure

        Args:
            target_obj (str): Target object to setup constraint for

        Returns:
            str: Created parentspace assets container name
        """

        # assets box
        assets_name = generate_unique_name(f"{target_obj}_parentspace")
        all_parentspace_assets = create_assets("parentspaceAssets", parent_assets=create_assets("RigAssets"))
        parentspace_assets = create_assets(assets_name, parent_assets=all_parentspace_assets)

        node_bw = cmds.createNode("blendMatrix", name=f"{target_obj}_spaceBW")
        node_getLocalMatrix = cmds.createNode("multMatrix", name=f"{target_obj}_getLocalMatrix")
        node_decMatrix = cmds.createNode("decomposeMatrix", name=f"{target_obj}_decomposeMatrix")
        node_parentMult = cmds.createNode("multMatrix", name=f"{target_obj}_parentMult")
        # parent connect
        cmds.setAttr(f"{node_parentMult}.matrixIn[0]",
                     get_local_matrix(target_obj),
                     type="matrix")
        cmds.connectAttr(f"{target_obj}.parentMatrix[0]",
                         f"{node_parentMult}.matrixIn[1]")
        cmds.connectAttr(f"{node_parentMult}.matrixSum",
                         f"{node_bw}.inputMatrix")
        # blend world matrix to local matrix
        cmds.connectAttr(f"{node_bw}.outputMatrix",
                         f"{node_getLocalMatrix}.matrixIn[0]")
        cmds.connectAttr(f"{target_obj}.parentInverseMatrix[0]",
                         f"{node_getLocalMatrix}.matrixIn[1]")
        cmds.connectAttr(f"{node_getLocalMatrix}.matrixSum",
                         f"{node_decMatrix}.inputMatrix")
        # decomposeMatrix
        cmds.connectAttr(f"{target_obj}.rotateOrder",
                         f"{node_decMatrix}.inputRotateOrder")
        cmds.connectAttr(f"{node_decMatrix}.outputTranslate",
                         f"{target_obj}.translate")
        cmds.connectAttr(f"{node_decMatrix}.outputRotate",
                         f"{target_obj}.rotate")
        cmds.connectAttr(f"{node_decMatrix}.outputScale",
                         f"{target_obj}.scale")
        cmds.connectAttr(f"{node_decMatrix}.outputShear",
                         f"{target_obj}.shear")
        cmds.connectAttr(f"{node_decMatrix}.outputQuat",
                         f"{target_obj}.rotateQuaternion")

        # assets
        cmds.container(parentspace_assets, e=1, addNode=[node_bw, node_getLocalMatrix, node_decMatrix, node_parentMult])
        cmds.container(parentspace_assets, e=1, publishName='inputBlendTarget')
        cmds.container(parentspace_assets, e=1, bindAttr=[f"{node_bw}.target", 'inputBlendTarget'])
        cmds.addAttr(parentspace_assets, ln=parentspace_attrName, at="enum", en="Parent", k=1)
        cmds.addAttr(parentspace_assets, ln=name_info, at="message")
        # add message info to obj
        if not cmds.objExists(f"{target_obj}.{name_info}"):
            cmds.addAttr(target_obj, ln=name_info, at="message")
        cmds.connectAttr(f"{parentspace_assets}.{name_info}",
                         f"{target_obj}.{name_info}")
        # add parentspace attr to obj
        if not cmds.objExists(f"{target_obj}.{parentspace_attrName}"):
            cmds.addAttr(target_obj, ln=parentspace_attrName, pxy=f"{parentspace_assets}.{parentspace_attrName}", k=1)
        else:
            cmds.addAttr(f"{target_obj}.{parentspace_attrName}", e=1, en="Parent", k=1)

        return parentspace_assets

    def _add_parentspace(control_obj: str,
                         target_obj: str,
                         nice_name: str = None,
                         translate=True,
                         rotate=True,
                         scale=True,
                         shear=True):
        """
        Add a new parent space option to the target object

        Args:
            control_obj (str): Control object to add as parent space
            target_obj (str): Target object to be constrained
            nice_name (str, optional): Custom name for space enum
            translate (bool): Enable translation
            rotate (bool): Enable rotation
            scale (bool): Enable scale
            shear (bool): Enable shear
        """
        # get parentspace assets
        if not cmds.objExists(f"{target_obj}.{name_info}"):
            parentspace_assets = _parentspace_constraint_pre(target_obj)
        else:
            parentspace_assets = cmds.listConnections(f"{target_obj}.{name_info}", s=1, d=0)[0]
        # nice name enum
        if not nice_name:
            nice_name = control_obj
        enum_str = cmds.addAttr(f"{parentspace_assets}.{parentspace_attrName}", q=1, en=1)
        nice_name_list = enum_str.split(":")
        nice_name_list.append(nice_name)
        enum_str = ":".join(nice_name_list)
        parent_indices = len(nice_name_list)-1
        # update parentspace enum
        cmds.addAttr(f"{parentspace_assets}.{parentspace_attrName}", e=1, en=enum_str)
        cmds.addAttr(f"{target_obj}.{parentspace_attrName}", e=1, en=enum_str)
        # get node blendMatrix
        bind_attr_list = cmds.container(parentspace_assets, q=1, bindAttr=1)
        node_bw_target_attr = bind_attr_list[bind_attr_list.index("inputBlendTarget")-1]
        # control_obj constraint target_obj
        offset_matrix = get_offset_matrix(get_world_matrix(target_obj),
                                          get_world_matrix(control_obj))
        node_multMatrix = cmds.createNode("multMatrix", name=f"{control_obj}_{target_obj}_multMatrix")
        cmds.setAttr(f"{node_multMatrix}.matrixIn[0]",
                     offset_matrix,
                     type="matrix")
        cmds.connectAttr(f"{control_obj}.worldMatrix[0]",
                         f"{node_multMatrix}.matrixIn[1]")
        # connect to blendMatrix
        cmds.connectAttr(f'{node_multMatrix}.matrixSum',
                         f"{node_bw_target_attr}[{parent_indices}].targetMatrix")
        # version switch
        if cmds.about(api=True) >= 20230000:
            status = [translate, rotate, scale, shear]
            for i, attr in enumerate(["translateWeight", "rotateWeight", "scaleWeight", "shearWeight"]):
                cmds.addAttr(parentspace_assets, ln=f"{attr}_{parent_indices}", at="double", min=0, max=1, k=1, dv=float(status[i]))
                cmds.connectAttr(f"{parentspace_assets}.{attr}_{parent_indices}",
                                 f"{node_bw_target_attr}[{parent_indices}].{attr}", f=1)
        else:
            status = [translate, rotate, scale, shear]
            for i, attr in enumerate(["useTranslate", "useRotate", "useScale", "useShear"]):
                cmds.addAttr(parentspace_assets, ln=f"{attr}_{parent_indices}", at="bool", min=0, max=1, k=1, dv=status[i])
                cmds.connectAttr(f"{parentspace_assets}.{attr}_{parent_indices}",
                                 f"{node_bw_target_attr}[{parent_indices}].{attr}", f=1)

        # sdk
        cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                               cd=f"{parentspace_assets}.{parentspace_attrName}",
                               dv=parent_indices - 1, v=0)
        cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                               cd=f"{parentspace_assets}.{parentspace_attrName}",
                               dv=parent_indices, v=1)
        cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                               cd=f"{parentspace_assets}.{parentspace_attrName}",
                               dv=parent_indices + 1, v=0)

        node_sdk = cmds.listConnections(f"{node_bw_target_attr}[{parent_indices}].weight", s=1, d=0)
        cmds.container(parentspace_assets, e=1, addNode=[node_multMatrix]+node_sdk)
    if len(arg) == 0:
        sel = cmds.ls(sl=1)
        if len(sel) < 2:
            om.MGlobal.displayError("Please select at least two objects.")
            return
        control_obj_list = cmds.ls(sl=1)[:-1]
        target_obj = cmds.ls(sl=1)[-1]
    else:
        control_obj_list = []
        control_obj_list.extend(arg[:-1])
        target_obj = arg[-1]

    for control_obj in control_obj_list:
        _add_parentspace(control_obj, target_obj, **kwargs)


def reset_transform_value(obj, transform=True, userDefined=True):
    def _set_trsv(obj, trs):
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
        for i, attr in enumerate(attrs):
            try:
                cmds.setAttr(f"{obj}.{attr}", trs[i])
            except Exception as e:
                om.MGlobal.displayInfo(str(e))
    if transform:
        _set_trsv(obj, [0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
    if userDefined:
        user_defined = cmds.listAttr(obj, ud=1, u=1)
        if not user_defined:
            return
        for x in user_defined:
            try:
                v = cmds.addAttr(f"{obj}.{x}", q=1, dv=1)
                cmds.setAttr(f"{obj}.{x}", v)
            except Exception as e:
                om.MGlobal.displayInfo(str(e))


def reset_transform_value_cmd(transform=True, userDefined=False):
    def _show_message(msg):
        message = f"<hl> {msg} </hl>"
        cmds.inViewMessage(amg=message, pos='botRight', fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)
    for obj in cmds.ls(sl=1):
        reset_transform_value(obj, transform, userDefined)
    msg = "Reset transform value."
    if userDefined:
        msg = "Reset value (all)."
    _show_message(msg)
