from maya import cmds
from maya.api import OpenMaya as om
from UTILS.create.assetCallback import AssetCallback

import yaml
from dataclasses import dataclass


@dataclass
class PoseControllerDataItem(yaml.YAMLObject):
    yaml_tag = 'ControllerDataItem'
    name: str
    value: dict
    type: int


@dataclass
class DriverData(yaml.YAMLObject):
    yaml_tag = 'Driver'

    driverObject: str
    driverTwistAxis: int
    driverEulerTwist: bool
    driverController: list


@dataclass
class PoseData(yaml.YAMLObject):
    yaml_tag = 'Pose'

    poseName: str
    isEnabled: bool
    poseType: int
    poseFalloff: float
    isIndependent: bool
    poseRotationFalloff: float
    poseTranslationFalloff: float
    poseRotation: list
    poseTranslation: list
    controllerData: list

    def postValueChange(self):
        if self.poseFalloff < 0.001:
            self.poseFalloff = 0.001
        if self.poseRotationFalloff < 0.001:
            self.poseRotationFalloff = 0.001
        if self.poseTranslationFalloff < 0.001:
            self.poseTranslationFalloff = 0.001


@dataclass
class PoseInterpolatorData(yaml.YAMLObject):
    yaml_tag = 'PoseInterpolator'

    name: str
    regularization: float
    outputSmoothing: float
    interpolation: int
    allowNegativeWeights: bool
    enableRotation: bool
    enableTranslation: bool
    driver: list
    pose: list


def get_psdData(psd):
    # utils info
    psd_driver = cmds.poseInterpolator(psd, q=1, d=1) or []
    psd_poseIdx = cmds.poseInterpolator(psd, q=1, i=1)
    psd_poseName = cmds.poseInterpolator(psd, q=1, pn=1)
    psd_poseInfo = zip(psd_poseIdx, psd_poseName)

    # get interpolator data
    regularization = cmds.getAttr(f"{psd}.regularization")
    outputSmoothing = cmds.getAttr(f"{psd}.outputSmoothing")
    interpolation = cmds.getAttr(f"{psd}.interpolation")
    allowNegativeWeights = cmds.getAttr(f"{psd}.allowNegativeWeights")
    enableRotation = cmds.getAttr(f"{psd}.enableRotation")
    enableTranslation = cmds.getAttr(f"{psd}.enableTranslation")

    # get driver data
    driverData = []
    for driverIdx, driver in enumerate(psd_driver):
        _driverData = DriverData(driver,
                                 cmds.getAttr(f"{psd}.driver[{driverIdx}].driverTwistAxis"),
                                 cmds.getAttr(f"{psd}.driver[{driverIdx}].driverEulerTwist"),
                                 cmds.listConnections(f"{psd}.driver[{driverIdx}].driverController", p=1, d=0) or [])
        driverData.append(_driverData)

    # get pose data
    poseData = []
    for poseIdx, poseName in psd_poseInfo:
        # pose transform data, (rotation and translation)
        poseRotation_list = []
        poseTranslation_list = []
        for driverIdx, driver in enumerate(psd_driver):
            poseRotation_list.append(cmds.getAttr(f"{psd}.pose[{poseIdx}].poseRotation[{driverIdx}]"))
            poseTranslation_list.append(cmds.getAttr(f"{psd}.pose[{poseIdx}].poseTranslation[{driverIdx}]"))

        # controls data
        controllersData = []
        for controllerAttr in cmds.ls(f"{psd}.pose[{poseIdx}].poseControllerData[*]"):
            _controllerData = []
            for itemAttr in cmds.ls(f"{controllerAttr}.poseControllerDataItem[*]"):
                item_name = cmds.getAttr(f"{itemAttr}.poseControllerDataItemName")
                item_type = cmds.getAttr(f"{itemAttr}.poseControllerDataItemType")
                item_value = cmds.getAttr(f"{itemAttr}.poseControllerDataItemValue")
                itemData = PoseControllerDataItem(name=item_name,
                                                  type=item_type,
                                                  value=list(item_value[0]) if isinstance(item_value, list) else item_value)
                _controllerData.append(itemData)
            controllersData.append(_controllerData)

        # pose attr
        poseType = cmds.getAttr(f"{psd}.pose[{poseIdx}].poseType")
        isEnabled = cmds.getAttr(f"{psd}.pose[{poseIdx}].isEnabled")
        poseFalloff = cmds.getAttr(f"{psd}.pose[{poseIdx}].poseFalloff")
        isIndependent = cmds.getAttr(f"{psd}.pose[{poseIdx}].isIndependent")
        poseRotationFalloff = cmds.getAttr(f"{psd}.pose[{poseIdx}].poseRotationFalloff")
        poseTranslationFalloff = cmds.getAttr(f"{psd}.pose[{poseIdx}].poseTranslationFalloff")

        _poseData = PoseData(poseName=poseName,
                             poseRotation=poseRotation_list,
                             poseTranslation=poseTranslation_list,
                             poseType=poseType,
                             isEnabled=isEnabled,
                             poseFalloff=poseFalloff,
                             isIndependent=isIndependent,
                             poseRotationFalloff=poseRotationFalloff,
                             poseTranslationFalloff=poseTranslationFalloff,
                             controllerData=controllersData)
        _poseData.postValueChange()
        poseData.append(_poseData)

    return PoseInterpolatorData(name=psd,
                                driver=driverData,
                                pose=poseData,
                                regularization=regularization,
                                outputSmoothing=outputSmoothing,
                                interpolation=interpolation,
                                allowNegativeWeights=allowNegativeWeights,
                                enableRotation=enableRotation,
                                enableTranslation=enableTranslation)


