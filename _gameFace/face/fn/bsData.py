from maya import cmds
from maya.api import OpenMaya as om
import yaml


class PoseControllerDataItem(yaml.YAMLObject):
    yaml_tag = 'ControlData'
    
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type


class DriverData(yaml.YAMLObject):
    yaml_tag = 'DriverData'

    def __init__(self, driverObject, driverTwistAxis, driverEulerTwist, driverController):
        self.driverObject = driverObject
        self.driverTwistAxis = driverTwistAxis
        self.driverEulerTwist = driverEulerTwist
        self.driverController = driverController


class PoseData(yaml.YAMLObject):
    yaml_tag = 'PoseData'

    def __init__(self, poseName, poseType, controllerData, isEnabled, poseFalloff,
                 isIndependent, poseRotationFalloff, poseTranslationFalloff, 
                 poseRotation, poseTranslation):
        self.poseName = poseName
        self.poseType = poseType
        self.controllerData = controllerData
        self.isEnabled = isEnabled
        self.poseFalloff = poseFalloff
        self.isIndependent = isIndependent
        self.poseRotationFalloff = poseRotationFalloff
        self.poseTranslationFalloff = poseTranslationFalloff
        self.poseRotation = poseRotation
        self.poseTranslation = poseTranslation
        self.postValueChange()

    def postValueChange(self):
        if self.poseFalloff < 0.001:
            self.poseFalloff = 0.001
        if self.poseRotationFalloff < 0.001:
            self.poseRotationFalloff = 0.001
        if self.poseTranslationFalloff < 0.001:
            self.poseTranslationFalloff = 0.001


class PoseInterpolatorData(yaml.YAMLObject):
    yaml_tag = 'PoseInterpolatorData'

    def __init__(self, name, driver, pose, regularization, outputSmoothing,
                 interpolation, allowNegativeWeights, enableRotation, enableTranslation):
        self.name = name
        self.driver = driver
        self.pose = pose
        self.regularization = regularization
        self.outputSmoothing = outputSmoothing
        self.interpolation = interpolation
        self.allowNegativeWeights = allowNegativeWeights
        self.enableRotation = enableRotation
        self.enableTranslation = enableTranslation


def load_dataByNode(node_name):
    controls_obj_list = []
    # get interpolator data
    regularization = cmds.getAttr("{0}.regularization".format(node_name))
    outputSmoothing = cmds.getAttr("{0}.outputSmoothing".format(node_name))
    interpolation = cmds.getAttr("{0}.interpolation".format(node_name))
    allowNegativeWeights = cmds.getAttr("{0}.allowNegativeWeights".format(node_name))
    enableRotation = cmds.getAttr("{0}.enableRotation".format(node_name))
    enableTranslation = cmds.getAttr("{0}.enableTranslation".format(node_name))
    
    # get driver data
    driver_data = []
    for i, driver in enumerate(cmds.poseInterpolator(node_name, q=1, d=1)):
        driverObject = driver
        driverTwistAxis = cmds.getAttr("{0}.driver[{1}].driverTwistAxis".format(node_name, i))
        driverEulerTwist = cmds.getAttr("{0}.driver[{1}].driverEulerTwist".format(node_name, i))
        driverController = cmds.listConnections("{0}.driver[{1}].driverController".format(node_name, i), p=1, d=0)
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
            poseRotation_list.append(cmds.getAttr("{0}.pose[{1}].poseRotation[{2}]".format(node_name, i, dr_i)))
            poseTranslation_list.append(cmds.getAttr("{0}.pose[{1}].poseTranslation[{2}]".format(node_name, i, dr_i)))
        # controls data
        ctl_data = []
        for ctl in cmds.ls("{0}.pose[{1}].poseControllerData[*]".format(node_name, i)):
            item_data = []
            for item in cmds.ls("{0}.poseControllerDataItem[*]".format(ctl)):
                item_name = cmds.getAttr("{0}.poseControllerDataItemName".format(item))
                item_type = cmds.getAttr("{0}.poseControllerDataItemType".format(item))
                item_value = cmds.getAttr("{0}.poseControllerDataItemValue".format(item))[0]
                if len(item_value) == 3:
                    item_value = {"x": item_value[0], "y": item_value[1], "z": item_value[2]}
                data = PoseControllerDataItem(name=item_name,
                                              type=item_type,
                                              value=item_value)
                item_data.append(data)
            ctl_data.append(item_data)
        # pose attr
        poseType = cmds.getAttr("{0}.pose[{1}].poseType".format(node_name, i))
        isEnabled = cmds.getAttr("{0}.pose[{1}].isEnabled".format(node_name, i))
        poseFalloff = cmds.getAttr("{0}.pose[{1}].poseFalloff".format(node_name, i))
        isIndependent = cmds.getAttr("{0}.pose[{1}].isIndependent".format(node_name, i))
        poseRotationFalloff = cmds.getAttr("{0}.pose[{1}].poseRotationFalloff".format(node_name, i))
        poseTranslationFalloff = cmds.getAttr("{0}.pose[{1}].poseTranslationFalloff".format(node_name, i))
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


