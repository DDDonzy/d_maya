from maya import cmds
from maya.api import OpenMaya as om
from UTILS.transform import get_worldMatrix, get_relativesMatrix, matrix_to_trs

bake_dict = {
    "RootX_M": {
        "PARENT": r"pelvis",
        "ROT_OFFSET": [90, 90, 0],
        "OUT_JOINT": r"pelvis",
    },
    "IKSpine1_M": {
        "PARENT": r"pelvis",
        "ROT_OFFSET": [90, 90, 0],
        "OUT_JOINT": r"pelvis",
    },
    "IKhybridSpine1_M": {
        "PARENT": r"pelvis",
        "ROT_OFFSET": [180, 0, 0],
        "OUT_JOINT": r"pelvis",
    },
    "IKSpine3_M": {
        "PARENT": r"spine_04",
        "ROT_OFFSET": [90, 90, 0],
        "OUT_JOINT": r"spine_04",
    },
    "IKhybridSpine3_M": {
        "PARENT": r"spine_04",
        "ROT_OFFSET": [180, 0, 0],
        "OUT_JOINT": r"spine_04",
    },
    "FKRoot_M": {
        "PARENT": r"pelvis",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"pelvis",
    },
    "FKSpine1_M": {
        "PARENT": r"spine_01",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"spine_01",
    },
    "FKSpine2_M": {
        "PARENT": r"spine_02",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"spine_02",
    },
    "FKSpine3_M": {
        "PARENT": r"spine_03",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"spine_03",
    },
    "FKChest_M": {
        "PARENT": r"spine_04",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"spine_04",
    },
    "FKChestEnd_M": {
        "PARENT": r"spine_05",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"spine_05",
    },
    "FKScapula_L": {
        "PARENT": r"clavicle_l",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"clavicle_l",
    },
    "FKScapula_R": {
        "PARENT": r"clavicle_r",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"clavicle_r",
    },
    "IKLeg_R": {
        "PARENT": r"foot_r",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"foot_r",
    },
    "IKLeg_L": {
        "PARENT": r"foot_l",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"foot_l",
    },
    "IKArm_R": {
        "PARENT": r"hand_r",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"hand_r",
    },
    "IKArm_L": {
        "PARENT": r"hand_l",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"hand_l",
    },
    "FKNeck_M": {
        "PARENT": r"neck_01",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"neck_01",
    },
    "FKHead_M": {
        "PARENT": r"head",
        "ROT_OFFSET": [-180, 0, 0],
        "OUT_JOINT": r"head",
    },
}


target_namespace = "TestCharacter_rig"
source_namespace = "Retarget_M_Blade_Stand_Idle"


constraint_group = cmds.createNode("transform", name="Bake_Constraints_Group")

for k, v in bake_dict.items():
    control = f"{target_namespace}:{k}" if target_namespace else k
    source = f"{source_namespace}:{v['PARENT']}" if source_namespace else v["PARENT"]
    out_joint = f"{target_namespace}:{v['OUT_JOINT']}" if target_namespace else v["OUT_JOINT"]
    rot_offset = v["ROT_OFFSET"]

    if not (cmds.objExists(control) and cmds.objExists(source)):
        om.MGlobal.displayWarning(f"Control '{control}' does not exist.")
        continue

    try:
        offset = matrix_to_trs(
            get_relativesMatrix(
                get_worldMatrix(control),
                get_worldMatrix(out_joint),
            )
        )
        parent_con = cmds.parentConstraint(source, control, mo=True)[0]
        cmds.parent(parent_con, constraint_group)
        cmds.setAttr(f"{parent_con}.target[0].targetOffsetTranslate", *offset[0:3])
        cmds.setAttr(f"{parent_con}.target[0].targetOffsetRotate", *offset[3:6])

    except Exception as e:
        om.MGlobal.displayWarning("CONSTRAINT ERROR: " + str(e))
        continue
