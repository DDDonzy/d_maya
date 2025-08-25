from maya import cmds
from UTILS.dag.iterHierarchy import IterHierarchy


def isController(obj):
    for shape in cmds.listRelatives(obj, s=1) or []:
        if cmds.objectType(shape, isa="nurbsCurve"):
            return True
    return False



def lockAttrs(obj):
    attrs = cmds.listAttr(obj) or []
    for attr in attrs:
        try:
            cmds.setAttr(f"{obj}.{attr}", lock=True, channelBox=False, keyable=False)
        except RuntimeError:
            pass



rig_group = r"MotionSystem"
for obj, dag in IterHierarchy(rig_group):
    if cmds.objectType(obj, isAType="joint") or not cmds.objectType(obj, isAType="transform"):
        continue
    if not isController(obj):
        lockAttrs(obj)
        cmds.controller(obj)