def create_nodeByData(data):
    controls_obj_list = []

    # set driver data
    driver_obj_list = [x.driverObject for x in data.driver]
    node_name = cmds.poseInterpolator(driver_obj_list, d=1, name=data.name)[0]
    for i, x in enumerate(data.driver):
        cmds.setAttr("{0}.driver[{1}].driverTwistAxis".format(node_name, i), x.driverTwistAxis)
        cmds.setAttr("{0}.driver[{1}].driverEulerTwist".format(node_name, i), x.driverEulerTwist)
        for c_i, c in enumerate(x.driverController):
            cmds.connectAttr(c, "{0}.driver[{1}].driverController[{2}]".format(node_name, i, c_i))
            control_object = c.split(".")[0]
            if control_object not in controls_obj_list:
                controls_obj_list.append(control_object)

    # set interpolator data
    cmds.setAttr("{0}.regularization".format(node_name), data.regularization)
    cmds.setAttr("{0}.outputSmoothing".format(node_name), data.outputSmoothing)
    cmds.setAttr("{0}.interpolation".format(node_name), data.interpolation)
    cmds.setAttr("{0}.allowNegativeWeights".format(node_name), data.allowNegativeWeights)
    cmds.setAttr("{0}.enableRotation".format(node_name), data.enableRotation)
    cmds.setAttr("{0}.enableTranslation".format(node_name), data.enableTranslation)

    # add pose
    for i, pose in enumerate(data.pose):
        cmds.poseInterpolator(node_name, e=1, ap=pose.poseName)
        # pose driver data
        for dr_i, dr_obj in enumerate(cmds.poseInterpolator(node_name, q=1, d=1)):
            cmds.setAttr("{0}.pose[{1}].poseRotation[{2}]".format(node_name, i, dr_i), pose.poseRotation[dr_i], type="doubleArray")
            cmds.setAttr("{0}.pose[{1}].poseTranslation[{2}]".format(node_name, i, dr_i), pose.poseTranslation[dr_i], type="doubleArray")

        # pose controller data
        pose_attr = "{0}.pose[{1}]".format(node_name, i)  # psd.pose[*]
        if pose.controllerData:
            for c_i, ctl in enumerate(pose.controllerData):
                ctl_attr = "{0}.poseControllerData[{1}]".format(pose_attr, c_i)
                for i_i, item in enumerate(ctl):
                    item_attr = "{0}.poseControllerDataItem[{1}]".format(ctl_attr, i_i)
                    cmds.setAttr("{0}.poseControllerDataItemName".format(item_attr), item.name, type='string')
                    cmds.setAttr("{0}.poseControllerDataItemType".format(item_attr), item.type)
                    cmds.setAttr("{0}.poseControllerDataItemValue".format(item_attr), *item.value.values(), type="double3")
        # pose attr
        cmds.setAttr("{0}.pose[{1}].poseType".format(node_name, i), pose.poseType)
        cmds.setAttr("{0}.pose[{1}].isEnabled".format(node_name, i), pose.isEnabled)
        cmds.setAttr("{0}.pose[{1}].poseFalloff".format(node_name, i), pose.poseFalloff)
        cmds.setAttr("{0}.pose[{1}].isIndependent".format(node_name, i), pose.isIndependent)
        cmds.setAttr("{0}.pose[{1}].poseRotationFalloff".format(node_name, i), pose.poseRotationFalloff)
        cmds.setAttr("{0}.pose[{1}].poseTranslationFalloff".format(node_name, i), pose.poseTranslationFalloff)


def import_proxyTransformData():
    """
    create proxy transform by data files
    """
    def create_proxyTransform(obj, parent, name):
        pxy_parent = cmds.createNode("transform", name="{0}_pxyParentTransform".format(name))
        pxy_obj = cmds.createNode("transform", name="{0}_pxyTransform".format(name), parent=pxy_parent)
        cmds.delete(cmds.parentConstraint(obj, pxy_parent))
        cmds.parentConstraint(parent, pxy_parent, mo=1)
        cmds.orientConstraint(obj, pxy_obj)
    path = cmds.fileDialog2(dialogStyle=2, caption="Load proxy transform data", fileFilter="YAML file(*.yaml)", fileMode=1)
    if not path:
        return
    path = path[0]
    with open(path, "r") as f:
        data = yaml.load(f)
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
        yaml.dump(data_list, f, indent=4, width=80)


