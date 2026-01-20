# !/usr/bin/python
# -*- coding: utf-8 -*-
import json
from imp import reload
from maya import cmds
import pymel.core as pm
from ..UI import mainProgress as UI


def findBw(inputObj):
	with pm.UndoChunk():
		blendWList = []
		upObj = pm.listConnections(inputObj, scn=True, s=True, d=False)
		for i in upObj:
			if pm.nodeType(i) == 'blendWeighted':
				blendWList.append(i)
			elif pm.nodeType(i) == 'addDoubleLinear':
				bw = pm.listConnections(i, scn=True, s=True, d=False)[0]
				blendWList.append(bw)
		return blendWList


def addMatrix(parentCtl='', childCtl='', childCtlOffect='', attrPlace='', value=1, parentGRP=['CTL_SDK', 'CTL_Matrix'],
			  addPass=False):
	with pm.UndoChunk():
		baseParentCtl = parentCtl
		baseChildCtl = childCtl
		if pm.objExists(pm.PyNode(childCtl).name() + '_getParent'):
			getParentOBJ = pm.PyNode(pm.PyNode(childCtl).name() + '_getParent')
			if pm.PyNode(parentCtl).name() in eval(getParentOBJ.parentInfomation.get()):
				deleteMatrix(childCtl, parentCtl)
		matrixInfoGRP = 'MatrixNodesInfo_GRP'
		if pm.objExists(matrixInfoGRP) == False:
			matrixInfoGRP = pm.group(em=1, name='MatrixNodesInfo_GRP')
		for attr in pm.PyNode(parentCtl).listAttr(ud=1):
			if 'matrixBase' in attr.name():
				parentCtl = pm.PyNode(attr.get())
		if pm.objExists(pm.PyNode(childCtl).name() + '_getParent'):
			getParentOBJ = pm.PyNode(pm.PyNode(childCtl).name() + '_getParent')
			if pm.PyNode(parentCtl).name() in eval(getParentOBJ.parentInfomation.get()):
				deleteMatrix(childCtl, parentCtl)
		parentCtl = pm.PyNode(parentCtl)
		childCtl = pm.PyNode(childCtl)
		childCtlOffect = pm.PyNode(childCtlOffect)
		prefix = pm.PyNode(parentCtl).name() + '_' + pm.PyNode(childCtl).name()
		attrsPrefix = pm.PyNode(parentCtl).name()
		####	getParentNode
		if pm.objExists(pm.PyNode(childCtl).name() + '_getParent'):
			getParentInfo = pm.PyNode(pm.PyNode(childCtl).name() + '_getParent')
		else:
			getParentInfo = pm.group(em=1, name=pm.PyNode(childCtl).name() + '_getParent')
			pm.parent(getParentInfo, matrixInfoGRP)
			pm.addAttr(getParentInfo, ln='parentInfomation', dt='string')
			pm.addAttr(getParentInfo, ln='nodesInfomation', dt='string')
			pm.addAttr(getParentInfo, ln='attrsInfomation', dt='string')
			pm.setAttr(getParentInfo.parentInfomation, '[]', type='string')
			pm.setAttr(getParentInfo.nodesInfomation, '[]', type='string')
			pm.setAttr(getParentInfo.attrsInfomation, '[]', type='string')
			for x in getParentInfo.listAttr(k=1):
				x.lock()
				pm.setAttr(x, k=0)
		parentInfomation = eval(getParentInfo.parentInfomation.get())
		nodesInfomation = eval(getParentInfo.nodesInfomation.get())
		addNodesInfomation = []
		attrsInfomation = eval(getParentInfo.attrsInfomation.get())
		addAttrsInfomation = []
		####	 getChildrenNode
		if pm.objExists(pm.PyNode(baseParentCtl).name() + '_getChildren'):
			getChildrenInfo = pm.PyNode(pm.PyNode(baseParentCtl).name() + '_getChildren')
		else:
			getChildrenInfo = pm.group(em=1, name=pm.PyNode(baseParentCtl).name() + '_getChildren')
			pm.parent(getChildrenInfo, matrixInfoGRP)
			pm.addAttr(getChildrenInfo, ln='childrenInfomation', dt='string')
			pm.setAttr(getChildrenInfo.childrenInfomation, '[]', type='string')
			for x in getChildrenInfo.listAttr(k=1):
				x.lock()
				pm.setAttr(x, k=0)
		childrenInfomation = eval(getChildrenInfo.childrenInfomation.get())
		childrenInfomation.append(pm.PyNode(childCtl).name())
		pm.setAttr(getChildrenInfo.childrenInfomation, str(childrenInfomation), type='string')
		attrPlace = getParentInfo
		## step 1: FBF_matrix create (parent-->child)  get Node: dec_mtx
		# Find out loc Matrix
		loc = pm.spaceLocator()
		pm.delete(pm.parentConstraint(childCtl, loc, mo=False))
		pm.parent(loc, parentCtl)
		mtx = loc.getMatrix()
		pm.delete(loc)

		mtxLs = []  # loc Matrix list
		for i in mtx:
			for j in i:
				mtxLs.append(j)
		# matrix transfer
		fbf = pm.createNode('fourByFourMatrix', n=prefix + '_Fbf')
		addNodesInfomation.append(fbf.name())
		fbflis = ['in00', 'in01', 'in02', 'in03', 'in10', 'in11', 'in12', 'in13', 'in20', 'in21', 'in22', 'in23',
				  'in30',
				  'in31', 'in32', 'in33']
		for i in range(len(fbflis)):
			pm.setAttr('%s%s%s' % (fbf, '.', fbflis[i]), mtxLs[i])
		mult_mtx = pm.createNode('multMatrix', n=prefix + '_Multmtx')
		inv_mtx = pm.createNode('inverseMatrix', n=prefix + '_Invmtx')
		dec_mtx = pm.createNode('decomposeMatrix', n=prefix + '_Decmtx')
		addNodesInfomation.append(mult_mtx.name())
		addNodesInfomation.append(inv_mtx.name())
		addNodesInfomation.append(dec_mtx.name())
		pm.PyNode('%s%s' % (parentCtl, '.matrix')) >> mult_mtx.matrixIn[1]
		fbf.output >> mult_mtx.matrixIn[0]
		fbf.output >> inv_mtx.inputMatrix
		inv_mtx.outputMatrix >> mult_mtx.matrixIn[2]
		mult_mtx.matrixSum >> dec_mtx.inputMatrix
		## step 2 : blendWeighted connections
		# dec_mtx output list
		decLs = []
		decAtr = ['outputTranslateX', 'outputTranslateY', 'outputTranslateZ', 'outputRotateX', 'outputRotateY',
				  'outputRotateZ', 'outputScaleX', 'outputScaleY', 'outputScaleZ']
		for k in decAtr:
			dl = pm.PyNode('%s.%s' % (dec_mtx, k))
			decLs.append(dl)
		# branch
		# add overall attribute
		pm.addAttr(attrPlace, ln='%s' % (prefix + '_Weight'), nn='%s' % (attrsPrefix + '_Weight'), at='float', dv=0)
		addAttrsInfomation.append(attrPlace + '.%s' % (prefix + '_Weight'))
		pm.setAttr('%s.%s' % (attrPlace, prefix + '_Weight'), e=True, channelBox=True, keyable=False)
		als = []
		attrLs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
		for i in attrLs:
			pm.addAttr(attrPlace, ln='%s_%s' % (prefix + '_Weight', i), nn='%s_%s' % (attrsPrefix + '_Weight', i),
					   at='float', dv=value, k=True)
			als.append('%s_%s' % (prefix + '_Weight', i))
			addAttrsInfomation.append(attrPlace + '.%s_%s' % (prefix + '_Weight', i))
		if pm.listConnections(childCtlOffect, type='blendWeighted') == []:
			attrOp = []
			attrLs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
			for i in attrLs:
				eg = pm.PyNode('%s.%s' % (childCtlOffect, i))
				attrOp.append(eg)
			for i in range(len(als) - 3):
				attrIp = pm.PyNode('%s.%s' % (attrPlace, als[i]))
				bw = pm.createNode('blendWeighted', n='%s_%s' % (als[i], 'Bw'))
				attrIp >> bw.weight[0]
				bw.output >> attrOp[i]
				decLs[i] >> bw.input[0]
			for j in range(6, len(als)):
				atls = pm.PyNode('%s.%s' % (attrPlace, als[j]))
				bw = pm.createNode('blendWeighted', n='%s_%s' % (als[j], 'Bw'))
				adlF = pm.createNode('addDoubleLinear', n='%s_%s' % (als[j], 'F_Adl'))
				addNodesInfomation.append(adlF.name())
				adlF.input2.set(-1)
				atls >> bw.weight[0]
				decLs[j] >> adlF.input1
				adlF.output >> bw.input[0]
				adlD = pm.createNode('addDoubleLinear', n='%s_%s' % (als[j], 'D_Adl'))
				adlD.input2.set(1)
				bw.output >> adlD.input1
				adlD.output >> attrOp[j]
		else:
			bwLs = pm.listConnections(childCtlOffect, type='blendWeighted')
			numLs = []
			bw = pm.PyNode(bwLs[0])
			bw_indexBool = False
			bw_index = 0
			while (bw_indexBool == False):
				inputList = bw.input[bw_index].inputs()
				if inputList == []:
					bw_indexBool = True
					num = bw_index
				bw_index = bw_index + 1
			# blendWeight num add
			bWight = findBw(childCtlOffect)
			for i in range(len(bWight) - 3):
				atls = pm.PyNode('%s.%s' % (attrPlace, als[i]))
				atls >> bWight[i].weight[int(num)]
				decLs[i] >> bWight[i].input[int(num)]
			for j in range(6, len(als)):
				atls = pm.PyNode('%s.%s' % (attrPlace, als[j]))
				adlF = pm.createNode('addDoubleLinear', n='%s_%s' % (als[j], 'F_Adl'))
				adlF.input2.set(-1)
				atls >> bWight[j].weight[int(num)]
				decLs[j] >> adlF.input1
				adlF.output >> bWight[j].input[int(num)]
		parentInfomation.append(pm.PyNode(baseParentCtl).name())
		pm.setAttr(getParentInfo.parentInfomation, str(parentInfomation), type='string')
		nodesInfomation.append(addNodesInfomation)
		pm.setAttr(getParentInfo.nodesInfomation, str(nodesInfomation), type='string')
		attrsInfomation.append(addAttrsInfomation)
		pm.setAttr(getParentInfo.attrsInfomation, str(attrsInfomation), type='string')
		######   parentGRP
		for x in parentGRP:
			n = ''
			for i in parentCtl.name().split('_')[0:-1]:
				n = n + i + '_'
			grpName = n + x
			grp = pm.PyNode(grpName)
			if grp in mult_mtx.inputs():
				pass
				# print(grp.name() + '__' in 'mult_mtx')
			else:
				inv_mtx.outputMatrix // mult_mtx.matrixIn[len(mult_mtx.matrixIn.inputs()) - 1]
				grp.matrix >> mult_mtx.matrixIn[len(mult_mtx.matrixIn.inputs())]
				inv_mtx.outputMatrix >> mult_mtx.matrixIn[len(mult_mtx.matrixIn.inputs())]
		if addPass is True:
			addPassAttr(passObj=parentCtl, inputObj=childCtl)
		return addAttrsInfomation


