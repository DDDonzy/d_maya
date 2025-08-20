import maya.cmds as cmds


def cal_pv(name="xxx_"):
    try:
        container = cmds.container(type="dagContainer", name=f"{name}Calculate_PV_Container")
        cmds.container(container, e=1, c=1)

        start = cmds.spaceLocator(name=f"{name}ik_start")[0]
        end = cmds.spaceLocator(name=f"{name}ik_end")[0]
        pv = cmds.spaceLocator(name=f"{name}ik_pv")[0]

        loc_result = cmds.spaceLocator(name=f"{name}out_pv")[0]

        ik_start = cmds.createNode("decomposeMatrix")
        ik_end = cmds.createNode("decomposeMatrix")
        ik_pv = cmds.createNode("decomposeMatrix")

        pma_vec_a = cmds.createNode("plusMinusAverage")
        cmds.setAttr(f"{pma_vec_a}.operation", 2)  # 设置为 Subtract (减法)

        pma_vec_b = cmds.createNode("plusMinusAverage")
        cmds.setAttr(f"{pma_vec_b}.operation", 2)  # 设置为 Subtract (减法)

        vp_dot_product = cmds.createNode("vectorProduct")
        cmds.setAttr(f"{vp_dot_product}.operation", 1)  # 设置为 Dot Product (点积)

        vp_vec_a_squared = cmds.createNode("vectorProduct")
        cmds.setAttr(f"{vp_vec_a_squared}.operation", 1)  # 设置为 Dot Product (点积)

        md_scalar_division = cmds.createNode("multiplyDivide")
        cmds.setAttr(f"{md_scalar_division}.operation", 2)  # 设置为 Divide (除法)

        md_project_vector_mult = cmds.createNode("multiplyDivide")
        cmds.setAttr(f"{md_project_vector_mult}.operation", 1)  # 设置为 Multiply (乘法)

        pma_add_to_origin = cmds.createNode("plusMinusAverage")
        cmds.setAttr(f"{pma_add_to_origin}.operation", 1)  # 设置为 Sum (求和)

        pma_sub_to_project = cmds.createNode("plusMinusAverage")
        cmds.setAttr(f"{pma_sub_to_project}.operation", 2)  # 设置为 Subtract (减法)

        md_final_vector_mult = cmds.createNode("multiplyDivide")

        normalize_vector = cmds.createNode("normalize")

        cmds.connectAttr(f"{start}.worldMatrix[0]", f"{ik_start}.inputMatrix")
        cmds.connectAttr(f"{end}.worldMatrix[0]", f"{ik_end}.inputMatrix")
        cmds.connectAttr(f"{pv}.worldMatrix[0]", f"{ik_pv}.inputMatrix")

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

        cmds.addAttr(container, ln="len", at="double", k=1, dv=50)
        cmds.connectAttr(f"{container}.len", f"{md_final_vector_mult}.input1X")
        cmds.connectAttr(f"{container}.len", f"{md_final_vector_mult}.input1Y")
        cmds.connectAttr(f"{container}.len", f"{md_final_vector_mult}.input1Z")

        return start, end, pv, loc_result
    finally:
        cmds.container(container, e=1, c=0)