def import_poseInterpolatorData():
    """
    import poseInterpolator node from files.
    """
    path = cmds.fileDialog2(dialogStyle=2, caption="Load poseInterpolator data", fileFilter="YAML file(*.yaml)", fileMode=1)
    if not path:
        return
    path = path[0]
    with open(path, "r") as f:
        data_list = yaml.load(f)
        for data in data_list:
            create_nodeByData(data)


def add_bsTarget(bs, name):
    """ add blendShape target
    Args:
        bs (str): blendShape name
        name (str): target name
    Returns:
        target_name (str): blendShape.w[*]
    """
    w_mi = cmds.getAttr("{0}.w".format(bs), mi=1)
    i = w_mi[-1]+1 if w_mi else 0
    cmds.setAttr("{0}.w[{1}]".format(bs, i), 0)
    if cmds.objExists("{0}.{1}".format(bs, name)):
        num = 0
        base_name = name
        while cmds.objExists("{0}.{1}".format(bs, name)):
            num += 1
            name = "{0}{1}".format(base_name, num)
    cmds.aliasAttr(name, "{0}.w[{1}]".format(bs, i))
    cmds.setAttr("{0}.it[0].itg[{1}].iti[6000].ipt".format(bs, i), *[1, (0, 0, 0, 1)], type="pointArray")
    cmds.setAttr("{0}.it[0].itg[{1}].iti[6000].ict".format(bs, i), *[1, "vtx[0]"], type="componentList")
    return "{0}.{1}".format(bs, name)

def del_bsTargetData(bs, index):
    """ del blendShape target data
    Args:
        bs (str): blendShape name
        index (str): target index
    """
    cmds.setAttr("{0}.it[0].itg[{1}].iti[6000].ipt".format(bs, index), *[1, (0, 0, 0, 1)], type="pointArray")
    cmds.setAttr("{0}.it[0].itg[{1}].iti[6000].ict".format(bs, index), *[1, "vtx[0]"], type="componentList")
    


def create_bsByPSD(bs, psd_node_list=None):
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
        out_attr_list += ["{0}.output[{1}]".format(psd_node, i) for i in out_index]
        pose_name = cmds.poseInterpolator(psd_node, q=1, pn=1)
        prefix = psd_node.replace("_poseInterpolator", "")
        pose_name_list += ["{0}_{1}".format(prefix, n) for n in pose_name]
    for i, x in enumerate(out_attr_list):
        attr = x
        name = pose_name_list[i]
        if "DefaultPose" in name:
            name = "__" + name.replace("DefaultPose", "_")
        if cmds.objExists("{0}.{1}".format(bs, name)):
            cmds.setDrivenKeyframe("{0}.{1}".format(bs, name), cd=attr, driverValue=0, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setDrivenKeyframe("{0}.{1}".format(bs, name), cd=attr, driverValue=1, v=1, inTangentType="linear", outTangentType="linear")
            continue
        bs_wAttr = add_bsTarget(bs, name)
        cmds.setDrivenKeyframe(bs_wAttr, cd=attr, driverValue=0, v=0, inTangentType="linear", outTangentType="linear")
        cmds.setDrivenKeyframe(bs_wAttr, cd=attr, driverValue=1, v=1, inTangentType="linear", outTangentType="linear")


class FingerTargetData(yaml.YAMLObject):
    yaml_tag = "FingerTargetData"
    
    def __init__(self, TargetName, DriverAttr=None, DriverMin=0, DriverMax=0):
        self.TargetName = TargetName
        self.DriverAttr = DriverAttr
        self.DriverMin = DriverMin 
        self.DriverMax = DriverMax


def create_fingerTarget(bs):
    path = cmds.fileDialog2(dialogStyle=2, caption="Load finger blendShape data", fileFilter="YAML file(*.yaml)", fileMode=1)
    if not path:
        return
    path = path[0]
    with open(path, "r") as f:
        data_list = yaml.load(f)
        for x in data_list:
            attr = add_bsTarget(bs, x.TargetName)
            if x.DriverAttr:
                cmds.setDrivenKeyframe(attr, cd=x.DriverAttr,
                                       driverValue=x.DriverMin, v=0,
                                       inTangentType="linear", outTangentType="linear")
                cmds.setDrivenKeyframe(attr, cd=x.DriverAttr,
                                       driverValue=x.DriverMax, v=1,
                                       inTangentType="linear", outTangentType="linear")