def replaceObjAttr(inputObj, replaceObj):
	with pm.UndoChunk():
		inputObj = pm.PyNode(inputObj)
		if pm.objExists(inputObj.name() + '.matrixBase'):
			# print(inputObj.name() + ' already has matrixBase')
			pass
		else:
			pm.addAttr(inputObj, ln='matrixBase', dt='string')
			inputObj.matrixBase.set(str(pm.PyNode(replaceObj).name()))


def findChildren(inputObj, selectMode=False):
	with pm.UndoChunk():
		inputObj = pm.PyNode(inputObj)
		if pm.objExists(inputObj.name() + '_getChildren'):
			inputObj = pm.PyNode(inputObj.name() + '_getChildren')
			for attr in inputObj.listAttr(ud=1):
				if 'childrenInfomation' in attr.name():
					childrenList = eval(inputObj.childrenInfomation.get())
		if selectMode == True: pm.select(childrenList)
		return childrenList


def findParent(inputObj, selectMode=False):
	with pm.UndoChunk():
		parentList = []
		inputObj = pm.PyNode(inputObj)
		if pm.objExists(inputObj.name() + '_getParent'):
			inputObj = pm.PyNode(inputObj.name() + '_getParent')
			for attr in inputObj.listAttr(ud=1):
				if 'parentInfomation' in attr.name():
					parentList = eval(inputObj.parentInfomation.get())
		if selectMode == True: pm.select(parentList)
		return parentList


