from face.fn.createBase import CreateBase
from face.fn.apiundo import commit
from face.fn.transform import matrixConstraint

from maya import cmds


class skinClusterToLocal(CreateBase):

    def create(self):
        skin = self.name
        shape = cmds.skinCluster(skin, q=True, g=True)[0]
        shape_transform = cmds.listRelatives(shape, parent=True)[0]
        shape_worldMatrix = "{}.worldMatrix[0]".format(shape)
        if not cmds.objExists("{}.relativeSpaceEnable".format(shape_transform)):
            cmds.addAttr(shape_transform, ln="relativeSpaceEnable", at="bool", dv=0, k=1)

        self.relativesSpace_loc = cmds.createNode('transform', name='{}_relativesSpace'.format(skin))
        cmds.addAttr(self.relativesSpace_loc, ln="relativeSpaceEnable", at="bool", dv=0, k=1, pxy="{}.relativeSpaceEnable".format(shape_transform))
        relativesSpace_worldMatrixI = "{}.worldInverseMatrix[0]".format(self.relativesSpace_loc)

        sk_bindPreMatrix = "{}.bindPreMatrix".format(skin)
        cmds.addAttr(skin, ln="bindPreMatrixBake", at="matrix", m=1)
        sk_bindPreMatrixBake = "{}.bindPreMatrixBake".format(skin)

        sk_geomMatrix = "{}.geomMatrix".format(skin)
        cmds.addAttr(skin, ln="skin_geoMatrixBake", at="matrix")
        sk_geomMatrixBake = "{}.skin_geoMatrixBake".format(skin)
        cmds.setAttr(sk_geomMatrixBake, cmds.getAttr(shape_worldMatrix), type='matrix')

        choice = cmds.createNode("choice", n="{}_choiceGeoMatrix".format(skin))

        # geomMatrix choice
        cmds.connectAttr(sk_geomMatrixBake,
                         "{}.input[0]".format(choice))
        cmds.connectAttr(shape_worldMatrix,
                         "{}.input[1]".format(choice))
        cmds.connectAttr("{}.output".format(choice), sk_geomMatrix)
        cmds.connectAttr("{}.relativeSpaceEnable".format(self.relativesSpace_loc), "{}.selector".format(choice))

        indexes = cmds.getAttr(sk_bindPreMatrix, mi=1) or []
        for i in indexes:
            # get bindPreMatrix
            bindPreMatrix = cmds.getAttr("{}[{}]".format(sk_bindPreMatrix, i))
            # bake bindPreMatrix
            cmds.setAttr("{}[{}]".format(sk_bindPreMatrixBake, i), bindPreMatrix, type='matrix')
            # create matrix mult
            # (bind.I * relativesSpace).I = relativesSpace.I * (bind.I).I = relativesSpace.I * bind
            mult = cmds.createNode('multMatrix', name="{}_localSkin{}".format(skin, i))
            cmds.connectAttr(relativesSpace_worldMatrixI,
                             "{}.matrixIn[0]".format(mult))
            cmds.connectAttr("{}[{}]".format(sk_bindPreMatrixBake, i),
                             "{}.matrixIn[1]".format(mult))
            # switch
            choice = cmds.createNode("choice", n="{}_choice{}".format(skin, i))
            cmds.connectAttr("{}[{}]".format(sk_bindPreMatrixBake, i),
                             "{}.input[0]".format(choice))
            cmds.connectAttr("{}.matrixSum".format(mult),
                             "{}.input[1]".format(choice))
            cmds.connectAttr("{}.output".format(choice), "{}[{}]".format(sk_bindPreMatrix, i))
            cmds.connectAttr("{}.relativeSpaceEnable".format(self.relativesSpace_loc), "{}.selector".format(choice))

        matrixConstraint(shape_transform, self.relativesSpace_loc, mo=1)

    def _pre_create(self):
        skin = self.name
        skin_bindPreMatrix = "{}.bindPreMatrix".format(skin)
        self.bindPreMatrixBake = {}
        indexes = cmds.getAttr(skin_bindPreMatrix, mi=1) or []
        for index in indexes:
            self.bindPreMatrixBake.update({index: cmds.getAttr("{}[{}]".format(skin_bindPreMatrix, index))})

        def _undo():
            for index, matrix in self.bindPreMatrixBake.items():
                cmds.setAttr("{}[{}]".format(skin_bindPreMatrix, index), matrix, type='matrix')
        commit(_undo, self.create)
    
    def _post_create(self):
        cmds.setAttr("{}.{}".format(self.relativesSpace_loc, "relativeSpaceEnable"), 1)

