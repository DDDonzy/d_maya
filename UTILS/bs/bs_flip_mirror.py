# coding=utf-8
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om
import numpy as np
import UTILS.bs.dslReverseShape as dsl


import os
import sys


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


# 定义一个 目标bs 的数据结构
class bs_targetData():
    def __init__(self):
        self.name = ""
        self.index = 0
        self.inputTargetItems = []
        self.postDeformersMode = 0


# 创建bs节点
def create_blendShapeNode(objectName, name="New_Blendshapes"):
    bsNode = cmds.blendShape(objectName, name=name)[0]
    return bsNode


# 添加bs目标体
def add_bsTarget(blendShapeNode, targetName):
    bsData = get_bsData(blendShapeNode)
    targetListCount = len(bsData)
    bsBaseShape = cmds.blendShape(blendShapeNode, q=1, geometry=1)[0]
    targetBaseShape = cmds.createNode("mesh")
    cmds.connectAttr("{}.outMesh".format(bsBaseShape), "{}.inMesh".format(targetBaseShape))
    cmds.refresh()
    cmds.disconnectAttr("{}.outMesh".format(bsBaseShape), "{}.inMesh".format(targetBaseShape))
    cmds.blendShape(blendShapeNode, e=1, t=(bsBaseShape, targetListCount, targetBaseShape, 1))
    cmds.blendShape(blendShapeNode, e=1, rtd=(0, targetListCount))
    while targetName in bsData:
        targetName = targetName + "_copy"
    cmds.aliasAttr(targetName, "%s.w[%s]" % (blendShapeNode, targetListCount))
    cmds.delete(cmds.listRelatives(targetBaseShape, p=1)[0])

    bsData = get_bsData(blendShapeNode)
    return bsData[targetName]


# 删除bs目标体
def delete_bsTarget(blendShapeNode, targetName):
    targetIndex = get_bsData(blendShapeNode)[targetName].index
    mel.eval("blendShapeDeleteTargetGroup %s %s" % (blendShapeNode, targetIndex))


# 获取bs数据
# dirt ={name:bs_targetData}
#             bs_targetData.name
#             bs_targetData.index
#             bs_targetData.inputTargetItems
#             bs_targetData.postDeformMode
def get_bsData(blendShapeNode):
    targetNameList = cmds.listAttr(blendShapeNode + '.weight', m=True)
    targetIndexList = cmds.getAttr(blendShapeNode + '.weight', mi=True)
    bsDict = {}
    if targetNameList is not None:
        for name in targetNameList:
            targetData = bs_targetData()
            targetData.name = name
            targetData.index = targetIndexList[targetNameList.index(name)]
            targetData.inputTargetItems = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem"
                                                       % (blendShapeNode, targetData.index), mi=1)
            targetData.postDeformersMode = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].postDeformersMode"
                                                        % (blendShapeNode, targetData.index))
            bsDict.update({name: targetData})
    return bsDict


# 翻转bs目标提形态
def flip_bsTarget(blendShapeNode,
                  targetName,
                  axis="x"):
    if type(targetName) != list:
        targetName = [targetName]
    targetData = get_bsData(blendShapeNode)
    for x in targetName:
        cmds.blendShape(blendShapeNode, e=1, flipTarget=(0, targetData[x].index), symmetryAxis=axis, symmetrySpace=1)
        print("Flip_bsTarget:  %s" % x)
    cmds.symmetricModelling(e=True, r=1)


# 镜像bs目标
# mirrorDirection = 0    +X   --->   -X
# mirrorDirection = 1    -X   --->   +X
def mirror_bsTarget(blendShapeNode,
                    targetName,
                    axis="x",
                    mirrorDirection=0):
    if type(targetName) != list:
        targetName = [targetName]
    targetData = get_bsData(blendShapeNode)
    for x in targetName:
        cmds.blendShape(blendShapeNode, e=1, mirrorTarget=(0, targetData[x].index),
                        symmetryAxis=axis, mirrorDirection=mirrorDirection, symmetrySpace=1)
        print("Mirror_bsTarget:  %s" % x)
    cmds.symmetricModelling(e=True, r=1)


# 复制 bs目标提数据 到 新的目标体上
def copy_bsTargetData(blendShapeNode,
                      sourceTargetName,
                      newTargetName):
    reset_bsTargetData(blendShapeNode, newTargetName)
    targetData = get_bsData(blendShapeNode)
    sourceTargetIndex = targetData[sourceTargetName].index
    targetIndex = targetData[newTargetName].index
    sourceTargetInbetween = targetData[sourceTargetName].inputTargetItems
    if not sourceTargetInbetween:
        return
    for inbetween in sourceTargetInbetween:
        pointArray = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem[%s].inputPointsTarget"
                                  % (blendShapeNode, sourceTargetIndex, inbetween))
        componentList = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem[%s].inputComponentsTarget"
                                     % (blendShapeNode, sourceTargetIndex, inbetween))
        pointArray.insert(0, len(pointArray))
        componentList.insert(0, len(componentList))
        cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem[%s].inputPointsTarget"
                     % (blendShapeNode, targetIndex, inbetween), type="pointArray", *pointArray)
        cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem[%s].inputComponentsTarget"
                     % (blendShapeNode, targetIndex, inbetween), type="componentList", *componentList)
        print("Copy_bsTarget:  %s[%s] ------>   %s[%s]" % (sourceTargetName, inbetween, newTargetName, inbetween))


