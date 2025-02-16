from UTILS.apiundo import commit
from UTILS.getHistory import get_history

from collections import defaultdict
from functools import partial

import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def unite(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                if self.rank[root_x] == self.rank[root_y]:
                    self.rank[root_x] += 1


def get_mesh_components(mesh: str):
    mesh_mDag = om.MSelectionList().add(mesh).getDagPath(0)
    mesh = om.MFnMesh(mesh_mDag)
    num_faces = mesh.numPolygons
    if num_faces == 0:
        return {}

    uf = UnionFind(num_faces)

    edge_iter = om.MItMeshEdge(mesh.object())
    while not edge_iter.isDone():
        connected_faces = edge_iter.getConnectedFaces()
        if len(connected_faces) >= 2:
            first_face = connected_faces[0]
            for face in connected_faces[1:]:
                uf.unite(first_face, face)
        edge_iter.next()

    component_dict = defaultdict(set)
    face_iter = om.MItMeshPolygon(mesh.object())
    while not face_iter.isDone():
        face_index = face_iter.index()
        component_id = uf.find(face_index)
        vertex_indices = face_iter.getVertices()
        component_dict[component_id].update(vertex_indices)
        face_iter.next()

    result = {}
    for idx, (_, indices) in enumerate(component_dict.items()):
        result[idx] = sorted(indices)
    return result


def get_origMesh(mesh):
    shapes = cmds.listRelatives(mesh, s=1) or []
    orig = []
    if shapes:
        for s in shapes:
            if cmds.getAttr(f"{s}.intermediateObject"):
                orig.append(s)
    return orig


def get_bsComponentsList(componentAttrName):
    """"get component list from
        blendShape1.it[0].itg[0].iti[6000].inputComponentsTarget
    """
    compList_mPlug = om.MSelectionList().add(componentAttrName).getPlug(0)
    compList_mObj = om.MFnComponentListData(compList_mPlug.asMObject()).get(0)

    bs_fnDep = om.MFnDependencyNode(compList_mPlug.node())
    orig_mPlug = bs_fnDep.findPlug("originalGeometry", False)
    orig_mDataHandle = orig_mPlug.elementByLogicalIndex(0).asMDataHandle()

    compList = []
    iter = om.MItGeometry(orig_mDataHandle, compList_mObj)
    while not iter.isDone():
        compList.append(iter.index())
        iter.next()
    return compList


def scaleUvPin(uvPin, scale, componentCenterPointIndex=0, scaleBlendShape=False):

    bs_list = get_history(uvPin, "blendShape")
    orig = (get_origMesh(uvPin) or [uvPin])

    for mesh in orig:
        mDag = om.MSelectionList().add(mesh).getDagPath(0)
        components = get_mesh_components(mesh=mesh)
        fnMesh = om.MFnMesh(mDag)
        base_points = fnMesh.getPoints(om.MSpace.kWorld)
        new_points = om.MPointArray(base_points)
        for component_id in components:
            center_point_index = components[component_id][componentCenterPointIndex]
            center_point = om.MVector(fnMesh.getPoint(center_point_index, om.MSpace.kWorld))
            for vertex_index in components[component_id]:
                point = om.MVector(fnMesh.getPoint(vertex_index, om.MSpace.kWorld))
                scaled_point = (point - center_point) * scale + center_point
                new_points[vertex_index] = om.MPoint(scaled_point)

        _doit = partial(fnMesh.setPoints, new_points, om.MSpace.kWorld)
        _undo = partial(fnMesh.setPoints, base_points, om.MSpace.kWorld)
        _doit()
        commit(undo=_undo, redo=_doit)

    if not scaleBlendShape:
        return

    for bs in bs_list:
        target_list = cmds.getAttr(f"{bs}.w", mi=True)
        for target in target_list:
            item_list = cmds.getAttr(f"{bs}.it[0].itg[{target}].iti", mi=True)
            for item in item_list:
                bs_target_points = cmds.getAttr(f"{bs}.it[0].itg[{target}].iti[{item}].ipt")
                bs_compList = get_bsComponentsList(f"{bs}.it[0].itg[{target}].iti[{item}].ict")
                for component_id in components:
                    center_point_index = components[component_id][componentCenterPointIndex]
                    if center_point_index in bs_compList:
                        center_point = om.MVector(om.MPoint(bs_target_points[bs_compList.index(center_point_index)]))
                    else:
                        center_point = om.MVector()
                    for vertex_index in components[component_id]:
                        if vertex_index in bs_compList:
                            i = bs_compList.index(vertex_index)
                            point = om.MVector(om.MPoint(bs_target_points[i]))
                            scaled_point = (point - center_point) * scale + center_point
                            bs_target_points[i] = om.MPoint(scaled_point)
                    cmds.setAttr(f"{bs}.it[0].itg[{target}].iti[{item}].ipt", len(bs_target_points), *bs_target_points, type="pointArray")


def normalizedUvPinWeights(uvPinMesh: str, componentNumVertices: int = 5, componentCenterPointIndex: int = 0):
    skinCluster = get_history(uvPinMesh, "skinCluster")[0]
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
        ref_i = componentCenterPointIndex * numInf + i
        weight[i: i+numInf*componentNumVertices] = weight[ref_i:ref_i+numInf] * componentNumVertices

    _doit = partial(fnSkin.setWeights, uvPinMesh_mDag, vertexComp, om.MIntArray(list(range(numInf))), om.MDoubleArray(weight))
    _undo = partial(fnSkin.setWeights, uvPinMesh_mDag, vertexComp, om.MIntArray(list(range(numInf))), weight_base)

    _doit()
    commit(_undo, _doit)


if __name__ == "__main__":
    mesh = "xc_gd:Jianjia_Uvpin"
    # normalizedUvPinWeights(mesh, 5, 1)
    


for x in cmds.ls(type="uvPin"):
    mesh = cmds.listConnections(x+".deformedGeometry", s=1)[0]
    scaleUvPin(mesh, 100, 4)