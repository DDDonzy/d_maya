import maya.cmds as cmds
from m_utils.compounds.decomMatrix import decomMatrix
from m_utils.create.createBase import CreateBase, CreateNode

class offsetFK(CreateBase):
    """Create offset fk system"""

    def __init__(self, *args, **kwargs):
        """
            Args:
            *args: Variable length argument list.
                args[0] (list): List of controllers if not provided in kwargs.
                args[1] (list): List of offsets if not provided in kwargs.
            **kwargs: Arbitrary keyword arguments.
                controllerList (list): List of controllers. Default is an empty list.
                offsetList (list): List of offsets. Default is an empty list.
        """
        # get parameter
        self.controllerList = kwargs.get("controllerList") or kwargs.get("cl") or []
        self.offsetList = kwargs.get("offsetList") or kwargs.get("ol") or []
        #
        if not self.controllerList:
            self.controllerList = args[0] if args else []
        if not self.offsetList:
            self.offsetList = args[1] if args else []
        if not self.controllerList or not self.offsetList:
            raise RuntimeError("Input error!")

        super().__init__(*args, **kwargs)

    def create(self):
        for i, control in enumerate(self.controllerList[:-1]):
            offset = self.offsetList[i]
            next_offset = self.offsetList[i + 1]
            next_control = self.controllerList[i + 1]

            node_multMatrix = CreateNode("multMatrix", name=f"{next_control}_multMatrix_{self.thisType}1")
            node_decom = decomMatrix(name=next_offset)
            # get offset matrix from 'offset_obj' with 'next offset_obj'
            cmds.connectAttr(f"{next_offset}.parentMatrix[0]",
                             f"{node_multMatrix}.matrixIn[0]")
            cmds.connectAttr(f"{offset}.parentInverseMatrix[0]",
                             f"{node_multMatrix}.matrixIn[1]")
            # controller constraint it
            cmds.connectAttr(f"{control}.worldMatrix[0]",
                             f"{node_multMatrix}.matrixIn[2]")
            # matrix to trs
            cmds.connectAttr(f"{node_multMatrix}.matrixSum",
                             node_decom.inputMatrix)
            
if __name__ == "__main__":
    offsetFK(controllerList=["ctrl1", "ctrl2"],
             offsetList=["offset1", "offset2"])