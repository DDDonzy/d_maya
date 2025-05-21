from maya import cmds
from maya.api import OpenMaya as om
from UTILS.create.assetCallback import AssetCallback

import yaml
from dataclasses import dataclass


@dataclass
class PoseControllerDataItem(yaml.YAMLObject):
    yaml_tag = 'ControlData'
    name: str
    value: dict
    type: int


@dataclass
class DriverData(yaml.YAMLObject):
    yaml_tag = 'DriverData'

    driverObject: str
    driverTwistAxis: int
    driverEulerTwist: bool
    driverController: list


@dataclass
class PoseData(yaml.YAMLObject):
    yaml_tag = 'PoseData'

    poseName: str
    poseType: int
    controllerData: list
    isEnabled: bool
    poseFalloff: float
    isIndependent: bool
    poseRotationFalloff: float
    poseTranslationFalloff: float
    poseRotation: list
    poseTranslation: list

    def postValueChange(self):
        if self.poseFalloff < 0.001:
            self.poseFalloff = 0.001
        if self.poseRotationFalloff < 0.001:
            self.poseRotationFalloff = 0.001
        if self.poseTranslationFalloff < 0.001:
            self.poseTranslationFalloff = 0.001


@dataclass
class PoseInterpolatorData(yaml.YAMLObject):
    yaml_tag = 'PoseInterpolatorData'

    name: str
    driver: list
    pose: list
    regularization: float
    outputSmoothing: float
    interpolation: int
    allowNegativeWeights: bool
    enableRotation: bool
    enableTranslation: bool


def load_dataByNode(node_name):
    controls_obj_list = []
    # get interpolator data
    regularization = cmds.getAttr(f"{node_name}.regularization")
    outputSmoothing = cmds.getAttr(f"{node_name}.outputSmoothing")
    interpolation = cmds.getAttr(f"{node_name}.interpolation")
    allowNegativeWeights = cmds.getAttr(f"{node_name}.allowNegativeWeights")
    enableRotation = cmds.getAttr(f"{node_name}.enableRotation")
    enableTranslation = cmds.getAttr(f"{node_name}.enableTranslation")
    # get driver data
    driver_data = []
    for pose_idx, driver in enumerate(cmds.poseInterpolator(node_name, q=1, d=1)):
        driverObject = driver
        driverTwistAxis = cmds.getAttr(f"{node_name}.driver[{pose_idx}].driverTwistAxis")
        driverEulerTwist = cmds.getAttr(f"{node_name}.driver[{pose_idx}].driverEulerTwist")
        driverController = cmds.listConnections(f"{node_name}.driver[{pose_idx}].driverController", p=1, d=0)
        if not driverController:
            driverController = []
        controls_obj_list += driverController
        driver_data.append(DriverData(driverObject,
                                      driverTwistAxis,
                                      driverEulerTwist,
                                      driverController))
    controls_obj_list = [x.split(".")[0] for x in list(set(controls_obj_list))]

    # get pose data
    pose_data = []
    pose_name_list = cmds.poseInterpolator(node_name, q=1, pn=1)
    pose_index_list = cmds.poseInterpolator(node_name, q=1, i=1)
    for i, poseName in enumerate(pose_name_list):
        # pose
        pose_idx = pose_index_list[i]
        poseRotation_list = []
        poseTranslation_list = []
        # pose driver data
        for dr_i, dr_obj in enumerate(cmds.poseInterpolator(node_name, q=1, d=1)):
            poseRotation_list.append(cmds.getAttr(f"{node_name}.pose[{pose_idx}].poseRotation[{dr_i}]"))
            poseTranslation_list.append(cmds.getAttr(f"{node_name}.pose[{pose_idx}].poseTranslation[{dr_i}]"))
        # controls data
        ctl_data = []
        for ctl in cmds.ls(f"{node_name}.pose[{pose_idx}].poseControllerData[*]"):
            item_data = []
            for item in cmds.ls(f"{ctl}.poseControllerDataItem[*]"):
                item_name = cmds.getAttr(f"{item}.poseControllerDataItemName")
                item_type = cmds.getAttr(f"{item}.poseControllerDataItemType")
                item_value = cmds.getAttr(f"{item}.poseControllerDataItemValue")
                if item_type == 8:
                    item_value = {"x": item_value[0][0], "y": item_value[0][1], "z": item_value[0][2]}
                data = PoseControllerDataItem(name=item_name,
                                              type=item_type,
                                              value=item_value)
                item_data.append(data)
            ctl_data.append(item_data)
        # pose attr
        poseType = cmds.getAttr(f"{node_name}.pose[{pose_idx}].poseType")
        isEnabled = cmds.getAttr(f"{node_name}.pose[{pose_idx}].isEnabled")
        poseFalloff = cmds.getAttr(f"{node_name}.pose[{pose_idx}].poseFalloff")
        isIndependent = cmds.getAttr(f"{node_name}.pose[{pose_idx}].isIndependent")
        poseRotationFalloff = cmds.getAttr(f"{node_name}.pose[{pose_idx}].poseRotationFalloff")
        poseTranslationFalloff = cmds.getAttr(f"{node_name}.pose[{pose_idx}].poseTranslationFalloff")
        pose_i = PoseData(poseName=poseName,
                          poseRotation=poseRotation_list,
                          poseTranslation=poseTranslation_list,
                          poseType=poseType,
                          isEnabled=isEnabled,
                          poseFalloff=poseFalloff,
                          isIndependent=isIndependent,
                          poseRotationFalloff=poseRotationFalloff,
                          poseTranslationFalloff=poseTranslationFalloff,
                          controllerData=ctl_data)
        pose_i.postValueChange()
        pose_data.append(pose_i)
    return PoseInterpolatorData(name=node_name,
                                driver=driver_data,
                                pose=pose_data,
                                regularization=regularization,
                                outputSmoothing=outputSmoothing,
                                interpolation=interpolation,
                                allowNegativeWeights=allowNegativeWeights,
                                enableRotation=enableRotation,
                                enableTranslation=enableTranslation)