# 重置bs目标体上的变形数据
def reset_bsTargetData(blendShapeNode, targetName):
    if type(targetName) != list:
        targetName = [targetName]
    targetData = get_bsData(blendShapeNode)
    for x in targetName:
        targetIndex = targetData[x].index
        targetInbetween = targetData[x].inputTargetItems
        if targetInbetween:
            for inbetween in targetInbetween:
                cmds.removeMultiInstance('%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem[%s]'
                                         % (blendShapeNode, targetIndex, inbetween))
        print("Reset bsTargetData:  %s" % x)


# 设置bs目标体的post 为 transformSpace模式
def set_bsTargetPostMode_to_TransformSpace(blendShapeNode="", targetName="", transformObject=None):
    postDeformersMode_TransformSpace = 2
    targetData = get_bsData(blendShapeNode)
    index = targetData[targetName].index
    cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s].postDeformersMode"
                 % (blendShapeNode, index), postDeformersMode_TransformSpace)
    if transformObject is not None:
        cmds.connectAttr("%s.worldMatrix[0]" % transformObject, "%s.inputTarget[0].inputTargetGroup[%s].targetMatrix"
                         % (blendShapeNode, index), f=1)
        transformObjectMatrix = om.MMatrix(cmds.getAttr("%s.worldMatrix[0]" % transformObject))
        cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s].targetBindMatrix"
                     % (blendShapeNode, index), transformObjectMatrix.inverse(), type="matrix")
    message = "<hl> %s.%s.postMode</hl> set as transformSpace\nTransform Object = <hl>%s</hl> " \
              % (blendShapeNode, targetName, transformObject)
    # cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)
    print("Output: '{}.{}' set to 'transformSpace'--------->{}".format(blendShapeNode, targetName, transformObject))


# 创建包裹(旧版包裹 速度慢）
# createWrap("pCube1","pSphere1")
def createWrap(*args, **kwargs):
    influence = args[0]
    surface = args[1]

    shapes = cmds.listRelatives(influence, shapes=True)
    influenceShape = shapes[0]

    weightThreshold = kwargs.get('weightThreshold', 0.0)
    maxDistance = kwargs.get('maxDistance', 1.0)
    exclusiveBind = kwargs.get('exclusiveBind', True)
    autoWeightThreshold = kwargs.get('autoWeightThreshold', True)
    falloffMode = kwargs.get('falloffMode', 1)

    wrapData = cmds.deformer(surface, type='wrap')
    wrapNode = wrapData[0]

    cmds.setAttr(wrapNode + '.weightThreshold', weightThreshold)
    cmds.setAttr(wrapNode + '.maxDistance', maxDistance)
    cmds.setAttr(wrapNode + '.exclusiveBind', exclusiveBind)
    cmds.setAttr(wrapNode + '.autoWeightThreshold', autoWeightThreshold)
    cmds.setAttr(wrapNode + '.falloffMode', falloffMode)
    cmds.connectAttr(surface + '.worldMatrix[0]', wrapNode + '.geomMatrix')

    duplicateData = cmds.duplicate(influence, name=influence + 'Base')
    base = duplicateData[0]
    shapes = cmds.listRelatives(base, shapes=True)
    baseShape = shapes[0]
    cmds.hide(base)

    if not cmds.attributeQuery('dropoff', n=influence, exists=True):
        cmds.addAttr(influence, sn='dr', ln='dropoff', dv=4.0, min=0.0, max=20.0)
        cmds.setAttr(influence + '.dr', k=True)
    if cmds.nodeType(influenceShape) == 'mesh':
        if not cmds.attributeQuery('smoothness', n=influence, exists=True):
            cmds.addAttr(influence, sn='smt', ln='smoothness', dv=0.0, min=0.0)
            cmds.setAttr(influence + '.smt', k=True)
        if not cmds.attributeQuery('inflType', n=influence, exists=True):
            cmds.addAttr(influence, at='short', sn='ift', ln='inflType', dv=2, min=1, max=2)
        cmds.connectAttr(influenceShape + '.worldMesh', wrapNode + '.driverPoints[0]')
        cmds.connectAttr(baseShape + '.worldMesh', wrapNode + '.basePoints[0]')
        cmds.connectAttr(influence + '.inflType', wrapNode + '.inflType[0]')
        cmds.connectAttr(influence + '.smoothness', wrapNode + '.smoothness[0]')

    if cmds.nodeType(influenceShape) == 'nurbsCurve' or cmds.nodeType(influenceShape) == 'nurbsSurface':
        if not cmds.attributeQuery('wrapSamples', n=influence, exists=True):
            cmds.addAttr(influence, at='short', sn='wsm', ln='wrapSamples', dv=10, min=1)
            cmds.setAttr(influence + '.wsm', k=True)
        cmds.connectAttr(influenceShape + '.ws', wrapNode + '.driverPoints[0]')
        cmds.connectAttr(baseShape + '.ws', wrapNode + '.basePoints[0]')
        cmds.connectAttr(influence + '.wsm', wrapNode + '.nurbsSamples[0]')
    cmds.connectAttr(influence + '.dropoff', wrapNode + '.dropoff[0]')
    return wrapNode, base


