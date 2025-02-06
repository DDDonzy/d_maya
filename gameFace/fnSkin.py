import yaml

from .getHistory import get_history
from .choseFile import choseFile

from UTILS.ui.showMessage import showMessage

from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oma
from maya import cmds


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
        self.component = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
        self.shape = cmds.skinCluster(self.skinDep.name(), q=1, g=1)[0]
        self.shape = om.MSelectionList().add(self.shape).getDagPath(0)

        super().__init__(mObj)

    def auto_getWeights(self, indexList=None):
        infList = self.influenceObjects()
        infCount = len(infList)
        if not isinstance(indexList, list):
            indexList = om.MIntArray(range(infCount))
        else:
            indexList = om.MIntArray(indexList)

        weightData = list(self.getWeights(self.shape, self.component, indexList))
        blendWeightData = list(self.getBlendWeights(self.shape, self.component))
        infDict = {}
        for x in indexList:
            name = infList[x].partialPathName()
            infDict.update({x: name})
        weightDict = {"meshShape": self.shape.partialPathName(),
                      "influence": infDict,
                      "weights": weightData,
                      "blendWeight": blendWeightData}
        return weightDict

    def auto_setWeights(self, weightDict):
        indexList = om.MIntArray(list(weightDict["influence"].keys()))
        self.setWeights(self.shape, self.component, indexList, om.MDoubleArray(weightDict["weights"]), True)
        self.setBlendWeights(self.shape, self.component, om.MDoubleArray(weightDict["blendWeight"]))


def exportWeights(obj=None, path=None, indexList=None):
    if not obj:
        obj = cmds.ls(sl=1)[0]

    path = choseFile(path, dialogStyle=2, caption="Export weights", fileFilter="Weight YAML file(*.yaml)")
    if not path:
        return

    fnSkin = D_FnSkin(obj)
    weights = fnSkin.auto_getWeights(indexList)

    with open(path, "w") as f:
        yaml.dump(weights, f, sort_keys=False, indent=4, width=80)

    showMessage("Export weights.")


def importWeights(obj=None, path=None, indexList=None):
    if not obj:
        obj = cmds.ls(sl=1)[0]
    if not cmds.objExists(obj):
        raise RuntimeError(f"Can not find '{obj}'.")

    path = choseFile(path, dialogStyle=2, caption="Import weights", fileFilter="Weight YAML file(*.yaml)", fileMode=1)
    if not path:
        return

    with open(path, "r") as f:
        data = yaml.unsafe_load(f)

    for k, v in data["influence"].items():
        if not cmds.objExists(v):
            raise RuntimeError(f"Can not find '{v}'.")

    try:
        obj = cmds.skinCluster(list(data["influence"].values()), obj, tsb=1, rui=0, name=f"{obj}_skinCluster")[0]
    except:
        pass

    fnSkin = D_FnSkin(obj)
    fnSkin.auto_setWeights(data)

    showMessage("Import weights.")