def create_nodeByData(data: PoseInterpolatorData):
    controls_obj_list = []

    # set driver data
    driver_obj_list = [x.driverObject for x in data.driver]
    node_name = cmds.poseInterpolator(driver_obj_list, d=1, name=data.name)[0]
    for i, x in enumerate(data.driver):
        cmds.setAttr(f"{node_name}.driver[{i}].driverTwistAxis", x.driverTwistAxis)
        cmds.setAttr(f"{node_name}.driver[{i}].driverEulerTwist", x.driverEulerTwist)
        for c_i, c in enumerate(x.driverController):
            cmds.connectAttr(c, f"{node_name}.driver[{i}].driverController[{c_i}]")
            control_object = c.split(".")[0]
            if control_object not in controls_obj_list:
                controls_obj_list.append(control_object)

    # set interpolator data
    cmds.setAttr(f"{node_name}.regularization", data.regularization)
    cmds.setAttr(f"{node_name}.outputSmoothing", data.outputSmoothing)
    cmds.setAttr(f"{node_name}.interpolation", data.interpolation)
    cmds.setAttr(f"{node_name}.allowNegativeWeights", data.allowNegativeWeights)
    cmds.setAttr(f"{node_name}.enableRotation", data.enableRotation)
    cmds.setAttr(f"{node_name}.enableTranslation", data.enableTranslation)

    # add pose
    for i, pose in enumerate(data.pose):
        cmds.poseInterpolator(node_name, e=1, ap=pose.poseName)
        # pose driver data
        for dr_i, dr_obj in enumerate(cmds.poseInterpolator(node_name, q=1, d=1)):
            cmds.setAttr(f"{node_name}.pose[{i}].poseRotation[{dr_i}]", pose.poseRotation[dr_i], type="doubleArray")
            cmds.setAttr(f"{node_name}.pose[{i}].poseTranslation[{dr_i}]", pose.poseTranslation[dr_i], type="doubleArray")

        # pose controller data
        pose_attr = f"{node_name}.pose[{i}]"  # psd.pose[*]
        if pose.controllerData:
            for c_i, ctl in enumerate(pose.controllerData):
                ctl_attr = f"{pose_attr}.poseControllerData[{c_i}]"
                for i_i, item in enumerate(ctl):
                    item_attr = f"{ctl_attr}.poseControllerDataItem[{i_i}]"
                    cmds.setAttr(f"{item_attr}.poseControllerDataItemName", item.name, type='string')
                    cmds.setAttr(f"{item_attr}.poseControllerDataItemType", item.type)
                    if item.type == 8:
                        cmds.setAttr(f"{item_attr}.poseControllerDataItemValue", *item.value.values(), type="double3")
                    else:
                        cmds.setAttr(f"{item_attr}.poseControllerDataItemValue", item.value)
        # pose attr
        cmds.setAttr(f"{node_name}.pose[{i}].poseType", pose.poseType)
        cmds.setAttr(f"{node_name}.pose[{i}].isEnabled", pose.isEnabled)
        cmds.setAttr(f"{node_name}.pose[{i}].poseFalloff", pose.poseFalloff)
        cmds.setAttr(f"{node_name}.pose[{i}].isIndependent", pose.isIndependent)
        cmds.setAttr(f"{node_name}.pose[{i}].poseRotationFalloff", pose.poseRotationFalloff)
        cmds.setAttr(f"{node_name}.pose[{i}].poseTranslationFalloff", pose.poseTranslationFalloff)


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


