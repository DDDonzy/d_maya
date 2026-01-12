from maya import cmds

# 设置gloabl
global_dict = {
    "FKShoulder_L.Global": 10,
    "FKShoulder_R.Global": 10,
    "FKNeck_M.Global": 10,
    "FKHead_M.Global": 10,
    "FKHip_L.Global": 10,
    "FKHip_R.Global": 10,
}


def do_set_global(target_namespace):
    bake_list = []

    for x, value in global_dict.items():
        cmds.setAttr(f"{target_namespace}:{x}", value)
        bake_list.append(f"{target_namespace}:{x}")

    return bake_list
