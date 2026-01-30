from dataclasses import dataclass
import yaml

from maya import cmds
from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oma

import log

from m_utils.dag.getHistory import get_history
from m_utils.other.choseFile import choseFile


@dataclass
class WeightsData(yaml.YAMLObject):
    yaml_tag = "WeightsData"

    mesh: str
    component: list
    influenceIndex: list
    influenceName: list
    weights: list
    blendWeights: list


class D_FnSkin(oma.MFnSkinCluster):
    def __init__(self, obj):
        if not cmds.objExists(obj):
            raise RuntimeError(f"Can not find '{obj}'.")

        mObj = om.MSelectionList().add(obj).getDependNode(0)

        if mObj.hasFn(om.MFn.kDagNode):
            skinNode = (get_history(obj, "skinCluster") or [None])[0]
            if not skinNode:
                raise RuntimeError(f"Can not find {obj}'s skinCluster.")
            mObj = om.MSelectionList().add(skinNode).getDependNode(0)

        if mObj.apiType() != om.MFn.kSkinClusterFilter:
            raise RuntimeError(f"'{obj}' is not skinCluster.")

        self.skinDep = om.MFnDependencyNode(mObj)
        self.shape = cmds.skinCluster(self.skinDep.name(), q=1, g=1)[0]
        self.shape = om.MSelectionList().add(self.shape).getDagPath(0)

        super().__init__(mObj)

    def auto_getWeights(self, **kwargs):
        inf_list = self.influenceObjects()

        # component
        component_list = kwargs.get("component", [])
        if not isinstance(component_list, list):
            raise RuntimeError("Input 'component' is not list")
        component = om.MFnSingleIndexedComponent()
        component_mObj = component.create(om.MFn.kMeshVertComponent)
        component.addElements(component_list)

        # influenceIndex
        influenceIndex = kwargs.get("influenceIndex", [])
        if not isinstance(influenceIndex, list):
            raise RuntimeError("Input 'influenceIndex' is not list")
        if not influenceIndex:
            influenceIndex = [i for i in range(len(inf_list))]

        # influenceName
        influenceName = []
        for x in influenceIndex:
            influenceName.append(inf_list[x].partialPathName())

        # get weights
        weight = list(self.getWeights(self.shape, component_mObj, om.MIntArray(influenceIndex)))
        blendWeight = list(self.getBlendWeights(self.shape, component_mObj))

        # data
        data = WeightsData(mesh=self.shape.partialPathName(), component=component_list, influenceIndex=influenceIndex, influenceName=influenceName, weights=weight, blendWeights=blendWeight)
        return data

    def auto_setWeights(self, weightData: WeightsData):
        # influence name and index
        index_list = []
        noInSkinInfluence = []

        inf_list = self.influenceObjects()
        inf_name = [x.partialPathName() for x in inf_list]

        for name in weightData.influenceName:
            if name not in inf_name:
                noInSkinInfluence.append(name)
            if name in inf_name:
                index_list.append(inf_name.index(name))

        if noInSkinInfluence:
            raise RuntimeError(f"'{noInSkinInfluence}' not in skinCluster.")
        # component
        component = om.MFnSingleIndexedComponent()
        component_mObj = component.create(om.MFn.kMeshVertComponent)
        component.addElements(weightData.component)

        self.setWeights(self.shape, component_mObj, om.MIntArray(index_list), om.MDoubleArray(weightData.weights), True, False)
        if weightData.blendWeights:
            self.setBlendWeights(self.shape, component_mObj, om.MDoubleArray(weightData.blendWeights))


def exportWeights(obj=None, path=None, **kwargs):
    if not obj:
        obj = cmds.ls(sl=1)[0]

    path = choseFile(path, dialogStyle=2, caption="Export weights", fileFilter="Weight YAML file(*.yaml)")
    if not path:
        return
    fnSkin = D_FnSkin(obj)
    weights = fnSkin.auto_getWeights(**kwargs)

    with open(path, "w") as f:
        yaml.dump(weights, f, sort_keys=False, indent=4, width=80)

    log.success("Export weights.")


def importWeights(obj=None, path=None, data=None):
    if not obj:
        obj = cmds.ls(sl=1)[0]
    if not cmds.objExists(obj):
        raise RuntimeError(f"Can not find '{obj}'.")

    if not data:
        path = choseFile(path, dialogStyle=2, caption="Import weights", fileFilter="Weight YAML file(*.yaml)", fileMode=1)
        if not path:
            return

        with open(path, "r") as f:
            data = yaml.unsafe_load(f)

    noFindJoint = []
    for x in data.influenceName:
        if not cmds.objExists(x):
            noFindJoint.append(x)
    if noFindJoint:
        raise RuntimeError(f"Can not find '{noFindJoint}'.")

    try:
        obj = cmds.skinCluster(data.influenceName, obj, tsb=1, rui=0, name=f"{obj}_skinCluster")[0]
    except Exception:
        print("SkinCluster already exists, skip create new one.")

    fnSkin = D_FnSkin(obj)
    fnSkin.auto_setWeights(data)

    log.success("Import weights.")