def export_poseInterpolatorData(node=None):
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
        data_list.append(load_dataByNode(i))
    path = cmds.fileDialog2(dialogStyle=2, caption="Export poseInterpolator data", fileFilter="YAML file(*.yaml)")
    if not path:
        return
    path = path[0]
    with open(path, "w") as f:
        yaml.dump(data_list, f, sort_keys=False, indent=4, width=80)


def import_poseInterpolatorData():
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
            create_nodeByData(data)


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


def create_bsByPSD(bs: str, psd_node_list: list = None):
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

    out_attr_list = []
    pose_name_list = []
    for psd_node in psd_node_list:
        out_index = cmds.poseInterpolator(psd_node, q=1, i=1)
        out_attr_list += [f"{psd_node}.output[{i}]" for i in out_index]
        pose_name = cmds.poseInterpolator(psd_node, q=1, pn=1)
        prefix = psd_node.replace("_poseInterpolator", "")
        pose_name_list += []
        for n in pose_name:
            if prefix not in n:
                pose_name_list.append(f"__{prefix}_{n}__")
            else:
                pose_name_list.append(n)
    for i, x in enumerate(out_attr_list):
        attr = x
        name = pose_name_list[i]
        if not cmds.objExists(f"{bs}.{name}"):
            bs_wAttr = add_bsTarget(bs, name)
            if "Default" in name:
                cmds.setAttr(f"{bs}.{name}", l=1)
                continue
            cmds.setDrivenKeyframe(bs_wAttr, cd=attr, driverValue=0, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setDrivenKeyframe(bs_wAttr, cd=attr, driverValue=1, v=1, inTangentType="linear", outTangentType="linear")
            
        if "Default" in name:
            cmds.setAttr(f"{bs}.{name}", l=1)
            continue
        else:
            cmds.setDrivenKeyframe(f"{bs}.{name}", cd=attr, driverValue=0, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setDrivenKeyframe(f"{bs}.{name}", cd=attr, driverValue=1, v=1, inTangentType="linear", outTangentType="linear")



@dataclass
class FingerTargetData(yaml.YAMLObject):
    yaml_tag = "FingerTargetData"
    TargetName: str
    DriverAttr: str = None
    DriverMin: float = 0
    DriverMax: float = 0


def create_fingerTarget(bs):
    path = cmds.fileDialog2(dialogStyle=2, caption="Load finger blendShape data", fileFilter="YAML file(*.yaml)", fileMode=1)
    if not path:
        return
    path = path[0]
    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)
        for x in data_list:
            attr = add_bsTarget(bs, x.TargetName)
            if x.DriverAttr:
                cmds.setDrivenKeyframe(attr, cd=x.DriverAttr,
                                       driverValue=x.DriverMin, v=0,
                                       inTangentType="linear", outTangentType="linear")
                cmds.setDrivenKeyframe(attr, cd=x.DriverAttr,
                                       driverValue=x.DriverMax, v=1,
                                       inTangentType="linear", outTangentType="linear")


# import_proxyTransformData()
# export_poseInterpolatorData(cmds.ls(sl=1))
# import_poseInterpolator_data()
# create_bsByPSD("blendShape1")
# create_finger_bs("blendShape1")
