from maya import cmds
from UTILS.create.createBase import CreateBase


class skinClusterToLocal(CreateBase):

    def create(self):
        skin = self.name
        local_transform = cmds.createNode('transform', name=f'{skin}_localSkin')

        skin_bindPreMatrix = f"{skin}.bindPreMatrix"
        skin_geomMatrix = f"{skin}.geomMatrix"

        shape = cmds.skinCluster(skin, q=True, g=True)[0]
        geo_transform = cmds.listRelatives(shape, p=True)[0]
        geo_offsetParentMatrix = f"{geo_transform}.offsetParentMatrix"

        local_worldMatrix = f"{local_transform}.worldMatrix[0]"
        local_worldInverseMatrix = f"{local_transform}.worldInverseMatrix[0]"

        cmds.connectAttr(local_worldMatrix, skin_geomMatrix)
        cmds.connectAttr(local_worldMatrix, geo_offsetParentMatrix)

        indexes = cmds.getAttr(skin_bindPreMatrix, mi=1) or []
        for index in indexes:
            mult = cmds.createNode('multMatrix', name=f"{skin}_localSkin{index}")
            bindPreMatrix = cmds.getAttr(f"{skin_bindPreMatrix}[{index}]")
            cmds.connectAttr(local_worldInverseMatrix, f"{mult}.matrixIn[0]")
            cmds.setAttr(f"{mult}.matrixIn[1]", bindPreMatrix, type='matrix')
            cmds.connectAttr(f"{mult}.matrixSum", f"{skin_bindPreMatrix}[{index}]")
