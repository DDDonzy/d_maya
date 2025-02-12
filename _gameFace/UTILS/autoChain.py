import numpy as np
from maya import cmds
from maya.api import OpenMaya as om
from UTILS.other.attr import lockAttr
from UTILS.create.createBase import CreateBase
from UTILS.ui.showMessage import muteMessage


def get_neighbor_edgeVtx(mesh):
    mSel = om.MSelectionList()
    mSel.add(mesh)
    mDag = mSel.getDagPath(0)
    # fnMesh, iterMesh
    mIterMesh = om.MItMeshVertex(mDag)
    # neighbor, position
    vtx_neighbor = []
    # iter
    for x in range(mIterMesh.count()):
        mIterMesh.setIndex(x)
        connected_vtx = mIterMesh.getConnectedVertices()
        vtx_neighbor.append(connected_vtx)
    return vtx_neighbor


def get_neighbor_faceVtx(mesh):
    mSel = om.MSelectionList()
    mSel.add(mesh)
    mDag = mSel.getDagPath(0)

    mIterMesh = om.MItMeshVertex(mDag)
    mIterFace = om.MItMeshPolygon(mDag)

    face_vertices = []
    while not mIterFace.isDone():
        face_vertices.append(mIterFace.getVertices())
        mIterFace.next()

    vtx_neighbor = []
    while not mIterMesh.isDone():
        connected_faces = mIterMesh.getConnectedFaces()
        this_vertex = set()
        for face_index in connected_faces:
            this_vertex.update(face_vertices[face_index])
        vtx_neighbor.append(this_vertex)
        mIterMesh.next()

    return vtx_neighbor


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


def selectVertexByIndex(mesh, indexList):
    mDag = om.MSelectionList().add(mesh).getDagPath(0)

    fn_component = om.MFnSingleIndexedComponent()
    component_mObj = fn_component.create(om.MFn.kMeshVertComponent)
    fn_component.addElements(indexList)

    selection_list = om.MSelectionList()
    selection_list.add((mDag, component_mObj))
    om.MGlobal.setActiveSelectionList(selection_list)


def getGrowVtxGroup(mesh, step=1):
    vtx_neighbor = get_neighbor_faceVtx(mesh)
    vtxIndex_list = getSelectedVertexIndex()

    filter_list = set(vtxIndex_list)

    step_list = [vtxIndex_list]
    step_temp = []

    iter_l = vtxIndex_list
    iter_num = 0
    while iter_l:
        iter_num += 1
        add = set()
        # iter
        for x in iter_l:
            new_neighbors = set(vtx_neighbor[x]) - filter_list
            add.update(new_neighbors)
        filter_list.update(add)
        step_temp.extend(add)
        # step
        if iter_num % step == 0:
            if step_temp:
                step_list.append(step_temp)
            step_temp = []
        # update iter
        iter_l = add
    if step_temp:
        step_list.append(step_temp)

    return step_list


def calCenterPosition(vtxGroup, mesh):
    mDag = om.MSelectionList().add(mesh).getDagPath(0)
    fnMesh = om.MFnMesh(mDag)
    position = fnMesh.getPoints(om.MSpace.kWorld)
    position = np.array(position)

    center_list = []
    for v_list in vtxGroup:
        points = np.array(position[v_list])[:, :-1]
        center_list.append(np.mean(points, axis=0))
    return center_list


class chainFit(CreateBase):
    isBlackBox = False

    def __init__(self, *args, **kwargs):

        self.step = kwargs.get("step") or kwargs.get("stp") or 1
        selVtx = getSelectedVertexIndex()
        if not selVtx:
            raise RuntimeError("Please select vertex.")

        selection_list = om.MGlobal.getActiveSelectionList()
        self.mesh, component = selection_list.getComponent(0)
        self.name = f"{self.mesh}"
        kwargs.update({"name": self.name})

        super().__init__(*args, **kwargs)

    def create(self):
        cvTransform, cvShape = self.buildCurve()

    def _post_create(self):
        muteMessage(True)
        lockAttr(self.thisAssetName.name)
        muteMessage(False)

    def buildCurve(self):
        cvPosition = calCenterPosition(getGrowVtxGroup(self.mesh, step=self.step), self.mesh)
        cvTransform = cmds.curve(d=1, ep=cvPosition, name=self.createName("curve"))
        cvShape = cmds.rename(cmds.listRelatives(cvTransform, s=1)[0], f"{cvTransform}Shape")
        cvRebuild = cmds.createNode("rebuildCurve", name=self.createName("rebuildCurve"))

        typedAttr = om.MFnTypedAttribute()

        baseCurveAttr = typedAttr.create("origCurve", "bc", om.MFnData.kNurbsCurve)
        mObj_cvRebuild = om.MSelectionList().add(cvRebuild).getDependNode(0)
        mDep_cvRebuild = om.MFnDependencyNode(mObj_cvRebuild)
        mDep_cvRebuild.addAttribute(baseCurveAttr)
        origPlug = mDep_cvRebuild.findPlug("origCurve", True)

        origPlug_base = om.MSelectionList().add(f"{cvShape}.local").getPlug(0)
        mDataHandle = origPlug_base.asMDataHandle()
        origPlug.setMDataHandle(mDataHandle)

        cmds.setAttr(f"{cvRebuild}.keepRange", 0)
        cmds.setAttr(f"{cvShape}.dispCV", 1)
        cmds.setAttr(f"{cvShape}.lineWidth", 3)
        cmds.setAttr(f"{cvShape}.overrideColor", 10)
        cmds.setAttr(f"{cvShape}.overrideEnabled", 1)
        cmds.setAttr(f"{cvShape}.alwaysDrawOnTop", 1)
        cmds.addAttr(cvTransform, ln="spans", proxy=f"{cvRebuild}.spans", k=1)
        cmds.addAttr(cvTransform, ln="degree", proxy=f"{cvRebuild}.degree", k=1)
        cmds.addAttr(cvTransform, ln="smooth", proxy=f"{cvRebuild}.smooth", k=1)
        cmds.setAttr(f"{cvRebuild}.spans", cmds.getAttr(f"{cvShape}.spans"))

        cmds.connectAttr(f"{cvRebuild}.origCurve", f"{cvRebuild}.inputCurve")
        cmds.connectAttr(f"{cvRebuild}.outputCurve", f"{cvShape}.create")
        self.publishNode([cvTransform, cvShape])
        lockAttr(cvTransform)
        return cvTransform, cvShape

    def buildJoints(num: int = 3):
        for x in range(3):
            pass
