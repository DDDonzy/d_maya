from maya import cmds
from maya.api import OpenMaya as om


def get_world_matrix(obj: str) -> om.MMatrix:
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).inclusiveMatrix()


def get_uv_by_closest_point(point, shape: str):
    p = om.MPoint(*point, 0)
    sel: om.MSelectionList = om.MGlobal.getSelectionListByName(shape)
    dag: om.MDagPath = sel.getDagPath(0)
    fn_mesh = om.MFnMesh(dag)
    set_name = fn_mesh.currentUVSetName()
    return fn_mesh.getUVAtPoint(p, space=om.MSpace.kWorld, uvSet=set_name)[0:2]


def get_current_uvSet_name(shape):
    sel: om.MSelectionList = om.MGlobal.getSelectionListByName(shape)
    dag: om.MDagPath = sel.getDagPath(0)
    fn_mesh = om.MFnMesh(dag)
    return fn_mesh.currentUVSetName()


def create_uvPin(obj_list: list, new_transform=False, plane_size=0.1, name: str = "uvPin"):
    print("CREATE UV_PIN")
    if not obj_list:
        return

    plane_list = []
    for i, obj in enumerate(obj_list):
        print(f"        create plane {i}")
        obj_world_matrix = get_world_matrix(obj)
        mesh = cmds.polyPlane(ax=(1, 0, 0), sh=2, sw=2, sx=2, w=plane_size, h=plane_size, ch=0, name=name)[0]
        cmds.setAttr(".offsetParentMatrix", obj_world_matrix, type="matrix")
        cmds.polyEditUV(".map[*]", pu=0, pv=0, u=i, v=0)
        plane_list.append(mesh)
        cmds.refresh()

    print("    combine mesh")
    if len(plane_list) > 1:
        mesh = cmds.polyUnite(plane_list, ch=0, mergeUVSets=1, name=name)[0]

    print("    create uvPin node")
    node_uvPin = cmds.createNode("uvPin", name=name)
    orig_outMesh = cmds.deformableShape(mesh, cog=1)[0]
    cmds.setAttr(".normalAxis", 0)
    cmds.setAttr(".tangentAxis", 5)
    cmds.setAttr(f"{node_uvPin}.uvSetName",
                 get_current_uvSet_name(mesh), type="string")
    cmds.connectAttr(orig_outMesh,
                     f"{node_uvPin}.originalGeometry")
    cmds.connectAttr(f"{mesh}.worldMesh[0]",
                     f"{node_uvPin}.deformedGeometry")

    for i, obj in enumerate(obj_list):
        print(f"        connect uvPin{i}")
        p = cmds.xform(obj, q=1, t=1, ws=1)
        cmds.setAttr(f"{node_uvPin}.coordinate[{i}].coordinateU", i + 0.5)
        cmds.setAttr(f"{node_uvPin}.coordinate[{i}].coordinateV", 0.5)
        if new_transform:
            loc = cmds.createNode("transform", name=f"{obj}_uvPinLoc")
            cmds.connectAttr(f"{node_uvPin}.outputMatrix[{i}]",
                             f"{loc}.offsetParentMatrix")
            cmds.parentConstraint(loc, obj)

        else:
            cmds.connectAttr(f"{node_uvPin}.outputMatrix[{i}]",
                             f"{obj}.offsetParentMatrix")

    print("    result transform")
    for x in obj_list:
        for i in "xyz":
            cmds.setAttr(f"{x}.t{i}", 0)
            cmds.setAttr(f"{x}.r{i}", 0)

    print("UV_PIN DONE")


create_uvPin(cmds.ls(sl=1), new_transform=False)
