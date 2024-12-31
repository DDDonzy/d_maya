from maya import cmds
from maya.api import OpenMaya as om


def set_trsv(obj, trs):
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
    for i, attr in enumerate(attrs):
        try:
            cmds.setAttr(f"{obj}.{attr}", trs[i])
        except Exception as e:
            om.MGlobal.displayWarning(str(e))


def reset_transform_value(obj, transform=True, userDefined=True):
    if transform:
        set_trsv(obj, [0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
    if userDefined:
        user_defined = cmds.listAttr(obj, ud=1, u=1)
        if not user_defined:
            return
        for x in user_defined:
            try:
                v = cmds.addAttr(f"{obj}.{x}", q=1, dv=1)
                cmds.setAttr(f"{obj}.{x}", v)
            except:
                print(f"{x} ---> can't reset")


def reset_transform_value_cmd(transform=True, userDefined=False):
    for obj in cmds.ls(sl=1):
        reset_transform_value(obj, transform, userDefined)


if __name__ == "__main__":
    reset_transform_value_cmd()