def create_psd(data: PoseInterpolatorData):
    # create psd
    psd_name = cmds.poseInterpolator([x.driverObject for x in data.driver], d=1, name=data.name)[0]
    # controls_obj_list = []

    # set interpolator data
    cmds.setAttr(f"{psd_name}.regularization", data.regularization)
    cmds.setAttr(f"{psd_name}.outputSmoothing", data.outputSmoothing)
    cmds.setAttr(f"{psd_name}.interpolation", data.interpolation)
    cmds.setAttr(f"{psd_name}.allowNegativeWeights", data.allowNegativeWeights)
    cmds.setAttr(f"{psd_name}.enableRotation", data.enableRotation)
    cmds.setAttr(f"{psd_name}.enableTranslation", data.enableTranslation)

    # set driver and controller object
    for driver_idx, driver in enumerate(data.driver):
        cmds.setAttr(f"{psd_name}.driver[{driver_idx}].driverTwistAxis", driver.driverTwistAxis)
        cmds.setAttr(f"{psd_name}.driver[{driver_idx}].driverEulerTwist", driver.driverEulerTwist)
        for controllerIdx, controllerData in enumerate(driver.driverController):
            if cmds.objExists(controllerData):
                cmds.connectAttr(controllerData, f"{psd_name}.driver[{driver_idx}].driverController[{controllerIdx}]")
            else:
                om.MGlobal.displayWarning("Driver controller not exists.")

    # set pose data
    for pose_idx, pose in enumerate(data.pose):
        # add pose
        cmds.poseInterpolator(psd_name, e=1, ap=pose.poseName)
        # pose attr
        cmds.setAttr(f"{psd_name}.pose[{pose_idx}].poseType", pose.poseType)
        cmds.setAttr(f"{psd_name}.pose[{pose_idx}].isEnabled", pose.isEnabled)
        cmds.setAttr(f"{psd_name}.pose[{pose_idx}].poseFalloff", pose.poseFalloff)
        cmds.setAttr(f"{psd_name}.pose[{pose_idx}].isIndependent", pose.isIndependent)
        cmds.setAttr(f"{psd_name}.pose[{pose_idx}].poseRotationFalloff", pose.poseRotationFalloff)
        cmds.setAttr(f"{psd_name}.pose[{pose_idx}].poseTranslationFalloff", pose.poseTranslationFalloff)

        # set pose transform data
        for t_idx, t in enumerate(pose.poseTranslation):
            cmds.setAttr(f"{psd_name}.pose[{pose_idx}].poseTranslation[{t_idx}]", t, type="doubleArray")
        for r_idx, r in enumerate(pose.poseRotation):
            cmds.setAttr(f"{psd_name}.pose[{pose_idx}].poseRotation[{r_idx}]", r, type="doubleArray")

        # set pose controller data
        # .pose[*]
        poseAttr = f"{psd_name}.pose[{pose_idx}]"
        if pose.controllerData:
            for controllerIdx, controllerData in enumerate(pose.controllerData):
                # .pose[*].poseControllerData[*]
                controllerAttr = f"{poseAttr}.poseControllerData[{controllerIdx}]"
                for itemIdx, itemData in enumerate(controllerData):
                    # .pose[*].poseControllerData[*].poseControllerDataItem[*]
                    itemAttr = f"{controllerAttr}.poseControllerDataItem[{itemIdx}]"
                    # set poseControllerDataItemName
                    if itemData.name and cmds.objExists(itemData.name):
                        cmds.setAttr(f"{itemAttr}.poseControllerDataItemName", itemData.name, type='string')
                    # set poseControllerDataItemType
                    if itemData.type:
                        cmds.setAttr(f"{itemAttr}.poseControllerDataItemType", itemData.type)
                    # set poseControllerDataItemValue
                    if itemData.value:
                        if isinstance(itemData.value, list) or isinstance(itemData.value, tuple):
                            cmds.setAttr(f"{itemAttr}.poseControllerDataItemValue", *itemData.value, type="double3")
                        else:
                            cmds.setAttr(f"{itemAttr}.poseControllerDataItemValue", itemData.value)