def deleteMatrix(inputChild, inputParent=None):
	with pm.UndoChunk():
		baseInput = inputParent
		try:
			for attr in pm.PyNode(inputParent).listAttr(ud=1):
				if 'matrixBase' in attr.name():
					inputParent = attr.get()
			if pm.objExists(pm.PyNode(inputChild).name() + '_getParent'):
				childrenInfo = pm.PyNode(pm.PyNode(inputChild).name() + '_getParent')
				children_parent = eval(childrenInfo.parentInfomation.get())
				attrsInfomation = eval(childrenInfo.attrsInfomation.get())
				nodesInfomation = eval(childrenInfo.nodesInfomation.get())

				if inputParent != None:
					parentInfo = pm.PyNode(pm.PyNode(inputParent).name() + '_getChildren')
					parent_children = eval(pm.PyNode(parentInfo).childrenInfomation.get())
					listIndex = children_parent.index(inputParent)
					for x in attrsInfomation[listIndex][1:]:
						x = pm.PyNode(x)
						x.set(0)
						BW = x.outputs()[0]
						BW_Weight = x.outputs(p=1)[0]
						BW_Index = int(BW_Weight.name()[BW_Weight.name().index('[') + 1:BW_Weight.name().index(']')])
						x // BW_Weight
						BW_Weight.set(0)
						BW_Input = BW.input[BW_Index]
						BW_Input.inputs(p=1)[0] // BW_Input
						BW_Input.set(0)
						if BW.inputs() == []:
							pm.delete(BW)
					pm.deleteAttr(attrsInfomation[listIndex])
					pm.delete(nodesInfomation[listIndex])
					children_parent.remove(inputParent)
					parent_children.remove(inputChild)
					nodesInfomation.remove(nodesInfomation[listIndex])
					attrsInfomation.remove(attrsInfomation[listIndex])
					pm.setAttr(childrenInfo.parentInfomation, str(children_parent), type='string')
					pm.setAttr(childrenInfo.nodesInfomation, str(nodesInfomation), type='string')
					pm.setAttr(childrenInfo.attrsInfomation, str(attrsInfomation), type='string')
					pm.setAttr(parentInfo.childrenInfomation, str(parent_children), type='string')
				else:
					xh = children_parent[::]
					for p in xh:
						parentInfo = pm.PyNode(pm.PyNode(p).name() + '_getChildren')
						parent_children = eval(pm.PyNode(parentInfo).childrenInfomation.get())
						listIndex = children_parent.index(p)
						for x in attrsInfomation[listIndex][1:]:
							x = pm.PyNode(x)
							x.set(0)
							BW = x.outputs()[0]
							BW_Weight = x.outputs(p=1)[0]
							BW_Index = int(
								BW_Weight.name()[BW_Weight.name().index('[') + 1:BW_Weight.name().index(']')])
							x // BW_Weight
							BW_Weight.set(0)
							BW_Input = BW.input[BW_Index]
							BW_Input.inputs(p=1)[0] // BW_Input
							BW_Input.set(0)
							if BW.inputs() == []:
								pm.delete(BW)
						pm.deleteAttr(attrsInfomation[listIndex])
						pm.delete(nodesInfomation[listIndex])
						children_parent.remove(p)
						parent_children.remove(inputChild)
						nodesInfomation.remove(nodesInfomation[listIndex])
						attrsInfomation.remove(attrsInfomation[listIndex])
						pm.setAttr(childrenInfo.parentInfomation, str(children_parent), type='string')
						pm.setAttr(childrenInfo.nodesInfomation, str(nodesInfomation), type='string')
						pm.setAttr(childrenInfo.attrsInfomation, str(attrsInfomation), type='string')
						pm.setAttr(parentInfo.childrenInfomation, str(parent_children), type='string')
		except:
			inputParent = baseInput
			if pm.objExists(pm.PyNode(inputChild).name() + '_getParent'):
				childrenInfo = pm.PyNode(pm.PyNode(inputChild).name() + '_getParent')
				children_parent = eval(childrenInfo.parentInfomation.get())
				attrsInfomation = eval(childrenInfo.attrsInfomation.get())
				nodesInfomation = eval(childrenInfo.nodesInfomation.get())

				if inputParent != None:
					parentInfo = pm.PyNode(pm.PyNode(inputParent).name() + '_getChildren')
					parent_children = eval(pm.PyNode(parentInfo).childrenInfomation.get())
					listIndex = children_parent.index(inputParent)
					for x in attrsInfomation[listIndex][1:]:
						x = pm.PyNode(x)
						x.set(0)
						BW = x.outputs()[0]
						BW_Weight = x.outputs(p=1)[0]
						BW_Index = int(BW_Weight.name()[BW_Weight.name().index('[') + 1:BW_Weight.name().index(']')])
						x // BW_Weight
						BW_Weight.set(0)
						BW_Input = BW.input[BW_Index]
						BW_Input.inputs(p=1)[0] // BW_Input
						BW_Input.set(0)
						if BW.inputs() == []:
							pm.delete(BW)
					pm.deleteAttr(attrsInfomation[listIndex])
					pm.delete(nodesInfomation[listIndex])
					children_parent.remove(inputParent)
					parent_children.remove(inputChild)
					nodesInfomation.remove(nodesInfomation[listIndex])
					attrsInfomation.remove(attrsInfomation[listIndex])
					pm.setAttr(childrenInfo.parentInfomation, str(children_parent), type='string')
					pm.setAttr(childrenInfo.nodesInfomation, str(nodesInfomation), type='string')
					pm.setAttr(childrenInfo.attrsInfomation, str(attrsInfomation), type='string')
					pm.setAttr(parentInfo.childrenInfomation, str(parent_children), type='string')
				else:
					xh = children_parent[::]
					for p in xh:
						parentInfo = pm.PyNode(pm.PyNode(p).name() + '_getChildren')
						parent_children = eval(pm.PyNode(parentInfo).childrenInfomation.get())
						listIndex = children_parent.index(p)
						for x in attrsInfomation[listIndex][1:]:
							x = pm.PyNode(x)
							x.set(0)
							BW = x.outputs()[0]
							BW_Weight = x.outputs(p=1)[0]
							BW_Index = int(
								BW_Weight.name()[BW_Weight.name().index('[') + 1:BW_Weight.name().index(']')])
							x // BW_Weight
							BW_Weight.set(0)
							BW_Input = BW.input[BW_Index]
							BW_Input.inputs(p=1)[0] // BW_Input
							BW_Input.set(0)
							if BW.inputs() == []:
								pm.delete(BW)
						pm.deleteAttr(attrsInfomation[listIndex])
						pm.delete(nodesInfomation[listIndex])
						children_parent.remove(p)
						parent_children.remove(inputChild)
						nodesInfomation.remove(nodesInfomation[listIndex])
						attrsInfomation.remove(attrsInfomation[listIndex])
						pm.setAttr(childrenInfo.parentInfomation, str(children_parent), type='string')
						pm.setAttr(childrenInfo.nodesInfomation, str(nodesInfomation), type='string')
						pm.setAttr(childrenInfo.attrsInfomation, str(attrsInfomation), type='string')
						pm.setAttr(parentInfo.childrenInfomation, str(parent_children), type='string')


