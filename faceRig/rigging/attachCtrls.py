from imp import reload
from pymel.core import *
import rigTool as rigTool ; reload(rigTool)
def attachCtrls(mesh = '' , ctrlsList = []):
	mesh = PyNode(mesh)
	meshShape = mesh.getShapes()[0]
	ctrlsList = [PyNode(x) for x in ctrlsList]

	for x in ctrlsList :
		follicleShape = createNode('follicle' , name = x.name()+'_attachFollicleShape')
		follicle = follicleShape.getParent()
		meshShape.outMesh>>follicleShape.inputMesh
		cpom = createNode('closestPointOnMesh' , name = 'Temp_closestPointOnMesh')
		meshShape.outMesh >> cpom.inMesh
		cpom.inPosition.set(xform(x,q=1,t=1,ws=1))
		follicleShape.parameterU.set(cpom.parameterU.get())
		follicleShape.parameterV.set(cpom.parameterV.get())
		follicleShape.outTranslateX>>follicle.tx
		follicleShape.outTranslateY>>follicle.ty
		follicleShape.outTranslateZ>>follicle.tz

		follicleShape.outRotateX>>follicle.rx
		follicleShape.outRotateY>>follicle.ry
		follicleShape.outRotateZ>>follicle.rz
		x.rename(x.name()+'___Temp')
		rigTool.addGroup(obj=x.name(),objSuffix='___Temp',grpSuffixList=['_AttachOppsite_GRP','_AttachCon_GRP','_AttachGRP'])
		x.rename(x.name().replace('___Temp' , ''))
		xOppsite =PyNode(x.name()+'_AttachOppsite_GRP')
		xGRP = PyNode(x.name()+'_AttachGRP')
		delete(cpom)
		DPM = createNode('decomposeMatrix' , name = x.name()+'_DecomposeMatrix')
		x.inverseMatrix>>DPM.inputMatrix
		DPM.outputTranslateX>>xOppsite.tx
		DPM.outputTranslateY>>xOppsite.ty
		DPM.outputTranslateZ>>xOppsite.tz
		DPM.outputRotateX>>xOppsite.rx
		DPM.outputRotateY>>xOppsite.ry
		DPM.outputRotateZ>>xOppsite.rz
		#DPM.outputScaleX>>xOppsite.sx
		#DPM.outputScaleY>>xOppsite.sy
		#DPM.outputScaleZ>>xOppsite.sz

		parentConstraint(follicle , xGRP , mo = 1 )