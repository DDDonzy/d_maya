from m_utils.compounds.decomMatrix import decomMatrix
from m_utils.compounds.matrixConstraint import matrixConstraint
from m_utils.transform import *


import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

from m_utils.create.createBase import CreateBase, CreateNode
from m_utils.create.generateUniqueName import generateUniqueName

import json


class uvPin(CreateBase):
    """Create uvPin constraint"""

    isBlackBox = False

    def __init__(self, *args, **kwargs):
        """
        Args:
        *args: Variable length argument list.
            args[0] (list): List of target objects if not provided in kwargs.
        **kwargs: Arbitrary keyword arguments.
            targetList (list): List of target objects. Default is the current selection.
            size (float): Size of the UV pin. Default is 0.1.
            name (str): Name of the UV pin. Default is 'uvPin'.
        """

        self.targetList = kwargs.get("targetList") or kwargs.get("tl") or args[0] if args else cmds.ls(sl=1)
        self.size = kwargs.get("size") or kwargs.get("s") or 0.1
        self.name = kwargs.get("name") or kwargs.get("n") or "uvPin"

        if not isinstance(self.targetList, list):
            self.targetList = [self.targetList]
        if not self.targetList:
            raise ValueError("No object need to create uvPin, please input object list. or select some object.")

        super().__init__(*args, **kwargs)

    def create(self):
        # create mesh
        self.mesh, self.meshShape = uvPin.create_planeByObjectList(targetList=self.targetList, size=self.size, name=f"{self.name}_uvPinMesh")
        # create uvPin node
        self.uvPinNode = CreateNode("uvPin", name=f"{self.name}_uvPin")
        orig_outMesh = cmds.deformableShape(self.mesh, cog=1)[0]
        cmds.setAttr(f"{self.uvPinNode}.normalAxis", 0)
        cmds.setAttr(f"{self.uvPinNode}.tangentAxis", 5)
        cmds.setAttr(f"{self.uvPinNode}.uvSetName", uvPin.get_currentUVSetName(self.mesh), type="string")
        cmds.connectAttr(orig_outMesh, f"{self.uvPinNode}.originalGeometry")
        cmds.connectAttr(f"{self.mesh}.worldMesh[0]", f"{self.uvPinNode}.deformedGeometry")
        for i, obj in enumerate(self.targetList):
            # set uvPin.uv value
            cmds.setAttr(f"{self.uvPinNode}.coordinate[{i}].coordinateU", i + 0.5)
            cmds.setAttr(f"{self.uvPinNode}.coordinate[{i}].coordinateV", 0.5)
            node_decom = decomMatrix(name=obj, scale=False, shear=False)
            cmds.connectAttr(f"{self.uvPinNode}.outputMatrix[{i}]", node_decom.inputMatrix)

    @staticmethod
    def create_planeByObjectList(targetList, size=0.1, name="uvPinPlane", buildInMaya=True):
        if not targetList:
            raise ValueError("No object need to create plane, please input object list first.")
        num = len(targetList)

        base_vtx_pos_ary = [[0.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]]
        base_poly_count = [3, 3, 3, 3]
        base_poly_connect = [1, 4, 0, 4, 3, 0, 3, 2, 0, 2, 1, 0]
        base_uvCounts = [3, 3, 3, 3]
        base_uvIds = [0, 1, 2, 1, 3, 2, 3, 4, 2, 4, 0, 2]
        base_u = [1, 0.5, 0.5, 0, 0.5]
        base_v = [0.5, 1, 0.5, 0.5, 0]

        base_vtx_num = len(base_vtx_pos_ary)
        pos_ary = []
        face_connect_ary = []
        face_count_ary = base_poly_count * num

        uvCounts = base_uvCounts * num
        u = []
        v = base_v * num
        uvIds = []

        info = []
        # num
        for i in range(num):
            info.append({"driven": targetList[i], "meshComponent": list(range(5 * i, 5 * i + 5))})
            # pos_ary
            mult_matrix = get_worldMatrix(targetList[i])
            for pos in base_vtx_pos_ary:
                pos_ary.append(om.MPoint(pos) * size * mult_matrix)
            # face_connect_ary
            for vtx in base_poly_connect:
                face_connect_ary.append(vtx + (i * base_vtx_num))
            # u
            for u_value in base_u:
                u.append(u_value + i)
            # uvIds
            for id in base_uvIds:
                uvIds.append(id + (i * base_vtx_num))

        if not buildInMaya:
            data = om.MFnMeshData()
            mObject = data.create()
            fnMesh = om.MFnMesh()
            fnMesh.create(pos_ary, face_count_ary, face_connect_ary, parent=mObject)
            fnMesh.setUVs(u, v)
            fnMesh.assignUVs(uvCounts, uvIds)
            return fnMesh, data

        fnMesh = om.MFnMesh()
        transform: str = CreateNode("transform", name=name)
        mObject = om.MSelectionList().add(transform).getDependNode(0)
        mObj = fnMesh.create(pos_ary, face_count_ary, face_connect_ary, parent=mObject)
        fnMesh.setUVs(u, v)
        fnMesh.assignUVs(uvCounts, uvIds)
        fnDep = om.MFnDependencyNode(mObj)
        fnDep.setName(f"{transform}Shape")

        try:
            cmds.addAttr(transform, ln="notes", dt="string")
        except:
            pass

        infoStr = json.dumps(info, indent=4)
        cmds.setAttr(f"{transform}.notes", infoStr, type="string")

        return transform, fnDep.name()

    @staticmethod
    def get_UVByClosestPoint(point, shape: str):
        p = om.MPoint(point)
        sel: om.MSelectionList = om.MGlobal.getSelectionListByName(shape)
        dag: om.MDagPath = sel.getDagPath(0)
        fn_mesh = om.MFnMesh(dag)
        set_name = fn_mesh.currentUVSetName()
        return fn_mesh.getUVAtPoint(p, space=om.MSpace.kWorld, uvSet=set_name)[0:2]

    @staticmethod
    def get_currentUVSetName(shape):
        sel: om.MSelectionList = om.MGlobal.getSelectionListByName(shape)
        dag: om.MDagPath = sel.getDagPath(0)
        fn_mesh = om.MFnMesh(dag)
        return fn_mesh.currentUVSetName()

    @staticmethod
    def normalizedWeights(uvPinMesh: str, skinCluster: str):
        mSel = om.MSelectionList()
        mSel.add(uvPinMesh)
        mSel.add(skinCluster)
        uvPinMesh_mDag = mSel.getDagPath(0)
        skin_mObj = mSel.getDependNode(1)
        fnSkin = oma.MFnSkinCluster(skin_mObj)
        singleIdComp = om.MFnSingleIndexedComponent()
        vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)
        weight, infCount = fnSkin.getWeights(uvPinMesh_mDag, vertexComp)
        for i in range(0, len(weight), infCount):
            print([weight[i]] * 4)
            print(weight[i + 1 : i + 5])
            # weight[i + 1:i + 5] = [weight[i]] * 4

        # fnSkin.setWeights(uvPinMesh_mDag, vertexComp, om.MIntArray(list(range(infCount))), weight)
        # TODO complete this function


