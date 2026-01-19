import m_utils.transform as transform
import maya.cmds as cmds
import log

root = "FKRootGround_M"
world_controls = ["IKLeg_R", "IKLeg_L", "RootX_M", "IKArm_L", "IKArm_R", "PoleArm_R", "PoleArm_L", "PoleLeg_R", "PoleLeg_L"]
local_controls = [
    "FKRingFinger1_R",
    "IKToes_L",
    "FKHip_L",
    "FKIKArm_R",
    "FKIndexFingerRoot_R",
    "FKCup_L",
    "FKChestEnd_M",
    "FKRingFingerRoot_R",
    "FKIndexFinger2_L",
    "IKSpine3_M",
    "FKPinkyFinger2_L",
    "FKThumbFinger3_R",
    "FKKnee_R",
    "IKSpine1_M",
    "FKIndexFinger3_L",
    "FKMiddleFingerRoot_R",
    "FKScapula_R",
    "FKFootIndexFinger2_L",
    "FKFootThumbFinger2_R",
    "FKFootMiddleFinger1_L",
    "FKMiddleFinger3_L",
    "FKFootIndexFinger1_L",
    "FKIndexFinger3_R",
    "FKRingFingerRoot_L",
    "FKRoot_M",
    "FKFootPinkyFinger1_R",
    "FKShoulder_R",
    "FKSpine3_M",
    "IKLeg_L",
    "FKElbow_R",
    "FKThumbFinger2_L",
    "FKThumbFinger1_R",
    "FKFootPinkyFinger2_L",
    "FKScapula_L",
    "HipSwinger_M",
    "IKArm_L",
    "FKFootMiddleFinger2_R",
    "Fingers_L",
    "RollHeel_L",
    "FKNeck1_M",
    "FKWeapon3_R",
    "FKFootIndexFinger3_R",
    "FKFootRingFinger2_L",
    "FKIndexFinger1_L",
    "IKSpine2_M",
    "FKHip_R",
    "FKIKArm_L",
    "FKToes_L",
    "FKHead_M",
    "FKPinkyFinger1_L",
    "FKIndexFinger2_R",
    "FKIndexFingerRoot_L",
    "RollToesEnd_R",
    "FKPinkyFinger3_R",
    "FKIndexFinger1_R",
    "FKRingFinger1_L",
    "PoleArm_L",
    "FKKnee_L",
    "PoleArm_R",
    "FKFootRingFinger1_R",
    "FKWrist_L",
    "FKFootMiddleFinger2_L",
    "FKIKLeg_L",
    "FKMiddleFinger1_L",
    "FKRingFinger3_R",
    "FKSpine1_M",
    "FKPinkyFinger2_R",
    "FKFootPinkyFinger1_L",
    "FKFootThumbFinger1_R",
    "FKMiddleFinger2_L",
    "FKRingFinger2_R",
    "FKThumbFinger2_R",
    "FKIKSpine_M",
    "PoleLeg_L",
    "FKPinkyFingerRoot_L",
    "FKFootRingFinger3_R",
    "FKWeapon_R",
    "FKPinkyFinger1_R",
    "FKIKLeg_R",
    "RollToesEnd_L",
    "FKFootMiddleFinger3_R",
    "IKArm_R",
    "FKElbow_L",
    "Fingers_R",
    "FKAnkle_R",
    "IKToes_R",
    "FKFootRingFinger3_L",
    "FKMiddleFinger1_R",
    "FKRingFinger2_L",
    "FKFootRingFinger2_R",
    "FKFootIndexFinger2_R",
    "FKWeaponGimbal_R",
    "FKAnkle_L",
    "FKFootThumbFinger1_L",
    "FKToes_R",
    "FKFootMiddleFinger3_L",
    "FKPinkyFinger3_L",
    "RollToes_L",
    "FKMiddleFinger2_R",
    "RootX_M",
    "FKFootIndexFinger1_R",
    "FKWeapon1_R",
    "FKRingFinger3_L",
    "FKFootThumbFinger2_L",
    "FKMiddleFinger3_R",
    "FKWeapon2_R",
    "RollHeel_R",
    "FKNeck_M",
    "PoleLeg_R",
    "FKShoulder_L",
    "FKMiddleFingerRoot_L",
    "FKPinkyFingerRoot_R",
    "FKFootPinkyFinger2_R",
    "FKFootIndexFinger3_L",
    "FKCup_R",
    "FKThumbFinger3_L",
    "IKLeg_R",
    "FKSpine2_M",
    "FKThumbFinger1_L",
    "FKFootMiddleFinger1_R",
    "FKFootRingFinger1_L",
    "RollToes_R",
    "FKWrist_R",
    "FKChest_M",
]

func_list = []


def copyPose():
    try:
        namespace = cmds.ls(sl=1)[-1].split(":")[0]
    except Exception:
        log.error("请选择Root控制器")
        return

    current_root_matrix = transform.get_worldMatrix(f"{namespace}:{root}")

    for x in world_controls:
        offset_matrix = transform.get_relativesMatrix(transform.get_worldMatrix(f"{namespace}:{x}"), current_root_matrix)

        def set(new_root_matrix, object=f"{namespace}:{x}", offset_matrix=offset_matrix):
            transform.set_worldMatrix(object, offset_matrix * new_root_matrix)

        func_list.append(set)

    for x in local_controls:
        if x not in world_controls:
            offset_matrix = transform.get_localMatrix(f"{namespace}:{x}")

            def set(new_root_matrix, object=f"{namespace}:{x}", offset_matrix=offset_matrix):
                transform.set_localMatrix(object, offset_matrix)

            func_list.append(set)


def pastePose():
    try:
        namespace = cmds.ls(sl=1)[-1].split(":")[0]
    except Exception:
        log.error("请选择Root控制器")
        return

    root_matrix = transform.get_worldMatrix(f"{namespace}:{root}")
    for func in func_list:
        func(root_matrix)