def import_proxyTransformData():
    """
    create proxy transform by data files
    """
    def create_proxyTransform(obj, parent, name):
        pxy_parent = cmds.createNode("transform", name=f"{name}_pxyParentTransform")
        pxy_obj = cmds.createNode("transform", name=f"{name}_pxyTransform", parent=pxy_parent)
        cmds.delete(cmds.parentConstraint(obj, pxy_parent))
        cmds.parentConstraint(parent, pxy_parent, mo=1)
        cmds.orientConstraint(obj, pxy_obj)
    path = cmds.fileDialog2(dialogStyle=2, caption="Load proxy transform data", fileFilter="YAML file(*.yaml)", fileMode=1)
    if not path:
        return
    path = path[0]
    with open(path, "r") as f:
        with AssetCallback(name="proxyTransform",
                           force=True,
                           isBlackBox=False,
                           isDagAsset=True):
            data = yaml.unsafe_load(f)
            for x in data:
                for i in x:
                    create_proxyTransform(x[i]["Joint"], x[i]["Parent"], i)


def export_psd(node=None):
    """
    export poseInterpolator's data as file
    Args:
        node (_type_, optional): poseInterpolator's name
    """
    if not node:
        node = cmds.ls(type="poseInterpolator")
        node = [cmds.listRelatives(x, p=1)[0] for x in node]
    if type(node) is not list:
        node = [node]

    data_list = []
    for i in node:
        data_list.append(get_psdData(i))
    path = cmds.fileDialog2(dialogStyle=2, caption="Export poseInterpolator data", fileFilter="YAML file(*.yaml)")
    if not path:
        return
    path = path[0]
    with open(path, "w") as f:
        yaml.dump(data_list, f, sort_keys=False, indent=4, width=80)


def import_psd():
    """
    import poseInterpolator node from files.
    """
    path = cmds.fileDialog2(dialogStyle=2, caption="Load poseInterpolator data", fileFilter="YAML file(*.yaml)", fileMode=1)
    if not path:
        return
    path = path[0]
    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)
        for data in data_list:
            create_psd(data)


