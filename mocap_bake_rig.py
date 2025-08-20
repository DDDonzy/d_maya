from maya import cmds
from maya.api import OpenMaya as om
from UTILS.transform import get_worldMatrix, get_relativesMatrix
from UTILS.compounds import matrixConstraint
from UTILS.create.assetCallback import AssetCallback

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


def cal_main(pelvis, pelvis_ctl, main_ctl, frontAxis="Z", t=1, r=1):
    with AssetCallback(name="cal_main", isDagAsset=True) as asset:
        offset = get_relativesMatrix(
            get_worldMatrix(pelvis_ctl),
            get_worldMatrix(pelvis),
        )
        proxy_loc = cmds.spaceLocator(name="cal_main_pelvis_loc")[0]
        pelvis_con = matrixConstraint(pelvis, proxy_loc)
        cmds.setAttr(pelvis_con.inputOffsetMatrix, offset, type="matrix")
        # pelvis ground
        pelvis_ground_loc = cmds.spaceLocator(name="cal_main_pelvis_ground_loc")[0]
        cmds.parentConstraint(proxy_loc, pelvis_ground_loc, mo=False, skipTranslate="y")[0]

        pelvis_ground_aim_loc = cmds.spaceLocator(name="cal_main_pelvis_ground_aim_loc")[0]
        aim_parentCon = cmds.parentConstraint(pelvis_ground_loc, pelvis_ground_aim_loc, mo=False, skipTranslate="y")[0]
        cmds.setAttr(f"{aim_parentCon}.target[0].targetOffsetTranslate{frontAxis}", 100)

        cmds.pointConstraint(pelvis_ground_loc, main_ctl, mo=0)
        aimVector = {"X": [1, 0, 0], "Y": [0, 1, 0], "Z": [0, 0, 1]}
        cmds.aimConstraint(pelvis_ground_aim_loc, main_ctl, aimVector=aimVector[frontAxis], worldUpType="scene", upVector=[0, 1, 0])

        if not t:
            cmds.setAttr(f"{main_ctl}.translate", 0, 0, 0)
            cmds.mute(f"{main_ctl}.translate")
        if not r:
            cmds.setAttr(f"{main_ctl}.rotate", 0, 0, 0)
            cmds.mute(f"{main_ctl}.rotate")

    return asset


def pre_bakeAnimations(
    target_namespace="TestCharacter_rig",
    source_namespace="Retarget_M_Blade_Stand_Idle",
    main_t=True,
    main_r=True,
):
    # pre
    with AssetCallback(name="bakeConstraint", isDagAsset=False) as asset:
        # bake offset data
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

        # do fk constraints
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

        # constraint main
        cal_main(f"{source_namespace}:pelvis", f"{target_namespace}:RootX_M", f"{target_namespace}:Main", frontAxis="Z", t=main_t, r=main_r)

        bake_list = list(bake_pv_dict.keys()) + list(bake_dict.keys()) + ["Main"]
        bake_list = [f"{target_namespace}:{x}*" if target_namespace else x for x in bake_list]

    return asset, bake_list


def bakeAnimations(bake_list, time=(0, 1000)):
    layers_before = set(cmds.ls(type="animLayer"))

    cmds.bakeResults(
        bake_list,
        at=["t", "r", "s"],
        t=time,
        sb=1,
        simulation=1,
        bakeOnOverrideLayer=1,
    )

    layers_after = set(cmds.ls(type="animLayer"))
    new_layer_set = layers_after - layers_before

    if new_layer_set:
        new_layer_default_name = new_layer_set.pop()
        cmds.rename(new_layer_default_name, "MOCAP_ANIM_LAYER")

    for x in cmds.ls(type="animBlendNodeAdditiveScale"):
        cmds.setAttr(f"{x}.inputA", 1)

    for x in cmds.ls(type="animBlendNodeAdditiveRotation"):
        cmds.setAttr(f"{x}.inputA", *(0, 0, 0))

    for x in cmds.ls(type="animBlendNodeAdditiveDL"):
        cmds.setAttr(f"{x}.inputA", 0)


if __name__ == "__main__":
    asset, bake_list = pre_bakeAnimations(
        target_namespace="TestCharacter_rig1",
        source_namespace="Retarget_M_Blade_Stand_Run_F_Loop_",
        main_t=True,
        main_r=True,
    )

    bakeAnimations(
        bake_list=bake_list,
        time=(0, 1200),
    )

    cmds.delete(asset)
