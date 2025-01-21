from maya import cmds
from maya.api import OpenMaya as om
from UTILS.createBase import CreatorBase
from UTILS.transform.transform import get_worldMatrix, matrixConstraint, decomMatrix
from UTILS.generateUniqueName import generateUniqueName


class uvPin(CreatorBase):
    def _post_init(self, *args, **kwargs):
        self.targetList = kwargs.get("targetList") or kwargs.get("tl") or args[0] if args else cmds.ls(sl=1)
        if not isinstance(self.targetList, list):
            self.targetList = [self.targetList]
        self.size = kwargs.get("size") or kwargs.get("s") or 0.1
        self.name = kwargs.get("name") or kwargs.get("n") or 'uvPin'
        if not self.targetList:
            raise ValueError("No object need to create uvPin, please input object list. or select some object.")

    def create(self):
        # create mesh
        mesh, shape = uvPin.create_planeByObjectList(targetList=self.targetList,
                                                     size=self.size,
                                                     name=f"{self.name}_mesh")

        # create uvPin node
        node_uvPin = cmds.createNode("uvPin", name=f"{self.name}_uvPin")
        orig_outMesh = cmds.deformableShape(mesh, cog=1)[0]
        cmds.setAttr(".normalAxis", 0)
        cmds.setAttr(".tangentAxis", 5)
        cmds.setAttr(f"{node_uvPin}.uvSetName",
                     uvPin.get_currentUVSetName(mesh),
                     type="string")
        cmds.connectAttr(orig_outMesh,
                         f"{node_uvPin}.originalGeometry")
        cmds.connectAttr(f"{mesh}.worldMesh[0]",
                         f"{node_uvPin}.deformedGeometry")
        for i, obj in enumerate(self.targetList):
            # set uvPin.uv value
            cmds.setAttr(f"{node_uvPin}.coordinate[{i}].coordinateU", i + 0.5)
            cmds.setAttr(f"{node_uvPin}.coordinate[{i}].coordinateV", 0.5)
            node_decom = decomMatrix(name=obj, scale=False, shear=False)
            cmds.connectAttr(f"{node_uvPin}.outputMatrix[{i}]", node_decom.inputMatrix)

    @staticmethod
    def get_UVByClosestPoint(point, shape: str):
        p = om.MPoint(*point, 0)
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
    def create_planeByObjectList(targetList, size=1, name="uvPinPlane"):
        if not targetList:
            raise ValueError("No object need to create plane, please input object list first.")
        num = len(targetList)
        transform = cmds.createNode("transform", name=name)
        mSel = om.MSelectionList()
        mSel.add(transform)
        mObject = mSel.getDependNode(0)

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
        # num
        for i in range(num):
            # pos_ary
            mult_matrix = get_worldMatrix(targetList[i])
            for pos in base_vtx_pos_ary:
                pos_ary.append(om.MPoint(pos) * size * mult_matrix)
            # face_connect_ary
            for vtx in base_poly_connect:
                face_connect_ary.append(vtx + (i * base_vtx_num))
            # u
            for u_value in base_u:
                u.append(u_value+i)
            # uvIds
            for id in base_uvIds:
                uvIds.append(id + (i * base_vtx_num))

        fnMesh = om.MFnMesh()
        mObj = fnMesh.create(pos_ary, face_count_ary, face_connect_ary, parent=mObject)
        fnDep = om.MFnDependencyNode(mObj)
        fnDep.setName(f"{transform}Shape")

        fnMesh.setUVs(u, v)
        fnMesh.assignUVs(uvCounts, uvIds)
        return transform, fnDep.name()


class follicle(uvPin):
    def create(self):
        mesh, shape = follicle.create_planeByObjectList(targetList=self.targetList,
                                                        size=self.size,
                                                        name=f"{self.name}_mesh")
        for i, obj in enumerate(self.targetList):
            node_follicle = generateUniqueName(f"{obj}_follicle")
            node_follicle = cmds.createNode("transform", name=node_follicle)
            cmds.setAttr(f"{node_follicle}.v", 0)
            follicle_shape = cmds.createNode("follicle", name=f"{node_follicle}Shape", parent=node_follicle)
            cmds.connectAttr(f"{mesh}.outMesh", f"{follicle_shape}.inputMesh")
            cmds.connectAttr(f"{mesh}.worldMatrix[0]", f"{follicle_shape}.inputWorldMatrix")
            cmds.setAttr(f"{follicle_shape}.parameterU", i + 0.5)
            cmds.setAttr(f"{follicle_shape}.parameterV", 0.5)
            cmds.connectAttr(f"{follicle_shape}.outTranslate", f"{node_follicle}.translate")
            cmds.connectAttr(f"{follicle_shape}.outRotate", f"{node_follicle}.rotate")
            matrixCon = matrixConstraint(node_follicle, obj, scale=False, shear=False)

# uvPin(cmds.ls(sl=1), plane_size=0.3)
# follicle(cmds.ls(sl=1), plane_size=0.3)
