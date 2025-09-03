import maya.cmds as cmds
from UTILS.compounds.decomMatrix import decomMatrix
from UTILS.create.createBase import CreateBase, CreateNode
from UTILS.transform import get_localMatrix, get_offsetMatrix, get_worldMatrix


class parentSpaceConstraint(CreateBase):
    """Create parentspace constraint"""

    isDagAsset: bool = False
    attrName = "parentSpace"

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                translate (bool): Default is True.
                rotate (bool): Default is True.
                scale (bool): Default is True.
                shear (bool): Default is True.
                niceName (str or list): A nice name for the controller(s). Default is an empty list.
                proxyAttrObject (str): Default is an empty string.
                force (bool): Default is False.
        """
        self.translate = kwargs.get("translate", True) and kwargs.get("t", True)
        self.rotate = kwargs.get("rotate", True) and kwargs.get("r", True)
        self.scale = kwargs.get("scale", True) and kwargs.get("s", True)
        self.shear = kwargs.get("shear", True) and kwargs.get("sh", True)
        self.proxyAttrObject = kwargs.get("proxyAttrObject") or kwargs.get("pxy") or ""

        # get controller and target
        if len(args) < 2:
            sel = cmds.ls(sl=1)
            if len(sel) < 2:
                raise RuntimeError("Please select at least 2 objects.")
            self.target = sel.pop()
            self.controller = sel
        else:
            self.target = args[-1]
            self.controller = args[0:-1]
        # get nice name
        self.niceName = kwargs.get("niceName") or kwargs.get("nn") or []
        if not isinstance(self.niceName, list):
            self.niceName = [self.niceName]
        if len(self.niceName) != len(self.controller):
            self.niceName = self.controller

        # create \ edit \ query
        self.isForce = kwargs.get("force") or kwargs.get("f") or False
        if cmds.objExists(f"{self.target}.{self.attrName}"):
            if self.isForce:
                cmds.deleteAttr(f"{self.target}.{self.attrName}")
            else:
                self.isEdit = True
        # attr object
        if not self.proxyAttrObject:
            self.proxyAttrObject = self.target
        super().__init__(*args, **kwargs)

    def create(self):
        self.createParentSpaceLogic()
        for i, controller in enumerate(self.controller):
            self.addParentSpaceController(controller=controller,
                                          niceName=self.niceName[i])

    def createParentSpaceLogic(self):
        localMatrix = get_localMatrix(self.target)
        # connect to chose
        node_choseControllerMatrix = CreateNode("choice", name=self.createName("choice"))
        node_choseOffsetMatrix = CreateNode("choice", name=self.createName(keyword="offsetChoice"))
        # add matrix
        cmds.addAttr(node_choseControllerMatrix, ln="controllerMatrix", at="matrix", m=1)
        cmds.addAttr(node_choseOffsetMatrix, ln="offsetMatrix", at="matrix", m=1)
        cmds.connectAttr(f"{node_choseControllerMatrix}.controllerMatrix[0]", f"{node_choseControllerMatrix}.input[0]")
        cmds.connectAttr(f"{node_choseOffsetMatrix}.offsetMatrix[0]", f"{node_choseOffsetMatrix}.input[0]")

        # cal world matrix
        node_calWorldMatrix = CreateNode("multMatrix", name=self.createName("parentMultMatrix"))
        cmds.connectAttr(f"{node_choseOffsetMatrix}.output", f"{node_calWorldMatrix}.matrixIn[0]")
        cmds.connectAttr(f"{node_choseControllerMatrix}.output", f"{node_calWorldMatrix}.matrixIn[1]")
        # chose to decomposeMatrix
        node_decom = decomMatrix(name=self.name,
                                 translate=self.translate,
                                 rotate=self.rotate,
                                 scale=self.scale,
                                 shear=self.shear)
        cmds.connectAttr(f"{node_calWorldMatrix}.matrixSum", node_decom.inputMatrix)
        # add parentspace switch attr
        cmds.addAttr(node_choseControllerMatrix, ln=self.attrName, at="enum", en="Parent", k=1)

        self.publishAttr(data={"inputRotateOrder": node_decom.inputRotateOrder,
                               "inputRelativeSpaceMatrix": node_decom.inputRelativeSpaceMatrix,
                               "outputTranslate": node_decom.outputTranslate,
                               "outputRotate": node_decom.outputRotate,
                               "outputScale": node_decom.outputScale,
                               "outputShear": node_decom.outputShear,
                               "parentspace": f"{node_choseControllerMatrix}.{self.attrName}",
                               "controllerMatrix": f"{node_choseControllerMatrix}.controllerMatrix",
                               "offsetMatrix": f"{node_choseOffsetMatrix}.offsetMatrix"})

        cmds.connectAttr(self.parentspace, f"{node_choseControllerMatrix}.selector")
        cmds.connectAttr(f"{node_choseControllerMatrix}.selector", f"{node_choseOffsetMatrix}.selector")

        # parent matrix * base local matrix
        cmds.connectAttr(f"{self.target}.parentMatrix[0]", f"{self.controllerMatrix}[0]")
        cmds.setAttr(f"{self.offsetMatrix}[0]", localMatrix, type="matrix")

        # add parentspace attr to obj        
        if cmds.objExists(f"{self.proxyAttrObject}.{self.attrName}"):
            cmds.deleteAttr(f"{self.proxyAttrObject}.{self.attrName}")
        cmds.addAttr(self.proxyAttrObject, ln=self.attrName, k=1, pxy=self.parentspace)
        # # add info
        # cmds.addAttr(self.proxyAttrObject, ln="parentSpaceChoice", at="message")
        # cmds.addAttr(node_choseControllerMatrix, ln="parentSpaceTarget", at="message")
        # cmds.connectAttr(f"{node_choseControllerMatrix}.parentSpaceTarget", f"{self.proxyAttrObject}.parentSpaceChoice")

    def addParentSpaceController(self,
                                 controller: str,
                                 niceName: str):

        # get index
        enum_str = cmds.addAttr(f"{self.proxyAttrObject}.{self.attrName}", q=1, en=1)
        nice_name_list = enum_str.split(":")
        nice_name_list.append(niceName)
        enum_str = ":".join(nice_name_list)
        parent_indices = len(nice_name_list)-1

        # update parentspace enum
        cmds.addAttr(f"{self.proxyAttrObject}.{self.attrName}", e=1, en=enum_str)
        cmds.addAttr(self.parentspace, e=1, en=enum_str)

        # offset matrix to chose
        offsetMatrix = get_offsetMatrix(get_worldMatrix(self.target),
                                        get_worldMatrix(controller))
        cmds.setAttr(f"{self.offsetMatrix}[{parent_indices}]", offsetMatrix, type="matrix")
        # controller matrix to chose
        cmds.connectAttr(f"{controller}.worldMatrix[0]", f"{self.controllerMatrix}[{parent_indices}]")

        # update chose input data
        controller_chose = cmds.listConnections(f"{self.controllerMatrix}[0]", p=0, d=1, s=0)[0]
        offset_chose = cmds.listConnections(f"{self.offsetMatrix}[0]", p=0, d=1, s=0)[0]
        cmds.connectAttr(f"{self.controllerMatrix}[{parent_indices}]", f"{controller_chose}.input[{parent_indices}]")
        cmds.connectAttr(f"{self.offsetMatrix}[{parent_indices}]", f"{offset_chose}.input[{parent_indices}]")
