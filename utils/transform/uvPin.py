from maya import cmds
from maya.api import OpenMaya as om
from utils.transform.transform import get_worldMatrix, matrixConstraint, create_decomposeMatrix
from utils.generateUniqueName import generateUniqueName


def get_UVByClosestPoint(point, shape: str):
    p = om.MPoint(*point, 0)
    sel: om.MSelectionList = om.MGlobal.getSelectionListByName(shape)
    dag: om.MDagPath = sel.getDagPath(0)
    fn_mesh = om.MFnMesh(dag)
    set_name = fn_mesh.currentUVSetName()
    return fn_mesh.getUVAtPoint(p, space=om.MSpace.kWorld, uvSet=set_name)[0:2]


def get_currentUVSetName(shape):
    sel: om.MSelectionList = om.MGlobal.getSelectionListByName(shape)
    dag: om.MDagPath = sel.getDagPath(0)
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
    # num
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
    fnDep.setName(f"{transform}Shape")

    fnMesh.setUVs(u, v)
    fnMesh.assignUVs(uvCounts, uvIds)
    return transform


def create_uvPin(obj_list: list, plane_size=0.3, name: str = "uvPin"):
    if not obj_list:
        raise ValueError("No object need to create uvPin, please input object list first.")
    # create mesh
    mesh = create_planeByObjectList(obj_list, size=plane_size, name=f"{name}_mesh")

    # create uvPin node
    node_uvPin = cmds.createNode("uvPin", name=name)
    orig_outMesh = cmds.deformableShape(mesh, cog=1)[0]
    cmds.setAttr(".normalAxis", 0)
    cmds.setAttr(".tangentAxis", 5)
    cmds.setAttr(f"{node_uvPin}.uvSetName",
                 get_currentUVSetName(mesh), type="string")
    cmds.connectAttr(orig_outMesh,
                     f"{node_uvPin}.originalGeometry")
    cmds.connectAttr(f"{mesh}.worldMesh[0]",
                     f"{node_uvPin}.deformedGeometry")

    for i, obj in enumerate(obj_list):
        # set uvPin.uv value
        cmds.setAttr(f"{node_uvPin}.coordinate[{i}].coordinateU", i + 0.5)
        cmds.setAttr(f"{node_uvPin}.coordinate[{i}].coordinateV", 0.5)
        node_decom = create_decomposeMatrix(obj, scale=False)
        cmds.connectAttr(f"{node_uvPin}.outputMatrix[{i}]",
                         f"{node_decom}.inputMatrix")


def create_follicle(obj_list: list, plane_size=0.3, name: str = "follicle"):
    if not obj_list:
        raise ValueError("No object need to create uvPin, please input object list first.")
    # create mesh
    mesh = create_planeByObjectList(obj_list, size=plane_size, name="uvPin")
    for i, obj in enumerate(obj_list):
        follicle = generateUniqueName(name)
        follicle = cmds.createNode("transform", name=follicle)
        follicle_shape = cmds.createNode("follicle", name=f"{follicle}Shape", parent=follicle)
        cmds.connectAttr(f"{mesh}.outMesh", f"{follicle_shape}.inputMesh")
        cmds.connectAttr(f"{mesh}.worldMatrix[0]", f"{follicle_shape}.inputWorldMatrix")
        cmds.setAttr(f"{follicle_shape}.parameterU", i + 0.5)
        cmds.setAttr(f"{follicle_shape}.parameterV", 0.5)
        cmds.connectAttr(f"{follicle_shape}.outTranslate", f"{follicle}.translate")
        cmds.connectAttr(f"{follicle_shape}.outRotate", f"{follicle}.rotate")
        matrixConstraint(follicle, obj)


# create_uvPin(cmds.ls(sl=1), plane_size=0.3)
# create_follicle(cmds.ls(sl=1), plane_size=0.3)
