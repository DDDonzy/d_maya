from maya import cmds

skin_mesh = "bs_split:cheekMouth"
sculpt_mesh = "f5:M_Head_base14"

# get mesh shapes
skin_meshShape = cmds.listRelatives(skin_mesh, s=1)[0]

# get skin node
node_skin = None
his = cmds.listHistory(skin_mesh, pdo=1, il=1)
for node in his:
    if cmds.objectType(node) == 'skinCluster':
        node_skin = node
if not node_skin:
    cmds.error("No skinCluster")
# get skin inference
inf_list = cmds.skinCluster(node_skin, q=1, inf=1)


# create weight node
comFalloff_node = cmds.createNode("componentFalloff", name=f"{skin_mesh}_componentFalloff")
falloffEval_node = cmds.createNode("falloffEval", name=f"{skin_mesh}_falloffEval")
cmds.connectAttr(f"{node_skin}.perInfluenceWeights",
                 f"{comFalloff_node}.weightLayers")

cmds.connectAttr(f"{node_skin}.outputGeometry[0]",
                 f"{comFalloff_node}.weightedGeometry")

cmds.connectAttr(f"{comFalloff_node}.outputWeightFunction",
                 f"{falloffEval_node}.weightFunction")

cmds.connectAttr(f"{node_skin}.outputGeometry[0]",
                 f"{falloffEval_node}.currentGeometry")

cmds.connectAttr(f"{node_skin}.outputGeometry[0]",
                 f"{falloffEval_node}.originalGeometry")


# create base mesh
split_mesh = cmds.polyCube(ch=0)[0]
split_meshShape = cmds.listRelatives(split_mesh, s=1)[0]
cmds.connectAttr(f"{skin_meshShape}.outMesh",
                 f"{split_meshShape}.inMesh")
cmds.refresh()
cmds.disconnectAttr(f"{skin_meshShape}.outMesh",
                    f"{split_meshShape}.inMesh")

node_bs = cmds.blendShape(split_mesh)[0]
for i, x in enumerate(inf_list):
    cmds.blendShape(node_bs, e=1, t=(split_meshShape, i, sculpt_mesh, 1))
    cmds.aliasAttr(x.split(":")[-1], f"{node_bs}.w[{i}]")
    cmds.setAttr(f"{node_bs}.w[{i}]", 0)
    cmds.setAttr(f"{comFalloff_node}.weightInfoLayers[{i}].defaultWeight", 0)
    cmds.connectAttr(f"{falloffEval_node}.perFunctionWeights[{i}].perFunctionVertexWeights",
                     f"{node_bs}.inputTarget[0].inputTargetGroup[{i}].targetWeights")
