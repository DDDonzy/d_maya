
import numpy as np
from maya.api import OpenMaya as om
from maya import cmds
from gameFace.bSpline import CurveData
from gameFace.fnSkin import D_FnSkin
from UTILS.autoChain import *


def calWeights(controls, degree=2):
    vtx_index, mesh = getSelectedVertexIndex()
    controlsPosition = om.MPointArray()
    for control in controls:
        control_position = om.MPoint(cmds.xform(control, q=1, t=1, ws=1))
        controlsPosition.append(control_position)

    if len(controls) < 2:
        raise RuntimeError("Please input two+ controls.")
    maxDegree = len(controls) - 1

    degree = clamp(degree, 1, maxDegree)

    d1, d2, lerpValue = lerp_degree(degree)
    d1 = clamp(d1, 1, maxDegree)
    d2 = clamp(d2, 1, maxDegree)
    cv1 = CurveData(controlsPosition, d1)
    cv2 = CurveData(controlsPosition, d2)

    weightList1 = []
    weightList2 = []
    fnMesh = om.MFnMesh(mesh)
    for i in vtx_index:
        vtx_position = fnMesh.getPoint(i, space=om.MSpace.kWorld)
        p, t1 = cv1.closestPoint(vtx_position)
        p, t2 = cv2.closestPoint(vtx_position)
        weightList1.extend(cv1.get_tWeights(t=t1))
        weightList2.extend(cv2.get_tWeights(t=t2))
    w1 = np.array(weightList1)
    w2 = np.array(weightList2)
    return list(w1 + lerpValue * (w2 - w1))


def set_calWeights(joints, skinCluster, weights):
    vtx_index, mesh = getSelectedVertexIndex()
    fnSkin = D_FnSkin(skinCluster)
    mSel = om.MSelectionList()
    infIndexList = om.MIntArray()
    for i, x in enumerate(joints):
        if not cmds.objExists(x):
            raise RuntimeError(f"Can not find '{x}'")
        mSel.add(x)
        infIndexList.append(fnSkin.indexForInfluenceObject(mSel.getDagPath(i)))

    fn_component = om.MFnSingleIndexedComponent()
    component_mObj = fn_component.create(om.MFn.kMeshVertComponent)
    fn_component.addElements(vtx_index)
    print(mesh,component_mObj,infIndexList)
    fnSkin.setWeights(mesh, component_mObj, infIndexList, om.MDoubleArray(weights), True, True)


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def lerp_degree(floatDegree, degreeList=[1, 2, 3, 5]):
    floatDegree = clamp(floatDegree, degreeList[0], degreeList[-1])
    d1 = 0
    d2 = 1
    for i, degree in enumerate(degreeList):
        if floatDegree >= degree:
            d1 = degreeList[i]
            d2 = degreeList[i+1]

    return d1, d2, (floatDegree-d1)/(d2-d1)


def sharpen_weights(arr, intensity):
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr, dtype=np.float64)
    max_val = arr.max() 
    weights = 1 / max_val * arr  
    weights[weights != 1] = 0  
    weights /= weights.sum()
    result = arr + intensity * (weights - arr)
    result /= result.sum()
    return result