def addMatrix2():
	with pm.UndoChunk():
		parentCtl = pm.selected()[0]
		childrenCtl = pm.selected()[1:]
		for x in childrenCtl:
			addMatrix(parentCtl=parentCtl, childCtl=x, childCtlOffect=x.name() + '_Matrix', attrPlace='', value=1)


def deleteMatrix2():
	with pm.UndoChunk():
		parentCtl = pm.selected()[0]
		childrenCtl = pm.selected()[1:]
		for x in childrenCtl:
			deleteMatrix(x, parentCtl)


def findWeightObj(inputObj, selectMode=False):
	with pm.UndoChunk():
		try:
			inputObj = pm.PyNode(inputObj)
			weightObj = pm.PyNode(inputObj.name() + '_getParent')
			if selectMode == True:
				pm.select(weightObj)
			return weightObj
		except:
			pass


def addPassAttr(passObj=None, inputObj=None):
	with pm.UndoChunk():
		if not inputObj:
			passObj = pm.selected()[0:-1]
			inputObj = pm.selected()[1]
		else:
			passObj = [pm.PyNode(passObj)]
			inputObj = pm.PyNode(inputObj)
		inputObj = pm.PyNode(findWeightObj(inputObj))
		if not pm.objExists(inputObj.name() + '.passList'):
			pm.addAttr(inputObj, ln='passList', dt='string')
			pm.setAttr(inputObj.passList, str('[]'), type='string')
		passList = eval(inputObj.passList.get())
		for x in passObj:
			passList.append(x.name())
		pm.setAttr(inputObj.passList, str(passList), type='string')


