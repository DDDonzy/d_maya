from imp import reload

from pymel.core import *
import maya.cmds as cmds

from ..matrixTool import matrixTool as matrix
from .rigTool import addGroup



class spherePath():
	def __init__(self, loc=''):
		with UndoChunk():
			if loc == '':
				self.loc = spaceLocator(name='Position_LOC')
				select(self.loc)
				message = '<hl> Please move the locator ! </hl>'
				inViewMessage(amg=message, pos='midCenterBot', fade=True)
			else:
				self.loc = loc

	def doSets(self, inputObj, aimVector=[0, 0, 1], addDepthAttr=False, changeSoure=False, matrixReplace=False,
			   prefix=''):
		with UndoChunk():
			inputObj = PyNode(inputObj)
			rootGRP = group(em=1, name=prefix + 'spherePath_GRP')
			start = group(em=1, name=prefix + 'spherePath_start')
			endGRP = group(em=1, name=prefix + 'spherePath_endGRP')
			end = group(em=1, name=prefix + 'spherePath_end')
			pos = group(em=1, name=prefix + '_pos')
			delete(parentConstraint(inputObj, pos))
			delete(parentConstraint(self.loc, start))
			delete(parentConstraint(inputObj, endGRP))
			delete(aimConstraint(endGRP, start, aimVector=aimVector))
			parent(end, endGRP)
			parent(endGRP, start)
			parent(pos, rootGRP)
			parent(start, rootGRP)
			end.rotate.set([0, 0, 0])
			end.translate.set([0, 0, 0])
			endGRP.rotate.set([0, 0, 0])
			aimConstraint(pos, start, aimVector=aimVector, worldUpType='objectrotation', worldUpObject=inputObj)
			scaleConstraint(pos, endGRP)
			output = group(em=1, name=prefix + 'spherePath_CTL')
			parent(output, rootGRP)
			parentConstraint(end, output)
			scaleConstraint(end, output)
			addGroup(obj=output.name(), objSuffix='CTL', grpSuffix=['CTL_SDK', 'CTL_Matrix', 'CTL_GRP'])
			self.output = output
			if addDepthAttr == True:
				addAttr(inputObj, ln='depth', at='double', k=1)
				inputObj.depth >> end.tz
			if changeSoure == True:
				soure = inputObj.name().replace('CTL', 'CTL_GRP')
				translateList = xform(self.output, q=1, ws=1, t=1)
				rotateList = xform(self.output, q=1, ws=1, ro=1)
				xform(soure, t=translateList, ws=1)
				xform(soure, ro=rotateList, ws=1)
			addGroup(obj=start.name(), objSuffix='_start', grpSuffix=['_start_Matrix', '_start_GRP'])
			addGroup(obj=pos.name(), objSuffix='_pos', grpSuffix=['_pos_Matrix', '_pos_GRP'])
			matrix.addMatrix(PyNode(inputObj).name(), PyNode(pos).name(), PyNode(pos).name() + '_Matrix', addPass=True)
			if matrixReplace == True:
				addAttr(inputObj, ln='matrixBase', dt='string')
				setAttr(inputObj.matrixBase, str(self.output.name()))
			return rootGRP, output, start

	def end(self):
		with UndoChunk():
			delete(self.loc)

