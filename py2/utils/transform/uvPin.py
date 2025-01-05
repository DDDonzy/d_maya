from maya import cmds
from maya.api import OpenMaya as om
from py2.utils.transform.transform import get_world_matrix, matrixConstraint
from py2.utils.generate_unique_name import generate_unique_name


def get_current_uvSet_name(shape):
    sel = om.MGlobal.getSelectionListByName(shape)
    dag = sel.getDagPath(0)
    fn_mesh = om.MFnMesh(dag)
    return fn_mesh.currentUVSetName()


def createPlane(object_list, size=1, name="uvPinPlane"):
    if not object_list:
        raise ValueError("No object need to create plane, please input object list first.")
    num = len(object_list)
    transform = cmds.createNode("transform", name=name)
    mSel = om.MSelectionList()
    mSel.add(transform)
    mObject = mSel.getDependNode(0)

    base_vtx_pos_ary = [[0.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]]
    base_poly_count = [3, 3, 3, 3]
    base_poly_connect = [1, 4, 0, 4, 3, 0, 3, 2, 0, 2, 1, 0]
    base_uvCounts = [3, 3, 3, 3]
    base_uvIds = [0, 1, 2, 1, 3, 2, 3, 4, 2, 4, 0, 2]
    base_u = [1, 0.5, 0.5, 0, 0.5]
    base_v = [0.5, 1, 0.5, 0.5, 0]

    base_vtx_num = len(base_vtx_pos_ary)
    pos_ary = []
    face_connect_ary = []
    face_count_ary = base_poly_count * num

    uvCounts = base_uvCounts * num
    u = []
    v = base_v * num
    uvIds = []
    # num
    for i in range(num):
        # pos_ary
        mult_matrix = get_world_matrix(object_list[i])
        for pos in base_vtx_pos_ary:
            pos_ary.append(om.MPoint(pos) * size * mult_matrix)
        # face_connect_ary
        for vtx in base_poly_connect:
            face_connect_ary.append(vtx + (i * base_vtx_num))
        # u
        for u_value in base_u:
            u.append(u_value+i)
        # uvIds
        for id in base_uvIds:
            uvIds.append(id + (i * base_vtx_num))

    fnMesh = om.MFnMesh()
    mObj = fnMesh.create(pos_ary, face_count_ary, face_connect_ary, parent=mObject)
    fnDep = om.MFnDependencyNode(mObj)
    fnDep.setName("{0}Shape".format(transform))

    fnMesh.setUVs(u, v)
    fnMesh.assignUVs(uvCounts, uvIds)
    return transform


def create_uvPin(obj_list, new_transform=False, plane_size=0.3, name="uvPin"):
    if not obj_list:
        raise ValueError("No object need to create uvPin, please input object list first.")
    # create mesh
    mesh = createPlane(obj_list, size=plane_size, name="{0}_mesh".format(name))

    # create uvPin node
    node_uvPin = cmds.createNode("uvPin", name=name)
    orig_outMesh = cmds.deformableShape(mesh, cog=1)[0]
    cmds.setAttr(".normalAxis", 0)
    cmds.setAttr(".tangentAxis", 5)
    cmds.setAttr("{0}.uvSetName".format(node_uvPin),
                 get_current_uvSet_name(mesh), type="string")
    cmds.connectAttr(orig_outMesh,
                     "{0}.originalGeometry".format(node_uvPin))
    cmds.connectAttr("{0}.worldMesh[0]".format(mesh),
                     "{0}.deformedGeometry".format(node_uvPin))

    for i, obj in enumerate(obj_list):
        # set uvPin.uv value
        cmds.setAttr("{0}.coordinate[{1}].coordinateU".format(node_uvPin, i), i + 0.5)
        cmds.setAttr("{0}.coordinate[{1}].coordinateV".format(node_uvPin, i), 0.5)
        # create new transform
        if new_transform is True:
            loc = cmds.createNode("transform", name="{0}_uvPinLoc".format(obj))
            cmds.connectAttr("{0}.outputMatrix[{1}]".format(node_uvPin, i),
                             "{0}.offsetParentMatrix".format(loc))
            cmds.parentConstraint(loc, obj)
        else:
            cmds.connectAttr("{0}.outputMatrix[{1}]".format(node_uvPin, i),
                             "{0}.offsetParentMatrix".format(obj))
            for axis in "xyz":
                cmds.setAttr("{0}.t{1}".format(obj, axis), 0)
                cmds.setAttr("{0}.r{1}".format(obj, axis), 0)

# create_uvPin(cmds.ls(sl=1), plane_size=0.3, new_transform=False)


def create_follicle(obj_list, plane_size=0.3, name="follicle"):
    if not obj_list:
        raise ValueError("No object need to create uvPin, please input object list first.")
    # create mesh
    mesh = createPlane(obj_list, size=plane_size, name="uvPin")
    for i, obj in enumerate(obj_list):
        follicle = generate_unique_name(name)
        follicle = cmds.createNode("transform", name=follicle)
        follicle_shape = cmds.createNode("follicle", name="{0}Shape".format(follicle), parent=follicle)
        cmds.connectAttr("{0}.outMesh".format(mesh), "{0}.inputMesh".format(follicle_shape))
        cmds.connectAttr("{0}.worldMatrix[0]".format(mesh), "{0}.inputWorldMatrix".format(follicle_shape))
        cmds.setAttr("{0}.parameterU".format(follicle_shape), i + 0.5)
        cmds.setAttr("{0}.parameterV".format(follicle_shape), 0.5)
        cmds.connectAttr("{0}.outTranslate".format(follicle_shape), "{0}.translate".format(follicle))
        cmds.connectAttr("{0}.outRotate".format(follicle_shape), "{0}.rotate".format(follicle))
        matrixConstraint(follicle, obj)
