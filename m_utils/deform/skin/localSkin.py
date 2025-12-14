from m_utils.dag.getHistory import get_history
from maya import cmds
from m_utils.create.createBase import CreateBase
from m_utils.apiundo import commit
from m_utils.compounds import matrixConstraint

from maya import cmds
from m_utils.create.createBase import CreateBase


class skinClusterToLocal(CreateBase):

    def create(self):
        skin = self.name
        shape = cmds.skinCluster(skin, q=True, g=True)[0]
        shape_transform = cmds.listRelatives(shape, parent=True)[0]
        shape_worldMatrix = f"{shape}.worldMatrix[0]"
        if not cmds.objExists(f"{shape_transform}.relativeSpaceEnable"):
            cmds.addAttr(shape_transform, ln="relativeSpaceEnable", at="bool", dv=0, k=1)

        self.relativesSpace_loc = cmds.createNode('transform', name=f'{skin}_relativesSpace')
        cmds.addAttr(self.relativesSpace_loc, ln="relativeSpaceEnable", at="bool", dv=0, k=1, pxy=f"{shape_transform}.relativeSpaceEnable")
        relativesSpace_worldMatrixI = f"{self.relativesSpace_loc}.worldInverseMatrix[0]"

        sk_bindPreMatrix = f"{skin}.bindPreMatrix"
        cmds.addAttr(skin, ln="bindPreMatrixBake", at="matrix", m=1)
        sk_bindPreMatrixBake = f"{skin}.bindPreMatrixBake"

        sk_geomMatrix = f"{skin}.geomMatrix"
        cmds.addAttr(skin, ln="skin_geoMatrixBake", at="matrix")
        sk_geomMatrixBake = f"{skin}.skin_geoMatrixBake"
        cmds.setAttr(sk_geomMatrixBake, cmds.getAttr(shape_worldMatrix), type='matrix')

        choice = cmds.createNode("choice", n=f"{skin}_choiceGeoMatrix")

        # geomMatrix choice
        cmds.connectAttr(sk_geomMatrixBake,
                         f"{choice}.input[0]")
        cmds.connectAttr(shape_worldMatrix,
                         f"{choice}.input[1]")
        cmds.connectAttr(f'{choice}.output', sk_geomMatrix)
        cmds.connectAttr(f"{self.relativesSpace_loc}.relativeSpaceEnable", f"{choice}.selector")

        indexes = cmds.getAttr(sk_bindPreMatrix, mi=1) or []
        for i in indexes:
            # get bindPreMatrix
            bindPreMatrix = cmds.getAttr(f"{sk_bindPreMatrix}[{i}]")
            # bake bindPreMatrix
            cmds.setAttr(f"{sk_bindPreMatrixBake}[{i}]", bindPreMatrix, type='matrix')
            # create matrix mult
            # (bind.I * relativesSpace).I = relativesSpace.I * (bind.I).I = relativesSpace.I * bind
            mult = cmds.createNode('multMatrix', name=f"{skin}_localSkin{i}")
            cmds.connectAttr(relativesSpace_worldMatrixI,
                             f"{mult}.matrixIn[0]")
            cmds.connectAttr(f"{sk_bindPreMatrixBake}[{i}]",
                             f"{mult}.matrixIn[1]")
            # switch
            choice = cmds.createNode("choice", n=f"{skin}_choice{i}")
            cmds.connectAttr(f"{sk_bindPreMatrixBake}[{i}]",
                             f"{choice}.input[0]")
            cmds.connectAttr(f"{mult}.matrixSum",
                             f"{choice}.input[1]")
            cmds.connectAttr(f'{choice}.output', f"{sk_bindPreMatrix}[{i}]")
            cmds.connectAttr(f"{self.relativesSpace_loc}.relativeSpaceEnable", f"{choice}.selector")

        matrixConstraint(shape_transform, self.relativesSpace_loc, mo=1)

    def _pre_create(self):
        skin = self.name
        skin_bindPreMatrix = f"{skin}.bindPreMatrix"
        self.bindPreMatrixBake = {}
        indexes = cmds.getAttr(skin_bindPreMatrix, mi=1) or []
        for index in indexes:
            self.bindPreMatrixBake.update({index: cmds.getAttr(f"{skin_bindPreMatrix}[{index}]")})

        def _undo():
            for index, matrix in self.bindPreMatrixBake.items():
                cmds.setAttr(f"{skin_bindPreMatrix}[{index}]", matrix, type='matrix')
        commit(_undo, self.create)


def skinClusterToLocal_cmd():
    for x in cmds.ls(sl=1):
        sk = get_history(x, "skinCluster")
        if sk:
            sk = sk[0]
        else:
            print(f"{x} has no skinCluster")
            continue
        if not cmds.listConnections(sk+".bindPreMatrix"):
            s = skinClusterToLocal(sk)
        else:
            print("bind pass")

if __name__ == "__main__":
    skinClusterToLocal_cmd()
