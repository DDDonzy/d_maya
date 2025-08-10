from UTILS.dag.getHistory import get_orig, get_shape, get_obj
from maya.api import OpenMaya as om
import UTILS.apiundo as apiundo
from maya import cmds


def update_orig(sourceMesh: str, deformerMesh: str):
    target_shape = get_shape(sourceMesh)
    origs = get_orig(deformerMesh)
    if not (target_shape and origs):
        raise ValueError("Target mesh or original shape not found.")

    target_plug: om.MPlug = get_obj(f"{target_shape[0]}.outMesh", plug=True)
    for orig in origs:
        orig_plug: om.MPlug = get_obj(f"{orig}.outMesh", plug=True)

        data = target_plug.asMObject()
        bake_data = orig_plug.asMObject()

        def _doit():
            orig_plug.setMObject(data)

        def _undo():
            orig_plug.setMObject(bake_data)

        _doit()
        apiundo.commit(_undo, _doit)


def update_orig_cmd():
    sel = cmds.ls(sl=1)
    if len(sel) < 2:
        cmds.warning("Please select a deformer mesh and a target mesh.")
        return

    targetMesh = sel[0]
    deformerMeshes = sel[1:]
    for mesh in deformerMeshes:
        update_orig(targetMesh, mesh)


if __name__ == "__main__":
    update_orig_cmd()
