"""
================================================================================
Animation Baking Core Functions
================================================================================

[ 脚本目的 ]
该文件提供了将动画从一个源骨骼（UE 标准骨骼）烘焙到 绑定（Advanced Skeleton）的核心功能。
它通过创建一系列动态约束，将源骨骼的运动实时传递给目标绑定控制器，然后将这些运动的关键帧烘焙下来。

[ 核心组件 ]
1.  bake_dict:
    - 定义了目标绑定中 FK/IK 控制器与源骨骼关节的一对一映射关系。
    - 用于创建直接的矩阵约束（Matrix Constraint）。

2.  bake_pv_dict:
    - 定义了目标绑定中极向量（Pole Vector）控制器与源骨骼中对应 IK 链
      （如上臂、小臂、手）的映射关系。
    - 用于驱动极向量的动态计算。

[ 主要函数与工作流程 ]
1.  bakeAnimations(target_namespace, source_namespace, time):
    - 这是供外部调用的主入口函数。
    - 工作流程:
        a. 调用 `pre_bakeAnimations` 来创建所有的约束和计算节点。
        b. 调用 Maya 的 `bakeResults` 命令，对所有受约束的控制器在指定时间
           范围内进行烘焙，将动态的运动转化为静态的关键帧。
        c. 调用 `cmds.delete` 删除在预处理阶段创建的所有临时约束节点，
           保持场景干净。

2.  pre_bakeAnimations(...):
    - 烘焙前的预处理函数，负责搭建所有的“桥梁”。
    - 遍历 `bake_dict`，计算每个控制器相对于其驱动关节的初始偏移矩阵，
      并创建 `matrixConstraint` 将源关节的运动传递给目标控制器。
    - 遍历 `bake_pv_dict`，为每个 IK 链调用 `cal_pv` 函数，创建一套
      用于实时计算极向量位置的节点网络，并将计算结果约束到对应的极向量
      控制器上。
    - 返回所有被约束的控制器列表，供 `bakeResults` 使用。

3.  cal_pv(name):
    - 极向量位置的数学计算函数。
    - 它不使用简单的约束，而是通过创建一套 Maya 节点（如 plusMinusAverage,
      vectorProduct, multiplyDivide 等）来精确地、动态地计算出在 IK 链
      运动过程中，极向量应该处于的正确空间位置，以防止膝盖或手肘发生翻转。

[ 依赖项 ]
- 该脚本依赖于一系列自定义的工具函数，位于 `UTILS` 模块下，如
  `get_worldMatrix`, `matrixConstraint` 等。

================================================================================
"""

from maya import cmds
from maya.api import OpenMaya as om
from m_utils.transform import get_worldMatrix, get_relativesMatrix
from m_utils.compounds import matrixConstraint
from m_utils.create.assetCallback import AssetCallback

# 烘焙 ADV IK 向量控制器映射表
bake_pv_dict = {
    "PoleArm_L": {
        "START": "upperarm_l",
        "MID": "lowerarm_l",
        "END": "hand_l",
    },
    "PoleArm_R": {
        "START": "upperarm_r",
        "MID": "lowerarm_r",
        "END": "hand_r",
    },
    "PoleLeg_L": {
        "START": "thigh_l",
        "MID": "calf_l",
        "END": "foot_l",
    },
    "PoleLeg_R": {
        "START": "thigh_r",
        "MID": "calf_r",
        "END": "foot_r",
    },
}
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