# 创建包裹(新包裹 速度快）
# createProxWrap("pCube1","pSphere1")
def createProxWrap(*args, **kwargs):
    influence = args[0]
    surface = args[1]

    shapes = None
    for x in cmds.listRelatives(influence, s=1):
        if cmds.getAttr(x+".intermediateObject") == False:
            shapes = x

    wrapData = cmds.deformer(surface, type='proximityWrap')
    wrapNode = wrapData[0]

    wrapMode = kwargs.get('wrapMode', 1)
    falloffScale = kwargs.get("falloffScale", 200)

    cmds.setAttr(wrapNode + ".wrapMode", wrapMode)
    cmds.setAttr(wrapNode + ".falloffScale", falloffScale)
    cmds.setAttr(wrapNode + ".smoothInfluences", 3)
    cmds.setAttr(wrapNode + ".smoothNormals", 3)

    cmds.deformableShape(influence, cog=1)
    inf_orig = cmds.deformableShape(influence, cog=1)[0]

    cmds.connectAttr(inf_orig, wrapNode + ".drivers[0].driverBindGeometry")
    cmds.connectAttr(shapes + ".outMesh", wrapNode + ".drivers[0].driverGeometry")

    return wrapNode, None


# 查询bs节点属于哪一个模型
def get_bsBaseGeometry(bsNode):
    geometryShape = cmds.blendShape(bsNode, q=1, g=1)[0]
    geometry = cmds.listRelatives(geometryShape, p=1)[0]
    return geometry, geometryShape


# 获取 bs目标体的变形数据   pointArray   componentList
def get_inputPointsTargetArray(baseMesh, sculptMesh):
    # get  base points poisition
    basePositions = cmds.xform(baseMesh + '.pnts[*]', q=True, os=True, t=True)
    # get  componentList
    numVtx = cmds.getAttr(sculptMesh + '.vrts', s=True)
    componentList = [numVtx] + ['vtx[{}]'.format(i) for i in range(numVtx)]
    # get inputPointsTargetArray
    sculpt_positions = cmds.xform(sculptMesh + '.pnts[*]', q=True, os=True, t=True)
    pointArray = list(np.array(sculpt_positions) - np.array(basePositions))
    pointArray = [numVtx] + zip(pointArray[0::3], pointArray[1::3], pointArray[2::3])
    return pointArray, componentList


