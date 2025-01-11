from maya import cmds
from maya.api import OpenMaya as om
from utils.transform.transform import get_worldMatrix, matrixConstraint, create_decomposeMatrix
from utils.generateUniqueName import generateUniqueName
from utils.createAssets import createAssets


def get_UVByClosestPoint(point, shape):
    p = om.MPoint(point, 0)
    sel = om.MSelectionList()
    sel.add(shape)
    dag = sel.getDagPath(0)
    fn_mesh = om.MFnMesh(dag)
    set_name = fn_mesh.currentUVSetName()
    return fn_mesh.getUVAtPoint(p, space=om.MSpace.kWorld, uvSet=set_name)[0:2]


def get_currentUVSetName(shape):
    sel = om.MSelectionList()
    sel.add(shape)
    dag = sel.getDagPath(0)
    fn_mesh = om.MFnMesh(dag)
    return fn_mesh.currentUVSetName()


def create_planeByObjectList(object_list, size=1, name="uvPinPlane"):
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
    for i in range(num):
        # pos_ary
        mult_matrix = get_worldMatrix(object_list[i])
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
    fnDep.setName("{}Shape".format(transform))

    fnMesh.setUVs(u, v)
    fnMesh.assignUVs(uvCounts, uvIds)
    return transform, fnDep.name()


def create_uvPin(obj_list=[], plane_size=0.3, name="uvPin"):
    if not obj_list:
        obj_list = cmds.ls(sl=1)
        if not obj_list:
            raise ValueError("No object need to create uvPin, please input object list or select some object.")
    # create mesh
    mesh, shape = create_planeByObjectList(obj_list, size=plane_size, name="{}_mesh".format(name))

    # create uvPin node
    node_uvPin = cmds.createNode("uvPin", name=name)
    orig_outMesh = cmds.deformableShape(mesh, cog=1)[0]
    cmds.setAttr(".normalAxis", 0)
    cmds.setAttr(".tangentAxis", 5)
    cmds.setAttr("{}.uvSetName".format(node_uvPin),
                 get_currentUVSetName(mesh), type="string")
    cmds.connectAttr(orig_outMesh,
                     "{}.originalGeometry".format(node_uvPin))
    cmds.connectAttr("{}..worldMesh[0]".format(mesh),
                     "{}.deformedGeometry".format(node_uvPin))
    _add_nodeList = [node_uvPin]
    for i, obj in enumerate(obj_list):
        # set uvPin.uv value
        cmds.setAttr("{}.coordinate[{}].coordinateU".format(node_uvPin, i), i + 0.5)
        cmds.setAttr("{}.coordinate[{}].coordinateV".format(node_uvPin, i), 0.5)
        node_decom = create_decomposeMatrix(obj, scale=False, shear=False)
        cmds.connectAttr("{}.outputMatrix[{}]".format(node_uvPin, i), "{}.inputMatrix".format(node_decom))
        _add_nodeList.append(node_decom)
    _assets_uvPin = createAssets(name="{}_uvPinNodes".format(name), assetsType="UVPinConstraint", addNode=_add_nodeList)
    _assets = createAssets(name="{}_uvPinConstraint".format(name), assetsType="UVPinConstraint", addNode=[mesh, shape, orig_outMesh, _assets_uvPin], blackBox=0)
    return _assets


def create_follicle(obj_list=[], plane_size=0.3, name="follicle"):
    if not obj_list:
        obj_list = cmds.ls(sl=1)
        if not obj_list:
            raise ValueError("No object need to create uvPin, please input object list or select some object.")
    # create mesh
    mesh, shape = create_planeByObjectList(obj_list, size=plane_size, name=generateUniqueName("{}_mesh".format(name)))
    _add_nodeList = []
    for i, obj in enumerate(obj_list):
        follicle = generateUniqueName("{}_follicle".format(obj))
        follicle = cmds.createNode("transform", name=follicle)
        cmds.setAttr("{}.v".format(follicle), 0)
        follicle_shape = cmds.createNode("follicle", name="{}Shape".format(follicle), parent=follicle)
        cmds.connectAttr("{}.outMesh".format(mesh), "{}.inputMesh".format(follicle_shape))
        cmds.connectAttr("{}.worldMatrix[0]".format(mesh), "{}.inputWorldMatrix".format(follicle_shape))
        cmds.setAttr("{}.parameterU".format(follicle_shape), i + 0.5)
        cmds.setAttr("{}.parameterV".format(follicle_shape), 0.5)
        cmds.connectAttr("{}.outTranslate".format(follicle_shape), "{}.translate".format(follicle))
        cmds.connectAttr("{}.outRotate".format(follicle_shape), "{}.rotate".format(follicle))
        matrixCon = matrixConstraint(follicle, obj, scale=False, shear=False)
        _add_nodeList.extend([follicle, follicle_shape, matrixCon])
    _assets_follicle = createAssets(name="{}_follicleNodes".format(name), assetsType="FollicleConstraint", addNode=_add_nodeList)
    _assets = createAssets(name="{}_follicleConstraint".format(name), assetsType="FollicleConstraint", addNode=[mesh, shape, _assets_follicle], blackBox=0)
    return _assets
