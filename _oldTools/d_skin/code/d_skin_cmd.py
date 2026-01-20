from .core import *
import time
import numpy


def alignTransform(baseOBJ, targetOBJ):
    try:
        cmds.delete(cmds.parentConstraint(baseOBJ, targetOBJ))
        cmds.delete(cmds.scaleConstraint(baseOBJ, targetOBJ))
    except:
        pass


def addGroup(obj='', objSuffix='', grpSuffix=''):
    if type(obj) == str:
        objList = [obj]
    else:
        objList = obj
    if type(grpSuffix) == str:
        if ',' in grpSuffix:
            grpSuffixList = grpSuffix.split(',')
        else:
            grpSuffixList = [grpSuffix]
    else:
        grpSuffixList = grpSuffix
    for obj in objList:
        obj_parent = cmds.listRelatives(obj, parent=1)
        obj_grpList = []
        for obj_grp in grpSuffixList:
            if objSuffix == '':
                obj_grpName = obj + '_' + obj_grp
            elif objSuffix in obj:
                obj_grpName = obj.replace(objSuffix, obj_grp)
            else:
                obj_grpName = obj + '_' + obj_grp
            obj_grp = cmds.group(em=1, name=obj_grpName)
            obj_grpList.append(obj_grp)
        for grp in obj_grpList:
            grp_index = obj_grpList.index(grp)
            try:
                cmds.parent(obj_grpList[grp_index + 1], grp)
            except:
                pass
        cmds.parent(obj_grpList[0], obj)
        for xyz in 'xyz':
            for tr in 'tr':
                cmds.setAttr('%s.%s%s' % (obj_grpList[0], tr, xyz), 0)
            cmds.setAttr('%s.%s%s' % (obj_grpList[0], 's', xyz), 1)
        cmds.parent(obj_grpList[0], world=1)
        try:
            cmds.parent(obj_grpList[0], obj_parent)
        except:
            pass
        cmds.parent(obj, obj_grpList[-1])


def getHistoryNode(mesh, nodeType):
    try:
        hisList = cmds.listHistory(mesh, pdo=1)
        for his in hisList:
            if cmds.objectType(his) == nodeType:
                node = his
                return node
    except:
        return None
    return None


def loadMesh_cmd(mesh='No Mesh'):
    if mesh == 'No Mesh':
        try:
            mesh = cmds.ls(sl=1)[0]
        except:
            om.MPxCommand().displayError('Please select mesh')
            return 'No Mesh'
    if '_Graph_set' in mesh:
        mesh = mesh.replace('_Graph_set', '_Mask_mesh')
    try:
        shape = cmds.listRelatives(mesh, shapes=1)[0]
        if cmds.objectType(shape) == 'mesh':
            return mesh
    except:
        om.MPxCommand().displayError('%s type is not mesh' % mesh)
        return 'No Mesh'


def loadSkinNode_cmd(node='No Skin Node'):
    if node == 'No Skin Node':
        try:
            mesh = cmds.ls(sl=1)[0]
        except:
            om.MPxCommand().displayError('Please select object')
            return 'No Skin Node'
        if '_Graph_set' in mesh:
            mesh = mesh.replace('_Graph_set', '_Mask_mesh')
    if '_Graph_set' in node:
        mesh = node.replace('_Graph_set', '_Mask_mesh')
    try:
        return getHistoryNode(mesh, 'skinCluster')
    except:
        om.MPxCommand().displayError('Can not find skinCluster')
        return 'No Skin Node'


def getBlendShapeItem(blendShapeNode):
    iTg = '%s.inputTarget[0]' % blendShapeNode
    iTi = '.inputTargetItem'
    blendShapeItem = {}
    targetNameList = cmds.listAttr(blendShapeNode + '.weight', m=True)
    targetIndexList = cmds.getAttr(blendShapeNode + '.weight', mi=True)
    for target in targetNameList:
        blendShapeItem[target] = targetIndexList[targetNameList.index(target)]
    return blendShapeItem


def duplicateMesh(mesh=None, name=None):
    if mesh == None:
        try:
            mesh = cmds.ls(sl=1)[0]
        except:
            om.MPxCommand().displayError('Please select object')
            return
    if name == None:
        name = mesh + '_dup'
    meshShape = cmds.createNode('mesh', name=name + 'Shape')
    newMesh = cmds.listRelatives(meshShape, p=1)[0]
    newMesh = cmds.rename(newMesh, name)
    cmds.connectAttr('%s.outMesh' % mesh, '%s.inMesh' % newMesh)
    cmds.refresh(cv=1)
    cmds.disconnectAttr('%s.outMesh' % mesh, '%s.inMesh' % newMesh)
    cmds.hyperShade(meshShape, a='lambert1')
    return newMesh


