from pymel.core import *
import maya.mel
class mainProgress ():
	def __init__(self,maxValue,status):
		self.gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')
		self.maxValue = maxValue
		self.status = status
		progressBar( self.gMainProgressBar , edit=True , beginProgress=True , isInterruptable=True , status=self.status , maxValue=self.maxValue)

	def update(self,step = 1):
		progressBar(self.gMainProgressBar, edit=True, step= step)
	def end(self):
		progressBar(self.gMainProgressBar, edit=True, endProgress=True)