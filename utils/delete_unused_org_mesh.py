from maya import cmds


def get_orig_mesh(obj):
    orig_list = []

    shape_list = cmds.listRelatives(obj, s=1)
    no_intermediate_shape_list = cmds.ls(shape_list, ni=1, s=1)

    for shape in no_intermediate_shape_list:
        orig = cmds.deformableShape(shape, originalGeometry=1)[0].split(".")[0]
        if not orig:
            continue
        orig_list.append(orig)
    return orig_list


def delete_unused_orig_mesh(obj):
    shape_list = cmds.listRelatives(obj, s=1)
    no_intermediate_shape_list = cmds.ls(shape_list, ni=1, s=1)
    intermediate_shape_list = cmds.ls(shape_list, io=1, s=1)

    for shape in no_intermediate_shape_list:
        orig = cmds.deformableShape(shape, originalGeometry=1)[0].split(".")[0]
        if not orig:
            continue
        for intermediate_shape in intermediate_shape_list:
            if intermediate_shape != orig:
                cmds.delete(intermediate_shape)
                print(f"DELETE UNUSED SHAPE: {shape}")


def update_orig(old_mesh, new_mesh):
    orig = get_orig_mesh(old_mesh)
    if not orig:
        raise RuntimeError(f"{old_mesh} do not have orig mesh")
    shape_list = cmds.listRelatives(new_mesh, s=1)
    shape = cmds.ls(shape_list, ni=1, s=1)[0]
    for x in orig:
        cmds.connectAttr(f"{shape}.outMesh",
                         f"{x}.inMesh")
        cmds.refresh()
        cmds.disconnectAttr(f"{shape}.outMesh",
                            f"{x}.inMesh")


def update_orig_cmd():
    sel = cmds.ls(sl=1)
    new_mesh = sel[0]
    old_mesh = sel[1:]
    for x in old_mesh:
        update_orig(x, new_mesh)


def delete_unused_orig_mesh_cmd():
    sel = cmds.ls(sl=1)
    for x in sel:
        delete_unused_orig_mesh(x)


update_orig_cmd()