def reSkin(mesh):
    if not mesh:
        mesh = cmds.ls(sl=1)[0]
    skinNode = getHistoryNode(mesh, 'skinCluster')
    jointList = cmds.skinCluster(skinNode, q=1, inf=1)
    cmds.skinCluster(skinNode, e=1, ub=1)
    new_skinNode = cmds.skinCluster(mesh, jointList, tsb=1, name=skinNode)[0]
    cmds.skinPercent(new_skinNode, mesh, rtd=1)
    cmds.select(cl=1)


def createWeightGraph(mesh, prefix='', convert=False):
    baseMesh = duplicateMesh(mesh, name=prefix + '_Base_mesh')
    maskMesh = duplicateMesh(mesh, name=prefix + '_Mask_mesh')
    outMesh = duplicateMesh(mesh, name=prefix + '_Out_mesh')
    graphSets = cmds.group(em=1, name=prefix + '_Graph_set')
    maskSets = cmds.group(em=1, name=prefix + '_Mask_set')
    meshSets = cmds.group(em=1, name=prefix + '_Mesh_set')
    cmds.parent(baseMesh, maskMesh, meshSets, maskSets, outMesh, graphSets)
    cmds.setAttr(baseMesh + '.hiddenInOutliner', 1)
    cmds.setAttr(baseMesh + '.visibility', 0)
    cmds.setAttr(outMesh + '.visibility', 0)
    cmds.setAttr(maskSets + '.visibility', 0)
    cmds.setAttr(meshSets + '.visibility', 0)
    if convert == False:
        addMask(prefix=prefix, name='base')
    if convert == True:
        baseSkinClusterNode = getHistoryNode(mesh, 'skinCluster')
        baseJointsList = cmds.skinCluster(baseSkinClusterNode, q=1, inf=1)
        base_D_skin = D_skinTool(baseSkinClusterNode)
        baseWeightsInfo = base_D_skin.exportWeights()
        for baseJoint in sorted(baseJointsList):
            maskJoint = addMask(prefix=prefix, name=baseJoint, parent=baseJoint)[0]
            alignTransform(baseJoint, cmds.listRelatives(maskJoint, p=1))
        reSkin(maskMesh)
        newJoint = {}
        mask_D_skin = D_skinTool(getHistoryNode(maskMesh, 'skinCluster'))
        for x in baseWeightsInfo[0]:
            newJoint.update({x: '%s_%s_mask' % (prefix, baseWeightsInfo[0][x])})
        newWeightsInfo = [newJoint, baseWeightsInfo[1]]
        mask_D_skin.importWeights(newWeightsInfo)
    return graphSets


def getMessageFromScene(prefix=''):
    if '_Graph_set' in prefix:
        prefix = prefix.replace('_Graph_set', '')
    message = {}
    try:
        baseMesh = cmds.ls('%s_Base_mesh' % prefix)[0]
        maskMesh = cmds.ls('%s_Mask_mesh' % prefix)[0]
        outMesh = cmds.ls('%s_Out_mesh' % prefix)[0]
        graphSets = cmds.ls('%s_Graph_set' % prefix)[0]
        maskSets = cmds.ls('%s_Mask_set' % prefix)[0]
        meshSets = cmds.ls('%s_Mesh_set' % prefix)[0]
        meshList = cmds.listRelatives(meshSets, c=1)
        jointList = cmds.listRelatives(maskSets, c=1)
        message.update({'baseMesh': baseMesh,
                        'maskMesh': maskMesh,
                        'outMesh': outMesh,
                        'graphSets': graphSets,
                        'maskSets': maskSets,
                        'meshSets': meshSets,
                        'meshList': meshList,
                        'jointList': jointList})
        for i in meshList:
            try:
                secJoint = cmds.skinCluster(i, q=1, inf=1)
                if not secJoint:
                    secJoint = []
            except:
                secJoint = []
            message.update({i: secJoint})
        return message
    except:
        return message


