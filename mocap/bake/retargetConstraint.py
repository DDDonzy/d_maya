import log

from maya import cmds
import m_utils.transform as transform
from m_utils.compounds import matrixConstraint

# ADV 控制器对应UE骨骼控制表
bake_dict = {
    "FKAnkle_L": {"PARENT": "foot_l"},
    "FKAnkle_R": {"PARENT": "foot_r"},
    "FKChestEnd_M": {"PARENT": "spine_05"},
    "FKChest_M": {"PARENT": "spine_04"},
    "FKElbow_L": {"PARENT": "lowerarm_l"},
    "FKElbow_R": {"PARENT": "lowerarm_r"},
    "FKHead_M": {"PARENT": "head"},
    "FKHip_L": {"PARENT": "thigh_l"},
    "FKHip_R": {"PARENT": "thigh_r"},
    "FKKnee_L": {"PARENT": "calf_l"},
    "FKKnee_R": {"PARENT": "calf_r"},
    "FKNeck_M": {"PARENT": "neck_01"},
    "FKRoot_M": {"PARENT": "pelvis"},
    "FKScapula_L": {"PARENT": "clavicle_l"},
    "FKScapula_R": {"PARENT": "clavicle_r"},
    "FKShoulder_L": {"PARENT": "upperarm_l"},
    "FKShoulder_R": {"PARENT": "upperarm_r"},
    "FKSpine1_M": {"PARENT": "spine_01"},
    "FKSpine2_M": {"PARENT": "spine_02"},
    "FKSpine3_M": {"PARENT": "spine_03"},
    "FKToes_L": {"PARENT": "ball_l"},
    "FKToes_R": {"PARENT": "ball_r"},
    "FKWrist_L": {"PARENT": "hand_l"},
    "FKWrist_R": {"PARENT": "hand_r"},
    "IKArm_L": {"PARENT": "hand_l"},
    "IKArm_R": {"PARENT": "hand_r"},
    "IKLeg_L": {"PARENT": "foot_l"},
    "IKLeg_R": {"PARENT": "foot_r"},
    "IKSpine1_M": {"PARENT": "pelvis"},
    "IKSpine3_M": {"PARENT": "spine_04"},
    "IKToes_L": {"PARENT": "ball_l"},
    "IKToes_R": {"PARENT": "ball_r"},
    "IKhybridSpine1_M": {"PARENT": "pelvis"},
    "IKhybridSpine3_M": {"PARENT": "spine_04"},
    "RootX_M": {"PARENT": "pelvis"},
}


def do_constraint(source_namespace="", target_namespace=""):
    """
    由于绑定使用ADV，ADV输出骨骼直接约束我们的引擎骨骼，
    所以我们绑定文件自带一个约束骨骼的偏差矩阵。
    而我们的动捕数据是使用UE骨骼重定向的，
    所以直接在绑定文件中获取偏差矩阵，使用 `偏差矩阵 * 重新重定向骨骼矩阵` 烘焙到控制器上。
    """
    
    bake_list = []
    # 获取 offset matrix
    for k, v in bake_dict.items():
        control = f"{target_namespace}:{k}" if target_namespace else k
        source = f"{source_namespace}:{v['PARENT']}" if source_namespace else v["PARENT"]
        out_joint = f"{target_namespace}:{v['PARENT']}" if target_namespace else v["PARENT"]

        if not (cmds.objExists(control) and cmds.objExists(source)):
            log.warning(f"Control '{control}' does not exist.")
            continue

        offset = transform.get_relativesMatrix(
            transform.get_worldMatrix(control),
            transform.get_worldMatrix(out_joint),
        )
        v["OFFSET"] = offset

    # 使用自定义节点做矩阵约束
    for k, v in bake_dict.items():
        control = f"{target_namespace}:{k}" if target_namespace else k
        source = f"{source_namespace}:{v['PARENT']}" if source_namespace else v["PARENT"]
        out_joint = f"{target_namespace}:{v['PARENT']}" if target_namespace else v["PARENT"]

        if not (cmds.objExists(control) and cmds.objExists(source)):
            continue

        try:
            matrix_con = matrixConstraint(source, control)
            cmds.setAttr(f"{matrix_con.thisAssetName}.inputOffsetMatrix", v["OFFSET"], type="matrix")
            bake_list.append(f"{control}.tx")
            bake_list.append(f"{control}.ty")
            bake_list.append(f"{control}.tz")
            bake_list.append(f"{control}.rx")
            bake_list.append(f"{control}.ry")
            bake_list.append(f"{control}.rz")
        except Exception as e:
            log.warning("CONSTRAINT ERROR: " + str(e))
            continue

    return bake_list
