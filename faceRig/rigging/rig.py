# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from imp import reload

import temp
import maya.mel
from pymel.core import *
import rigging.rigTool as rigTool; reload ( rigTool )
import matrixTool.matrixTool as matrix ;reload(matrix)
import maya.cmds as cmds
import rigging.spherePath as spherePath;reload(spherePath)
import UI.mainProgress as UI; reload ( UI )
class rig():
	def __init__(self , faceGeo = [] , EyeBallGeo = [] , upperTeethGeo = [] , lowerTeethGeo = [] , tongueGeo = [] , otherGeo = []):
		with UndoChunk():
			self.faceGeo = faceGeo
			self.EyeBallGeo = EyeBallGeo
			self.upperTeethGeo = upperTeethGeo
			self.lowerTeethGeo = lowerTeethGeo
			self.tongueGeo = tongueGeo
			self.otherGeo = otherGeo
			self.rootPosition = 'M_Head_Position'
			self.headSkeleton = 'M_Head_Skeleton'
			self.jawLowerSkeleton = 'M_JawLower_Position_Skeleton'
			self.jawUpperSkeleton = 'M_JawUpper_Position_Skeleton'
			self.teethUpperSkeleton = 'M_TeethUpper_00_Skeleton'
			self.teethLowerSkeleton = 'M_TeethLower_00_Skeleton'
			self.headUpperSkeleton = 'M_HeadUpper_Skeleton'
			self.headLowerSkeleton = 'M_HeadLower_Skeleton'
			self.L_EyeSkeleton = 'L_Eye_00_Gross_Skeleton'
			self.R_EyeSkeleton = 'R_Eye_00_Gross_Skeleton'
			self.L_LipConnerSkeleton = 'L_LipConner_00_Skeleton'
			self.R_LipConnerSkeleton = 'R_LipConner_00_Skeleton'
			self.M_upperLipSkeleton = 'M_LipUpper_00_Skeleton'
			self.M_lowerLipSkeleton = 'M_LipLower_00_Skeleton'
			self.L_eyeBallSkeleton = 'L_EyeBall_00_Skeleton'
			self.R_eyeBallSkeleton = 'R_EyeBall_00_Skeleton'
			self.ctrlPositionList = ls('*_CtrlPosition')
			self.M_MouthGrossPosition = 'M_Mouth_00_Gross_CtrlPosition'
			self.lipUpperGrossPosition = 'M_LipUpper_00_Gross_CtrlPosition'
			self.lipLowerGrossPosition = 'M_LipLower_00_Gross_CtrlPosition'
			self.L_lipUpperGrossPosition = 'L_LidUpper_00_Gross_CtrlPosition'
			self.R_lipUpperGrossPosition = 'R_LidUpper_00_Gross_CtrlPosition'
			self.L_lipLowerGrossPosition = 'L_LidLower_00_Gross_CtrlPosition'
			self.R_lipLowerGrossPosition = 'R_LidLower_00_Gross_CtrlPosition'
			self.TeethUpperSecondGRP = 'TeethUpper_Second_GRP'
			self.TeethLowerSecondGRP = 'TeethLower_Second_GRP'
			self.headJNT = self.headSkeleton.replace('Skeleton','JNT')
			self.jawUpperJNT = self.jawUpperSkeleton.replace('Skeleton','JNT')
			self.jawLowerJNT = self.jawLowerSkeleton.replace('Skeleton','JNT')
			self.teethUpperJNT = self.teethUpperSkeleton.replace('Skeleton','JNT')
			self.teethLowerJNT = self.teethLowerSkeleton.replace('Skeleton','JNT')
			self.L_eyeBallJNT = self.L_eyeBallSkeleton.replace('Skeleton','JNT')
			self.R_eyeBallJNT = self.R_eyeBallSkeleton.replace('Skeleton','JNT')
			self.headCTL = self.headSkeleton.replace('Skeleton','CTL')
			self.jawLowerCTL = self.jawLowerSkeleton.replace('Skeleton','CTL')
			self.jawUpperCTL = self.jawUpperSkeleton.replace('Skeleton','CTL')
			self.L_EyeCTL = self.L_EyeSkeleton.replace('Skeleton','CTL')
			self.R_EyeCTL = self.R_EyeSkeleton.replace('Skeleton','CTL')
			self.headUpperCTL = self.headUpperSkeleton.replace('Skeleton','CTL')
			self.headLowerCTL = self.headLowerSkeleton.replace('Skeleton','CTL')
			self.teethUpperCTL =self.teethUpperSkeleton.replace('Skeleton','CTL')
			self.teethLowerCTL =self.teethLowerSkeleton.replace('Skeleton','CTL')
			self.L_LipConnerCTL = self.L_LipConnerSkeleton.replace('Skeleton','Gross_CTL')
			self.R_LipConnerCTL = self.R_LipConnerSkeleton.replace('Skeleton','Gross_CTL')
			self.M_upperLipGrossCTL = self.M_upperLipSkeleton.replace('Skeleton','Gross_CTL')
			self.M_lowerLipGrossCTL = self.M_lowerLipSkeleton.replace('Skeleton','Gross_CTL')
			self.L_eyeBallCTL = self.L_eyeBallSkeleton.replace('Skeleton','CTL')
			self.R_eyeBallCTL = self.R_eyeBallSkeleton.replace('Skeleton','CTL')
			self.M_MouthGrossCTL = self.M_MouthGrossPosition.replace('CtrlPosition','CTL')
			self.lipUpperGrossCTL = self.lipUpperGrossPosition.replace('CtrlPosition','CTL')
			self.lipLowerGrossCTL = self.lipLowerGrossPosition.replace('CtrlPosition','CTL')
			self.L_lipUpperGroosCTL = self.L_lipUpperGrossPosition.replace('CtrlPosition' , 'CTL')
			self.R_lipUpperGroosCTL = self.R_lipUpperGrossPosition.replace('CtrlPosition' , 'CTL')
			self.L_lipLowerGroosCTL = self.L_lipLowerGrossPosition.replace('CtrlPosition' , 'CTL')
			self.R_lipLowerGroosCTL = self.R_lipLowerGrossPosition.replace('CtrlPosition' , 'CTL')
			self.skeletonGRP = PyNode('Facial_Skeleton_GRP')
			self.allSkeletonList = ls('*_Skeleton')
			self.tongueSkeletonList = ls('*Tongue*Skeleton')
			self.teethSecSkeletonList = ls('*Teeth*Sec*Skeleton')
			self.lipSkeletonList = ls('*Lip*_Skeleton')
			self.L_lidSkeletonList = ls('*L_*Lid*_Skeleton')
			self.R_lidSkeletonList = ls('*R_*Lid*_Skeleton')
			self.facialRigGRP = group(em=1,name = 'FacialRig_GRP')
			self.moduleGRP = group(em=1,name = 'FacialModule_GRP')
			self.jointList = []
			self.jointGRP = group(em=1,name = 'FacialJoint_GRP')
			self.ctrlList = []
			self.ctrlGRP = group(em=1,name = 'FacialCtrl_GRP')
			self.secCtrlGRP = group(em=1,name = 'SecCtrl_GRP')
			self.partCtrlGRP = group(em=1,name = 'PartCtrl_GRP')
			self.grossCtrlGRP = group(em=1,name = 'GrossCtrl_GRP')
			self.otherCtrlGRP = group(em=1,name = 'OtherCtrl_GRP')
			self.MatrixNodesGRP = group(em=1,name = 'MatrixNodesInfo_GRP')
			parent(self.jointGRP,self.ctrlGRP,self.moduleGRP,self.facialRigGRP)
			parent(self.MatrixNodesGRP , self.facialRigGRP)
			self.skeletonGRP.hide()
			###################################
			#######	addBaseJoints	 ######
			###################################
			addBaseCtrlsSkeleton = list(set(self.allSkeletonList)^set(self.tongueSkeletonList)^set(self.teethSecSkeletonList))
			createJointUI = UI.mainProgress(maxValue = len(addBaseCtrlsSkeleton) , status = 'Create Joints...')								########  MainProgreess  Start
			for x in addBaseCtrlsSkeleton :
				select(cl=1)
				jnt = joint(name = x.name().replace('Skeleton' , 'JNT'))
				self.jointList.append(jnt)
				rigTool.alignObj([x],[jnt])		#delete(parentConstraint(x,jnt))
				createJointUI.update()																										########  MainProgreess  Update
			makeIdentity(self.jointList,a=1,t=1,r=1,s=1,n=0,pn=1)
			parent(self.jointList,self.jointGRP)
			parent(list(set(self.jointList)^set([PyNode(self.headJNT)])),PyNode(self.headJNT))
			createJointUI.end()																												########  MainProgreess   End
			###################################
			#######	addBaseCtrls	 #######
			###################################
			self.baseCtrlsList = []
			createJointUI = UI.mainProgress(maxValue = len(self.jointList) , status = 'Create Base Ctrls...')									########  MainProgreess  Start
			for jnt in self.jointList:
				if 'End' not in jnt.name() :
					ctrl = group(em=1 , name = jnt.name().replace('JNT','CTL'))
					rigTool.alignObj([jnt],[ctrl])		#delete(parentConstraint(jnt,ctrl))
					self.ctrlList.append(ctrl)
					self.baseCtrlsList.append(ctrl)
					rigTool.addGroup(obj=jnt.name(),objSuffix='JNT',grpSuffix=['JNT_SDK','JNT_Matrix','JNT_GRP'])
				else:
					parent(jnt,PyNode(jnt.name().replace('JNT','Skeleton')).getParent().name().replace('Skeleton','JNT'))
				createJointUI.update()																										########  MainProgreess  Update
			parent(self.ctrlList , self.ctrlGRP)
			parent(list(set(self.ctrlList)^set([PyNode(self.headCTL)])),PyNode(self.headCTL))
			createJointUI.end()																												########  MainProgreess   End
			createJointUI = UI.mainProgress(maxValue = len(self.jointList) , status = 'Connecting...')  										########  MainProgreess  Start
			for ctrl in self.ctrlList:
				rigTool.addGroup(obj=ctrl.name(),objSuffix='CTL',grpSuffix=['CTL_Place','CTL_SDK','CTL_Matrix','CTL_GRP'])
				if 'Lid' not in ctrl.name() and  'JawUpper' not in ctrl.name() and  'JawLower' not in ctrl.name():
					ctrlSDK = PyNode(ctrl.name().replace('CTL' , 'CTL_SDK'))
					ctrlMatrix = PyNode(ctrl.name().replace('CTL' , 'CTL_Matrix'))
					JNTSDK = PyNode(ctrl.name().replace('CTL' , 'JNT_SDK'))
					JNTMatrix = PyNode(ctrl.name().replace('CTL' , 'JNT_Matrix'))
					JNT = PyNode(ctrl.name().replace('CTL' , 'JNT'))
					ctrlSDK.translate>>JNTSDK.translate
					ctrlSDK.rotate>>JNTSDK.rotate
					ctrlSDK.scale>>JNTSDK.scale
					ctrlMatrix.translate>>JNTMatrix.translate
					ctrlMatrix.rotate>>JNTMatrix.rotate
					ctrlMatrix.scale>>JNTMatrix.scale
					ctrl.translate>>JNT.translate
					ctrl.rotate>>JNT.rotate
					ctrl.scale>>JNT.scale
				if 'JawLower' in ctrl.name() or 'JawUpper' in ctrl.name():
					JNTMatrix = PyNode(ctrl.name().replace('CTL' , 'JNT_Matrix'))
					JNT = PyNode(ctrl.name().replace('CTL' , 'JNT'))
					matrix.addMatrix(ctrl,JNT,JNTMatrix , addPass = True)
				createJointUI.update()																										########  MainProgreess  Update
			rigTool.addCircleShape(obj = self.ctrlList)
			rigTool.autoAssignColor(obj = [x.name() for x in self.ctrlList] , gloomy=1)
			matrix.addMatrix(self.jawUpperCTL,self.teethUpperCTL,self.teethUpperCTL+'_Matrix' , addPass = True)
			matrix.addMatrix(self.jawLowerCTL,self.teethLowerCTL,self.teethLowerCTL+'_Matrix' , addPass = True)
			createJointUI.end()																												########  MainProgreess  End
			#####################################
			#######	addPartCtrls	 #########
			#####################################
			self.partCtrlsList = []
			createJointUI = UI.mainProgress(maxValue = 100+len(self.ctrlPositionList) , status = 'Add Parts Ctrls...')  						########  MainProgreess  Start
			for x in self.ctrlPositionList:
				ctrl = group(em=1 , name = x.name().replace('_CtrlPosition','_CTL'))
				self.ctrlList.append(ctrl)
				self.partCtrlsList.append(ctrl)
				parent(ctrl,self.headCTL)
				rigTool.alignObj(soure = [x] , target = [ctrl])
				rigTool.addGroup(obj=ctrl.name() , objSuffix='CTL' , grpSuffix= ['CTL_SDK','CTL_Matrix','CTL_GRP'] )
				rigTool.replaceCVShape(soure = x.name(), target = [ctrl] , replace = 1)
				createJointUI.update(1)																										########  MainProgreess  Update
			rigTool.replaceCVShape(soure = 'Jaw_CV', target = [self.jawLowerCTL] , replace = 1)
			rigTool.replaceCVShape(soure = 'Jaw_CV', target = [self.jawUpperCTL] , replace = 1)
			rigTool.replaceCVShape(soure = 'Eye_CV', target = [self.L_EyeCTL,self.R_EyeCTL] , replace = 1)
			rigTool.replaceCVShape(soure = 'HeadUpper_CV', target = [self.headUpperCTL,self.headLowerCTL] , replace = 1)
			rigTool.replaceCVShape(soure = 'Head_CV', target = [self.headCTL] , replace = 1)
			rigTool.symmetryCV([self.L_EyeCTL])
			parentConstraint(self.headLowerCTL , self.M_MouthGrossCTL+'_GRP' , mo=1)
			scaleConstraint(self.headLowerCTL , self.M_MouthGrossCTL+'_GRP' , mo=1)
			createJointUI.update(40)																										########  MainProgreess  Update
			matrix.addMatrix(self.jawUpperCTL,self.lipUpperGrossCTL,self.lipUpperGrossCTL+'_Matrix' , value = 1 , addPass = True)
			matrix.addMatrix(self.jawUpperCTL,self.lipLowerGrossCTL,self.lipLowerGrossCTL+'_Matrix' , value = 0 , addPass = True)
			matrix.addMatrix(self.jawLowerCTL,self.lipUpperGrossCTL,self.lipUpperGrossCTL+'_Matrix' , value = 0 , addPass = True)
			matrix.addMatrix(self.jawLowerCTL,self.lipLowerGrossCTL,self.lipLowerGrossCTL+'_Matrix' , value = 1 , addPass = True)
			geo = self.faceGeo+self.EyeBallGeo+self.upperTeethGeo+self.lowerTeethGeo+self.tongueGeo+self.otherGeo
			geoList = list(set(geo))
			sk_geo = []
			skinGeoGRP = group(em=1 , name = 'Facial_SkinGeometry_GRP')
			for x in geoList:
				geo = duplicate(x,name = PyNode(x).name()+'_Skin')[0]
				sk_geo.append(geo)
				parent(geo , skinGeoGRP)
			#####################################
			#######	addTongueCtrls	 #######
			#####################################
			self.tongueCtrlsList = []
			tongue = rigTool.JointsOnSurface( point = [x.name() for x in self.tongueSkeletonList] , prefix = 'M_Tongue_' )
			tongue.rigging( keepLength = True , volume = True ,  scale = True , scaleOffset = False , separateCtrl = False , axis = ['z','x','y']  , numberOfJoints = 15)
			tongueFKCtrlsList , tongueIKCtrlsList = tongue.addTailCtrl()
			self.ctrlList = self.ctrlList + [PyNode(x) for x in tongueFKCtrlsList ] + [PyNode(x) for x in tongueIKCtrlsList ]
			self.tongueCtrlsList = [PyNode(x) for x in tongueFKCtrlsList] + [PyNode(x) for x in tongueIKCtrlsList ]
			tongueJointsList = tongue.addJoints()
			parent(tongue.RigGroup,self.moduleGRP)
			createJointUI.update(40)																										########  MainProgreess  Update
			connectAttr(tongue.RigGroup+'.scaleY' , tongue.RigGroup+'.globalScale')
			TongueCtrlsGRP = PyNode(tongue.CtrlGroup)
			parent(TongueCtrlsGRP,self.headCTL)
			matrix.addMatrix(self.jawLowerCTL,tongueFKCtrlsList[0] , tongueFKCtrlsList[0]+'_Matrix' , addPass = 1 )
			#scaleConsqtraint(self.jawLowerCTL,TongueCtrlsGRP,mo=1)
			parentConstraint(self.headJNT,tongue.RigGroup , mo = 1 )
			scaleConstraint(self.headJNT,tongue.RigGroup , mo = 1 )
			rigTool.replaceCVShape(soure = 'Teeth_CV', target = [self.teethUpperCTL,self.teethLowerCTL] , replace = 1)
			rigTool.autoAssignColor(obj = [self.teethUpperCTL,self.teethLowerCTL] , gloomy=1)
			createJointUI.update(10)																										########  MainProgreess  Update
			rigTool.autoAssignColor(obj = tongueFKCtrlsList  , gloomy=0)
			rigTool.autoAssignColor(obj = tongueIKCtrlsList  , gloomy=1)
			rigTool.scaleCtrlsShapes(obj = self.ctrlList , value = PyNode(self.rootPosition).scaleZ.get())
			createJointUI.update(10)																									########  MainProgreess  Update
			createJointUI.end()																												########  MainProgreess  End
			## lattice deform
			sj = tongue.jointsList[0]
			ee = tongue.jointsList[-1]
			distance = createNode('distanceBetween' , name = 'distanceBetween_TEMP')
			sj.worldMatrix>>distance.inMatrix1
			ee.worldMatrix>>distance.inMatrix2
			dis = distance.distance.get()
			delete(distance)
			defTongue = duplicate(tongue.surface , n = tongue.surface+'_Deform')[0]
			blendShape(defTongue,tongue.surface,w=(0,1) , name ='Facial_TongueSineDeform_BlendShape',foc=1)
			sineNode , sineHand = nonLinear(defTongue ,type = 'sine',name = 'M_Tongue_SineDeform')
			sineNode = sineNode.rename('M_Tongue_SineDeform')
			sineHand = sineHand.rename('M_Tongue_SineHandle')
			pos = group(em=1 , name = 'Temp')
			rigTool.alignObj([sj] , [pos])
			delete(aimConstraint(ee,pos,aim = [0,1,0]))
			t = xform(pos,q=1,ws=1,wd=1,t=1)
			ro = xform(pos,q=1 , ws=1,wd=1,ro=1)
			xform(sineHand,ws=1,wd=1,t=t)
			xform(sineHand,ws=1,wd=1,ro=ro)
			delete(pos)
			parent(sineHand,tongue.RigGroup)
			sineHand.scale.set([dis,dis,dis])
			sineNode.lowBound.set(0)
			sineNode.dropoff.set(-1)
			sineNode.wavelength.set(1)
			rigTool.addGroup(obj=sineHand.name() , objSuffix='SineHandle' , grpSuffix= ['SineHandle_SDK','SineHandle_Matrix','SineHandle_GRP'])
			sineHand.rotateY.set(90)
			sineHand.v.set(0)
			defCTL = group(em=1 , name = 'M_Tongue_Deform')
			rigTool.alignObj([tongueIKCtrlsList[-1]] , [defCTL])
			parent(defCTL,tongueIKCtrlsList[-1])
			rigTool.replaceCVShape(soure = 'Eye_CV', target = [defCTL] , replace = 1)
			rigTool.scaleCtrlsShapes([defCTL] , 0.2)
			rigTool.autoAssignColor(obj = [defCTL]  , gloomy=1)
			for x in defCTL.listAttr(k=1):
				setAttr(x,k=0,l=1)
			addAttr(defCTL , ln = '_' , at = 'enum' , nn = '_______' , en = 'Sine:' , k = 1)
			addAttr(defCTL , ln = 'envelope' , at = 'double' , dv = 1 , min = 0 , max = 1 ,  k = 1)
			addAttr(defCTL , ln = 'amplitude' , at = 'double' , dv = 0 ,  k = 1)
			addAttr(defCTL , ln = 'wavelength' , at = 'double' , dv = 1 ,  k = 1)
			addAttr(defCTL , ln = 'offset' , at = 'double' , dv = 0 ,  k = 1)
			addAttr(defCTL , ln = 'normal' , at = 'double' , dv = 90 ,  k = 1)
			addAttr(defCTL , ln = '__' , at = 'enum' , nn = '_______' , en = 'Stretchy:' , k = 1)
			addAttr(defCTL , ln = 'stretch' , at = 'double' , dv = 1 , min = 0 , max = 1 ,  k = 1)
			addAttr(defCTL , ln = 'volume' , at = 'double' , dv = 0 , min = 0 , max = 1 ,  k = 1)
			addAttr(defCTL , ln = '___' , at = 'enum' , nn = '_______' , en = 'Blend:' , k = 1)
			addAttr(defCTL , ln = 'bend' , at = 'double' , dv = 0  ,  k = 1)
			setAttr(defCTL._,lock=1)
			setAttr(defCTL.__,lock=1)
			setAttr(defCTL.___,lock=1)
			defCTL.envelope>>sineNode.envelope
			defCTL.amplitude>>sineNode.amplitude
			defCTL.wavelength>>sineNode.wavelength
			defCTL.offset>>sineNode.offset
			defCTL.normal>>sineHand.rotateY
			defCTL.stretch>>PyNode(tongue.RigGroup).stretch
			defCTL.volume>>PyNode(tongue.RigGroup).volume
			rigTool.scaleCtrlsShapes(obj = [defCTL] , value = PyNode(self.rootPosition).scaleZ.get())
			##  blend
			try:
				tongueBendGeo = duplicate(self.tongueGeo[0],name = 'Tongue_Bend')[0]
				bendNode , bendHand = nonLinear(tongueBendGeo ,type = 'bend',name = 'M_Tongue_BendDeform')
				bendNode = bendNode.rename('M_Tongue_BendDeform')
				bendHand = bendHand.rename('M_Tongue_BendHandle')
				parent(bendHand , tongue.RigGroup)
				tongueBendGeo.v.set(0)

				rigTool.addGroup(obj=bendHand.name() , objSuffix='BendHandle' , grpSuffix= ['BendHandle_SDK','BendHandle_Matrix','BendHandle_GRP'])
				bendHand.rotateZ.set(90)
				bendHand.v.set(0)
				defCTL.bend>>bendNode.curvature
				defCTL.envelope>>bendNode.envelope
				blendShape(tongueBendGeo,PyNode(self.tongueGeo[0]).name()+'_Skin',w=(0,1) , name ='Facial_TongueBendDeform_BlendShape',foc=1)
				parent(tongueBendGeo , tongue.RigGroup)
			except:
				pass
			###   teeth
			#self.TeethUpperSecondGRP
			teethGRP = PyNode('TeethUpper_Second_GRP')
			if teethGRP.v.get()==1:
				L_teethUpperJNTList = ls('L_TeethUpper_Sec_*_Skeleton')
				M_teethUpperJNTList = ls('M_TeethUpper_Sec_*_Skeleton')
				R_teethUpperJNTList = ls('R_TeethUpper_Sec_*_Skeleton')
				L_teethLowerJNTList = ls('L_TeethLower_Sec_*_Skeleton')
				M_teethLowerJNTList = ls('M_TeethLower_Sec_*_Skeleton')
				R_teethLowerJNTList = ls('R_TeethLower_Sec_*_Skeleton')
				R_Upper = sorted(R_teethUpperJNTList)
				R_Upper.reverse()
				R_Lower = sorted(R_teethLowerJNTList)
				R_Lower.reverse()
				teethUpperList = R_Upper+M_teethUpperJNTList+sorted(L_teethUpperJNTList)
				teethLowerList = R_Lower+M_teethLowerJNTList+sorted(L_teethLowerJNTList)
				teethUpper = rigTool.JointsOnSurface(prefix = 'TeethUpper_' , point = [x.name() for x in teethUpperList])
				teethLower = rigTool.JointsOnSurface(prefix = 'TeethLower_' , point = [x.name() for x in teethLowerList])
				teethUpper.rigging(scale = 1 , keepLength = 0 , volume = 0 , scaleOffset = 0 , axis = ['x','y','z'] , separateCtrl = 0 , numberOfJoints = 10)
				teethLower.rigging(scale = 1 , keepLength = 0 , volume = 0 , scaleOffset = 0 , axis = ['x','y','z'] , separateCtrl = 0 , numberOfJoints = 10)
				upperFK,upperIK = teethUpper.addTailCtrl(size = PyNode(self.rootPosition).scaleZ.get()*0.2)
				lowerFK,lowerIK = teethLower.addTailCtrl(size = PyNode(self.rootPosition).scaleZ.get()*0.2)
				teethUpper.addJoints()
				teethLower.addJoints()
				rigTool.autoAssignColor(obj = upperIK+lowerIK  , gloomy=1)
				for x in upperIK:
					x = PyNode(x)
					grp = PyNode(x.name()+'_GRP')
					parent(grp,self.teethUpperCTL)
				for x in lowerIK:
					x = PyNode(x)
					grp = PyNode(x.name()+'_GRP')
					parent(grp,self.teethLowerCTL)
				delete(upperFK[0]+'_GRP')
				delete(lowerFK[0]+'_GRP')
				parent(teethUpper.RigGroup , self.moduleGRP)
				parent(teethLower.RigGroup , self.moduleGRP)
				parentConstraint(self.teethUpperJNT , teethUpper.RigGroup , mo = 1 )
				scaleConstraint(self.teethUpperJNT , teethUpper.RigGroup , mo = 1 )
				parentConstraint(self.teethLowerJNT , teethLower.RigGroup , mo = 1 )
				scaleConstraint(self.teethLowerJNT , teethLower.RigGroup , mo = 1 )
				PyNode(teethUpper.RigGroup).scaleY>>PyNode(teethUpper.RigGroup).globalScale
				PyNode(teethLower.RigGroup).scaleY>>PyNode(teethLower.RigGroup).globalScale


			#####################################
			#######	LipSewSets	 ###########
			#####################################
			self.L_LipConnerCTL = PyNode(self.L_LipConnerCTL)
			self.R_LipConnerCTL = PyNode(self.R_LipConnerCTL)
			self.lipCtrlList = []
			self.lipUpperCtrlList = []
			self.lipLowerCtrlList = []
			self.lipSewBrigeList = []
			self.lipUpperSewBrigeList = []
			self.lipLowerSewBrigeList = []
			for x in self.lipSkeletonList:
				ctrl = PyNode(x.name().replace('_Skeleton','_CTL'))
				sewCTL = group(em=1,name = x.name().replace('Skeleton','SewBrige_CTL'))
				rigTool.alignObj(soure = [x] , target = [sewCTL])
				parent(sewCTL,self.headCTL)
				rigTool.addGroup(obj=sewCTL.name() , objSuffix='CTL' , grpSuffix= ['CTL_SDK','CTL_Matrix','CTL_GRP'] )
				self.lipCtrlList.append(ctrl)
				self.lipSewBrigeList.append(sewCTL)
				if 'Upper' in x.name():
					self.lipUpperCtrlList.append(ctrl)
					self.lipUpperSewBrigeList.append(sewCTL)
				if 'Lower' in x.name():
					self.lipLowerCtrlList.append(ctrl)
					self.lipLowerSewBrigeList.append(sewCTL)
			rigTool.addCircleShape(obj = self.lipSewBrigeList , r=0.15)
			rigTool.autoAssignColor(obj = [x.name() for x in self.lipSewBrigeList]  , gloomy=1)
			rigTool.scaleCtrlsShapes(obj = [x.name() for x in self.lipSewBrigeList]  , value = PyNode(self.rootPosition).scaleZ.get())
			for x in self.lipCtrlList:x.v.set(1)
			addAttr(self.L_LipConnerCTL , ln = '_' ,nn='_______', at ='enum' ,en='Attrs:', k=1)
			PyNode(self.L_LipConnerCTL)._.lock()
			addAttr(self.R_LipConnerCTL , ln = '_' ,nn='_______', at ='enum' ,en='Attrs:', k=1)
			PyNode(self.R_LipConnerCTL)._.lock()
			addAttr(self.L_LipConnerCTL , ln = 'lipSew' , at = 'double' , dv=0 ,min=0 , max=10 , k=1 )
			addAttr(self.R_LipConnerCTL , ln = 'lipSew' , at = 'double' , dv=0 ,min=0 , max=10 , k=1 )
			UpperLip = {}
			UpperSewLip = {}
			LowerLip = {}
			LowerSewLip = {}
			connerLip = {}
			connerSewLip = {}
			for x in self.lipUpperCtrlList :
				UpperLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipUpperSewBrigeList :
				UpperSewLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipLowerCtrlList :
				LowerLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipLowerSewBrigeList :
				LowerSewLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipCtrlList :
				if 'Conner' in x.name():
					connerLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipSewBrigeList :
				if 'Conner' in x.name():
					connerSewLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			UpperLip = sorted(UpperLip, key=lambda x:UpperLip[x])
			UpperSewLip = sorted(UpperSewLip, key=lambda x:UpperSewLip[x])
			LowerLip = sorted(LowerLip, key=lambda x:LowerLip[x])
			LowerSewLip = sorted(LowerSewLip, key=lambda x:LowerSewLip[x])
			connerLip = sorted(connerLip, key=lambda x:connerLip[x])
			connerSewLip = sorted(connerSewLip, key=lambda x:connerSewLip[x])
			for i in range(len(UpperLip)):
				matrix.addMatrix( parentCtl=UpperSewLip[i], childCtl=UpperLip[i], childCtlOffect=UpperLip[i]+'_Matrix' , value=0.5 , addPass = True)
				matrix.addMatrix( parentCtl=LowerSewLip[i], childCtl=UpperLip[i], childCtlOffect=UpperLip[i]+'_Matrix' , value=0.5 , addPass = True)
				matrix.addMatrix( parentCtl=LowerSewLip[i], childCtl=LowerLip[i], childCtlOffect=LowerLip[i]+'_Matrix' , value=0.5 , addPass = True)
				matrix.addMatrix( parentCtl=UpperSewLip[i], childCtl=LowerLip[i], childCtlOffect=LowerLip[i]+'_Matrix' , value=0.5 , addPass = True)
			for i in range(len(connerLip)):
				matrix.addMatrix( parentCtl=connerSewLip[i], childCtl=connerLip[i], childCtlOffect=connerLip[i]+'_Matrix' , value=1 , addPass = True)
			L_UpperLip = {}
			L_UpperSewLip = {}
			L_LowerLip = {}
			L_LowerSewLip = {}
			R_UpperLip = {}
			R_UpperSewLip = {}
			R_LowerLip = {}
			R_LowerSewLip = {}
			for x in self.lipUpperCtrlList :
				if 'L_' in x.name():
					L_UpperLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipUpperSewBrigeList :
				if 'L_' in x.name():
					L_UpperSewLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipLowerCtrlList :
				if 'L_' in x.name():
					L_LowerLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipLowerSewBrigeList :
				if 'L_' in x.name():
					L_LowerSewLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipUpperCtrlList :
				if 'R_' in x.name():
					R_UpperLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipUpperSewBrigeList :
				if 'R_' in x.name():
					R_UpperSewLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipLowerCtrlList :
				if 'R_' in x.name():
					R_LowerLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipLowerSewBrigeList :
				if 'R_' in x.name():
					R_LowerSewLip.update({x.name():xform(x,q=1,t=1,ws=1)[0]})
			for x in self.lipUpperCtrlList :
				if 'M_' in x.name():
					M_UpperLip =  x
			for x in self.lipUpperSewBrigeList :
				if 'M_' in x.name():
					M_UpperSewLip =  x
			for x in self.lipLowerCtrlList :
				if 'M_' in x.name():
					M_LowerLip =  x
			for x in self.lipLowerSewBrigeList :
				if 'M_' in x.name():
					M_LowerSewLip = x
			L_UpperLip = sorted(L_UpperLip, key=lambda x:L_UpperLip[x] , reverse  =1 )
			L_UpperSewLip = sorted(L_UpperSewLip, key=lambda x:L_UpperSewLip[x] , reverse  =1 )
			L_LowerLip = sorted(L_LowerLip, key=lambda x:L_LowerLip[x] , reverse  =1 )
			L_LowerSewLip = sorted(L_LowerSewLip, key=lambda x:L_LowerSewLip[x] , reverse  =1 )
			R_UpperLip = sorted(R_UpperLip, key=lambda x:R_UpperLip[x])
			R_UpperSewLip = sorted(R_UpperSewLip, key=lambda x:R_UpperSewLip[x])
			R_LowerLip = sorted(R_LowerLip, key=lambda x:R_LowerLip[x])
			R_LowerSewLip = sorted(R_LowerSewLip, key=lambda x:R_LowerSewLip[x])
			for x in range(len(L_UpperLip)):
				oldMinValue = 1.0/(len(L_UpperLip)+1)*x
				oldMaxValue = 1.0/(len(L_UpperLip)+1)*(x+1)
				setRange = createNode('setRange' , name = L_UpperLip[x].replace('Upper','')+'_setRange')
				self.L_LipConnerCTL.lipSew>>setRange.valueX
				setRange.oldMinX.set(10*oldMinValue)
				setRange.oldMaxX.set(10*oldMaxValue)
				setRange.minX.set(0)
				setRange.maxX.set(0.5)
				reverse = createNode('reverse' , name = L_UpperLip[x].replace('Upper','')+'_reverse')
				setRange.outValueX>>reverse.inputX
				getParentInfo = matrix.findWeightObj(L_UpperLip[x] , selectMode = 0)
				for a in getParentInfo.listAttr(k=1):
					if L_UpperSewLip[x] in a.name():
						reverse.outputX>>a
					else :
						setRange.outValueX>>a
				getParentInfo = matrix.findWeightObj(L_LowerLip[x] , selectMode = 0)
				for a in getParentInfo.listAttr(k=1):
					if L_LowerSewLip[x] in a.name():
						reverse.outputX>>a
					else :
						setRange.outValueX>>a
			for x in range(len(R_UpperLip)):
				oldMinValue = 1.0/(len(R_UpperLip)+1)*x
				oldMaxValue = 1.0/(len(R_UpperLip)+1)*(x+1)
				setRange = createNode('setRange' , name = R_UpperLip[x].replace('Upper','')+'_setRange')
				self.R_LipConnerCTL.lipSew>>setRange.valueX
				setRange.oldMinX.set(10*oldMinValue)
				setRange.oldMaxX.set(10*oldMaxValue)
				setRange.minX.set(0)
				setRange.maxX.set(0.5)
				reverse = createNode('reverse' , name = R_UpperLip[x].replace('Upper','')+'_reverse')
				setRange.outValueX>>reverse.inputX
				getParentInfo = matrix.findWeightObj(R_UpperLip[x] , selectMode = 0)
				for a in getParentInfo.listAttr(k=1):
					if R_UpperSewLip[x] in a.name():
						reverse.outputX>>a
					else :
						setRange.outValueX>>a
				getParentInfo = matrix.findWeightObj(R_LowerLip[x] , selectMode = 0)
				for a in getParentInfo.listAttr(k=1):
					if R_LowerSewLip[x] in a.name():
						reverse.outputX>>a
					else :
						setRange.outValueX>>a
			L_setRange = createNode('setRange' , name = 'L'+M_UpperLip.replace('Upper','')+'_setRange')
			self.L_LipConnerCTL.lipSew>>L_setRange.valueX
			L_setRange.oldMinX.set(7.5)
			L_setRange.oldMaxX.set(10)
			L_setRange.minX.set(0)
			L_setRange.maxX.set(0.25)
			getParentInfo = matrix.findWeightObj(M_UpperLip , selectMode = 0)
			R_setRange = createNode('setRange' , name = 'R'+M_UpperLip.replace('Upper','')+'_setRange')
			self.R_LipConnerCTL.lipSew>>R_setRange.valueX
			R_setRange.oldMinX.set(7.5)
			R_setRange.oldMaxX.set(10)
			R_setRange.minX.set(0)
			R_setRange.maxX.set(0.25)
			reverse = createNode('reverse' , name = M_UpperLip.replace('Upper','')+'_reverse')
			setRange_adl = createNode('addDoubleLinear' , name = M_UpperLip.replace('Upper','')+'_setRange_addDoubleLinear')
			L_setRange.outValueX>>setRange_adl.input1
			R_setRange.outValueX>>setRange_adl.input2
			setRange_adl.output>>reverse.inputX
			getParentInfo = matrix.findWeightObj(M_UpperLip , selectMode = 0)
			for a in getParentInfo.listAttr(k=1):
				if M_UpperSewLip.name() in a.name():
					reverse.outputX>>a
				else :
					setRange_adl.output>>a
			getParentInfo = matrix.findWeightObj(M_LowerLip , selectMode = 0)
			for a in getParentInfo.listAttr(k=1):
				if M_LowerSewLip.name() in a.name():
					reverse.outputX>>a
				else :
					setRange_adl.output>>a
			####parentCtrlsLayout
			for ctrl in PyNode(self.headCTL).getChildren() :
				if ctrl.type() != 'transform' :
					pass
				elif 'Gross' in ctrl.name():
					parent(ctrl , self.grossCtrlGRP)
				elif 'Part' in ctrl.name():
					parent(ctrl , self.partCtrlGRP)
				elif 'Jaw' in ctrl.name():
					parent(ctrl , self.grossCtrlGRP)
				elif 'HeadUpper' in ctrl.name() or 'HeadLower' in ctrl.name() :
					parent(ctrl , self.grossCtrlGRP)
				elif 'Teeth' in ctrl.name() or 'Tongue' in ctrl.name():
					parent(ctrl , self.otherCtrlGRP)
				else :
					parent(ctrl , self.secCtrlGRP)
			parent(self.grossCtrlGRP , self.headCTL)
			parent(self.partCtrlGRP , self.headCTL)
			parent(self.secCtrlGRP , self.headCTL)
			parent(self.otherCtrlGRP , self.headCTL)	
			#########Eye sets
			self.L_lidCtrlsList = [PyNode(x.name().replace('_Skeleton','_CTL')) for x in self.L_lidSkeletonList]
			self.R_lidCtrlsList = [PyNode(x.name().replace('_Skeleton','_CTL')) for x in self.R_lidSkeletonList]
			self.L_lidPartCtrlsList = [PyNode(x.name().replace('CTL','Part_CTL')) for x in self.L_lidCtrlsList]
			self.R_lidPartCtrlsList = [PyNode(x.name().replace('CTL','Part_CTL')) for x in self.R_lidCtrlsList]
			self.LidNodesGRP = group(em=1,name = 'LidNodes_GPR')
			self.LidNodesGRP.inheritsTransform.set(0)
			#### follow
			#self.L_eyeBallCTL
			#self.R_eyeBallCTL
			#self.L_lipUpperGroosCTL
			#self.R_lipUpperGroosCTL
			#self.L_lipLowerGroosCTL
			#self.R_lipLowerGroosCTL
			balls = [self.L_eyeBallCTL , self.R_eyeBallCTL]
			UD = [[self.L_lipUpperGroosCTL , self.L_lipLowerGroosCTL],[self.R_lipUpperGroosCTL , self.R_lipLowerGroosCTL]]
			for x in balls:
				ball = PyNode(x)
				addAttr(ball , ln = '_' , nn = '_______' , at = 'enum' ,en = 'LidAttr:', k=1 )
				ball._.lock()
				addAttr(ball , ln = 'fleshyEye' ,at = 'double' , dv=0.2 , min = 0 , max = 1 , k = 1 )
				addAttr(ball , ln = 'pupilIn' , at = 'double' , dv = 0 , min = -1 , max = 1 , k = 1 )
				addAttr(ball , ln = 'pupilOut' , at = 'double' , dv = 0 , min = -1 , max = 1 , k = 1 )
				target = UD[balls.index(x)]
				for i in target:
					i = PyNode(i)
					attrs = matrix.addMatrix(ball.name(),i.name(),i.name()+'_Matrix' , parentGRP = ['CTL_SDK'] , addPass = True)
					for a in attrs[1:]:
						ball.fleshyEye>>a


			parent(self.LidNodesGRP , self.moduleGRP)
			for i in [self.L_eyeBallCTL , self.R_eyeBallCTL ]:
				eyeIndex = [self.L_eyeBallCTL , self.R_eyeBallCTL ].index(i)
				lid = spherePath.spherePath()
				rigTool.alignObj([i],[lid.loc])
				for x in [self.L_lidCtrlsList,self.R_lidCtrlsList][eyeIndex]:
					rootGRP,output , start=lid.doSets(x , aimVector = [[0,0,1],[0,0,-1]][eyeIndex] , addDepthAttr = 1 , changeSoure = False , matrixReplace = True , prefix = x.name().replace('_CTL' , '_'))
					matrix.addMatrix(x,x.name().replace('CTL','JNT'),x.name().replace('CTL','JNT')+'_Matrix' , addPass = True)
					#parentConstraint(i , start , mo=1 , sr = ['x','y','z'])
					#scaleConstraint(i , start, mo=1)
					matrix.addMatrix(PyNode(i).name(),PyNode(start).name(),PyNode(start).name()+'_Matrix' , addPass = True)
					parent(rootGRP,self.LidNodesGRP)
				lid.end()
				lid = spherePath.spherePath()
				rigTool.alignObj([i],[lid.loc])
				for x in [self.L_lidPartCtrlsList,self.R_lidPartCtrlsList][eyeIndex]:
					rootGRP,output , start=lid.doSets(x , aimVector = [[0,0,1],[0,0,-1]][eyeIndex] , addDepthAttr = 1 , changeSoure = False , matrixReplace = True , prefix = x.name().replace('_CTL' , '_'))
					#parentConstraint(i , start , mo=1 , sr = ['x','y','z'])
					#scaleConstraint(i , start, mo=1)
					matrix.addMatrix(PyNode(i).name(),PyNode(start).name(),PyNode(start).name()+'_Matrix' , addPass = True)
					parent(rootGRP,self.LidNodesGRP)
				lid.end()
			parentConstraint(self.headCTL , self.LidNodesGRP , mo = 1)
			scaleConstraint(self.headCTL , self.LidNodesGRP , mo = 1 )
			#######  mouth Path
			ratio = PyNode(self.rootPosition).scaleZ.get()
			if objExists('MouthPath_position'):
				mouthPath = spherePath.spherePath(loc = 'MouthPath_position')
				L_pathRootGRP , L_pathOutput , L_pathStart = mouthPath.doSets(self.L_LipConnerCTL.name() ,aimVector = [0,0,1] , addDepthAttr = 1 , changeSoure = 1 , matrixReplace = 1 , prefix = self.L_LipConnerCTL.name().replace('_CTL' , '_'))
				R_pathRootGRP , R_pathOutput , R_pathStart = mouthPath.doSets(self.R_LipConnerCTL.name() ,aimVector = [0,0,-1] , addDepthAttr = 1 , changeSoure = 1 , matrixReplace = 1 , prefix = self.R_LipConnerCTL.name().replace('_CTL' , '_') )
				M_pathRootGRP , M_pathOutput , M_pathStart = mouthPath.doSets(PyNode(self.M_MouthGrossCTL).name() ,aimVector = [0,0,1] , addDepthAttr = 1 , changeSoure = 0 , matrixReplace = 1 , prefix = PyNode(self.M_MouthGrossCTL).name().replace('_CTL' , '_') )
				M_pathOutput = PyNode(M_pathOutput)
				M_pathOutput.tx.inputs(p=1)[0]//M_pathOutput.tx
				M_pathOutput.ty.inputs(p=1)[0]//M_pathOutput.ty
				M_pathOutput.tz.inputs(p=1)[0]//M_pathOutput.tz
				M_pathOutput.rx.inputs(p=1)[0]//M_pathOutput.rx
				M_pathOutput.rz.inputs(p=1)[0]//M_pathOutput.rz
				delete(M_pathOutput.sx.inputs()[0])
				renameAttr(self.M_MouthGrossCTL+'.matrixBase' ,  'matrix_Temp')
				matrix.addMatrix(PyNode(self.M_MouthGrossCTL).name(),M_pathOutput,M_pathOutput.name()+'_Matrix' , addPass = True)
				renameAttr(self.M_MouthGrossCTL+'.matrix_Temp' ,  'matrixBase')
				self.LipNodesGRP = group(em=1,name = 'LipNodes_GPR')
				self.LipNodesGRP.inheritsTransform.set(0)
				parent(L_pathRootGRP , R_pathRootGRP ,M_pathRootGRP, self.LipNodesGRP)
				parent(self.LipNodesGRP , self.moduleGRP)
				parentConstraint(self.jawUpperCTL , self.jawLowerCTL , L_pathStart , sr = ['x','y','z'] , mo=1)
				parentConstraint(self.jawUpperCTL , self.jawLowerCTL , R_pathStart , sr = ['x','y','z'] , mo=1)
				parentConstraint(self.jawUpperCTL , self.jawLowerCTL , M_pathStart , sr = ['x','y','z'] , mo=1)
				parentConstraint(self.headCTL , self.LipNodesGRP , mo = 1)
				scaleConstraint(self.headCTL , self.LipNodesGRP , mo = 1 )

			#matrix.importMtx(path = os.path.abspath(os.path.dirname(temp.__path__[0])+'/temp/defaultMatrix.mtx') )
			
			#####   LipConner Height
			for x in [self.L_LipConnerCTL,self.R_LipConnerCTL]:
				addAttr(x , ln = 'lipConnerHeight' , at ='double' , min = -10 , max = 10 , k=1)
				sdk = PyNode(x.name().replace('CTL' , 'CTL_SDK'))
				uu = createNode('animCurveUU' , name = sdk.name()+'_translateX_animCurveUU')
				x.lipConnerHeight>>uu.input
				uu.output>>sdk.ty
				setDrivenKeyframe( sdk.ty.name(), cd = x.lipConnerHeight.name() )
				x.lipConnerHeight.set(10)
				sdk.ty.set(ratio*2)
				setDrivenKeyframe( sdk.ty.name(), cd = x.lipConnerHeight.name() )
				x.lipConnerHeight.set(-10)
				sdk.ty.set(ratio*-2)
				setDrivenKeyframe( sdk.ty.name(), cd = x.lipConnerHeight.name() )
				x.lipConnerHeight.set(0)
				sr = createNode('setRange' , name = sdk.name()+'_lipConnerHeightRatio_setRange')
				sr.oldMinX.set(0)
				sr.oldMaxX.set(30)
				sr.minX.set(0)
				sr.maxX.set(1)
				mdl = createNode('multDoubleLinear' , name = sdk.name()+'_lipConnerHeightRatio_multDoubleLinear')
				PyNode(self.jawLowerCTL).rx>>sr.valueX
				x.lipConnerHeight>>mdl.input1
				sr.outValueX>>mdl.input2
				mdl.output>>uu.input
				keyTangent(uu,inTangentType='Linear',outTangentType='Linear')
			###   jaw collider
			#  self.jawLowerCTL
			#  self.jawUpperCTL
			ctl = PyNode(self.jawLowerCTL)
			sdk = PyNode(PyNode(self.jawLowerCTL).name().replace('CTL','CTL_SDK'))
			matrixGRP = PyNode(PyNode(self.jawLowerCTL).name().replace('CTL','CTL_Matrix'))
			upperSDK = PyNode(PyNode(self.jawUpperCTL).name().replace('CTL','CTL_SDK'))
			multMatrix = createNode('multMatrix' , name = 'JawCollider_multMatrix')
			#matrixGRP.matrix>>multMatrix.matrixIn[0]
			sdk.matrix>>multMatrix.matrixIn[0]
			ctl.matrix>>multMatrix.matrixIn[1]
			decomposeMatrix=createNode('decomposeMatrix' , name = 'JawCollider_decomposeMatrix')
			multMatrix.matrixSum>>decomposeMatrix.inputMatrix
			condition = createNode('condition' , name = 'JawCollider_condition')
			decomposeMatrix.outputRotateX>>condition.colorIfTrueR
			decomposeMatrix.outputRotateX>>condition.firstTerm
			condition.colorIfFalseR.set(0)
			condition.operation.set(4)
			ua = createNode('animCurveUA' , name = 'JawCollider_animCurveUA')
			condition.outColorR>>ua.input
			ua.output>>upperSDK.rx
			setDrivenKeyframe( upperSDK.rx.name(), cd = condition.outColorR.name() )
			keyframe(ua,option = 'over' , index = 0 , absolute = 1 , floatChange = -100 )
			keyframe(ua,option = 'over' , index = 0 , absolute = 1 , valueChange = -100 )
			setDrivenKeyframe( upperSDK.rx.name(), cd = condition.outColorR.name() )
			keyframe(ua,option = 'over' , index = 1 , absolute = 1 , floatChange = 100 )
			keyframe(ua,option = 'over' , index = 1 , absolute = 1 , valueChange = 100 )
			keyTangent(ua,inTangentType='Linear',outTangentType='Linear')
			####    mouth up down
			self.M_MouthGrossCTL = PyNode(self.M_MouthGrossCTL)
			addAttr(self.M_MouthGrossCTL , ln = '_' ,nn='_______', at ='enum' ,en='Attrs:', k=1)
			PyNode(self.M_MouthGrossCTL)._.lock()
			addAttr(self.M_MouthGrossCTL , ln = 'lipCenterHeight' , at= 'double' , min = -10 , max = 10 , k=1)
			for x in [self.M_upperLipGrossCTL,self.M_lowerLipGrossCTL]:
				x = PyNode(x)
				sdk = PyNode(x.name().replace('CTL' , 'CTL_SDK'))

				setDrivenKeyframe( sdk.ty.name(), cd = self.M_MouthGrossCTL.lipCenterHeight.name() )
				self.M_MouthGrossCTL.lipCenterHeight.set(10)
				sdk.ty.set(ratio*2)
				setDrivenKeyframe( sdk.ty.name(), cd = self.M_MouthGrossCTL.lipCenterHeight.name() )
				self.M_MouthGrossCTL.lipCenterHeight.set(-10)
				sdk.ty.set(ratio*-2)
				setDrivenKeyframe( sdk.ty.name(), cd = self.M_MouthGrossCTL.lipCenterHeight.name() )
				self.M_MouthGrossCTL.lipCenterHeight.set(0)
				keyTangent(sdk.ty.inputs()[0] ,inTangentType='Linear',outTangentType='Linear' )
			####  eyeSets
			# self.L_EyeCTL
			# self.R_EyeCTL
			# self.L_lipUpperGroosCTL
			# self.R_lipUpperGroosCTL
			# self.L_lipLowerGroosCTL
			# self.R_lipLowerGroosCTL
			for x in [self.L_EyeCTL , self.R_EyeCTL]:
				x_index = [self.L_EyeCTL , self.R_EyeCTL].index(x)
				x = PyNode(x)
				addAttr(x , ln = '_' , nn = '_______' , at = 'enum' , en = 'Attrs:' , k=1 )
				x._.lock()
				addAttr(x , ln = 'blink' , at = 'double' , min = -10 , max = 10 , k=1 )
				addAttr(x , ln = 'upperBlink' , at = 'double' , min = -10 , max = 10 , k=1 )
				addAttr(x , ln = 'lowerBlink' , at = 'double' , min = -10 , max = 10 , k=1 )
				addAttr(x , ln = 'lidCenterHeight' , at = 'double' , min = -10 , max = 10 , k=1 )
				EyeCtlList = [[self.L_lipUpperGroosCTL , self.L_lipLowerGroosCTL] , [self.R_lipUpperGroosCTL , self.R_lipLowerGroosCTL]]
				upper = PyNode(EyeCtlList[x_index][0].replace('CTL' , 'CTL_SDK'))
				lower = PyNode(EyeCtlList[x_index][1].replace('CTL' , 'CTL_SDK'))
				setDrivenKeyframe( upper.ty.name(), cd = x.blink.name() , itt = 'Linear' , ott = 'Linear')
				x.blink.set(10)
				upper.ty.set(ratio*1)
				setDrivenKeyframe( upper.ty.name(), cd = x.blink.name() , itt = 'Linear' , ott = 'Linear')
				x.blink.set(-10)
				upper.ty.set(ratio*-1)
				setDrivenKeyframe( upper.ty.name(), cd = x.blink.name() , itt = 'Linear' , ott = 'Linear')
				x.blink.set(0)
				setDrivenKeyframe( lower.ty.name(), cd = x.blink.name() , itt = 'Linear' , ott = 'Linear')
				x.blink.set(10)
				lower.ty.set(ratio*-1)
				setDrivenKeyframe( lower.ty.name(), cd = x.blink.name() , itt = 'Linear' , ott = 'Linear')
				x.blink.set(-10)
				lower.ty.set(ratio*1)
				setDrivenKeyframe( lower.ty.name(), cd = x.blink.name() , itt = 'Linear' , ott = 'Linear')
				x.blink.set(0)
				setDrivenKeyframe( upper.ty.name(), cd = x.lidCenterHeight.name() , itt = 'Linear' , ott = 'Linear')
				setDrivenKeyframe( lower.ty.name(), cd = x.lidCenterHeight.name() , itt = 'Linear' , ott = 'Linear')
				x.lidCenterHeight.set(10)
				upper.ty.set(ratio*1)
				lower.ty.set(ratio*1)
				setDrivenKeyframe( upper.ty.name(), cd = x.lidCenterHeight.name() , itt = 'Linear' , ott = 'Linear')
				setDrivenKeyframe( lower.ty.name(), cd = x.lidCenterHeight.name() , itt = 'Linear' , ott = 'Linear')
				x.lidCenterHeight.set(-10)
				upper.ty.set(ratio*-1)
				lower.ty.set(ratio*-1)
				setDrivenKeyframe( upper.ty.name(), cd = x.lidCenterHeight.name() , itt = 'Linear' , ott = 'Linear')
				setDrivenKeyframe( lower.ty.name(), cd = x.lidCenterHeight.name() , itt = 'Linear' , ott = 'Linear')
				x.lidCenterHeight.set(0)
				setDrivenKeyframe( upper.ty.name(), cd = x.upperBlink.name() , itt = 'Linear' , ott = 'Linear')
				x.upperBlink.set(10)
				upper.ty.set(ratio*1)
				setDrivenKeyframe( upper.ty.name(), cd = x.upperBlink.name() , itt = 'Linear' , ott = 'Linear')
				x.upperBlink.set(-10)
				upper.ty.set(ratio*-1)
				setDrivenKeyframe( upper.ty.name(), cd = x.upperBlink.name() , itt = 'Linear' , ott = 'Linear')
				x.upperBlink.set(0)
				setDrivenKeyframe( lower.ty.name(), cd = x.lowerBlink.name() , itt = 'Linear' , ott = 'Linear')
				x.lowerBlink.set(10)
				lower.ty.set(ratio*-1)
				setDrivenKeyframe( lower.ty.name(), cd = x.lowerBlink.name() , itt = 'Linear' , ott = 'Linear')
				x.lowerBlink.set(-10)
				lower.ty.set(ratio*1)
				setDrivenKeyframe( lower.ty.name(), cd = x.lowerBlink.name() , itt = 'Linear' , ott = 'Linear')
				x.lowerBlink.set(0)
			####  cheek
			#####  sets
			tongueJoint_set = sets(ls('*Tongue*_JNT') , name= 'TongueSkinJoints_Set')
			teethUpper_set = sets(ls('*TeethUpper*_JNT') , name= 'TeethUpperSkinJoints_Set')
			teethLower_set = sets(ls('*TeethLower*_JNT') , name= 'TeethLowerSkinJoints_Set')
			L_eyeBall_set = sets(ls('L_*EyeBall*_JNT'),name= 'L_EyeBall_Set')
			R_eyeBall_set = sets(ls('R_*EyeBall*_JNT'),name= 'R_EyeBall_Set')
			faceJoint_set = sets(list(set(ls('*_JNT'))^set(ls('*Tongue*_JNT')+ls('*TeethUpper*_JNT')+ls('*TeethLower*_JNT')+ls('L_*EyeBall*_JNT')+ls('R_*EyeBall*_JNT'))) , name = 'FaceSkinJoints_Set')
			allSkin_set = sets(tongueJoint_set,teethUpper_set,teethLower_set,L_eyeBall_set,R_eyeBall_set,faceJoint_set,name ='AllSkinJoint_Set' )
			####  skin
			for geo in self.faceGeo:
				try:skinCluster(faceJoint_set , geo+'_Skin' , name = 'FaceGeo_SkinCluster')
				except:pass
			for geo in self.tongueGeo:
				try:skinCluster(tongueJoint_set , geo+'_Skin' , name = 'TongueGeo_SkinCluster')
				except:pass
			for geo in self.upperTeethGeo:
				try:skinCluster(teethUpper_set , geo+'_Skin' , name = 'UpperTeethGeo_SkinCluster')
				except:pass
			for geo in self.lowerTeethGeo:
				try:skinCluster(teethLower_set , geo+'_Skin' , name = 'LpperTeethGeo_SkinCluster')
				except:pass
			for geo in self.EyeBallGeo:
				try:skinCluster(L_eyeBall_set,R_eyeBall_set , geo+'_Skin' , name = 'EyeBallGeo_SkinCluster')
				except:pass
			#######  Lattice
			#######  Lattice
			#######  Lattice
			#######  Lattice
			#######  Lattice
			#######  Lattice
			geo = self.faceGeo+self.EyeBallGeo+self.upperTeethGeo+self.lowerTeethGeo+self.tongueGeo+self.otherGeo
			geoList = list(set(geo))
			lattice_head_geo = []
			latticeRootCTL = group(em=1 , name = 'Lattice_global_CTL')
			baseJNTGRP = group(em=1 , name = 'Facial_Lattice_BaseJNT_GRP')
			select(cl=1)
			lattice_jaw_baseJNT = joint(name = 'Facial_LatticeJaw_BaseJNT')
			select(cl=1)
			lattice_head_baseJNT = joint(name = 'Facial_LatticeHead_BaseJNT')
			parent(baseJNTGRP , latticeRootCTL)
			parent(lattice_jaw_baseJNT , lattice_head_baseJNT , baseJNTGRP)
			lattice_jaw_geo = []
			latticeHeadGeoGRP = group(em=1 , name = 'Facial_LatticeHeadGeomtery_GRP')
			latticeJawGeoGRP = group(em=1 , name = 'Facial_LatticeJawGeomtery_GRP')
			for x in geoList:
				geo = duplicate(x,name = PyNode(x).name()+'_Head_Lattice')[0] 
				lattice_head_geo.append(geo)
				parent(geo , latticeHeadGeoGRP)
			for x in geoList:
				geo = duplicate(x,name = PyNode(x).name()+'_Jaw_Lattice')[0] 
				lattice_jaw_geo.append(geo)
				parent(geo , latticeJawGeoGRP)
			#baseLattice = PyNode('Facial_Lattice')
			#baseLatticeShape = baseLattice.getShapes()[0]
			#baseLatticeBase = PyNode('Facial_LatticeBase')
			LatticeMiddleLoc = ls('LatticeMiddle_*_LatticeLOC')
			LatticeUpperLoc = ls('LatticeUpper_*_LatticeLOC')
			LatticeLowerLoc = ls('LatticeLower_*_LatticeLOC')
			LatticeJawLoc = ls('LatticeJaw_*_LatticeLOC')
			baseDeformGRP = PyNode('Facial_Lattice_GRP')
			LatticeUpper = rigTool.JointsOnSurface( point = [x.name() for x in LatticeMiddleLoc]+[x.name() for x in LatticeUpperLoc] , prefix = 'LatticelUpper_' )
			LatticeUpper.rigging( keepLength = False , volume = True ,  scale = True , scaleOffset = False , separateCtrl = False , axis = ['y','x','z']  , numberOfJoints = 4)
			LatticeUpperJNTList = LatticeUpper.addJoints()
			LatticeUpperIKCtrlsList = LatticeUpper.addIKCtrl()

			LatticeLower = rigTool.JointsOnSurface( point = [x.name() for x in LatticeMiddleLoc]+[x.name() for x in LatticeLowerLoc] , prefix = 'LatticelLower_' )
			LatticeLower.rigging( keepLength = False , volume = True ,  scale = True , scaleOffset = False , separateCtrl = False , axis = ['y','x','z']  , numberOfJoints = 4)
			LatticeLowerJNTList = LatticeLower.addJoints()
			LatticeLowerIKCtrlsList = LatticeLower.addIKCtrl()

			LatticeJaw = rigTool.JointsOnSurface( point = [x.name() for x in LatticeJawLoc] , prefix = 'Lattice_Jaw_' )
			LatticeJaw.rigging( keepLength = False , volume = True ,  scale = True , scaleOffset = False , separateCtrl = False , axis = ['z','x','y']  , numberOfJoints = 4)
			LatticeJawJNTList = LatticeJaw.addJoints()
			LatticeJawIKCtrlsList = LatticeJaw.addIKCtrl()
			parent(LatticeUpper.CtrlGroup , LatticeJaw.CtrlGroup , LatticeLower.CtrlGroup , self.otherCtrlGRP)
			select(cl=1)
			#latticeLists = cmds.lattice(dv =(7,7,7) , n = 'LatticlDeform')
			#latticeDeform = PyNode(latticeLists[0])
			#latticeDeform.outsideLattice.set(1)
			#lattice = PyNode(latticeLists[1])
			#latticeShape = lattice.getShapes()[0]
			#base = PyNode(latticeLists[2])
			#latticeShape.sDivisions.set(baseLatticeShape.sDivisions.get())
			#latticeShape.tDivisions.set(baseLatticeShape.tDivisions.get())
			#latticeShape.uDivisions.set(baseLatticeShape.uDivisions.get())
			#delete(parentConstraint(baseLattice , lattice ))
			#delete(scaleConstraint(baseLattice , lattice ))
			#delete(parentConstraint(baseLatticeBase , base ))
			#delete(scaleConstraint(baseLatticeBase , base ))
			#lattice.setGeometry(latticeGeoGRP)
			#lattice.setGeometry(self.grossCtrlGRP)
			#lattice.setGeometry(self.partCtrlGRP)
			#lattice.setGeometry(self.secCtrlGRP)
			#lattice.setGeometry(self.otherCtrlGRP)
			LatticeJawGRP = PyNode(LatticeJaw.RigGroup)
			LatticeUpperGRP = PyNode(LatticeUpper.RigGroup)
			LatticeLowerGRP = PyNode(LatticeLower.RigGroup)
			latticeRootGRP = group(em=1 , name = 'Lattice_Rig_GRP')
			latticeGRP = group(em=1 , name = 'Lattice_GRP')
			#parent(lattice,base, latticeGRP)
			parent(latticeGRP,LatticeUpperGRP , LatticeJawGRP ,LatticeLowerGRP ,  latticeRootGRP)
			rigTool.addGroup(obj=latticeRootCTL.name(),objSuffix='CTL',grpSuffix=['CTL_SDK','CTL_Matrix','CTL_GRP'])
			latticeRootCTLGRP = PyNode(latticeRootCTL.name()+'_GRP')
			parent(latticeRootGRP , latticeRootCTL)
			parent(latticeRootCTLGRP , self.moduleGRP)
			matrix.addMatrix(PyNode(self.headCTL).name(),latticeRootCTL.name(),latticeRootCTL.name()+'_Matrix' , addPass = True)
			latticeGRP.inheritsTransform.set(0)
			latticeGRP.v.set(0)
			LatticeJawGRP.inheritsTransform.set(0)
			LatticeUpperGRP.inheritsTransform.set(0)
			#parentConstraint(latticeRootGRP , lattice)
			scaleConstraint(latticeRootGRP , LatticeJawGRP)
			parentConstraint(latticeRootGRP , LatticeUpperGRP)
			scaleConstraint(latticeRootGRP , LatticeUpperGRP)
			parentConstraint(latticeRootGRP , LatticeLowerGRP)
			scaleConstraint(latticeRootGRP , LatticeLowerGRP)
			#parentConstraint(latticeRootGRP , base , mo=1)
			#scaleConstraint(latticeRootGRP , base , mo=1)
			LatticeUpperGRP.scaleY>>LatticeUpperGRP.globalScale
			LatticeJawGRP.scaleY>>LatticeJawGRP.globalScale
			LatticeLowerGRP.scaleY>>LatticeLowerGRP.globalScale
			rigTool.autoAssignColor(obj = [PyNode(x).name() for x in LatticeUpperIKCtrlsList+LatticeJawIKCtrlsList+LatticeLowerIKCtrlsList] , gloomy=1)
			rigTool.scaleCtrlsShapes(obj = [PyNode(x).name() for x in LatticeUpperIKCtrlsList+LatticeJawIKCtrlsList+LatticeLowerIKCtrlsList] , value = PyNode(self.rootPosition).scaleZ.get())
			for x in LatticeJawIKCtrlsList+LatticeUpperIKCtrlsList+LatticeLowerIKCtrlsList:
				x = PyNode(x)
				x.v.unlock()
				x.v.set(0)
				x.v.lock()
			jawCTL = group(em=1 , name = 'M_JawLattice_CTL')
			upperCTL = group(em=1 , name = 'M_UpperLattice_CTL')
			middleCTL = group(em=1 , name = 'M_MiddleLattice_CTL')
			rigTool.replaceCVShape(soure = 'Lattice_CV', target = [middleCTL.name(), jawCTL.name() , upperCTL.name()] , replace = 1)
			rigTool.scaleCtrlsShapes(obj = [middleCTL] , value = PyNode(self.rootPosition).scaleZ.get())
			rigTool.scaleCtrlsShapes(obj = [jawCTL] , value = PyNode(self.rootPosition).scaleZ.get()*0.3)
			rigTool.scaleCtrlsShapes(obj = [upperCTL] , value = PyNode(self.rootPosition).scaleZ.get()*0.5)
			rigTool.autoAssignColor(obj = [ middleCTL , jawCTL , upperCTL ], gloomy=1)
			rigTool.alignObj([LatticeUpperIKCtrlsList[0],LatticeLowerIKCtrlsList[0]] , [middleCTL])
			rigTool.alignObj([LatticeJawIKCtrlsList[-1]] , [jawCTL])
			rigTool.alignObj([LatticeUpperIKCtrlsList[-1]] , [upperCTL] )
			middleCTL.rotate.set([0,0,0])
			jawCTL.rotate.set([0,0,0])
			upperCTL.rotate.set([0,0,0])
			parent(middleCTL , jawCTL, upperCTL , self.otherCtrlGRP)
			rigTool.addGroup(obj=middleCTL.name(),objSuffix='_CTL',grpSuffix=['_CTL_SDK','_CTL_Matrix','_CTL_GRP'])
			rigTool.addGroup(obj=jawCTL.name(),objSuffix='_CTL',grpSuffix=['_CTL_SDK','_CTL_Matrix','_CTL_GRP'])
			rigTool.addGroup(obj=upperCTL.name(),objSuffix='_CTL',grpSuffix=['_CTL_SDK','_CTL_Matrix','_CTL_GRP'])
			matrix.addMatrix(middleCTL.name() , LatticeUpperIKCtrlsList[0] , LatticeUpperIKCtrlsList[0]+'_Matrix' , addPass = 1 )
			matrix.addMatrix(middleCTL.name() , LatticeLowerIKCtrlsList[0] , LatticeLowerIKCtrlsList[0]+'_Matrix' , addPass = 1 )
			matrix.addMatrix(jawCTL.name() , LatticeJawIKCtrlsList[-1] , LatticeJawIKCtrlsList[-1]+'_Matrix' , addPass = 1 )
			matrix.addMatrix(upperCTL.name() , LatticeUpperIKCtrlsList[-1] , LatticeUpperIKCtrlsList[-1]+'_Matrix' , addPass = 1 )
			#skinCluster(LatticeUpperJNTList+LatticeJawJNTList , lattice , name = 'Lattice_SkinCluster')
			for x in lattice_head_geo:skinCluster([lattice_head_baseJNT]+LatticeUpperJNTList+LatticeLowerJNTList , x , name = x+'_Lattice_Head_SkinCluster')
			for x in lattice_jaw_geo:skinCluster([lattice_jaw_baseJNT]+LatticeJawJNTList , x , name = x+'_Lattice_Jase_SkinCluster')
			#LatticeJawIKCtrlsList
			##  jaw and lattice
			jawLatticeGRP = group(em=1 ,  name = 'jawLattice_GRP')
			ctl =PyNode(jawCTL)
			addAttr(ctl , ln = '_'  , nn = '_______' , at = 'enum' , en = 'Attrs'  , k = 1 )
			ctl._.lock()
			addAttr(ctl , ln = 'jaw' , at = 'double' , k = 1 , min = 0 , max = 1 , dv = 0 )
			#addAttr(ctl , ln = 'jawAngle' , at = 'double' , k = 1 , min = 0 , max = 1 , dv = 0 )
			select(cl=1)
			start = joint(name = 'jawLatticeStart_ikJOT')
			end = joint(name = 'jawLatticeEnd_ikJOT')
			rigTool.alignObj([self.jawLowerCTL] , [start])
			rigTool.alignObj([ctl] , [end])
			parent(start , jawLatticeGRP)
			parent(jawLatticeGRP , self.moduleGRP)
			rigTool.addGroup(obj=start.name(),objSuffix='_ikJOT',grpSuffix=['_ikJOT_SDK','_ikJOT_Matrix','_ikJOT_GRP'])
			makeIdentity(start,a=1,t=1,r=1,s=1,n=0,pn=1)
			ik = ikHandle(sj = start , ee = end , name = 'jawLattice_IKHandle')[0]
			parent(ik , jawLatticeGRP)
			parentConstraint( ctl , ik )
			parentConstraint( self.headLowerCTL , start , mo = 1 )
			bw = createNode('blendWeighted' , name = PyNode(self.jawLowerCTL).name()+'_rx_BW')
			start.rx>>bw.input[0]
			ctl.jaw>>bw.weight[0]
			bw.output>>PyNode(PyNode(self.jawLowerCTL).name()+'_SDK').rx
			jawLatticeGRP.v.set(0)

			jawStartLOC =  LatticeJawLoc[0]
			headMiddleLOC = LatticeMiddleLoc[0]
			jawStart = group(em=1 , name = 'Lattice_JawStart_LOC')
			headStart = group(em=1 , name = 'Lattice_HeadStart_LOC')
			rigTool.alignObj([jawStartLOC] , [jawStart])
			rigTool.alignObj([headMiddleLOC] , [headStart])
			parent(headStart , middleCTL)
			parent(jawStart , self.headCTL)
			aimConstraint(jawStart , LatticeJawIKCtrlsList[-1] , aimVector = [0,0,-1] , upVector = [0,0,1] ,worldUpVector = [0,0,1] , worldUpType = 'objectrotation' , worldUpObject = jawStart , mo=1)
			aimConstraint(headStart , LatticeUpperIKCtrlsList[-1] , aimVector = [0,1,0] , upVector = [0,0,1] ,worldUpVector = [0,0,1] , worldUpType = 'objectrotation' , worldUpObject = headStart , mo=1)
			aimConstraint(headStart , LatticeLowerIKCtrlsList[-1] , aimVector = [0,-1,0] , upVector = [0,0,1] ,worldUpVector = [0,0,1] , worldUpType = 'objectrotation' , worldUpObject = headStart , mo=1)



			#######   sec  
			geo = self.faceGeo+self.EyeBallGeo+self.upperTeethGeo+self.lowerTeethGeo+self.tongueGeo+self.otherGeo
			geoList = list(set(geo))
			sec_geo = []
			secGeoGRP = group(em=1 , name = 'Facial_SecondGeometry_GRP')
			for x in geoList:
				geo = duplicate(x,name = PyNode(x).name()+'_Second')[0] 
				sec_geo.append(geo)
				parent(geo , secGeoGRP)
			##########  output geometry
			geo = self.faceGeo+self.EyeBallGeo+self.upperTeethGeo+self.lowerTeethGeo+self.tongueGeo+self.otherGeo
			geoList = list(set(geo))
			output_geo = []
			outputGeoGRP = group(em=1 , name = 'Facial_OutputGeomtery_GRP')
			for x in geoList:
				geo = duplicate(x,name = PyNode(x).name()+'_Output')[0] 
				output_geo.append(geo)
				parent(geo , outputGeoGRP)
				blendShape(geo,x,w=(0,1) , name ='Facial_'+PyNode(x).name()+'_Assembly_BlendShape',foc=1)
			#####  blendShape connected
			# skinGeoGRP
			# latticeGeoGRP
			# secGeoGRP
			# outputGeoGRP
			try:
				bs = blendShape(skinGeoGRP , latticeHeadGeoGRP , latticeJawGeoGRP , secGeoGRP , outputGeoGRP , name = 'Facial_Assembly_BlendShape',foc=1)
				blendShape(bs , e = 1 , w = [(0,1),(1,1),(2,1),(3,1)])
			except:pass
			############################
			#######	Final	 #######
			############################
			geometryGRP = group(em=1 , name = 'Facial_Geometry_GRP')
			parent(skinGeoGRP , latticeHeadGeoGRP , latticeJawGeoGRP , secGeoGRP ,outputGeoGRP, geometryGRP)
			parent(geometryGRP , self.facialRigGRP)
			for x in [ latticeHeadGeoGRP , latticeJawGeoGRP , secGeoGRP ,outputGeoGRP, geometryGRP]:
				x.v.set(0)
			select(cl=1)
			print ('Rigging has been successful !')
			inViewMessage( amg='Rigging has been <hl>successful</hl> !', pos='midCenterBot', fade=True)