def addMask(prefix='', name='', parent=None):
    message = getMessageFromScene(prefix)
    baseMesh = message['baseMesh']
    maskMesh = message['maskMesh']
    outMesh = message['outMesh']
    graphSets = message['graphSets']
    maskSets = message['maskSets']
    meshSets = message['meshSets']
    secMesh = duplicateMesh(baseMesh, name='%s_%s_mesh' % (prefix, name))
    cmds.select(cl=1)
    maskJoint = cmds.joint(name='%s_%s_mask' % (prefix, name))
    cmds.parent(secMesh, meshSets)
    cmds.parent(maskJoint, maskSets)
    if parent:
        cmds.parentConstraint(parent, maskJoint)
        cmds.scaleConstraint(parent, maskJoint)
    addGroup(obj=[maskJoint], objSuffix='', grpSuffix='zero')
    skinClusterNode = getHistoryNode(maskMesh, 'skinCluster')
    if not skinClusterNode:
        skinClusterNode = cmds.skinCluster(maskMesh, maskJoint, name='%s_mask_skinCluster' % prefix)[0]
    else:
        skinClusterNode = getHistoryNode(maskMesh, 'skinCluster')
        cmds.skinCluster(skinClusterNode, e=1, ai=maskJoint, lw=1, wt=0)
        cmds.setAttr(maskJoint + '.liw', 0)
    blendShapeNode = getHistoryNode(outMesh, 'blendShape')
    if not blendShapeNode:
        blendShapeNode = cmds.blendShape(secMesh, outMesh, name='%s_Combine_blendShape' % prefix)[0]
        cmds.blendShape(blendShapeNode, e=1, w=[(0, 1)])
    else:
        try:
            newTargetIndex = sorted(getBlendShapeItem(blendShapeNode).values())[-1] + 1
        except:
            newTargetIndex = 0
        cmds.blendShape(blendShapeNode, e=1, t=(outMesh, newTargetIndex, secMesh, 1.0))
        cmds.blendShape(blendShapeNode, e=1, w=[(newTargetIndex, 1)])
    cmds.addAttr(secMesh, ln='maskJoint', dt='string')
    cmds.setAttr('{}.maskJoint'.format(secMesh), maskJoint, type='string')
    cmds.select(cl=1)
    return [maskJoint, secMesh, skinClusterNode]


def deleteMask(prefix='', name=''):
    message = getMessageFromScene(prefix)
    maskMesh = message['maskMesh']
    outMesh = message['outMesh']
    secMesh = '%s_%s_mesh' % (prefix, name)
    maskJoint = '%s_%s_mask' % (prefix, name)
    skinClusterNode = getHistoryNode(maskMesh, 'skinCluster')
    blendShapeNode = getHistoryNode(outMesh, 'blendShape')
    blendShapeTargetIndex = getBlendShapeItem(blendShapeNode)[secMesh]
    cmds.blendShape(blendShapeNode, e=1, rm=1, t=(outMesh, blendShapeTargetIndex, secMesh, 0))
    cmds.skinCluster(skinClusterNode, e=1, ri=maskJoint)
    if not cmds.skinCluster(skinClusterNode, q=1, inf=1):
        cmds.delete(skinClusterNode)
    cmds.delete(secMesh, cmds.listRelatives(maskJoint, p=1))
    if cmds.objExists(skinClusterNode):
        return skinClusterNode
    else:
        return None


def addInfluence(mesh='', influenceList=[]):
    skinClusterNode = getHistoryNode(mesh, 'skinCluster')
    if skinClusterNode:
        for x in influenceList:
            try:
                cmds.skinCluster(skinClusterNode, e=1, ai=x, lw=1, wt=0)
                cmds.setAttr(x + '.liw', 0)
            except:
                om.MPxCommand.displayInfo('Influence object %s is already attached' % x)
    else:
        cmds.skinCluster(mesh, influenceList, tsb=1, name=mesh + '_skinCluster')


def removeInfluence(mesh='', influenceList=[]):
    skinClusterNode = getHistoryNode(mesh, 'skinCluster')
    if skinClusterNode:
        cmds.skinCluster(skinClusterNode, e=1, ri=influenceList)
    if not cmds.skinCluster(skinClusterNode, q=1, inf=1):
        cmds.delete(skinClusterNode)


def sendToDeform(blendShapeNode='', maskMesh='', secondMesh=[]):
    time_start = time.time()
    bs_outAttr = '{}.outputGeometry[0]'.format(blendShapeNode)
    mesh = cmds.listConnections(bs_outAttr, s=0, d=1)[0]
    maskSkinCluster = getHistoryNode(maskMesh, 'skinCluster')
    mask_D_skin = D_skinTool(maskSkinCluster)
    vtxNum = cmds.getAttr('{}.vrts'.format(mesh), s=1)
    bs_targets = getBlendShapeItem(blendShapeNode)
    for x in secondMesh:
        maskJoint = cmds.getAttr('{}.maskJoint'.format(x))
        secondSkinCluster = getHistoryNode(x, 'skinCluster')
        bs_index = bs_targets[x]
        bs_weightAttr = '{}.inputTarget[0].inputTargetGroup[{}].targetWeights[0:{}]'.format(blendShapeNode, bs_index,
                                                                                            vtxNum - 1)
        mask_index = mask_D_skin.getInfluenceIndex(maskJoint)
        mask_Weihgt = mask_D_skin.getSkinWeights(mask_index)
        cmds.setAttr(bs_weightAttr, *mask_Weihgt)
    time_end = time.time()
    om.MPxCommand.displayInfo('Time :      ' + str(time_end - time_start))


