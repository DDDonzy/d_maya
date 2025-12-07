
import numpy as np
from maya import cmds
from maya.api import OpenMaya as om

from mutils.bSpline import CurveData
from mutils.skin.fnSkin import D_FnSkin, weightsData


class CalWeights(D_FnSkin):
    def __init__(self, skinClusterName):
        super().__init__(skinClusterName)

        self.skinClusterName = skinClusterName
        self.all_inf_list = self.influenceObjects()
        self.all_inf_name = [x.partialPathName() for x in self.all_inf_list]

        try:
            orig_mPlug = om.MSelectionList().add(f"{skinClusterName}.originalGeometry[0]").getPlug(0)
            mesh_mObj = orig_mPlug.asMDataHandle().asMesh()
            self.orig_fnMesh = om.MFnMesh(mesh_mObj)
        except:
            raise RuntimeError("Get Orig mesh fail.")

        self.setInfluence(self.all_inf_name)
        self.setVertex([x for x in range(self.orig_fnMesh.numVertices)])

    def updateComponent(self, componentList=[]):
        if not componentList:
            pass

    def setInfluence(self, influenceList=[]):
        if not influenceList:
            influenceList = cmds.ls(sl=1) or self.all_inf_name

        self.inf_name = influenceList
        self.inf_pos = om.MPointArray()

        index_list = []
        noInSkinInfluence = []
        for name in influenceList:
            if name not in self.all_inf_name:
                noInSkinInfluence.append(name)
            if name in self.all_inf_name:
                index_list.append(self.all_inf_name.index(name))

        for x in index_list:
            mSel = om.MGlobal.getSelectionListByName(f"{self.skinClusterName}.bindPreMatrix[{x}]")
            mPlug: om.MPlug = mSel.getPlug(0)
            mDataHandle: om.MDataHandle = mPlug.asMDataHandle()
            fnMatrix = om.MFnMatrixData(mDataHandle.data())
            mTransformMatrix = om.MTransformationMatrix(fnMatrix.matrix().inverse())
            self.inf_pos.append(mTransformMatrix.translation(om.MSpace.kWorld))

    def setVertex(self, componentList=[]):

        if not componentList:
            try:
                componentList, _ = CalWeights.getSelectedVertexIndex()
            except:
                componentList = [x for x in range(self.orig_fnMesh.numVertices)]

        self.componentList = componentList

        component = om.MFnSingleIndexedComponent()
        self.component_mObj = component.create(om.MFn.kMeshVertComponent)
        component.addElements(componentList)

        self.vtx_pos = om.MPointArray()
        for x in self.componentList:
            self.vtx_pos.append(self.orig_fnMesh.getPoint(x))

    def calWeights(self, degree: int = 2, smooth: float = 0.3):

        w = calWeightsBase(inf_position=self.inf_pos,
                           vtx_position=self.vtx_pos,
                           smooth=smooth,
                           degree=degree)
        data = weightsData(mesh=self.shape.partialPathName(),
                           component=self.componentList,
                           influenceIndex=[],
                           influenceName=self.inf_name,
                           weights=w,
                           blendWeights=[0]*len(self.componentList))
        self.auto_setWeights(data)

    @staticmethod
    def getSelectedVertexIndex():
        selection_list = om.MGlobal.getActiveSelectionList()
        vertex_indices = []
        for i in range(selection_list.length()):
            mDag, component = selection_list.getComponent(i)
            if component.apiType() == om.MFn.kMeshVertComponent:
                fn_component = om.MFnSingleIndexedComponent(component)
                indices = fn_component.getElements()
                vertex_indices.extend(indices)

        return vertex_indices, mDag


def remap_value(value, in_min, in_max, out_min, out_max):
    in_range = in_max - in_min
    out_range = out_max - out_min

    return out_min + ((value - in_min) / in_range) * out_range


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def lerp(t, start, end):
    return start + t * (end - start)


def calWeightsBase(inf_position: om.MPointArray,
                   vtx_position: om.MPointArray,
                   smooth: float = 0.3,
                   degree: int = 2):
    inf_count = len(inf_position)

    if not isinstance(smooth, list):
        smooth = [smooth] * inf_count
    smooth = [remap_value(clamp(x, 0, 1), 0, 1, 0, 0.5) for x in smooth]
    degree = clamp(degree, 1, 5)

    if len(inf_position) < 2:
        raise RuntimeError("Please input two+ influence.")

    new_inf_position = []

    for i in range(inf_count):
        if i == 0:
            p1 = lerp(smooth[i], inf_position[i], inf_position[i+1])
            new_inf_position.extend([inf_position[i], p1])
            continue

        if i == inf_count-1:
            p1 = lerp(smooth[i], inf_position[i], inf_position[i-1])
            new_inf_position.extend([p1, inf_position[i]])
            continue

        p1 = lerp(smooth[i], inf_position[i], inf_position[i-1])
        p2 = lerp(smooth[i], inf_position[i], inf_position[i+1])
        new_inf_position.extend([p1, inf_position[i], p2])

    combine_list = [[0, 1]]
    for i in range(2, len(new_inf_position)-2, 3):
        combine_list.append([i, i+1, i+2])
    combine_list.append([len(new_inf_position)-2, len(new_inf_position)-1])

    # curve
    cv = CurveData(new_inf_position, degree)
    # cv.build()

    weightList = []
    for vtx in vtx_position:
        _, t = cv.closestPoint(vtx)
        weightList.extend(cv.get_tWeights(t))

    weightList_nAry = np.array(weightList).reshape(len(vtx_position), len(new_inf_position)).T
    combineWeight_nAry = np.zeros((len(inf_position), len(vtx_position)))
    for i, x in enumerate(combine_list):
        for ii in x:
            combineWeight_nAry[i] += weightList_nAry[ii]
    return combineWeight_nAry.T.reshape(-1)


def sharpen_weights(weights, intensity):
    if not isinstance(weights, np.ndarray):
        weights = np.array(weights, dtype=np.float64)
    max_val = weights.max()
    weights = 1 / max_val * weights
    weights[weights != 1] = 0
    weights /= weights.sum()
    result = weights + intensity * (weights - weights)
    result /= result.sum()
    return result


a = CalWeights("skinCluster3")
a.setVertex([95, 96, 97, 98, 99, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 125, 126, 127,
            128, 129, 225, 226, 227, 228, 229, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249])
a.setInfluence(['R_LipCornerPart_SK', 'M_LipUpperPart_SK', 'L_LipCornerPart_SK'])
a.calWeights(2, [0, 0.3, 0])