def cal_pv(name="xxx"):
    """
    根据ik三段骨骼计算pv位置
    使用原骨骼，约束生成的locator，计算pv位置，约束到pv控制器上

    Returns: 输出四个定位器，前三个是ik骨骼位置，第四个是计算出来的pv位置
    """
    with AssetCallback(name=f"{name}_cal_pv", isDagAsset=False) as asset:
        start = cmds.spaceLocator(name=f"{name}ik_start")[0]
        mid = cmds.spaceLocator(name=f"{name}ik_mid")[0]
        end = cmds.spaceLocator(name=f"{name}ik_end")[0]

        loc_result = cmds.spaceLocator(name=f"{name}out_pv")[0]

        ik_start = cmds.createNode("decomposeMatrix")
        ik_end = cmds.createNode("decomposeMatrix")
        ik_pv = cmds.createNode("decomposeMatrix")

        pma_vec_a = cmds.createNode("plusMinusAverage")
        cmds.setAttr(f"{pma_vec_a}.operation", 2)

        pma_vec_b = cmds.createNode("plusMinusAverage")
        cmds.setAttr(f"{pma_vec_b}.operation", 2)

        vp_dot_product = cmds.createNode("vectorProduct")
        cmds.setAttr(f"{vp_dot_product}.operation", 1)

        vp_vec_a_squared = cmds.createNode("vectorProduct")
        cmds.setAttr(f"{vp_vec_a_squared}.operation", 1)

        md_scalar_division = cmds.createNode("multiplyDivide")
        cmds.setAttr(f"{md_scalar_division}.operation", 2)

        md_project_vector_mult = cmds.createNode("multiplyDivide")
        cmds.setAttr(f"{md_project_vector_mult}.operation", 1)

        pma_add_to_origin = cmds.createNode("plusMinusAverage")
        cmds.setAttr(f"{pma_add_to_origin}.operation", 1)

        pma_sub_to_project = cmds.createNode("plusMinusAverage")
        cmds.setAttr(f"{pma_sub_to_project}.operation", 2)

        md_final_vector_mult = cmds.createNode("multiplyDivide")

        normalize_vector = cmds.createNode("normalize")

        cmds.connectAttr(f"{start}.worldMatrix[0]", f"{ik_start}.inputMatrix")
        cmds.connectAttr(f"{end}.worldMatrix[0]", f"{ik_end}.inputMatrix")
        cmds.connectAttr(f"{mid}.worldMatrix[0]", f"{ik_pv}.inputMatrix")

        cmds.connectAttr(f"{ik_end}.outputTranslate", f"{pma_vec_a}.input3D[0]")
        cmds.connectAttr(f"{ik_start}.outputTranslate", f"{pma_vec_a}.input3D[1]")
        cmds.connectAttr(f"{ik_pv}.outputTranslate", f"{pma_vec_b}.input3D[0]")
        cmds.connectAttr(f"{ik_start}.outputTranslate", f"{pma_vec_b}.input3D[1]")

        cmds.connectAttr(f"{pma_vec_a}.output3D", f"{vp_dot_product}.input1")
        cmds.connectAttr(f"{pma_vec_b}.output3D", f"{vp_dot_product}.input2")

        cmds.connectAttr(f"{pma_vec_a}.output3D", f"{vp_vec_a_squared}.input1")
        cmds.connectAttr(f"{pma_vec_a}.output3D", f"{vp_vec_a_squared}.input2")

        cmds.connectAttr(f"{vp_dot_product}.outputX", f"{md_scalar_division}.input1X")
        cmds.connectAttr(f"{vp_vec_a_squared}.outputX", f"{md_scalar_division}.input2X")

        cmds.connectAttr(f"{md_scalar_division}.outputX", f"{md_project_vector_mult}.input1X")
        cmds.connectAttr(f"{md_scalar_division}.outputX", f"{md_project_vector_mult}.input1Y")
        cmds.connectAttr(f"{md_scalar_division}.outputX", f"{md_project_vector_mult}.input1Z")
        cmds.connectAttr(f"{pma_vec_a}.output3D", f"{md_project_vector_mult}.input2")

        cmds.connectAttr(f"{md_project_vector_mult}.output", f"{pma_sub_to_project}.input3D[1]")
        cmds.connectAttr(f"{pma_vec_b}.output3D", f"{pma_sub_to_project}.input3D[0]")
        cmds.connectAttr(f"{pma_sub_to_project}.output3D", f"{normalize_vector}.input")
        cmds.connectAttr(f"{normalize_vector}.output", f"{md_final_vector_mult}.input2")
        cmds.setAttr(f"{md_final_vector_mult}.input1", *(50, 50, 50))

        cmds.connectAttr(f"{md_final_vector_mult}.output", f"{pma_add_to_origin}.input3D[0]")
        cmds.connectAttr(f"{ik_start}.outputTranslate", f"{pma_add_to_origin}.input3D[1]")
        cmds.connectAttr(f"{md_project_vector_mult}.output", f"{pma_add_to_origin}.input3D[2]")

        cmds.connectAttr(f"{pma_add_to_origin}.output3D", f"{loc_result}.translate")

        cmds.addAttr(asset, ln="len", at="double", k=1, dv=50)
        cmds.connectAttr(f"{asset}.len", f"{md_final_vector_mult}.input1X")
        cmds.connectAttr(f"{asset}.len", f"{md_final_vector_mult}.input1Y")
        cmds.connectAttr(f"{asset}.len", f"{md_final_vector_mult}.input1Z")

    return start, mid, end, loc_result


