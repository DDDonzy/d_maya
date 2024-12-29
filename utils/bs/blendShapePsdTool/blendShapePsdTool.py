from maya import cmds
from maya.api import OpenMaya as om
import yaml
from dataclasses import dataclass


@dataclass
class poseControllerDataItem(yaml.YAMLObject):
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

    def post_value(self):
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


def load_data_by_node(node_name):
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
    for i, driver in enumerate(cmds.poseInterpolator(node_name, q=1, d=1)):
        driverObject = driver
        driverTwistAxis = cmds.getAttr(f"{node_name}.driver[{i}].driverTwistAxis")
        driverEulerTwist = cmds.getAttr(f"{node_name}.driver[{i}].driverEulerTwist")
        driverController = cmds.listConnections(f"{node_name}.driver[{i}].driverController", p=1, d=0)
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
    for i in cmds.poseInterpolator(node_name, q=1, i=1):
        # pose
        poseName = pose_name_list[i]
        poseRotation_list = []
        poseTranslation_list = []
        # pose driver data
        for dr_i, dr_obj in enumerate(cmds.poseInterpolator(node_name, q=1, d=1)):
            poseRotation_list.append(cmds.getAttr(f"{node_name}.pose[{i}].poseRotation[{dr_i}]"))
            poseTranslation_list.append(cmds.getAttr(f"{node_name}.pose[{i}].poseTranslation[{dr_i}]"))
        # controls data
        ctl_data = []
        for ctl in cmds.ls(f"{node_name}.pose[{i}].poseControllerData[*]"):
            item_data = []
            for item in cmds.ls(f"{ctl}.poseControllerDataItem[*]"):
                item_name = cmds.getAttr(f"{item}.poseControllerDataItemName")
                item_type = cmds.getAttr(f"{item}.poseControllerDataItemType")
                item_value = cmds.getAttr(f"{item}.poseControllerDataItemValue")[0]
                if len(item_value) == 3:
                    item_value = {"x": item_value[0], "y": item_value[1], "z": item_value[2]}
                data = poseControllerDataItem(name=item_name,
                                              type=item_type,
                                              value=item_value)
                item_data.append(data)
            ctl_data.append(item_data)
        # pose attr
        poseType = cmds.getAttr(f"{node_name}.pose[{i}].poseType")
        isEnabled = cmds.getAttr(f"{node_name}.pose[{i}].isEnabled")
        poseFalloff = cmds.getAttr(f"{node_name}.pose[{i}].poseFalloff")
        isIndependent = cmds.getAttr(f"{node_name}.pose[{i}].isIndependent")
        poseRotationFalloff = cmds.getAttr(f"{node_name}.pose[{i}].poseRotationFalloff")
        poseTranslationFalloff = cmds.getAttr(f"{node_name}.pose[{i}].poseTranslationFalloff")
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
        pose_i.post_value()
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


def create_node_by_data(data: PoseInterpolatorData):
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
                    cmds.setAttr(f"{item_attr}.poseControllerDataItemValue", *item.value.values(), type="double3")
        # pose attr
        cmds.setAttr(f"{node_name}.pose[{i}].poseType", pose.poseType)
        cmds.setAttr(f"{node_name}.pose[{i}].isEnabled", pose.isEnabled)
        cmds.setAttr(f"{node_name}.pose[{i}].poseFalloff", pose.poseFalloff)
        cmds.setAttr(f"{node_name}.pose[{i}].isIndependent", pose.isIndependent)
        cmds.setAttr(f"{node_name}.pose[{i}].poseRotationFalloff", pose.poseRotationFalloff)
        cmds.setAttr(f"{node_name}.pose[{i}].poseTranslationFalloff", pose.poseTranslationFalloff)