def mirrorWeight():
	with pm.UndoChunk():
		for x in pm.selected():
			if 'getParent' not in x.name():
				weightObj = findWeightObj(inputObj=x)
				attrs = weightObj.listAttr(ud=1)
			else:
				attrs = x.listAttr(ud=1)
			for a in attrs:
				if 'Weight' in str(a):
					OBJ = None
					Attr = None
					a_str = str(a)
					OBJ = a_str.split('.')[0].split('_')
					Attr = a_str.split('.')[1].split('_')
					if 'L' in OBJ:
						OBJ[OBJ.index('L')] = 'Temp'
					if 'R' in OBJ:
						OBJ[OBJ.index('R')] = 'L'
					if 'Temp' in OBJ:
						OBJ[OBJ.index('Temp')] = 'R'

					for i in Attr:
						if i == 'L':
							Attr[Attr.index(i)] = 'Temp'
					for i in Attr:
						if i == 'R':
							Attr[Attr.index(i)] = 'L'
					for i in Attr:
						if i == 'Temp':
							Attr[Attr.index(i)] = 'R'

					oppsiteOBJ = OBJ[0]
					for i in OBJ[1:]:
						oppsiteOBJ = oppsiteOBJ + '_' + i
					oppsiteAttr = Attr[0]
					for i in Attr[1:]:
						oppsiteAttr = oppsiteAttr + '_' + i
					try:
						oppsite = pm.PyNode(oppsiteOBJ + '.' + oppsiteAttr)
						oppsite.set(a.get())
					except:
						pass