def find_object_ignoring_namespace(obj_name):
    """
    查找物体，忽略 Namespace 层级
    """
    # 查找所有 transform 节点
    all_transforms = cmds.ls(type="transform")
    # 筛选
    result = [o for o in all_transforms if o == obj_name or o.endswith(":" + obj_name)]
    return result


def pre_bakeAnimations(
    target_namespace="TestCharacter_rig",
    source_namespace="Retarget_M_Blade_Stand_Idle",
    main_t=True,
    main_r=True,
):
    """
    烘焙预处理，生成约束等
    """
    # pre
    with AssetCallback(name="bakeConstraint", isDagAsset=False) as asset:
        # get offset data
        for k, v in bake_dict.items():
            control = f"{target_namespace}:{k}" if target_namespace else k
            source = f"{source_namespace}:{v['PARENT']}" if source_namespace else v["PARENT"]
            out_joint = f"{target_namespace}:{v['PARENT']}" if target_namespace else v["PARENT"]

            if not (cmds.objExists(control) and cmds.objExists(source)):
                om.MGlobal.displayWarning(f"Control '{control}' does not exist.")
                continue

            offset = get_relativesMatrix(
                get_worldMatrix(control),
                get_worldMatrix(out_joint),
            )
            v["OFFSET"] = offset

        # do constraints
        for k, v in bake_dict.items():
            control = f"{target_namespace}:{k}" if target_namespace else k
            source = f"{source_namespace}:{v['PARENT']}" if source_namespace else v["PARENT"]
            out_joint = f"{target_namespace}:{v['PARENT']}" if target_namespace else v["PARENT"]

            if not (cmds.objExists(control) and cmds.objExists(source)):
                continue

            try:
                matrix_con = matrixConstraint(source, control)
                cmds.setAttr(f"{matrix_con.thisAssetName}.inputOffsetMatrix", v["OFFSET"], type="matrix")
            except Exception as e:
                om.MGlobal.displayWarning("CONSTRAINT ERROR: " + str(e))
                continue

        # constraint pole vector
        for k, v in bake_pv_dict.items():
            start, mid, end, out = cal_pv(f"{k}")
            target_pv = f"{target_namespace}:{k}" if target_namespace else k
            if source_namespace:
                source_start = f"{source_namespace}:{v['START']}"
                source_mid = f"{source_namespace}:{v['MID']}"
                source_end = f"{source_namespace}:{v['END']}"
            else:
                source_start = v["START"]
                source_mid = v["MID"]
                source_end = v["END"]
            cmds.parentConstraint(source_start, start, mo=False)
            cmds.parentConstraint(source_mid, mid, mo=False)
            cmds.parentConstraint(source_end, end, mo=False)
            cmds.pointConstraint(out, target_pv, mo=False)

        bake_list = list(bake_pv_dict.keys()) + list(bake_dict.keys())
        bake_list = [f"{target_namespace}:{x}*" if target_namespace else x for x in bake_list]
        # root motion

        rootMotion = find_object_ignoring_namespace("rootMotion")
        if rootMotion:
            matrixConstraint(rootMotion[0], f"{target_namespace}:FKRootGround_M", mo=False)
            bake_list.append(f"{target_namespace}:FKRootGround_M" if target_namespace else "FKRootGround_M")

    return asset, bake_list


def bakeAnimations(target_namespace, source_namespace, time=(0, 1000)):
    asset, bake_list = pre_bakeAnimations(
        target_namespace=target_namespace,
        source_namespace=source_namespace,
        main_t=True,
        main_r=True,
    )

    cmds.bakeResults(
        bake_list,
        at=["t", "r", "s"],
        t=time,
        sb=1,
        simulation=1,
    )

    cmds.delete(asset)
