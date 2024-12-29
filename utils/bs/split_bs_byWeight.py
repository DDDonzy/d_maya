import numpy as np
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
from functools import partial
import time


class BaseCallBack(object):
	def __init__(self, func, *args, **kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs


class UndoCallback(BaseCallBack):
	def __call__(self, *args):
		cmds.undoInfo(openChunk=1)
		try:
			return self.func(*self.args, **self.kwargs)
		finally:
			cmds.undoInfo(closeChunk=1)


class D_skinTool(oma.MFnSkinCluster):

	def __init__(self, skinNodeName):
		self.skinNodeName = skinNodeName
		self.reload(skinNodeName)

	def reload(self, skinNodeName):
		skinNodeMObject = self.toApiMObject(skinNodeName)
		oma.MFnSkinCluster.__init__(self, skinNodeMObject)

	def toApiMObject(self, name):
		MSelectionList = om.MSelectionList().add(name)
		MObject = MSelectionList.getDependNode(0)
		return MObject

	def toApiMDagPath(self, name):
		MSelectionList = om.MSelectionList().add(name)
		MDagPath = MSelectionList.getDagPath(0)
		return MDagPath

	def getNameByDagPath(self, dagPath):
		MSelectionList = om.MSelectionList().add(dagPath)
		stringName = om.MFnDependencyNode(MSelectionList.getDependNode(0)).name()
		return stringName

	def getShape(self):
		shape = cmds.skinCluster(self.skinNodeName, q=True, g=True)
		return shape

	def getSkinWeights(self, *infIndex):
		meshMObject = self.toApiMDagPath(self.getShape()[0])
		singleIdComp = om.MFnSingleIndexedComponent()
		vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)

		weightData = self.getWeights(meshMObject, vertexComp, *infIndex)
		return weightData

	def getInfluenceIndex(self, influenceName):
		influenceIndex = cmds.skinCluster(self.skinNodeName, q=1, inf=1).index(influenceName)
		return influenceIndex

	def setInfluenceWeights(self, influenceIndex, weights):
		meshMObject = self.toApiMDagPath(self.getShape()[0])

		singleIdComp = om.MFnSingleIndexedComponent()
		vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)
		try:
			influenceIndexArray = om.MIntArray().append(influenceIndex)
		except:
			influenceIndexArray = influenceIndex

		self.setWeights(meshMObject, vertexComp, influenceIndexArray, weights, normalize=True, returnOldWeights=False)

	def exportWeights(self):
		weightsInfo = self.getSkinWeights()
		influenceNameList = self.influenceObjects()
		influenceNameList = [self.getNameByDagPath(x) for x in influenceNameList]
		weights = weightsInfo[0]
		influenceNum = weightsInfo[-1]
		influenceIndexDict = {}
		for x in range(len(influenceNameList)):
			influenceIndexDict.update({str(x): influenceNameList[x]})
		return influenceIndexDict, weights


class separateBlendshape():
	def showUI(self):
		if cmds.window('separateBlendshape_ui', q=1, ex=1): cmds.deleteUI('separateBlendshape_ui')
		win = cmds.window('separateBlendshape_ui')
		cmds.window(win, e=1, wh=[400, 155], title='SeparateBS by skin', s=0)
		c_layout = cmds.columnLayout(p=win, adj=1)
		cmds.separator(p=c_layout, h=20)
		self.skin_textFieldButtonGrp = cmds.textFieldButtonGrp(p=c_layout, label='Skin Mesh    :',
															   buttonLabel='Load Mesh', adjustableColumn3=1,
															   columnAlign3=['left', 'left', 'left'],
															   buttonCommand=partial(self.loadSkinMesh))
		self.target_textFieldButtonGrp = cmds.textFieldButtonGrp(p=c_layout, label='Target Mesh :',
																 buttonLabel='Load Mesh', adjustableColumn3=1,
																 columnAlign3=['left', 'left', 'left'],
																 buttonCommand=partial(self.loadTargetMesh))
		cmds.separator(p=c_layout, h=30)
		cmds.button(p=c_layout, l='Separate', h=30, command=UndoCallback(self.separateButton))
		cmds.separator(p=c_layout, style='none', h=5)
		cmds.text('by:Donzy      ', p=c_layout, h=15, align='right')
		cmds.separator(p=c_layout, style='none', h=5)
		cmds.showWindow(win)

	def loadSkinMesh(self):
		try:
			sel = cmds.ls(sl=1)[0]
			cmds.textFieldButtonGrp(self.skin_textFieldButtonGrp, e=1, text=sel)
		except:
			pass

	def loadTargetMesh(self):
		try:
			sel = cmds.ls(sl=1)[0]
			cmds.textFieldButtonGrp(self.target_textFieldButtonGrp, e=1, text=sel)
		except:
			pass

	def getSkinNode(self, mesh):
		hisList = cmds.listHistory(mesh, pdo=1)
		for x in hisList:
			if cmds.objectType(x) == 'skinCluster':
				return x

	def separateButton(self):
		goON = True
		skin_mesh = cmds.textFieldButtonGrp(self.skin_textFieldButtonGrp, q=1, text=1)
		target_mesh = cmds.textFieldButtonGrp(self.target_textFieldButtonGrp, q=1, text=1)
		for x in [skin_mesh, target_mesh]:
			shapes = cmds.listRelatives(x, s=1)[0]
			if cmds.objectType(shapes) != 'mesh':
				om.MGlobal.displayError('Mesh has been error')
				goON = False

		if goON == False:
			om.MGlobal.displayError('Mesh has been error')
		else:
			skinNode = D_skinTool(self.getSkinNode(skin_mesh))
			skinInfluenceList = cmds.skinCluster(skin_mesh, q=1, inf=1)
			for x in skinInfluenceList:
				x_index = skinNode.getInfluenceIndex(x)
				weigth = skinNode.getSkinWeights(x_index)
				x_outputShape_d = cmds.createNode('mesh')
				x_output_d = cmds.listRelatives(x_outputShape_d, parent=1)[0]
				cmds.connectAttr(skin_mesh + '.outMesh', x_outputShape_d + '.inMesh')
				x_output = cmds.duplicate(x_output_d, name='separateMesh_%s' % x_index)[0]
				cmds.delete(x_output_d)
				x_bs = cmds.blendShape(target_mesh, x_output)[0]
				cmds.blendShape(x_bs, e=1, w=[(0, 1)])
				vtxNum = cmds.getAttr(skin_mesh + '.vrts', s=1)
				bsAttr_longName = x_bs + '.inputTarget[0]' + '.inputTargetGroup[0]' + '.targetWeights[0:%s]' % (
						vtxNum - 1)
				cmds.setAttr(bsAttr_longName, *weigth)
				x_outputTarget = cmds.duplicate(x_output, name='separateTargetMesh_%s' % x_index)
				dupShapes = cmds.listRelatives(x_outputTarget, s=1)
				for s in dupShapes:
					if 'Orig' in s:
						cmds.delete(s)
				cmds.delete(x_output)


a = separateBlendshape()
a.showUI()