def mirrorMtx(OBJList=[]):
	with pm.UndoChunk():
		if OBJList == []:
			OBJList = pm.selected()
		for OBJ in OBJList:
			OBJ = pm.PyNode(OBJ)
			parentInfo = pm.PyNode(findWeightObj(inputObj=OBJ))
			passList = []
			if 'passList' in parentInfo.listAttr(ud=1):
				passList = eval(parentInfo.passList.get())
			if 'L' in OBJ.name():
				oppsiteOBJ = OBJ.name().replace('L_', 'Temp_')
			if 'R' in OBJ.name():
				oppsiteOBJ = OBJ.name().replace('R_', 'L_')
			if 'Temp_' in oppsiteOBJ:
				oppsiteOBJ = oppsiteOBJ.replace('Temp_', 'R_')
			oppsiteOBJ = pm.PyNode(oppsiteOBJ)

			parentList = list(set(findParent(inputObj=OBJ)) ^ set(passList))
			oppsiteParentList_like = []
			for x in parentList:
				if 'L_' in x:
					x = x.replace('L_', 'Temp_')
				if 'R_' in x:
					x = x.replace('R_', 'L_')
				if 'Temp_' in x:
					x = x.replace('Temp_', 'R_')
				oppsiteParentList_like.append(x)
			outParentGRP = []
			for i in parentList:
				if i not in passList:
					###  get parentGRP
					multMtx = pm.PyNode(eval(parentInfo.nodesInfomation.get())[parentList.index(i)][1])
					inputs = [n.name() for n in multMtx.inputs()]
					l = list(set(inputs) ^ set(
						[i] + [eval(parentInfo.nodesInfomation.get())[parentList.index(i)][0]] + [
							eval(parentInfo.nodesInfomation.get())[parentList.index(i)][2]]))
					for o in l:
						if 'CTL_Matrix' in o:
							outParentGRP.append('CTL_Matrix')
						if 'CTL_SDK' in o:
							outParentGRP.append('CTL_SDK')
			oppsiteParentList_like = list(set(oppsiteParentList_like) ^ set(findParent(inputObj=oppsiteOBJ)))
			for p in oppsiteParentList_like:
				addMatrix(parentCtl=p, childCtl=oppsiteOBJ.name(), childCtlOffect=oppsiteOBJ.name() + '_Matrix',
						  value=1, parentGRP=outParentGRP, addPass=False)
			pm.select(OBJ)
			mirrorWeight()


