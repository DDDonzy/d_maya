import maya.cmds as cmds
class createRotCenter():
    def __init__(self,inputList=[],name = '',prefix=''):
        self.inputList = inputList
        self.prefix = prefix
        self.name = name
    def createLoc(self):
        locName = '%ssvRotLoc'%self.prefix
        locShape = cmds.createNode('locator',name='%sShape'%locName)
        loc = cmds.listRelatives( locShape, parent=True )[0]
        cmds.delete(cmds.pointConstraint(self.inputList[0],loc,mo=False))
        cmds.setAttr('%s.tx'%loc,0)
        cmds.select(loc,r=True)
    def create(self,changeCtrlsRotate = 1):
        loc = '%ssvRotLoc'%self.prefix
        RotEndList = []
        RotMainGrpName = '%s%s_GRP'%(self.prefix,self.name)
        if cmds.objExists(RotMainGrpName):
            RotMainGrp = RotMainGrpName
        else:
            RotMainGrp = cmds.createNode('transform', name=RotMainGrpName)
            cmds.delete(cmds.parentConstraint(loc, RotMainGrp, mo=False))
        for input in self.inputList:
            RotTranName = '%s%s_RotTran' % (self.prefix,input)
            RotAimName = '%s%s_RotAim' % (self.prefix,input)
            RotEndName = '%s%s_RotEnd' % (self.prefix,input)
            RotConGrpName = '%s_%s_RotConGrp' % (self.prefix, input)
            RotConName = '%s%s_RotCon' % (self.prefix, input)
            RotRotName = '%s%s_RotRot' % (self.prefix, input)
            RotTran = cmds.createNode('transform', name=RotTranName)
            RotAim = cmds.createNode('transform', name=RotAimName)
            RotEnd = cmds.createNode('transform', name=RotEndName)
            RotConGrp = cmds.createNode('transform', name=RotConGrpName)
            RotCon = cmds.createNode('transform', name=RotConName)
            RotRot = cmds.createNode('transform', name=RotRotName)
            cmds.parent(RotTran,RotMainGrp)
            cmds.parent(RotCon, RotConGrp)
            cmds.parent(RotAim, RotConGrp,RotRot,RotTran)
            cmds.parent(RotEnd, RotAim)
            cmds.delete(cmds.parentConstraint(loc,RotTran,mo=False))
            cmds.delete(cmds.parentConstraint(input, RotConGrp, mo=False))
            cmds.aimConstraint(RotCon,RotAim,worldUpObject = RotRot,offset=(0,0,0),weight=1,aimVector=(1,0,0),upVector=(0,1,0),worldUpType='objectrotation',worldUpVector=(0,1,0))
            cmds.delete(cmds.parentConstraint(input,RotEnd,mo=False))
            cmds.addAttr(RotEnd, ln='Rot', at="double")
            cmds.setAttr('%s.Rot' % RotEnd, e=True, keyable=True)
            cmds.connectAttr('%s.translate' % input, '%s.translate' % RotCon)
            cmds.connectAttr('%s.Rot' % RotEnd, '%s.rotateX' % RotRot)
            RotEndList.append(RotEnd)
        returnList = [RotMainGrp,RotEndList]
        return returnList
seled = cmds.ls(sl=True)
CRot = createRotCenter(seled,name = 'Mouth')
CRot.createLoc()
CRot.create()
