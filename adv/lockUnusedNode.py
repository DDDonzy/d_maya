from maya import cmds
from m_utils.dag.iterHierarchy import IterHierarchy

lockAttr = {
    "visibility": {"channelBox": False, "lock": True, "keyable": False},
    "rotateOrder": {"channelBox": True, "lock": False, "keyable": True},
    "displayRotatePivot": {"channelBox": False, "lock": True, "keyable": False},
    "displayScalePivot": {"channelBox": False, "lock": True, "keyable": False},
    "maxScaleLimit": {"channelBox": False, "lock": True, "keyable": False},
    "maxScaleLimitEnable": {"channelBox": False, "lock": True, "keyable": False},
    "maxScaleXLimit": {"channelBox": False, "lock": True, "keyable": False},
    "maxScaleXLimitEnable": {"channelBox": False, "lock": True, "keyable": False},
    "maxScaleYLimit": {"channelBox": False, "lock": True, "keyable": False},
    "maxScaleYLimitEnable": {"channelBox": False, "lock": True, "keyable": False},
    "maxScaleZLimit": {"channelBox": False, "lock": True, "keyable": False},
    "maxScaleZLimitEnable": {"channelBox": False, "lock": True, "keyable": False},
    "minScaleLimit": {"channelBox": False, "lock": True, "keyable": False},
    "minScaleLimitEnable": {"channelBox": False, "lock": True, "keyable": False},
    "minScaleXLimit": {"channelBox": False, "lock": True, "keyable": False},
    "minScaleXLimitEnable": {"channelBox": False, "lock": True, "keyable": False},
    "minScaleYLimit": {"channelBox": False, "lock": True, "keyable": False},
    "minScaleYLimitEnable": {"channelBox": False, "lock": True, "keyable": False},
    "minScaleZLimit": {"channelBox": False, "lock": True, "keyable": False},
    "minScaleZLimitEnable": {"channelBox": False, "lock": True, "keyable": False},
    "rotateAxis": {"channelBox": False, "lock": True, "keyable": False},
    "rotateAxisX": {"channelBox": False, "lock": True, "keyable": False},
    "rotateAxisY": {"channelBox": False, "lock": True, "keyable": False},
    "rotateAxisZ": {"channelBox": False, "lock": True, "keyable": False},
    "rotatePivot": {"channelBox": False, "lock": True, "keyable": False},
    "rotatePivotTranslate": {"channelBox": False, "lock": True, "keyable": False},
    "rotatePivotTranslateX": {"channelBox": False, "lock": True, "keyable": False},
    "rotatePivotTranslateY": {"channelBox": False, "lock": True, "keyable": False},
    "rotatePivotTranslateZ": {"channelBox": False, "lock": True, "keyable": False},
    "rotatePivotX": {"channelBox": False, "lock": True, "keyable": False},
    "rotatePivotY": {"channelBox": False, "lock": True, "keyable": False},
    "rotatePivotZ": {"channelBox": False, "lock": True, "keyable": False},
    "rotateQuaternion": {"channelBox": False, "lock": True, "keyable": False},
    "rotateQuaternionW": {"channelBox": False, "lock": True, "keyable": False},
    "rotateQuaternionX": {"channelBox": False, "lock": True, "keyable": False},
    "rotateQuaternionY": {"channelBox": False, "lock": True, "keyable": False},
    "rotateQuaternionZ": {"channelBox": False, "lock": True, "keyable": False},
    "scalePivot": {"channelBox": False, "lock": True, "keyable": False},
    "scalePivotTranslate": {"channelBox": False, "lock": True, "keyable": False},
    "scalePivotTranslateX": {"channelBox": False, "lock": True, "keyable": False},
    "scalePivotTranslateY": {"channelBox": False, "lock": True, "keyable": False},
    "scalePivotTranslateZ": {"channelBox": False, "lock": True, "keyable": False},
    "scalePivotX": {"channelBox": False, "lock": True, "keyable": False},
    "scalePivotY": {"channelBox": False, "lock": True, "keyable": False},
    "scalePivotZ": {"channelBox": False, "lock": True, "keyable": False},
    "transMinusRotatePivot": {"channelBox": False, "lock": True, "keyable": False},
    "transMinusRotatePivotX": {"channelBox": False, "lock": True, "keyable": False},
    "transMinusRotatePivotY": {"channelBox": False, "lock": True, "keyable": False},
    "transMinusRotatePivotZ": {"channelBox": False, "lock": True, "keyable": False},
    "scaleX": {"channelBox": False, "lock": True, "keyable": False},
    "scaleY": {"channelBox": False, "lock": True, "keyable": False},
    "scaleZ": {"channelBox": False, "lock": True, "keyable": False},
}

lockTranslateObjects = [
    "FKKnee_R",
    "FKShoulder_L",
    "FKNeck_M",
    "FKHip_R",
    "FKAnkle_L",
    "FKToes_R",
    "FKRoot_M",
    "FKHead_M",
    "FKSpine2_M",
    "FKElbow_L",
    "FKChest_M",
    "FKElbow_R",
    "FKAnkle_R",
    "FKChestEnd_M",
    "FKWrist_L",
    "FKSpine1_M",
    "FKHip_L",
    "FKNeck1_M",
    "FKSpine3_M",
    "FKScapula_R",
    "FKToes_L",
    "FKScapula_L",
    "HipSwinger_M",
    "FKShoulder_R",
    "FKWrist_R",
    "FKKnee_L",
]
lockRotateXYObjects = ["FKElbow_L", "FKElbow_R", "FKKnee_R", "FKKnee_L"]


def isController(obj):
    for shape in cmds.listRelatives(obj, s=1) or []:
        if cmds.objectType(shape, isa="nurbsCurve"):
            return True
    return False


def lockAttrs(obj):
    for attr, value in lockAttr.items():
        try:
            cmds.setAttr(f"{obj}.{attr}", lock=value["lock"], channelBox=value["channelBox"], keyable=value["keyable"])
        except RuntimeError:
            pass


rig_group = r"MotionSystem"
for obj, dag in IterHierarchy(rig_group):
    if cmds.objectType(obj, isAType="joint") or not cmds.objectType(obj, isAType="transform"):
        continue
    elif isController(obj):
        for attr, value in lockAttr.items():
            try:
                cmds.setAttr(f"{obj}.{attr}", lock=value["lock"], channelBox=value["channelBox"], keyable=value["keyable"])
            except RuntimeError:
                pass
    else:
        attrs = cmds.listAttr(obj)
        for attr in attrs:
            try:
                cmds.setAttr(f"{obj}.{attr}", lock=True)
            except RuntimeError:
                pass

for x in lockRotateXYObjects:
    if cmds.objExists(x):
        try:
            cmds.setAttr(f"{x}.rotateX", lock=True, channelBox=False, keyable=False)
            cmds.setAttr(f"{x}.rotateY", lock=True, channelBox=False, keyable=False)
        except RuntimeError:
            pass

for x in lockTranslateObjects:
    if cmds.objExists(x):
        try:
            cmds.setAttr(f"{x}.translateX", lock=True, channelBox=False, keyable=False)
            cmds.setAttr(f"{x}.translateY", lock=True, channelBox=False, keyable=False)
            cmds.setAttr(f"{x}.translateZ", lock=True, channelBox=False, keyable=False)
        except RuntimeError:
            pass
