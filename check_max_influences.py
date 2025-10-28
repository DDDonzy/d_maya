from maya import cmds


joint_group = "Bones"
mesh_group = "Meshes"


sel = [x for x in cmds.ls(type="mesh", ni=1, l=1) if f"|{mesh_group}|" in x]

inf_list = []
for obj in sel:
    inf_list += cmds.skinCluster(obj, q=1, inf=1)
inf_list = set(inf_list)


for x in list(inf_list):
    iter_obj = x

    while iter_obj:
        if iter_obj == joint_group:
            break

        iter_obj = cmds.listRelatives(iter_obj, p=1)[0]

        if iter_obj:
            if iter_obj not in inf_list:
                inf_list.add(iter_obj)


influence_count = len(inf_list)
print(f"Influences Num: {influence_count}")


if influence_count >= 256:

    msg = f'Influences Num: <font color="red">{influence_count}</font>'
else:
    msg = f'Influences Num: <font color="#00FFFF">{influence_count}</font>'

cmds.inViewMessage(amg=msg, pos="botCenter", fade=True, fadeOutTime=3.0)