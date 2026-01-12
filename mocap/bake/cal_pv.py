from maya import cmds
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


def cal_pv(name):
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

        cmds.addAttr(asset, ln="len", at="double", k=1, dv=120)
        cmds.connectAttr(f"{asset}.len", f"{md_final_vector_mult}.input1X")
        cmds.connectAttr(f"{asset}.len", f"{md_final_vector_mult}.input1Y")
        cmds.connectAttr(f"{asset}.len", f"{md_final_vector_mult}.input1Z")

    return start, mid, end, loc_result


def do_cal_pv(
    source_namespace="MOCAP",
    target_namespace="RIG",
):
    """ """
    bake_list = []
    for k, v in bake_pv_dict.items():
        start, mid, end, out = cal_pv(name=k)
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
        bake_list.append(f"{target_pv}.tx")
        bake_list.append(f"{target_pv}.ty")
        bake_list.append(f"{target_pv}.tz")
    return bake_list