# 不同拓布模型，通过 warp传递bs
def remap_target(source_bsNode="", source_bsTarget=[],
                 new_mesh="", new_bsNode=None, wrapMode=0):
    # get source geometry
    source_geometry, source_geometryShape = get_bsBaseGeometry(source_bsNode)
    # if new_bsNode == None....  then create new blendshapes node
    if new_bsNode is None:
        new_bsNode = create_blendShapeNode(objectName=new_mesh, name="remapTarget_Blendshapes")
    elif not cmds.objExists(new_bsNode):
        new_bsNode = create_blendShapeNode(objectName=new_mesh, name=new_bsNode)
    # do wrap

    wrapBase = None
    wrapMeshShape = cmds.createNode("mesh", name="wrapTempShape")
    wrapMesh = cmds.listRelatives(wrapMeshShape, p=1)[0]
    cmds.connectAttr("{}.outMesh".format(new_mesh),
                     "{}.inMesh".format(wrapMeshShape))
    cmds.refresh()
    cmds.disconnectAttr("{}.outMesh".format(new_mesh),
                        "{}.inMesh".format(wrapMeshShape))
    if wrapMode == 0:
        wrapNode, wrapBase = createWrap(source_geometry, wrapMesh)
    if wrapMode == 1:
        wrapNode, wrapBase = createProxWrap(source_geometry, wrapMesh)
    # print("create Wrap !")
    # get source bs node data
    bsData = get_bsData(source_bsNode)
    # print("yes")
    # iterate the target that needs remap
    for source_targetName in source_bsTarget:
        source_target = bsData[source_targetName]  # source target data
        new_target = add_bsTarget(new_bsNode, source_target.name)  # create new target and get data
        # if postDeformersMode is transform space , then set new target
        if source_target.postDeformersMode == 2:
            targetMatrix_sourceConnect = cmds.listConnections("%s.inputTarget[0].inputTargetGroup[%s].targetMatrix"
                                                              % (source_bsNode, source_target.index), s=1, d=0)
            if targetMatrix_sourceConnect is not None:
                set_bsTargetPostMode_to_TransformSpace(new_bsNode, new_target.name, targetMatrix_sourceConnect[0])
            else:
                set_bsTargetPostMode_to_TransformSpace(new_bsNode, new_target.name)
        # disconnect bs weights to set value
        weight_sourceConnect = cmds.listConnections("%s.weight[%s]" % (source_bsNode, source_target.index), p=1, s=1,
                                                    d=0)
        if weight_sourceConnect is not None:
            cmds.disconnectAttr(weight_sourceConnect[0], "%s.weight[%s]" % (source_bsNode, source_target.index))
        # set source bs weights and copy wrap mesh position
        if not source_target.inputTargetItems:
            continue
        for item in source_target.inputTargetItems:
            w = 1 - (6000 - item) / 1000.0
            cmds.setAttr("%s.weight[%s]" % (source_bsNode, source_target.index), w)
            cmds.setAttr("%s.weight[%s]" % (new_bsNode, new_target.index), w)
            print("Output: remap '{}.{}' {}".format(new_bsNode, source_target.name, item))
            dsl.dslCorrectiveShape(skinGeo=new_mesh,
                                   sculptGeo=wrapMesh,
                                   blendShapeNode=new_bsNode,
                                   correctiveGroup=new_target.index,
                                   correctiveName=None,
                                   correctiveItem=item,
                                   inBetweenMode=True,
                                   flatten=None,
                                   keepSculpt=True)
        # end remap
        cmds.setAttr("%s.weight[%s]" % (source_bsNode, source_target.index), 0)
        cmds.setAttr("%s.weight[%s]" % (new_bsNode, new_target.index), 0)
        if weight_sourceConnect is not None:
            cmds.connectAttr(weight_sourceConnect[0], "%s.weight[%s]" % (source_bsNode, source_target.index))
            cmds.connectAttr(weight_sourceConnect[0], "%s.weight[%s]" % (new_bsNode, new_target.index))
    # delete wrap
    cmds.delete(wrapMesh, wrapBase)


# 自动翻转目标体到另一边
def autoFlipPose(blendShapeNode, replaceString=("L_", "R_")):
    bsTarget = cmds.channelBox("mainChannelBox", q=1, sha=1)
    data = get_bsData(blendShapeNode)
    if not bsTarget:
        bsTarget = list(data.keys())
    print("AUTO FLIP POSE:")
    for x in bsTarget:
        sourName = data[x].name
        if replaceString[0] not in sourName:
            print("    PASS---------", sourName)
            continue
        targName = sourName.replace(*replaceString)
        try:
            with HiddenPrints():
                copy_bsTargetData(blendShapeNode, sourName, targName)
                flip_bsTarget(blendShapeNode, targName)
            print("    SUCCESS------", sourName, " >>>>>>>>>> ", targName)
        except:
            print("    ERROR---------", sourName, " >>>>>>>>>> ", targName)


def autoRemap_target(**kwargs):
    baseMesh = kwargs.get('baseMesh', cmds.ls(sl=1)[0])
    newMesh = kwargs.get('newMesh', cmds.ls(sl=1)[1])
    # print(baseMesh)
    # print(newMesh)

    for x in cmds.listHistory(baseMesh, pdo=1, il=1):
        if cmds.objectType(x) == "blendShape":
            bsNode = x
            targetList = kwargs.get('targetList', get_bsData(bsNode).keys())
            # print(bsNode)
            # print(targetList)
            remap_target(source_bsNode=bsNode,
                         source_bsTarget=targetList,
                         new_mesh=newMesh,
                         new_bsNode=None)
#
# set_bsTargetPostMode_to_TransformSpace(blendShapeNode="body_bs",
#                                        targetName="Knee_R_0_0_60",
#                                        transformObject="Knee_R")

# remap_target(source_bsNode="", source_bsTarget=cmds.channelBox("mainChannelBox",q=1,sha=1),
#                  new_mesh="", new_bsNode=None, wrapMode=1)

# autoFlipPose()

# reset_bsTargetData(cmds.ls(sl=1)[0],cmds.channelBox("mainChannelBox",q=1,sha=1))
