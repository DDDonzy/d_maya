# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
from .. import temp
from pymel.core import *
import maya.cmds as cmds


def createFaceFitSkeleton():
	with UndoChunk():
		faceFitSkeletonPath = os.path.abspath(os.path.dirname(temp.__path__[0]) + '/temp/facialSkeleton.ma')
		if objExists('Facial_Skeleton_GRP'):
			message = '<hl>FaceFitSkeleton already in the scene</hl>'
			print("++++++	  FaceFitSkeleton already in the scene	  ++++++")
		else:
			cmds.file(faceFitSkeletonPath, i=True, ra=False, mergeNamespacesOnClash=False, options="v=0")
			message = 'Create has been <hl>successful</hl> !'
			print('Create has been successful !')
		inViewMessage(amg=message, pos='midCenterBot', fade=True)


def positionCtrlsVisibility():
	with UndoChunk():
		positionCtrlsGRP = PyNode('Facial_CtrlsSpace_GRP')
		positionCtrlsGRP.v.unlock()
		baseValue = positionCtrlsGRP.v.get()
		if baseValue >= 0.5:
			value = 0
			message = 'Position ctrls group is now <hl>hidden</hl> .'
		else:
			value = 1
			message = 'Position ctrls group is now <hl>displayed</hl> .'
		positionCtrlsGRP.v.set(value)
		positionCtrlsGRP.v.lock()
		inViewMessage(amg=message, pos='midCenterBot', fade=True)


def addMouthPath():
	with UndoChunk():
		if objExists('MouthPath_position'):
			delete('MouthPath_position')
			message = '<hl> MouthPath delete ! </hl>'
			inViewMessage(amg=message, pos='midCenterBot', fade=True)
		else:
			loc = spaceLocator(name='MouthPath_position')
			parent(loc, 'HeadLower_None_GRP')
			message = '<hl> Please move the locator ! </hl>'
			inViewMessage(amg=message, pos='midCenterBot', fade=True)


def latticeVisibility():
	with UndoChunk():
		LatticeCtrlsGRP = PyNode('Facial_Lattice_CTL_GRP')
		LatticeCtrlsGRP.v.unlock()
		baseValue = LatticeCtrlsGRP.v.get()
		if baseValue >= 0.5:
			value = 0
			message = 'Lattice is now <hl>hidden</hl> .'
		else:
			value = 1
			message = 'Lattice is now now <hl>displayed</hl> .'
		LatticeCtrlsGRP.v.set(value)
		LatticeCtrlsGRP.v.lock()
		inViewMessage(amg=message, pos='midCenterBot', fade=True)


def addTeethSecond():
	with UndoChunk():
		# TeethUpper_Second_GRP
		# TeethLower_Second_GRP
		# TeethUpper_cv
		# TeethLower_cv
		for x in ['TeethUpper_Second_GRP', 'TeethLower_Second_GRP', 'TeethUpper_cv', 'TeethLower_cv']:
			x = PyNode(x)
			baseValue = x.v.get()
			if baseValue >= 0.5:
				value = 0
			else:
				value = 1
			x.v.unlock()
			x.v.set(value)
			x.v.lock()
