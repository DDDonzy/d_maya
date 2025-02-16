import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
from UTILS.apiundo import commit
from functools import partial


def normalizedUvPinWeights(uvPinMesh: str, skinCluster: str, componentNumVertices: int = 5, referenceComponentIndex: int = 0):
    mSel = om.MSelectionList()
    mSel.add(uvPinMesh)
    mSel.add(skinCluster)
    uvPinMesh_mDag = mSel.getDagPath(0)
    skin_mObj = mSel.getDependNode(1)
    fnSkin = oma.MFnSkinCluster(skin_mObj)
    singleIdComp = om.MFnSingleIndexedComponent()
    vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)
    weight_base, numInf = fnSkin.getWeights(uvPinMesh_mDag, vertexComp)
    weight = list(weight_base)
    numVertices = int(len(weight)/numInf)
    for i in range(0, len(weight), numVertices):
        weight[i: i+numInf*componentNumVertices] = weight[i:i+numInf] * componentNumVertices

    _doit = partial(fnSkin.setWeights, uvPinMesh_mDag, vertexComp, om.MIntArray(list(range(numInf))), om.MDoubleArray(weight))
    _undo = partial(fnSkin.setWeights, uvPinMesh_mDag, vertexComp, om.MIntArray(list(range(numInf))), weight_base)

    _doit()
    commit(_undo, _doit)


normalizedUvPinWeights("pPlane1", "skinCluster1")