def add_bsTarget(bs: str, name: str):
    """ add blendShape target
    Args:
        bs (str): blendShape name
        name (str): target name
    Returns:
        target_name (str): blendShape.w[*]
    """
    w_mi = cmds.getAttr(f"{bs}.w", mi=1)
    i = w_mi[-1]+1 if w_mi else 0
    cmds.setAttr(f"{bs}.w[{i}]", 0)
    if cmds.objExists(f"{bs}.{name}"):
        num = 0
        base_name = name
        while cmds.objExists(f"{bs}.{name}"):
            num += 1
            name = f"{base_name}{num}"
    cmds.aliasAttr(name, f"{bs}.w[{i}]")
    cmds.setAttr(f"{bs}.it[0].itg[{i}].iti[6000].ipt", *[1, (0, 0, 0, 1)], type="pointArray")
    cmds.setAttr(f"{bs}.it[0].itg[{i}].iti[6000].ict", *[1, "vtx[0]"], type="componentList")
    return f"{bs}.{name}"


def del_bsTargetData(bs: str, index: int):
    """ del blendShape target data
    Args:
        bs (str): blendShape name
        index (str): target index
    """
    cmds.setAttr(f"{bs}.it[0].itg[{index}].iti[6000].ipt", *[1, (0, 0, 0, 1)], type="pointArray")
    cmds.setAttr(f"{bs}.it[0].itg[{index}].iti[6000].ict", *[1, "vtx[0]"], type="componentList")


def create_bsTargetByPsd(bs: str, psd_node_list: list = None):
    """
    create blendShape target by poseInterpolator's pose output
    if psd_node_list is None, will be get poseInterpolator from selections list
    Args:
        bs (str): blendShape name
        psd_node_list (list): poseInterpolator node list
    """

    if not psd_node_list:
        psd_node_list = cmds.ls(sl=1)
        if not psd_node_list:
            om.MGlobal.displayError("No poseInterpolator node selected.")
            return

    for psd_node in psd_node_list:
        pas_prefix = psd_node.replace("_poseInterpolator", "")

        out_index = cmds.poseInterpolator(psd_node, q=1, i=1)
        targetOutAttr_list = [f"{psd_node}.output[{i}]" for i in out_index]
        targetName_list = cmds.poseInterpolator(psd_node, q=1, pn=1)

        if not cmds.objExists(f"{bs}.__{pas_prefix}__"):
            add_bsTarget(bs, f"__{pas_prefix}__")
        for idx, name in enumerate(targetName_list):
            if "neutral" in name or "Neutral" in name:
                continue

            outAttr = targetOutAttr_list[idx]

            if not cmds.objExists(f"{bs}.{name}"):
                add_bsTarget(bs, name)

            cmds.setDrivenKeyframe(f"{bs}.{name}", cd=outAttr, driverValue=0, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setDrivenKeyframe(f"{bs}.{name}", cd=outAttr, driverValue=1, v=1, inTangentType="linear", outTangentType="linear")


@dataclass
class FingerTargetData(yaml.YAMLObject):
    yaml_tag = "FingerTargetData"
    TargetName: str
    DriverAttr: str = None
    DriverMin: float = 0
    DriverMax: float = 0


def create_fingerBsTarget(bsNode):
    path = cmds.fileDialog2(dialogStyle=2, caption="Load finger blendShape data", fileFilter="YAML file(*.yaml)", fileMode=1)
    if not path:
        return
    path = path[0]
    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)
        for x in data_list:
            attr = add_bsTarget(bsNode, x.TargetName)
            if x.DriverAttr:
                cmds.setDrivenKeyframe(attr, cd=x.DriverAttr,
                                       driverValue=x.DriverMin, v=0,
                                       inTangentType="linear", outTangentType="linear")
                cmds.setDrivenKeyframe(attr, cd=x.DriverAttr,
                                       driverValue=x.DriverMax, v=1,
                                       inTangentType="linear", outTangentType="linear")


# import_proxyTransformData()
# export_psd(cmds.ls(sl=1))
# import_psd()
# create_bsTargetByPsd("blendShape1")
# create_fingerBsTarget("blendShape1")
