from maya import cmds

from m_utils.deform.skin.getSkinJoint import get_skinJoint


mesh = "M_Head_base"
ssdr_list = []


def create_continuous_zigzag(name="Zigzag_Curve", center=(0, 0, 0), size=1.0, divisions=100, parent=None):
    half = size / 2.0
    cx, cy, cz = center
    # 计算 x 的步长
    step_size = size / float(divisions - 1)

    points = []
    # 遍历 divisions 次
    for i in range(divisions):
        x = cx - half + (i * step_size)
        # 奇偶行决定方向：偶数行从底到顶，奇数行从顶到底
        if i % 2 == 0:
            points.append((x, cy - half, cz))
            points.append((x, cy + half, cz))
        else:
            points.append((x, cy + half, cz))
            points.append((x, cy - half, cz))
    # 创建曲线
    curve = cmds.curve(p=points, d=1, name=name)
    shape = cmds.listRelatives(curve, s=1)[0]
    cmds.setAttr(f"{shape}.alwaysDrawOnTop", 1)
    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.overrideRGBColors", 1)
    cmds.setAttr(f"{shape}.overrideColorR", 1)
    cmds.setAttr(f"{shape}.overrideColorG", 0.5)
    cmds.setAttr(f"{shape}.overrideColorB", 0)
    cmds.setAttr(f"{shape}.overrideColorA", 0.05)
    cmds.setAttr(f"{shape}.lineWidth", 5)

    if parent:
        cmds.parent(shape, parent, r=1, s=1)
        cmds.delete(curve)
        return cmds.rename(shape, f"{parent}Shape")
    return shape


skin_inf = get_skinJoint(mesh)
for x in skin_inf:
    parent = cmds.listRelatives(x, p=True) or []
    ssdr = cmds.createNode("transform", name=f"{x}_ssdr", p=parent[0] if parent else None)
    create_continuous_zigzag(parent=ssdr, size=0.05)
    cmds.parent(x, ssdr)
    ssdr_list.append(ssdr)

cmds.sets(ssdr_list, n="ssdrSet")
