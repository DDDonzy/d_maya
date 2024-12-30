from maya.api import OpenMaya as om
from maya import cmds


def get_world_matrix(obj: str) -> om.MMatrix:
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).inclusiveMatrix()


def createPlane(object_list, size=1, name="uvPinPlane"):
    if not object_list:
        return
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
    fnDep.setName(f"{transform}Shape")

    fnMesh.setUVs(u, v)
    fnMesh.assignUVs(uvCounts, uvIds)
    return transform