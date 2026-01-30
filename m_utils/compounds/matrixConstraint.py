import maya.cmds as cmds
from m_utils.compounds.decomMatrix import decomMatrix
from m_utils.create.createBase import CreateBase, CreateNode
from m_utils.transform import get_offsetMatrix, get_worldMatrix


class matrixConstraint(CreateBase):
    """Create matrix constraint node"""

    isDagAsset: bool = True

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Variable length argument list.
                controller: args[0], If not args, will be get it from selection list[0]
                target: args[1], If not args, will be get it from selection list[1]
            **kwargs: Arbitrary keyword arguments.
                query (bool): Default is False.
                edit (bool): Default is False.
                translate (bool): Default is True.
                rotate (bool): Default is True.
                scale (bool): Default is True.
                shear (bool): Default is True.
        """
        self.keepOffset = kwargs.get("maintainOffset", True) and kwargs.get("mo", True)
        self.translate = kwargs.get("translate", True) and kwargs.get("t", True)
        self.rotate = kwargs.get("rotate", True) and kwargs.get("r", True)
        self.scale = kwargs.get("scale", True) and kwargs.get("s", True)
        self.shear = kwargs.get("shear", True) and kwargs.get("sh", True)
        if len(args) == 2:
            self.controller, self.target = args
        else:
            sel = cmds.ls(sl=1)
            if len(sel) == 2:
                self.controller, self.target = sel
            else:
                raise RuntimeError("Please input or select two objects.")
        self.name = self.target

        super().__init__(*args, **kwargs)

    def create(self):
        self.hasJointOrient = cmds.objExists(f"{self.target}.jointOrient")

        offsetMatrix = get_offsetMatrix(child_worldMatrix=get_worldMatrix(obj=self.target), parent_worldMatrix=get_worldMatrix(obj=self.controller))

        node_multMatrix = CreateNode("multMatrix", name=self.createName("multMatrix"))

        node_decom = decomMatrix(name=self.name, translate=self.translate, rotate=self.rotate, scale=self.scale, shear=self.shear)

        self.publishAttr(
            data={
                "inputOffsetMatrix": f"{node_multMatrix}.matrixIn[0]",
                "inputControllerMatrix": f"{node_multMatrix}.matrixIn[1]",
                "inputRotateOrder": node_decom.inputRotateOrder,
                "inputRelativeSpaceMatrix": node_decom.inputRelativeSpaceMatrix,
                "outputTranslate": node_decom.outputTranslate,
                "outputRotate": node_decom.outputRotate,
                "outputScale": node_decom.outputScale,
                "outputShear": node_decom.outputShear,
            }
        )
        if self.hasJointOrient:
            self.publishAttr(data={"inputTargetJointOrient": node_decom.inputJointOrient})

        # Internal connects
        cmds.connectAttr(f"{node_multMatrix}.matrixSum", node_decom.inputMatrix)
        # External connects
        if self.keepOffset:
            cmds.setAttr(f"{node_multMatrix}.matrixIn[0]", offsetMatrix, type="matrix")
        cmds.connectAttr(f"{self.controller}.worldMatrix[0]", f"{node_multMatrix}.matrixIn[1]")