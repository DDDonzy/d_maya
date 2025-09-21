set# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import math
from pymel.core import *
import maya.cmds as cmds


def scaleCtrlsShapes(obj=[], value=1):
    with UndoChunk():
        for x in obj:
            shapes = PyNode(x).getShapes()
            for s in shapes:
                select(s.cv[0:s.numCVs() - 1])
                scale(value, value, value, r=1)
        select(cl=1)


def autoAssignColor(obj=[], gloomy=False):
    with UndoChunk():
        for x in obj:
            shapes = PyNode(x).getShapes()
            for s in shapes:
                s.overrideEnabled.set(1)
                if 'L_' in x and gloomy == False:
                    setAttr(s.name() + '.overrideColor', 6)
                if 'L_' in x and gloomy == True:
                    setAttr(s.name() + '.overrideColor', 29)
                if 'R_' in x and gloomy == False:
                    setAttr(s.name() + '.overrideColor', 13)
                if 'R_' in x and gloomy == True:
                    setAttr(s.name() + '.overrideColor', 4)
                if 'R_' not in x and 'L_' not in x and gloomy == False:
                    setAttr(s.name() + '.overrideColor', 17)
                if 'R_' not in x and 'L_' not in x and gloomy == True:
                    setAttr(s.name() + '.overrideColor', 21)


def alignObj(soure=[], target=[], s=0):
    with UndoChunk():
        for x in target:
            delete(parentConstraint(soure, x))
            if s == 1:
                delete(scaleConstraint(soure, x))


def symmetryCV(obj=selected()):
    with UndoChunk():
        sl = [PyNode(x) for x in obj]
        for x in sl:
            shapes = x.getShapes()
            for z in shapes:
                if 'L_' in z.name():
                    oppsite = PyNode(z.name().replace('L_', 'R_'))
                if 'R_' in z.name():
                    oppsite = PyNode(z.name().replace('R_', 'L_'))
                transformList = z.numCVs()
                for i in range(transformList):
                    pos = z.getCV(i, space='world')
                    xform(oppsite.cv[i], t=[-pos[0], pos[1], pos[2]], ws=1)


def replaceCVShape(soure='', target=[], replace=1):
    with UndoChunk():
        if not soure:
            soure = selected()[0]
        else:
            soure = PyNode(soure)
        if not target:
            target = selected()[1:]
        else:
            target = [PyNode(x) for x in target]
        for x in target:
            if replace == 1:
                delete(x.getShapes())
            tempSoure = duplicate(soure, name='tempSoure')[0]
            tempSoureShape = [rename(i, tempSoure.name() + 'Shape') for i in tempSoure.getShapes()]
            for shape in tempSoureShape:
                parent(shape, x, r=1, s=1)
                shape.rename(x.name() + 'Shape')
            delete(tempSoure)


def mirrorTransform(obj=None, duplicateMode=False):
    with UndoChunk():
        sl = selected()
        if sl == []:
            sl = ls('L_*CTL')
        if type(obj) == str:
            sl = [obj]
        if type(obj) == list:
            sl = obj
        for x in sl:
            if type(obj) == list:
                x = PyNode(x)
            loc = spaceLocator(name='temp')
            delete(parentConstraint(x, loc))
            t = xform(loc, q=1, t=1, ws=1)
            r = xform(loc, q=1, ro=1, ws=1)
            oppsiteT = [-t[0], t[1], t[2]]
            oppsiteR = [-r[0], -r[1] - 180, -r[2]]
            delete(loc)
            if 'L_' in x.name() or 'R_' in x.name():
                if duplicateMode == False:
                    if 'L_' in x.name():
                        oppsiteOBJ = PyNode(x.name().replace('L_', 'R_'))
                    if 'R_' in x.name():
                        oppsiteOBJ = PyNode(x.name().replace('R_', 'L_'))
                else:
                    if 'L_' in x.name():
                        oppsiteOBJ = duplicate(x, name=x.name().replace('L_', 'R_'))[0]
                    if 'R_' in x.name():
                        oppsiteOBJ = duplicate(x, name=x.name().replace('R_', 'L_'))[0]
                xform(oppsiteOBJ, t=oppsiteT, ws=1)
                xform(oppsiteOBJ, ro=oppsiteR, ws=1)
            select(sl)
            inViewMessage(amg='Mirror has been <hl>successful</hl> !', pos='midCenterBot', fade=True)


def addGroup(obj='', objSuffix='', grpSuffix=''):
    if type(obj) != list:
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

    grpSuffixList.reverse()

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


def addCircleShape(obj=[], r=0.1):
    with UndoChunk():
        for x in obj:
            circleCtrl = circle(name=x.name() + 'CircleTemp', nr=[0, 0, 1], r=r)[0]
            circleShape = circleCtrl.getShape()
            cmds.DeleteHistory(circleCtrl)
            parent(circleShape, x, r=1, s=1)
            circleShape.rename(x.name() + 'Shape')
            delete(circleCtrl)


def localRotateAxes(sel=None):
    with UndoChunk():
        if sel == None:
            sel = selected()
            if sel == []:
                sel = ls('*_JNT') + ls('*_Skeleton')
        v = PyNode(sel[0]).displayLocalAxis.get()
        if v == True:
            v = False
        else:
            v = True
        for x in sel:
            PyNode(x).displayLocalAxis.set(v)