def import_proxy_transform_data():
    """
    create proxy transform by data files
    """
    def create_proxy_transform(obj, parent, name):
        pxy_parent = cmds.createNode("transform", name=f"{name}_pxyParentTransform")
        pxy_obj = cmds.createNode("transform", name=f"{name}_pxyTransform", parent=pxy_parent)
        cmds.delete(cmds.parentConstraint(obj, pxy_parent))
        cmds.parentConstraint(parent, pxy_parent, mo=1)
        cmds.orientConstraint(obj, pxy_obj)
    path = cmds.fileDialog2(dialogStyle=2, caption="Load proxy transform data", fileFilter="YAML file(*.yaml)", fileMode=1)[0]
    with open(path, "r") as f:
        data = yaml.unsafe_load(f)
        for x in data:
            for i in x:
                create_proxy_transform(x[i]["Joint"], x[i]["Parent"], i)


def export_poseInterpolator_data(node=None):
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
        data_list.append(load_data_by_node(i))
    path = cmds.fileDialog2(dialogStyle=2, caption="Export poseInterpolator data", fileFilter="YAML file(*.yaml)")[0]
    with open(path, "w") as f:
        yaml.dump(data_list, f, sort_keys=False, indent=4, width=80)


def import_poseInterpolator_data():
    """
    import poseInterpolator node from files.
    """
    path = cmds.fileDialog2(dialogStyle=2, caption="Load poseInterpolator data", fileFilter="YAML file(*.yaml)", fileMode=1)[0]
    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)
        for data in data_list:
            create_node_by_data(data)


def add_bs_target(bs: str, name: str):
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
    return f"{bs}.{name}"


def create_bs_by_psd(bs: str, psd_node_list: list = None):
    """
    create blendShape target by poseInterpolator's pose output
    if psd_node_list is None, will be get poseInterpolator from selections list
    Args:
        bs (str): blendShape name
        psd_node_list (list): poseInterpolator node list
    """

    if psd_node_list is None:
        psd_node_list = cmds.ls(sl=1)

    out_attr_list = []
    pose_name_list = []
    for psd_node in psd_node_list:
        out_index = cmds.poseInterpolator(psd_node, q=1, i=1)
        out_attr_list += [f"{psd_node}.output[{i}]" for i in out_index]
        pose_name = cmds.poseInterpolator(psd_node, q=1, pn=1)
        prefix = psd_node.replace("_poseInterpolator", "")
        pose_name_list += [f"{prefix}_{n}" for n in pose_name]
    for i, x in enumerate(out_attr_list):
        attr = x
        name = pose_name_list[i]
        if "DefaultPose" in name:
            name = "__" + name.replace("DefaultPose", "_")
            bs_wAttr = add_bs_target(bs, name)
        else:
            bs_wAttr = add_bs_target(bs, name)
            cmds.setDrivenKeyframe(bs_wAttr, cd=attr, driverValue=0, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setDrivenKeyframe(bs_wAttr, cd=attr, driverValue=1, v=1, inTangentType="linear", outTangentType="linear")


@dataclass
class FingerTargetData(yaml.YAMLObject):
    yaml_tag = "FingerTargetData"
    TargetName: str
    DriverAttr: str = None
    DriverMin: float = 0
    DriverMax: float = 0


def create_finger_bs(bs):
    path = cmds.fileDialog2(dialogStyle=2, caption="Load finger blendShape data", fileFilter="YAML file(*.yaml)", fileMode=1)[0]
    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)
        for x in data_list:
            attr = add_bs_target(bs, x.TargetName)
            if x.DriverAttr:
                cmds.setDrivenKeyframe(attr, cd=x.DriverAttr,
                                       driverValue=x.DriverMin, v=0,
                                       inTangentType="linear", outTangentType="linear")
                cmds.setDrivenKeyframe(attr, cd=x.DriverAttr,
                                       driverValue=x.DriverMax, v=1,
                                       inTangentType="linear", outTangentType="linear")


# import_proxy_transform_data()
# export_poseInterpolator_data(cmds.ls(sl=1))
# import_poseInterpolator_data()
# create_bs_by_psd("blendShape1")
# create_finger_bs("blendShape1")