def sendToSkinCluster(blendShapeNode='', maskMesh='', secondMesh=[]):
    time_start = time.time()
    bs_outAttr = '{}.outputGeometry[0]'.format(blendShapeNode)
    mesh = cmds.listConnections(bs_outAttr, s=0, d=1)[0]
    maskSkinCluster = getHistoryNode(maskMesh, 'skinCluster')
    mask_D_skin = D_skinTool(maskSkinCluster)
    vtxNum = cmds.getAttr('{}.vrts'.format(mesh), s=1)
    bs_targets = getBlendShapeItem(blendShapeNode)
    for x in secondMesh:
        maskJoint = cmds.getAttr('{}.maskJoint'.format(x))
        secondSkinCluster = getHistoryNode(x, 'skinCluster')
        bs_index = bs_targets[x]
        bs_weightAttr = '{}.inputTarget[0].inputTargetGroup[{}].targetWeights[0:{}]'.format(blendShapeNode, bs_index,
                                                                                            vtxNum - 1)
        bs_weight = cmds.getAttr(bs_weightAttr)
        mask_index = mask_D_skin.getInfluenceIndex(maskJoint)
        mask_Weihgt = mask_D_skin.setInfluenceWeights(mask_index, bs_weight)
    time_end = time.time()
    om.MPxCommand.displayInfo('Time :      ' + str(time_end - time_start))


def combinedWeights(prefix):
    message = getMessageFromScene(prefix)
    allInf = []
    blendShapeNode = getHistoryNode(message['outMesh'], 'blendShape')
    mesh = cmds.listRelatives(message['meshSets'], c=1)
    meshSkinNodeList = []
    for x in mesh:
        skinNode = getHistoryNode(x, 'skinCluster')
        meshSkinNodeList.append(skinNode)
        inf = cmds.skinCluster(skinNode, q=1, inf=1)
        allInf = allInf + inf
    combineMesh = duplicateMesh(message['baseMesh'], 'combineSkinCluster_Mesh')
    combineSkinNode = cmds.skinCluster(combineMesh, allInf, tsb=1)[0]
    combineSkin = D_skinTool(combineSkinNode)
    combineWeights = combineSkin.exportWeights()
    inf_Index = combineWeights[0]
    allWeights = {}
    for x in mesh:
        numVtx = cmds.getAttr(x + '.vrts', s=True) - 1
        x_targetIndex = getBlendShapeItem(blendShapeNode)[x]
        x_bsWeights = cmds.getAttr(
            '{}.inputTarget[0].inputTargetGroup[{}].targetWeights[0:{}]'.format(blendShapeNode, x_targetIndex, numVtx))
        s_skinNode = meshSkinNodeList[mesh.index(x)]
        x_DST = D_skinTool(s_skinNode)
        x_weightInfo = x_DST.exportWeights()
        d_typeWeightList = numpy.matrix(numpy.array_split(x_weightInfo[1], numVtx + 1)).T.tolist()
        d_typeWeight = []
        for x in d_typeWeightList:
            d_typeWeight.extend(x)
        newWeight = numpy.array(x_bsWeights * len(x_weightInfo[0])) * numpy.array(d_typeWeight)
        splitList = numpy.array_split(newWeight, len(x_weightInfo[0]))
        i_index = 0
        for i in splitList:
            secInf = x_weightInfo[0][i_index]
            allWeights.update({secInf: i})
            i_index = i_index + 1
    onlyWeights = []
    for x in inf_Index:
        jointName = inf_Index[x]
        onlyWeights.append(allWeights[jointName])
    onlyWeightsMatrix = numpy.matrix(onlyWeights).T
    onlyWeightsMatrix = onlyWeightsMatrix.tolist()
    onlyWeights = []
    for x in onlyWeightsMatrix:
        onlyWeights.extend(x)
    combineWeights[1] = om.MDoubleArray(onlyWeights)
    combineSkin.importWeights(combineWeights)
