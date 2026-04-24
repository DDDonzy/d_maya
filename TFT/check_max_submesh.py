from maya import cmds

submesh_dict = {}

all_materials = cmds.ls(materials=1)

for x in all_materials:
    submesh_attr = None

    for name in [f"{x}.submesh", f"{x}.Submesh"]:
        if cmds.objExists(name):
            submesh_attr = name
    if submesh_attr is None:
        continue

    submesh_name = cmds.getAttr(submesh_attr)
    this_submesh_list = submesh_dict.get(submesh_name, [])
    this_submesh_list.append(x)
    submesh_dict[submesh_name] = this_submesh_list


msg = f'Submesh Count: {len(submesh_dict)}'
print(msg)
cmds.inViewMessage(amg=msg, pos="botCenter", fade=True, fadeOutTime=3.0)
