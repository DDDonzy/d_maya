"""
解决 Maya 中 skinCluster 在远离原点（大坐标）时产生的精度丢失问题。

Context:
    Maya 的模型顶点数据 (Mesh Vertices) 使用单精度浮点数 (float) 存储，而 Transform 变换矩阵使用双精度 (double)。
    当蒙皮物体移动到距原点极远的位置（例如 > 50,000 单位）时，单精度浮点数的有效位数不足以支撑微小的形变计算，
    导致模型表面出现抖动、闪烁或精度丢失。

Logic:
    本工具通过构建一个“相对空间”来接管 skinCluster 的计算逻辑：
    1. 在模型上添加 `relativeSpaceEnable` 属性（默认`False`）。
    2. 开启 (`True`) 时：
       - 利用矩阵运算抵消掉巨大的世界坐标偏移。
       - 动态修改 `skinCluster` 的 `bindPreMatrix` 和 `geomMatrix` 输入。
       - 迫使 `skinCluster` 在局部空间（数值较小）内完成形变计算，从而避免大坐标带来的精度问题。
    3. 关闭 (`False`) 时：
       - 恢复 Maya 默认行为

    需要手动让模型的 `transform` 跟随角色移动，常规情况下，使用大环约束模型的 `transform` 即可。
Usage:
    skinClusterToLocal(skinNode='skinCluster1')
"""

from maya import cmds
from m_utils.dag.getHistory import get_history
from m_utils.apiundo import commit
from m_utils.create.createBase import CreateBase
from m_utils.compounds import matrixConstraint


class skinClusterToLocal(CreateBase):
    def _pre_create(self):
        self.skinNode = self.kwargs.get("skinNode", None) or self.kwargs.get("sn", None)
        if not self.skinNode:
            raise TypeError("Please input skinNode")

        skin_bindPreMatrix = f"{self.skinNode}.bindPreMatrix"
        self.bindPreMatrixBake = {}
        indexes = cmds.getAttr(skin_bindPreMatrix, mi=1) or []
        for index in indexes:
            self.bindPreMatrixBake.update({index: cmds.getAttr(f"{skin_bindPreMatrix}[{index}]")})

        def _undo():
            for index, matrix in self.bindPreMatrixBake.items():
                cmds.setAttr(f"{skin_bindPreMatrix}[{index}]", matrix, type="matrix")

        commit(_undo, self.create)

    def create(self):
        self.skinNode = self.skinNode
        shape = cmds.skinCluster(self.skinNode, q=True, g=True)[0]
        shape_transform = cmds.listRelatives(shape, parent=True)[0]
        shape_worldMatrix = f"{shape}.worldMatrix[0]"
        if not cmds.objExists(f"{shape_transform}.relativeSpaceEnable"):
            cmds.addAttr(shape_transform, ln="relativeSpaceEnable", at="bool", dv=0, k=1)

        self.relativesSpace_loc = cmds.createNode("transform", name=f"{self.skinNode}_relativesSpace")
        cmds.addAttr(self.relativesSpace_loc, ln="relativeSpaceEnable", at="bool", dv=0, k=1, pxy=f"{shape_transform}.relativeSpaceEnable")
        relativesSpace_worldMatrixI = f"{self.relativesSpace_loc}.worldInverseMatrix[0]"

        sk_bindPreMatrix = f"{self.skinNode}.bindPreMatrix"
        cmds.addAttr(self.skinNode, ln="bindPreMatrixBake", at="matrix", m=1)
        sk_bindPreMatrixBake = f"{self.skinNode}.bindPreMatrixBake"

        sk_geomMatrix = f"{self.skinNode}.geomMatrix"
        cmds.addAttr(self.skinNode, ln="skin_geoMatrixBake", at="matrix")
        sk_geomMatrixBake = f"{self.skinNode}.skin_geoMatrixBake"
        cmds.setAttr(sk_geomMatrixBake, cmds.getAttr(shape_worldMatrix), type="matrix")

        choice = cmds.createNode("choice", n=f"{self.skinNode}_choiceGeoMatrix")

        # geomMatrix choice
        cmds.connectAttr(sk_geomMatrixBake, f"{choice}.input[0]")
        cmds.connectAttr(shape_worldMatrix, f"{choice}.input[1]")
        cmds.connectAttr(f"{choice}.output", sk_geomMatrix)
        cmds.connectAttr(f"{self.relativesSpace_loc}.relativeSpaceEnable", f"{choice}.selector")

        indexes = cmds.getAttr(sk_bindPreMatrix, mi=1) or []
        for i in indexes:
            # get bindPreMatrix
            bindPreMatrix = cmds.getAttr(f"{sk_bindPreMatrix}[{i}]")
            # bake bindPreMatrix
            cmds.setAttr(f"{sk_bindPreMatrixBake}[{i}]", bindPreMatrix, type="matrix")
            # create matrix mult
            # (bind.I * relativesSpace).I = relativesSpace.I * (bind.I).I = relativesSpace.I * bind
            mult = cmds.createNode("multMatrix", name=f"{self.skinNode}_localSkin{i}")
            cmds.connectAttr(relativesSpace_worldMatrixI, f"{mult}.matrixIn[0]")
            cmds.connectAttr(f"{sk_bindPreMatrixBake}[{i}]", f"{mult}.matrixIn[1]")
            # switch
            choice = cmds.createNode("choice", n=f"{self.skinNode}_choice{i}")
            cmds.connectAttr(f"{sk_bindPreMatrixBake}[{i}]", f"{choice}.input[0]")
            cmds.connectAttr(f"{mult}.matrixSum", f"{choice}.input[1]")
            cmds.connectAttr(f"{choice}.output", f"{sk_bindPreMatrix}[{i}]")
            cmds.connectAttr(f"{self.relativesSpace_loc}.relativeSpaceEnable", f"{choice}.selector")

        matrixConstraint(shape_transform, self.relativesSpace_loc, mo=1)


def skinClusterToLocal_cmd():
    for x in cmds.ls(sl=1):
        sk = get_history(x, "skinCluster")
        if sk:
            sk = sk[0]
        else:
            print(f"{x} has no skinCluster")
            continue
        if not cmds.listConnections(sk + ".bindPreMatrix"):
            skinClusterToLocal(skinNode=sk)
        else:
            print("bind pass")


if __name__ == "__main__":
    skinClusterToLocal_cmd()