class follicle(uvPin):
    """Create follicle constraint"""

    def create(self):
        mesh, shape = follicle.create_planeByObjectList(targetList=self.targetList, size=self.size, name=f"{self.name}_mesh")
        self.uvPinNode = []
        for i, obj in enumerate(self.targetList):
            node_follicle = generateUniqueName(f"{obj}_follicle")
            node_follicle = CreateNode("transform", name=node_follicle)
            cmds.setAttr(f"{node_follicle}.v", 0)
            follicle_shape = CreateNode("follicle", name=f"{node_follicle}Shape", parent=node_follicle)
            cmds.connectAttr(f"{mesh}.outMesh", f"{follicle_shape}.inputMesh")
            cmds.connectAttr(f"{mesh}.worldMatrix[0]", f"{follicle_shape}.inputWorldMatrix")
            cmds.setAttr(f"{follicle_shape}.parameterU", i + 0.5)
            cmds.setAttr(f"{follicle_shape}.parameterV", 0.5)
            cmds.connectAttr(f"{follicle_shape}.outTranslate", f"{node_follicle}.translate")
            cmds.connectAttr(f"{follicle_shape}.outRotate", f"{node_follicle}.rotate")
            matrixConstraint(node_follicle, obj, scale=False, shear=False)
            self.uvPinNode.append(follicle_shape)

        self.mesh = mesh
        self.meshShape = shape


try:
    if not cmds.about(api=1) >= 2020_0000:
        uvPin = follicle
except Exception:
    pass
