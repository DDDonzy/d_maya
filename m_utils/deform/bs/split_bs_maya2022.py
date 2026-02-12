from maya import cmds
from maya.api import OpenMaya as om
from m_utils.create.assetCallback import AssetCallback

from m_utils import apiundo


class DuplicateMeshCommand:
    def __init__(self, source, name):
        self.source = source
        self.name = name
        self.actual_created_name = None

    def doit(self):
        mSel = om.MSelectionList()
        mSel.add(self.source)
        source_shape_mDag = mSel.getDagPath(0)
        source_transform_mDag = om.MDagPath(source_shape_mDag)
        source_transform_fn = om.MFnTransform(source_transform_mDag)
        source_matrix = source_transform_fn.transformation().asMatrix()
        source_fnMesh = om.MFnMesh(source_shape_mDag)
        new_shape_mObj = source_fnMesh.copy(source_fnMesh.object())
        new_transform_fn = om.MFnTransform(new_shape_mObj)
        new_transform_fn.setTransformation(om.MTransformationMatrix(source_matrix))
        self.actual_created_name = new_transform_fn
        return new_transform_fn.setName(self.name)

    def undo(self):
        dag_modifier = om.MDagModifier()
        dag_modifier.deleteNode(self.actual_created_name.object())
        dag_modifier.doIt()

    def execute(self):
        name = self.doit()
        apiundo.commit(self.undo, self.doit)
        return name


def duplicate_mesh(source: str = None, name: str = None, materials=True) -> str:
    if not source:
        source = cmds.ls(sl=1)[0]
    if not name:
        name = f"{source}_duplicate"
    command = DuplicateMeshCommand(source=source, name=name)
    name = command.execute()
    if materials:
        try:
            idx = cmds.getAttr("initialShadingGroup.dagSetMembers", mi=1)[-1] + 1
            shape = cmds.listRelatives(name, s=1)[0]
            idx = cmds.getAttr("initialShadingGroup.dagSetMembers", mi=1)[-1] + 1
            cmds.connectAttr(f"{shape}.instObjGroups[0]", f"initialShadingGroup.dagSetMembers[{idx}]", f=1)
        except Exception:
            pass
    return name


def split_sculpt_by_skin(skin_mesh, sculpt_mesh):
    skin_mesh = "pSphere1"
    sculpt_mesh = "pSphere2"

    with AssetCallback("SplitSculpt"):
        # get skin node
        node_skin = None
        his = cmds.listHistory(skin_mesh, pdo=1, il=1)
        for node in his:
            if cmds.objectType(node) == "skinCluster":
                node_skin = node
        if not node_skin:
            cmds.error("No skinCluster")

        # create weight node
        comFalloff_node = cmds.createNode("componentFalloff", name=f"{skin_mesh}_componentFalloff")
        falloffEval_node = cmds.createNode("falloffEval", name=f"{skin_mesh}_falloffEval")
        cmds.connectAttr(f"{node_skin}.perInfluenceWeights", f"{comFalloff_node}.weightLayers")
        cmds.connectAttr(f"{node_skin}.originalGeometry[0]", f"{comFalloff_node}.weightedGeometry")
        cmds.connectAttr(f"{comFalloff_node}.outputWeightFunction", f"{falloffEval_node}.weightFunction")
        cmds.connectAttr(f"{node_skin}.originalGeometry[0]", f"{falloffEval_node}.currentGeometry")
        cmds.connectAttr(f"{node_skin}.originalGeometry[0]", f"{falloffEval_node}.originalGeometry")

    # duplicate
    split_mesh = duplicate_mesh("pSphere1", name="Split_Mesh")
    # get skin inference
    inf_list = cmds.skinCluster(node_skin, q=1, inf=1)
    node_bs = cmds.blendShape(split_mesh)[0]
    for i, x in enumerate(inf_list):
        cmds.blendShape(node_bs, e=1, t=(split_mesh, i, sculpt_mesh, 1))
        cmds.aliasAttr(x.split(":")[-1], f"{node_bs}.w[{i}]")
        cmds.setAttr(f"{node_bs}.w[{i}]", 0)
        cmds.setAttr(f"{comFalloff_node}.weightInfoLayers[{i}].defaultWeight", 0)
        cmds.connectAttr(f"{falloffEval_node}.perFunctionWeights[{i}].perFunctionVertexWeights", f"{node_bs}.inputTarget[0].inputTargetGroup[{i}].targetWeights")
