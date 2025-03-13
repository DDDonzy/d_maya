import maya.cmds as cmds
from UTILS.create.createBase import CreateBase, CreateNode


class relativesMatrix(CreateBase):
    """Create relatives matrix node"""
    isDagAsset: bool = False

    def create(self):
        node_multMatrix = CreateNode("multMatrix", name=self.createName("multMatrix"))
        node_inverseMatrix = CreateNode("inverseMatrix", name=self.createName("inverseMatrix"))
        cmds.connectAttr(f"{node_inverseMatrix}.outputMatrix", f"{node_multMatrix}.matrixIn[1]")

        self.inputMatrix = None
        self.inputRelativeMatrix = None
        self.outputMatrix = None
        self.publishAttr(data={"inputMatrix": f"{node_multMatrix}.matrixIn[0]",
                               "inputRelativeMatrix": f"{node_inverseMatrix}.inputMatrix",
                               "outputMatrix": f"{node_multMatrix}.matrixSum"})
