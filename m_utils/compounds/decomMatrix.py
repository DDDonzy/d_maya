import maya.cmds as cmds

from m_utils.create.createBase import CreateBase, CreateNode


class decomMatrix(CreateBase):
    """Create decompose a transformation matrix."""

    isDagAsset: bool = True

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                name (str): is not name input, will be get name by args[-1] or  selections[-1]
                query (bool):  Default is False.
                edit (bool):  Default is False.
                translate (bool): Default is True.
                rotate (bool): Default is True.
                scale (bool): Default is True.
                shear (bool): Default is True.
                relativesMatrix (bool): Default is True.
                force (bool): Default is True.
        """

        self.translate = kwargs.get("translate", True) and kwargs.get("t", True)
        self.rotate = kwargs.get("rotate", True) and kwargs.get("r", True)
        self.scale = kwargs.get("scale", True) and kwargs.get("s", True)
        self.shear = kwargs.get("shear", True) and kwargs.get("sh", True)
        self.isForce = kwargs.get("force", True) and kwargs.get("f", True)
        self.relativesMatrix = kwargs.get("relativesMatrix", True) and kwargs.get("rm", True)

        super().__init__(*args, **kwargs)

    def create(self):
        self.hasJointOrient = cmds.objExists(f"{self.name}.jointOrient")

        node_decom = CreateNode("decomposeMatrix", name=self.createName("decomposeMatrix"))
        node_mult = CreateNode("multMatrix", name=self.createName("getLocalMultMatrix"))
        node_matrixInverse = CreateNode("inverseMatrix", name=self.createName("inverseRelativesMatrix"))

        self.inputMatrix = None
        self.inputRotateOrder = None
        self.inputRelativeSpaceMatrix = None
        self.outputTranslate = None
        self.outputRotate = None
        self.outputScale = None
        self.outputShear = None

        self.publishAttr(
            data={
                "inputMatrix": f"{node_mult}.matrixIn[0]",
                "inputRotateOrder": f"{node_decom}.inputRotateOrder",
                "inputRelativeSpaceMatrix": f"{node_matrixInverse}.inputMatrix",
                "outputTranslate": f"{node_decom}.outputTranslate",
                "outputRotate": f"{node_decom}.outputRotate",
                "outputScale": f"{node_decom}.outputScale",
                "outputShear": f"{node_decom}.outputShear",
            }
        )

        # Internal connects
        cmds.connectAttr(f"{node_matrixInverse}.outputMatrix", f"{node_mult}.matrixIn[1]")
        cmds.connectAttr(f"{node_mult}.matrixSum", f"{node_decom}.inputMatrix")
        if self.hasJointOrient:
            node_euler_to_quat = CreateNode("eulerToQuat", name=self.createName("eulerToQuat"))
            node_invert_quat = CreateNode("quatInvert", name=self.createName("invertQuat"))
            node_prod_quat = CreateNode("quatProd", name=self.createName("prodQuat"))
            node_quat_to_euler = CreateNode("quatToEuler", name=self.createName("quatToEuler"))

            cmds.connectAttr(f"{node_decom}.inputRotateOrder", f"{node_quat_to_euler}.inputRotateOrder")
            cmds.connectAttr(f"{node_decom}.outputQuat", f"{node_prod_quat}.input1Quat")
            cmds.connectAttr(f"{node_euler_to_quat}.outputQuat", f"{node_invert_quat}.inputQuat")
            cmds.connectAttr(f"{node_invert_quat}.outputQuat", f"{node_prod_quat}.input2Quat")
            cmds.connectAttr(f"{node_prod_quat}.outputQuat", f"{node_quat_to_euler}.inputQuat")

            self.inputJointOrient = None
            self.outputRotate = None
            self.publishAttr(data={"inputJointOrient": f"{node_euler_to_quat}.inputRotate", "outputRotate": f"{node_quat_to_euler}.outputRotate"})

        # External connects
        if cmds.objExists(self.name):
            if self.hasJointOrient:
                cmds.connectAttr(f"{self.name}.jointOrient", self.inputJointOrient)  # in jointOrient
            if self.relativesMatrix:
                cmds.connectAttr(f"{self.name}.parentMatrix[0]", self.inputRelativeSpaceMatrix)  # input relatives space matrix
            cmds.connectAttr(f"{self.name}.rotateOrder", self.inputRotateOrder)  # in rotateOrder
            if self.translate:
                cmds.connectAttr(self.outputTranslate, f"{self.name}.translate", f=self.isForce)  # out translate
            if self.scale:
                cmds.connectAttr(self.outputScale, f"{self.name}.scale", f=self.isForce)  # out scale
            if self.shear:
                cmds.connectAttr(self.outputShear, f"{self.name}.shear", f=self.isForce)  # out shear
            if self.rotate:
                cmds.connectAttr(self.outputRotate, f"{self.name}.rotate", f=self.isForce)  # out rotate
                # cmds.connectAttr(f"{_assets}.outputQuat", f"{name}.rotateQuaternion")  # out rotate
                pass
