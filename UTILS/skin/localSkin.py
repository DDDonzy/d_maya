from maya import cmds
from UTILS.create.createBase import CreateBase
from UTILS.apiundo import commit
from UTILS import transform as t

from maya import cmds
from UTILS.create.createBase import CreateBase


class skinClusterToLocal(CreateBase):

    def create(self):
        skin = self.name
        self.local_transform = cmds.createNode('transform', name=f'{skin}_localSkin')

        skin_bindPreMatrix = f"{skin}.bindPreMatrix"
        skin_geomMatrix = f"{skin}.geomMatrix"

        shape = cmds.skinCluster(skin, q=True, g=True)[0]

        local_worldInverseMatrix = f"{self.local_transform}.worldInverseMatrix[0]"

        cmds.connectAttr(f"{shape}.worldMatrix[0]", skin_geomMatrix)

        indexes = cmds.getAttr(skin_bindPreMatrix, mi=1) or []
        for index in indexes:
            mult = cmds.createNode('multMatrix', name=f"{skin}_localSkin{index}")
            bindPreMatrix = cmds.getAttr(f"{skin_bindPreMatrix}[{index}]")
            cmds.connectAttr(local_worldInverseMatrix, f"{mult}.matrixIn[0]")
            cmds.setAttr(f"{mult}.matrixIn[1]", bindPreMatrix, type='matrix')
            cmds.connectAttr(f"{mult}.matrixSum", f"{skin_bindPreMatrix}[{index}]")
            
            
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
    
    def _post_create(self):
        cmds.parent(self.local_transform, w=1)



for x in cmds.ls(sl=1):
    sk = get_history(x,"skinCluster")[0]
    if not cmds.listConnections(sk+".bindPreMatrix"):
        s = skinClusterToLocal(sk)
        cmds.setAttr(s.local_transform+".tx",l=0)
        cmds.setAttr(s.local_transform+".tx",20)
    else:
        print("bind pass")