class JointsOnSurface(object):
    def __init__(self, prefix='sec1_', point=[]):
        self.prefix = prefix
        self.point = point
        self.RigGroup = None
        self.CtrlGroup = None
        self.ConnectGroup = None
        self.DeformGroup = None
        self.locatorList = []
        self.separateCtrl = None
        self.surface = ''
        self.scaleSurface = ''
        self.jointsList = None

    def rigging(self, scale=False, keepLength=False, volume=False, scaleOffset=False, axis=['x', 'y', 'z'],
                separateCtrl=False, numberOfJoints=20):
        if scaleOffset == True:
            if cmds.objExists('Sec_ScaleOffset_Exp'):
                self.expressionName = 'Sec_ScaleOffset_Exp'
                self.expressionScript = cmds.expression('Sec_ScaleOffset_Exp', q=1, s=1) + '\n%s\n' % (
                        '//////   ' + self.prefix + 'ScaleOffsetExp')
            else:
                self.expressionScript = '%s\n' % ('//////   ' + self.prefix + 'ScaleOffsetExp')
                self.expressionName = cmds.expression(s=self.expressionScript, n='Sec_ScaleOffset_Exp')
        if axis == ['x', 'y', 'z']:
            profilePoint = [[0, -0.1, 0], [0, 0.1, 0]]
        if axis == ['x', 'z', 'y']:
            profilePoint = [[0, 0, -0.1], [0, 0, 0.1]]
        if axis == ['y', 'x', 'z']:
            profilePoint = [[-0.1, 0, 0], [0.1, 0, 0]]
        if axis == ['y', 'z', 'x']:
            profilePoint = [[0, 0, -0.1], [0, 0, 0.1]]
        if axis == ['z', 'x', 'y']:
            profilePoint = [[-0.1, 0, 0], [0.1, 0, 0]]
        if axis == ['z', 'y', 'x']:
            profilePoint = [[0, -0.1, 0], [0, 0.1, 0]]
        #####  group
        self.RigGroup = cmds.group(em=1, name=self.prefix + 'Rig_GRP')
        self.CtrlGroup = cmds.group(em=1, name=self.prefix + 'Control_GRP')
        self.ConnectGroup = cmds.group(em=1, name=self.prefix + 'Connect_GRP')
        self.DeformGroup = cmds.group(em=1, name=self.prefix + 'Deform_GRP')
        SysGroup = cmds.group(em=1, name=self.prefix + 'Sys_GRP')
        LocGroup = cmds.group(em=1, name=self.prefix + 'Loc_GRP')
        cmds.parent(self.CtrlGroup, self.ConnectGroup, self.DeformGroup, self.RigGroup)
        cmds.parent(SysGroup, LocGroup, self.DeformGroup)
        position = []
        cmds.setAttr(self.ConnectGroup + '.inheritsTransform', 0)
        cmds.setAttr(self.DeformGroup + '.inheritsTransform', 0)
        cmds.setAttr(self.ConnectGroup + '.visibility', 0)
        cmds.setAttr(self.DeformGroup + '.visibility', 1)
        cmds.setAttr(SysGroup + '.visibility', 0)
        #####   build surface #####
        for x in self.point:
            OBJposition = cmds.xform(x, query=True, translation=True, worldSpace=True)
            position.append(OBJposition)
        pathCv = cmds.curve(degree=1, point=position, name=self.prefix + 'PathCv_curve')
        pathCvShape = cmds.listRelatives(pathCv, shapes=1)[0]
        profileCv = cmds.curve(degree=1, point=profilePoint, name=self.prefix + 'ProfileCv_curve')
        profileCvShape = cmds.listRelatives(profileCv, shapes=1)[0]
        cmds.delete(cmds.parentConstraint(self.point[0], profileCv))
        surface = cmds.extrude(profileCv, pathCv, et=2, name=self.prefix + 'surface')[0]
        surfaceShape = cmds.listRelatives(surface, shapes=1)[0]
        self.surface = surface
        cmds.DeleteHistory(surface)
        cmds.rebuildSurface(du=1, dv=3, kr=0, kcp=0, kc=0, sv=0, su=0, fr=0, dir=2, rpo=1, rt=0)
        cmds.parent(surface, SysGroup)
        if scaleOffset == True or scale == True:
            scaleSurface = cmds.duplicate(surface, name=self.prefix + 'scale_surface')[0]
            scaleSurfaceShape = cmds.listRelatives(scaleSurface, shapes=1)[0]
            self.scaleSurface = scaleSurface
        cmds.delete(pathCv)
        cmds.delete(profileCv)
        #####  addAttr
        cmds.addAttr(self.RigGroup, ln='FK_Visibility', at='double', dv=1, k=1)
        cmds.addAttr(self.RigGroup, ln='IK_Visibility', at='double', dv=1, k=1)
        if separateCtrl == True:
            cmds.addAttr(self.RigGroup, ln='separate_Visibility', at='double', dv=1, k=1)
        cmds.addAttr(self.RigGroup, ln='globalScale', at='double', dv=1, k=1)
        if scaleOffset == True:
            cmds.addAttr(self.RigGroup, ln='scaleOffset', at='double', k=1)
        if volume == True:
            cmds.addAttr(self.RigGroup, ln='volume', at='double', dv=1, k=1)
            cmds.addAttr(self.RigGroup, ln='globalVolume', at='double', dv=0, k=1)
        if volume == True and keepLength == True:
            cmds.addAttr(self.RigGroup, ln='conditionVolume', at='double', dv=0, k=1)
        if keepLength == True:
            cmds.addAttr(self.RigGroup, ln='stretch', at='double', dv=1, k=1)
            cmds.addAttr(self.RigGroup, ln='conditionStretch', at='double', dv=0, k=1)
        if keepLength == False and volume == False and scaleOffset == False:
            pass
        else:
            cmds.addAttr(self.RigGroup, ln='defaultArcLength', at='double', dv=0, k=1)
            cmds.addAttr(self.RigGroup, ln='arcLength', at='double', dv=0, k=1)
            cmds.addAttr(self.RigGroup, ln='lengthRatio', at='double', dv=0, k=1)
            cmds.addAttr(self.RigGroup, ln='lengthInverseRatio', at='double', dv=0, k=1)
        lenCFSI = cmds.createNode('curveFromSurfaceIso', name=self.prefix + 'spineLength_curveFromSurfaceIso')
        lenCvInfo = cmds.createNode('curveInfo', name=self.prefix + 'spineLength_curveInfo')
        cmds.connectAttr(surfaceShape + '.worldSpace', lenCFSI + '.inputSurface')
        cmds.setAttr(lenCFSI + '.isoparmValue', 0.5)
        cmds.setAttr(lenCFSI + '.isoparmDirection', 1)
        nc = cmds.createNode('nurbsCurve', name=self.prefix + 'lenCurveShape')
        cmds.connectAttr(lenCFSI + '.outputCurve', nc + '.create')
        cmds.setAttr(nc + '.visibility', 1)
        cmds.parent(cmds.listRelatives(nc, p=1), SysGroup)
        cmds.connectAttr(nc + '.worldSpace', lenCvInfo + '.inputCurve')
        if keepLength == False and volume == False and scaleOffset == False:
            pass
        else:
            defLenMD = cmds.createNode('multDoubleLinear', name=self.prefix + 'defLenMD_multDoubleLinear')
            cmds.connectAttr(self.RigGroup + '.globalScale', defLenMD + '.input1')
            cmds.setAttr(defLenMD + '.input2', cmds.getAttr(lenCvInfo + '.arcLength'))
            cmds.connectAttr(defLenMD + '.output', self.RigGroup + '.defaultArcLength')
            cmds.connectAttr(lenCvInfo + '.arcLength', self.RigGroup + '.arcLength')
            lenMD = cmds.createNode('multiplyDivide', name=self.prefix + 'LengthRatio_multiplyDivide')
            cmds.setAttr(lenMD + '.operation', 2)
            cmds.connectAttr(self.RigGroup + '.defaultArcLength', lenMD + '.input2.input2X')
            cmds.connectAttr(self.RigGroup + '.arcLength', lenMD + '.input1.input1X')
            cmds.connectAttr(lenMD + '.outputX', self.RigGroup + '.lengthRatio')
            inverseRatioMD = cmds.createNode('multiplyDivide', name=self.prefix + 'LengthInverseRatio_multplyDivide')
            cmds.setAttr(inverseRatioMD + '.operation', 2)
            cmds.connectAttr(self.RigGroup + '.defaultArcLength', inverseRatioMD + '.input1.input1X')
            cmds.connectAttr(self.RigGroup + '.arcLength', inverseRatioMD + '.input2.input2X')
            cmds.connectAttr(inverseRatioMD + '.outputX', self.RigGroup + '.lengthInverseRatio')
        if volume == True and keepLength == True:
            VBC = cmds.createNode('blendColors', name=self.prefix + 'volumeBlendColors')
            cmds.connectAttr(self.RigGroup + '.stretch', VBC + '.blender')
            cmds.setAttr(VBC + '.color2.color2R', 0)
            cmds.connectAttr(self.RigGroup + '.volume', VBC + '.color1.color1R')
            cmds.connectAttr(VBC + '.outputR', self.RigGroup + '.conditionVolume')
        if volume == True:
            globalMDL = cmds.createNode('multDoubleLinear', name=self.prefix + 'globalVolume_MDL')
            cmds.connectAttr(self.RigGroup + '.globalScale', globalMDL + '.input1')
            if keepLength == False:
                cmds.connectAttr(self.RigGroup + '.volume', globalMDL + '.input2')
            else:
                cmds.connectAttr(self.RigGroup + '.conditionVolume', globalMDL + '.input2')
            cmds.connectAttr(globalMDL + '.output', self.RigGroup + '.globalVolume')
        if keepLength == True:
            cond = cmds.createNode('condition', name=self.prefix + 'StretchCondition')
            cmds.connectAttr(self.RigGroup + '.arcLength', cond + '.firstTerm')
            cmds.connectAttr(self.RigGroup + '.defaultArcLength', cond + '.secondTerm')
            cmds.setAttr(cond + '.operation', 5)
            cmds.setAttr(cond + '.colorIfTrueR', 1)
            cmds.connectAttr(self.RigGroup + '.lengthRatio', cond + '.colorIfFalseR')
            cmds.connectAttr(cond + '.outColorR', self.RigGroup + '.conditionStretch')
        #######	add joints   ##########
        maxRangeV = cmds.getAttr(surfaceShape + '.minMaxRangeV')[0][-1]
        ratioRangeV = maxRangeV / (numberOfJoints - 1)
        for x in range(numberOfJoints):
            cmds.select(cl=1)
            starJointWeight = 1 - (1 / (numberOfJoints - 1.0)) * x
            endJointWeight = (1 / (numberOfJoints - 1.0)) * x
            #### locator
            loc = cmds.group(em=1, name=self.prefix + '0' + str(x + 1) + '_LOC')
            con = cmds.parentConstraint(self.point[0], self.point[-1], loc)[0]
            starWeightAttr = cmds.listConnections(con + '.target[0].targetWeight', p=1)[0]
            endWeightAttr = cmds.listConnections(con + '.target[1].targetWeight', p=1)[0]
            cmds.setAttr(starWeightAttr, starJointWeight)
            cmds.setAttr(endWeightAttr, endJointWeight)
            self.locatorList.append(loc)
            cmds.parent(loc, LocGroup)
            ##### constraint
            CPOS = cmds.createNode('closestPointOnSurface', n=surface + str(x) + '_CPOS')
            cmds.connectAttr(loc + '.translate', CPOS + '.inPosition')
            cmds.connectAttr(surfaceShape + '.worldSpace', CPOS + '.inputSurface')
            u = cmds.getAttr(CPOS + '.parameterU')
            v = cmds.getAttr(CPOS + '.parameterV')
            cmds.delete(con)
            cmds.delete(CPOS)
            POSI = cmds.createNode('pointOnSurfaceInfo', name=loc.replace('LOC', 'pointOnSurfaceInfo'))
            cmds.setAttr(POSI + '.parameterV', v)
            cmds.setAttr(POSI + '.parameterU', u)
            cmds.connectAttr(surfaceShape + '.worldSpace', POSI + '.inputSurface')
            mp = cmds.createNode('motionPath', name=loc.replace('LOC', 'motionPath'))
            cmds.connectAttr(nc + '.worldSpace', mp + '.geometryPath')
            cmds.setAttr(mp + '.fractionMode', 1)
            cpos = cmds.createNode('closestPointOnSurface', name=loc.replace('LOC', 'CPOS'))
            cmds.connectAttr(mp + '.allCoordinates', cpos + '.inPosition')
            cmds.connectAttr(surfaceShape + '.worldSpace', cpos + '.inputSurface')
            cmds.connectAttr(cpos + '.parameterU', POSI + '.parameterU')
            cmds.connectAttr(cpos + '.parameterV', POSI + '.parameterV')
            cmds.connectAttr(POSI + '.position', loc + '.translate', f=1)
            aimCon = cmds.createNode('aimConstraint', name=loc.replace('LOC', 'aimConstraint'))
            cmds.connectAttr(POSI + '.result.normal', aimCon + '.target[0].targetTranslate')
            cmds.connectAttr(POSI + '.result.tangentV', aimCon + '.worldUpVector')
            cmds.setAttr(aimCon + '.upVector' + axis[0].upper(), 1)
            cmds.setAttr(aimCon + '.upVector' + axis[1].upper(), 0)
            cmds.setAttr(aimCon + '.upVector' + axis[2].upper(), 0)
            cmds.setAttr(aimCon + '.aimVector' + axis[0].upper(), 0)
            cmds.setAttr(aimCon + '.aimVector' + axis[1].upper(), 0)
            cmds.setAttr(aimCon + '.aimVector' + axis[2].upper(), -1)
            cmds.connectAttr(aimCon + '.constraintRotate', loc + '.rotate', f=1)
            cmds.parent(aimCon, loc)
            cmds.setAttr(mp + '.follow', 0)
            cmds.setAttr(mp + '.uValue', ratioRangeV * x)
            if axis[0] == 'x':
                cmds.setAttr(mp + '.frontAxis', 0)
            if axis[0] == 'y':
                cmds.setAttr(mp + '.frontAxis', 1)
            if axis[0] == 'z':
                cmds.setAttr(mp + '.frontAxis', 2)
            cmds.connectAttr(self.RigGroup + '.globalScale', loc + '.scale' + str.upper(axis[0]), f=1)
            cmds.connectAttr(self.RigGroup + '.globalScale', loc + '.scale' + str.upper(axis[1]), f=1)
            cmds.connectAttr(self.RigGroup + '.globalScale', loc + '.scale' + str.upper(axis[2]), f=1)
            ######## stretch
            if keepLength == True:
                kmdl = cmds.createNode('multiplyDivide', name=loc.replace('LOC', 'UVRatio_MD'))
                cmds.connectAttr(self.RigGroup + '.conditionStretch', kmdl + '.input2.input2X')
                cmds.setAttr(kmdl + '.input1.input1X', ratioRangeV * x)
                cmds.setAttr(kmdl + '.operation', 2)
                bc = cmds.createNode('blendColors', name=loc.replace('LOC', 'blendColors'))
                cmds.connectAttr(self.RigGroup + '.stretch', bc + '.blender')
                cmds.connectAttr(kmdl + '.outputX', bc + '.color2.color2R')
                cmds.setAttr(bc + '.color1.color1R', ratioRangeV * x)
                cmds.connectAttr(bc + '.output.outputR', mp + '.uValue')
            ########   scale
            #######  volume
            if volume == True:
                cmds.addAttr(self.RigGroup, ln=self.prefix + '0%sVolumeSwitch' % str(x + 1), at='double', dv=1, k=1)
                cmds.setAttr(self.RigGroup + '.' + self.prefix + '0%sVolumeSwitch' % str(x + 1),
                             math.sin(1.570796 * 2 * (1.0 / (numberOfJoints - 1)) * x))
                volumePAM = cmds.createNode('addDoubleLinear', name=loc.replace('LOC', 'volumePAM_ADL'))
                cmds.setAttr(volumePAM + '.input2', -1)
                cmds.connectAttr(self.RigGroup + '.lengthInverseRatio', volumePAM + '.input1')
                stretchRatio = cmds.createNode('multDoubleLinear', name=loc.replace('LOC', 'stretchRatio'))
                cmds.connectAttr(volumePAM + '.output', stretchRatio + '.input1')
                cmds.connectAttr(self.RigGroup + '.' + self.prefix + '0%sVolumeSwitch' % str(x + 1),
                                 stretchRatio + '.input2')
                volumeBW = cmds.createNode('blendWeighted', name=loc.replace('LOC', 'volumeBW'))
                cmds.connectAttr(stretchRatio + '.output', volumeBW + '.input[0]')
                cmds.connectAttr(self.RigGroup + '.globalVolume', volumeBW + '.weight[0]')
                cmds.connectAttr(self.RigGroup + '.globalScale', volumeBW + '.input[1]')
                cmds.setAttr(volumeBW + '.weight[1]', 1)
                cmds.connectAttr(volumeBW + '.output', loc + '.scale' + str.upper(axis[1]), f=1)
                cmds.connectAttr(volumeBW + '.output', loc + '.scale' + str.upper(axis[2]), f=1)
            ######  scale
            if scale == True:
                XSurfaceParameterV = cmds.getAttr(POSI + '.parameterV')
                if XSurfaceParameterV == 1.0:
                    XSurfaceParameterV = 0.9999
                CFSI = cmds.createNode('curveFromSurfaceIso', name=loc.replace('LOC', 'curveFromSurfaceIso'))
                cmds.connectAttr(scaleSurfaceShape + '.worldSpace', CFSI + '.inputSurface')
                cmds.setAttr(CFSI + '.isoparmValue', XSurfaceParameterV)
                cmds.setAttr(CFSI + '.isoparmDirection', 0)
                cvInfo = cmds.createNode('curveInfo', name=loc.replace('LOC', 'curveInfo'))
                cmds.connectAttr(CFSI + '.outputCurve', cvInfo + '.inputCurve')
                cmds.addAttr(cvInfo, ln='defaultArcLength', k=1, at='double')
                cmds.setAttr(cvInfo + '.defaultArcLength', cmds.getAttr(cvInfo + '.arcLength'))
                SECRatio = cmds.createNode('multiplyDivide', name=loc.replace('LOC', 'SECRatio_MD_multiplyDivide'))
                cmds.setAttr(SECRatio + '.operation', 2)
                cmds.connectAttr(cvInfo + '.arcLength', SECRatio + '.input1.input1X')
                cmds.connectAttr(cvInfo + '.defaultArcLength', SECRatio + '.input2.input2X')
                scaleMDL = cmds.createNode('multDoubleLinear', name=loc.replace('LOC', 'scaleMDL'))
                if volume == True:
                    cmds.connectAttr(volumeBW + '.output', scaleMDL + '.input1')
                else:
                    cmds.connectAttr(self.RigGroup + '.globalScale', scaleMDL + '.input1')
                cmds.connectAttr(SECRatio + '.outputX', scaleMDL + '.input2')
                cmds.connectAttr(scaleMDL + '.output', loc + '.scale' + str.upper(axis[1]), f=1)
                cmds.connectAttr(scaleMDL + '.output', loc + '.scale' + str.upper(axis[2]), f=1)
            ########  scaleOffset
            if scaleOffset == True and scale == True:
                scaleOffsetPlus = cmds.createNode('addDoubleLinear',
                                                  name=loc.replace('LOC', 'scalseOffset_addDoubleLinear'))
                cmds.connectAttr(self.RigGroup + '.scaleOffset', scaleOffsetPlus + '.input1')
                cmds.setAttr(scaleOffsetPlus + '.input2', XSurfaceParameterV)
                self.expressionScript = self.expressionScript + CFSI + ".isoparmValue = " + scaleOffsetPlus + '.output%1;\n'
                cmds.expression(self.expressionName, e=1, s=self.expressionScript)
        ########	 addSeparateCtrl
        if separateCtrl == True:
            self.separateCtrl = []
            for x in self.locatorList:
                ctrl = cmds.group(em=1, name=x.replace('LOC', 'Separate_CTL'))
                cmds.delete(cmds.parentConstraint(x, ctrl))
                cmds.parent(ctrl, x)
                self.separateCtrl.append(ctrl)
                cmds.connectAttr(self.RigGroup + '.separate_Visibility', ctrl + '.visibility')
                cmds.setAttr(ctrl + '.visibility', l=1, k=0)
            self.locatorList = self.separateCtrl

    def addTailCtrl(self, size=1):
        IKCtrlList = []
        FKCtrlList = []
        IKConnectList = []
        FKConnectList = []
        JOTList = []
        ScaleJOTList = []

        IKCtrlGroup = cmds.group(em=1, name=self.prefix + 'IKCtrl_GRP')
        FKCtrlGroup = cmds.group(em=1, name=self.prefix + 'FKCtrl_GRP')
        IKConnectGroup = cmds.group(em=1, name=self.prefix + 'IKConnect_GRP')
        scaleConnectGroup = cmds.group(em=1, name=self.prefix + 'scaleConnect_GRP')
        cmds.parent(FKCtrlGroup, IKCtrlGroup, self.CtrlGroup)
        cmds.parent(IKConnectGroup, scaleConnectGroup, self.ConnectGroup)

        # fk
        for x in self.point:
            FKCtrl = cmds.circle(nr=[0, 0, 1], name=self.prefix + str(self.point.index(x)) + '_FK_CTL', r=size * 1.5)[0]
            cmds.delete(cmds.parentConstraint(x, FKCtrl))
            addGroup(obj=FKCtrl, objSuffix='CTL', grpSuffix=['CTL_SDK', 'CTL_Matrix', 'CTL_GRP'])
            FKCtrlList.append(FKCtrl)
            cmds.DeleteHistory(FKCtrl)
            shape = cmds.listRelatives(FKCtrl, s=1)[0]
            cmds.connectAttr(self.RigGroup + '.FK_Visibility', shape + '.visibility')

            FKControl = cmds.group(em=1, name=self.prefix + str(self.point.index(x)) + '_FK_Connected')
            FKConnectList.append(FKControl)
            cmds.delete(cmds.parentConstraint(x, FKControl))
            addGroup(obj=FKControl, objSuffix='Connected',
                     grpSuffix=['Connected_SDK', 'Connected_Matrix', 'Connected_GRP'])

            cmds.connectAttr(FKCtrl + '.translate', FKControl + '.translate')
            cmds.connectAttr(FKCtrl + '.rotate', FKControl + '.rotate')
            cmds.connectAttr(FKCtrl + '.scale', FKControl + '.scale')

            cmds.connectAttr(FKCtrl.replace('CTL', 'CTL_SDK') + '.translate',
                             FKControl.replace('Connected', 'Connected_SDK') + '.translate')
            cmds.connectAttr(FKCtrl.replace('CTL', 'CTL_SDK') + '.rotate',
                             FKControl.replace('Connected', 'Connected_SDK') + '.rotate')
            cmds.connectAttr(FKCtrl.replace('CTL', 'CTL_SDK') + '.scale',
                             FKControl.replace('Connected', 'Connected_SDK') + '.scale')

            cmds.connectAttr(FKCtrl.replace('CTL', 'CTL_Matrix') + '.translate',
                             FKControl.replace('Connected', 'Connected_Matrix') + '.translate')
            cmds.connectAttr(FKCtrl.replace('CTL', 'CTL_Matrix') + '.rotate',
                             FKControl.replace('Connected', 'Connected_Matrix') + '.rotate')
            cmds.connectAttr(FKCtrl.replace('CTL', 'CTL_Matrix') + '.scale',
                             FKControl.replace('Connected', 'Connected_Matrix') + '.scale')

        for x in range(len(FKCtrlList) - 1):
            cmds.parent(FKCtrlList[x + 1].replace('CTL', 'CTL_GRP'), FKCtrlList[x])
            cmds.parent(FKConnectList[x + 1].replace('Connected', 'Connected_GRP'), FKConnectList[x])
        # ik
        for x in self.point:
            IKCtrl = cmds.curve(
                p=[[-1 * size, -1 * size, 0 * size], [-1 * size, 1 * size, 0 * size], [1 * size, 1 * size, 0 * size],
                   [1 * size, -1 * size, 0 * size], [-1 * size, -1 * size, 0 * size]], d=1,
                name=self.prefix + str(self.point.index(x)) + '_IK_CTL')
            IKCtrlShape = cmds.rename(cmds.listRelatives(IKCtrl, s=1)[0], IKCtrl + 'Shape')
            cmds.connectAttr(self.RigGroup + '.IK_Visibility', IKCtrlShape + '.visibility')
            cmds.delete(cmds.parentConstraint(x, IKCtrl))
            addGroup(obj=IKCtrl, objSuffix='CTL', grpSuffix=['CTL_SDK', 'CTL_Matrix', 'CTL_GRP'])
            cmds.select(cl=1)

            IKControl = cmds.group(em=1, name=self.prefix + str(self.point.index(x)) + '_IK_Connected')
            IKConnectList.append(FKControl)
            cmds.delete(cmds.parentConstraint(x, IKControl))
            addGroup(obj=IKControl, objSuffix='Connected',
                     grpSuffix=['Connected_SDK', 'Connected_Matrix', 'Connected_GRP'])
            cmds.parent(IKControl.replace('IK_Connected', 'IK_Connected_GRP'),
                        IKControl.replace('IK_Connected', 'FK_Connected'))

            cmds.connectAttr(IKCtrl + '.translate', IKControl + '.translate')
            cmds.connectAttr(IKCtrl + '.rotate', IKControl + '.rotate')
            cmds.connectAttr(IKCtrl + '.scale', IKControl + '.scale')

            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_SDK') + '.translate',
                             IKControl.replace('Connected', 'Connected_SDK') + '.translate')
            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_SDK') + '.rotate',
                             IKControl.replace('Connected', 'Connected_SDK') + '.rotate')
            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_SDK') + '.scale',
                             IKControl.replace('Connected', 'Connected_SDK') + '.scale')

            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_Matrix') + '.translate',
                             IKControl.replace('Connected', 'Connected_Matrix') + '.translate')
            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_Matrix') + '.rotate',
                             IKControl.replace('Connected', 'Connected_Matrix') + '.rotate')
            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_Matrix') + '.scale',
                             IKControl.replace('Connected', 'Connected_Matrix') + '.scale')

            JOT = cmds.joint(name=IKCtrl.replace('IK_CTL', 'JOT'))
            cmds.parentConstraint(IKControl, JOT)
            cmds.connectAttr(self.RigGroup + '.globalScale', JOT + '.scaleX')
            cmds.connectAttr(self.RigGroup + '.globalScale', JOT + '.scaleY')
            cmds.connectAttr(self.RigGroup + '.globalScale', JOT + '.scaleZ')
            cmds.setAttr(JOT + '.visibility', 0)
            addGroup(obj=JOT, objSuffix='JOT', grpSuffix=['JOT_GRP'])
            cmds.parent(IKCtrl.replace('CTL', 'CTL_GRP'), IKCtrl.replace('IK_CTL', 'FK_CTL'))
            cmds.parent(JOT.replace('JOT', 'JOT_GRP'), IKConnectGroup)
            IKCtrlList.append(IKCtrl)
            JOTList.append(JOT)

            if cmds.objExists(self.scaleSurface):
                scaleConnect = cmds.group(em=1, name=self.prefix + str(self.point.index(x)) + '_Scale_Connected')
                cmds.select(cl=1)
                jnt = cmds.joint(name=self.prefix + str(self.point.index(x)) + '_Scale_JOT')
                ScaleJOTList.append(jnt)
                cmds.parent(jnt, scaleConnect)
                cmds.delete(cmds.parentConstraint(x, scaleConnect))
                addGroup(obj=scaleConnect, objSuffix='Connected',
                         grpSuffix=['Connected_SDK', 'Connected_Matrix', 'Connected_GRP'])
                cmds.parent(scaleConnect.replace('Connected', 'Connected_GRP'), scaleConnectGroup)
                cmds.connectAttr(IKControl + '.scaleX', scaleConnect + '.scaleX')
                cmds.connectAttr(IKControl + '.scaleY', scaleConnect + '.scaleY')
                cmds.connectAttr(IKControl + '.scaleZ', scaleConnect + '.scaleZ')

                cmds.connectAttr(IKControl + '_SDK.scaleX', scaleConnect + '_SDK.scaleX')
                cmds.connectAttr(IKControl + '_SDK.scaleY', scaleConnect + '_SDK.scaleY')
                cmds.connectAttr(IKControl + '_SDK.scaleZ', scaleConnect + '_SDK.scaleZ')

                cmds.connectAttr(IKControl + '_Matrix.scaleX', scaleConnect + '_Matrix.scaleX')
                cmds.connectAttr(IKControl + '_Matrix.scaleY', scaleConnect + '_Matrix.scaleY')
                cmds.connectAttr(IKControl + '_Matrix.scaleZ', scaleConnect + '_Matrix.scaleZ')

        if self.separateCtrl:
            loc = cmds.curve(d=1,
                             p=[[0, 0, 1 * size * 0.7], [0, 0, -1 * size * 0.7], [0, 0, 0, ], [1 * size * 0.7, 0, 0, ],
                                [-1 * size * 0.7, 0, 0], [0, 0, 0], [0, 1 * size * 0.7, 0], [0, -1 * size * 0.7, 0]],
                             name='Temp')
            shape = cmds.rename(cmds.listRelatives(loc, s=1)[0], loc + 'Shape')
            for x in self.separateCtrl:
                new = cmds.duplicate(loc, name=loc + x)[0]
                shape = cmds.rename(cmds.listRelatives(new, s=1)[0], x + 'Shape')
                cmds.parent(shape, x, r=1, s=1)
                cmds.delete(new)
            cmds.delete(loc)
        cmds.parent(FKCtrlList[0].replace('CTL', 'CTL_GRP'), self.CtrlGroup)
        cmds.parent(FKConnectList[0].replace('Connected', 'Connected_GRP'), self.RigGroup)
        cmds.skinCluster(JOTList, self.surface, dr=20, name=self.prefix + 'surface_skinCluster')
        if cmds.objExists(self.scaleSurface):
            cmds.skinCluster(ScaleJOTList, self.scaleSurface, dr=20, name=self.prefix + 'scaleSurface_skinCluster')

        return FKCtrlList, IKCtrlList

    def addIKCtrl(self, size=1):

        IKCtrlList = []
        IKConnectList = []
        JOTList = []
        ScaleJOTList = []

        IKCtrlGroup = cmds.group(em=1, name=self.prefix + 'IKCtrl_GRP')
        IKConnectGroup = cmds.group(em=1, name=self.prefix + 'IKConnect_GRP')
        scaleConnectGroup = cmds.group(em=1, name=self.prefix + 'scaleConnect_GRP')
        cmds.parent(IKCtrlGroup, self.CtrlGroup)
        cmds.parent(IKConnectGroup, scaleConnectGroup, self.ConnectGroup)

        for x in self.point:
            IKCtrl = cmds.curve(
                p=[[-1 * size, 0 * size, -1 * size], [-1 * size, 0 * size, 1 * size], [1 * size, 0 * size, 1 * size],
                   [1 * size, 0 * size, -1 * size], [-1 * size, 0 * size, -1 * size]], d=1,
                name=self.prefix + str(self.point.index(x)) + '_IK_CTL')
            cmds.delete(cmds.parentConstraint(x, IKCtrl))
            cmds.DeleteHistory(IKCtrl)
            shape = cmds.listRelatives(IKCtrl, s=1)[0]
            cmds.connectAttr(self.RigGroup + '.IK_Visibility', shape + '.visibility')
            cmds.parent(IKCtrl, IKCtrlGroup)
            addGroup(obj=IKCtrl, objSuffix='CTL', grpSuffix=['CTL_SDK', 'CTL_Matrix', 'CTL_GRP'])
            IKCtrlList.append(IKCtrl)
            cmds.setAttr(IKCtrl + '.visibility', k=0, l=1)

            IKControl = cmds.group(em=1, name=self.prefix + str(self.point.index(x)) + '_IK_Connected')
            cmds.delete(cmds.parentConstraint(x, IKControl))
            cmds.parent(IKControl, IKConnectGroup)
            addGroup(obj=IKControl, objSuffix='Connected',
                     grpSuffix=['Connected_SDK', 'Connected_Matrix', 'Connected_GRP'])
            IKConnectList.append(IKControl)

            cmds.connectAttr(IKCtrl + '.translate', IKControl + '.translate')
            cmds.connectAttr(IKCtrl + '.rotate', IKControl + '.rotate')
            cmds.connectAttr(IKCtrl + '.scale', IKControl + '.scale')

            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_SDK') + '.translate',
                             IKControl.replace('Connected', 'Connected_SDK') + '.translate')
            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_SDK') + '.rotate',
                             IKControl.replace('Connected', 'Connected_SDK') + '.rotate')
            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_SDK') + '.scale',
                             IKControl.replace('Connected', 'Connected_SDK') + '.scale')

            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_Matrix') + '.translate',
                             IKControl.replace('Connected', 'Connected_Matrix') + '.translate')
            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_Matrix') + '.rotate',
                             IKControl.replace('Connected', 'Connected_Matrix') + '.rotate')
            cmds.connectAttr(IKCtrl.replace('CTL', 'CTL_Matrix') + '.scale',
                             IKControl.replace('Connected', 'Connected_Matrix') + '.scale')

            JOT = cmds.joint(name=IKCtrl.replace('IK_CTL', 'JOT'))
            cmds.parentConstraint(IKControl, JOT)
            cmds.connectAttr(self.RigGroup + '.globalScale', JOT + '.scaleX')
            cmds.connectAttr(self.RigGroup + '.globalScale', JOT + '.scaleY')
            cmds.connectAttr(self.RigGroup + '.globalScale', JOT + '.scaleZ')
            cmds.setAttr(JOT + '.visibility', 0)
            addGroup(obj=JOT, objSuffix='JOT', grpSuffix=['JOT_GRP'])
            # cmds.parent(IKCtrl.replace('CTL' , 'CTL_GRP') , IKCtrl.replace('IK_CTL' , 'FK_CTL') )
            cmds.parent(JOT.replace('JOT', 'JOT_GRP'), IKConnectGroup)
            JOTList.append(JOT)

            if cmds.objExists(self.scaleSurface):
                scaleConnect = cmds.group(em=1, name=self.prefix + str(self.point.index(x)) + '_Scale_Connected')
                cmds.select(cl=1)
                jnt = cmds.joint(name=self.prefix + str(self.point.index(x)) + '_Scale_JOT')
                ScaleJOTList.append(jnt)
                cmds.parent(jnt, scaleConnect)
                cmds.delete(cmds.parentConstraint(x, scaleConnect))
                addGroup(obj=scaleConnect, objSuffix='Connected',
                         grpSuffix=['Connected_SDK', 'Connected_Matrix', 'Connected_GRP'])
                cmds.parent(scaleConnect.replace('Connected', 'Connected_GRP'), scaleConnectGroup)

                cmds.connectAttr(IKControl + '.scaleX', scaleConnect + '.scaleX')
                cmds.connectAttr(IKControl + '.scaleY', scaleConnect + '.scaleY')
                cmds.connectAttr(IKControl + '.scaleZ', scaleConnect + '.scaleZ')

                cmds.connectAttr(IKControl + '_SDK.scaleX', scaleConnect + '_SDK.scaleX')
                cmds.connectAttr(IKControl + '_SDK.scaleY', scaleConnect + '_SDK.scaleY')
                cmds.connectAttr(IKControl + '_SDK.scaleZ', scaleConnect + '_SDK.scaleZ')

                cmds.connectAttr(IKControl + '_Matrix.scaleX', scaleConnect + '_Matrix.scaleX')
                cmds.connectAttr(IKControl + '_Matrix.scaleY', scaleConnect + '_Matrix.scaleY')
                cmds.connectAttr(IKControl + '_Matrix.scaleZ', scaleConnect + '_Matrix.scaleZ')
        if self.separateCtrl:
            loc = cmds.curve(d=1,
                             p=[[0, 0, 1 * size * 0.7], [0, 0, -1 * size * 0.7], [0, 0, 0, ], [1 * size * 0.7, 0, 0, ],
                                [-1 * size * 0.7, 0, 0], [0, 0, 0], [0, 1 * size * 0.7, 0], [0, -1 * size * 0.7, 0]],
                             name='Temp')
            shape = cmds.rename(cmds.listRelatives(loc, s=1)[0], loc + 'Shape')
            for x in self.separateCtrl:
                new = cmds.duplicate(loc, name=loc + x)[0]
                shape = cmds.rename(cmds.listRelatives(new, s=1)[0], x + 'Shape')
                cmds.parent(shape, x, r=1, s=1)
                cmds.delete(new)
            cmds.delete(loc)
        cmds.skinCluster(JOTList, self.surface, dr=2, name=self.prefix + 'surface_skinCluster')
        if cmds.objExists(self.scaleSurface):
            cmds.skinCluster(ScaleJOTList, self.scaleSurface, dr=2, name=self.prefix + 'scaleSurface_skinCluster')

        return IKCtrlList

    def addJoints(self):
        self.jointsList = []
        if self.separateCtrl:
            for x in self.separateCtrl:
                select(cl=1)
                jnt = joint(name=x.replace('CTL', 'JNT'))
                delete(parentConstraint(x, jnt))
                parent(jnt, x)
                makeIdentity(jnt, a=1, t=1, r=1, s=1, n=0, pn=1)
                self.jointsList.append(jnt)
        else:
            for x in self.locatorList:
                select(cl=1)
                jnt = joint(name=x.replace('LOC', 'JNT'))
                delete(parentConstraint(x, jnt))
                parent(jnt, x)
                makeIdentity(jnt, a=1, t=1, r=1, s=1, n=0, pn=1)
                self.jointsList.append(jnt)
        return self.jointsList