def exportMtx():
	with pm.UndoChunk():
		path = pm.fileDialog2(dialogStyle=2, caption="Export matrix", fileFilter="Matrix information Files (*.mtx)")[0]
		sl = pm.selected()
		if sl == []:
			sl = pm.ls('*_getParent')
		else:
			sl = [findWeightObj(x, 0) for x in sl]
		exportDirt = {}
		for x in sl:
			x = pm.PyNode(x)
			try:
				key = x.name().replace('_getParent', '')
				try:
					passList = eval(x.passList.get())
				except:
					passList = []
				parentList = eval(x.parentInfomation.get())
				outParent = []
				outParentGRP = []
				for i in parentList:
					if i not in passList:
						outParent.append(i)
						###  get parentGRP
						multMtx = pm.PyNode(eval(x.nodesInfomation.get())[parentList.index(i)][1])
						inputs = [n.name() for n in multMtx.inputs()]
						l = list(set(inputs) ^ set([i] + [eval(x.nodesInfomation.get())[parentList.index(i)][0]] + [
							eval(x.nodesInfomation.get())[parentList.index(i)][2]]))
						for o in l:
							if 'CTL_Matrix' in o:
								outParentGRP.append('CTL_Matrix')
							if 'CTL_SDK' in o:
								outParentGRP.append('CTL_SDK')
				weight = []
				a = eval(x.attrsInfomation.get())
				for objAttrs in eval(x.attrsInfomation.get()):
					v = []
					for attr in objAttrs:
						if passList != []:
							for i in passList:
								if eval(x.attrsInfomation.get()).index(objAttrs) != parentList.index(i):
									v.append(pm.PyNode(attr).get())
						else:
							v.append(pm.PyNode(attr).get())
					if v != []: weight.append(v)
				value = []
				value.append(outParent)
				value.append(weight)
				value.append(outParentGRP)
				exportDirt.update({key: value})
			except:
				pass
		with open(path, 'w') as f:
			json.dump(exportDirt, f, indent=4)
		message = '<hl> Export Done </hl>'
		cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)


def importMtx(path=''):
	with pm.UndoChunk():
		if path == '':
			path = \
				pm.fileDialog2(dialogStyle=2, caption="Import matrix", fileFilter="Matrix information Files (*.mtx)",fm=1)[0]
		with open(path,'r') as f:
			importDirt = json.load(f)
		createJointUI = UI.mainProgress(maxValue=len(importDirt),
										status='Import matrix connections...')  ########  MainProgreess  Start
		for key in importDirt:
			if pm.objExists(key):
				# deleteMatrix(inputChild = key)
				parentObjList = importDirt[key][0]
				for parentObj in parentObjList:
					if pm.objExists(parentObj):
						if pm.objExists(key + '_getParent'):
							try:
								passList = eval(pm.PyNode(key + '_getParent').passList.get())
							except:
								passList = []
							if parentObj not in passList:
								try:
									deleteMatrix(inputChild=key, inputParent=parentObj)
								except:
									pass
		for key in importDirt:
			createJointUI.update(1)  ########  MainProgreess  Update
			if pm.objExists(key):
				parentObjList = importDirt[key][0]
				weightValueList = importDirt[key][1]
				parentGRPList = []
				try:
					parentGRPList = importDirt[key][2]
				except:
					pass
				if parentGRPList == []:
					parentGRPList = ['CTL_Matrix', 'CTL_SDK']
				for parentObj in parentObjList:
					if pm.objExists(parentObj):
						parentObjWeightList = weightValueList[parentObjList.index(parentObj)]
						if pm.objExists(key + '_getParent'):
							try:
								passList = eval(pm.PyNode(key + '_getParent').passList.get())
							except:
								passList = []
							if parentObj not in passList:
								NewAttrsList = addMatrix(parentObj, key, key + '_Matrix', parentGRP=parentGRPList)
								for x in NewAttrsList:
									v = parentObjWeightList[NewAttrsList.index(x)]
									x = pm.PyNode(x)
									x.set(v)
						else:
							NewAttrsList = addMatrix(parentObj, key, key + '_Matrix', parentGRP=parentGRPList)
							for x in NewAttrsList:
								v = parentObjWeightList[NewAttrsList.index(x)]
								x = pm.PyNode(x)
								x.set(v)
					else:
						pass
			else:
				pass
		createJointUI.end()
	message = '<hl> Import Done </hl>'
	cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)
