import maya.cmds as cmds

# 节点类型 : 输出属性名
SKIP_MAP = {
    "blendWeighted": "output",
    "unitConversion": "output",
    "animCurve": "output",
}


def get_sdk_driven(driver_attr, plug=True):
    # 1. 获取 SDK 曲线
    curves = cmds.listConnections(driver_attr, type="animCurve", d=True, s=False) or []
    results = []

    for curve in set(curves):
        # 使用 plugs=True 获取属性路径，而不是节点名
        current_plug = f"{curve}.output"

        # 队列式处理：为了处理“一个节点输出到多个目标”的分支情况
        queue = [current_plug]

        while queue:
            curr = queue.pop(0)
            # 获取下游连接（必须带 p=True 才能拿到属性路径）
            dest_plugs = cmds.listConnections(curr, d=True, s=False, p=True) or []

            for dest in dest_plugs:
                node = dest.split(".")[0]

                # 检查是否为跳过节点
                skip_found = False
                for node_type, out_attr in SKIP_MAP.items():
                    if cmds.objectType(node, isa=node_type):
                        # 如果需要跳过，将该节点的输出属性加入队列，继续搜索
                        queue.append(f"{node}.{out_attr}")
                        skip_found = True
                        break

                if not skip_found and cmds.objectType(node) == "transform":
                    results.append(dest if plug else node)

    return list(set(results))  # 去重


# 使用示例
targets = get_sdk_driven("L_Brow_A_ctrl_zero.L_Brow_UD")
for x in targets:
    print(x)
