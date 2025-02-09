from maya import cmds

from gameFace import fit
from gameFace import build as b
fit.importFit()
fit.exportFit()
fit.hideClass()
fit.autoCalClassPosition()
fit.mirrorDuplicateTransform_cmd()


b.build("Face")

from gameFace import createControls as cc
cc.get_controlsByLabel("Sec")
fit.get_fitJointByLabel("Class")


import UTILS.skin.fnSkin as sk
sk.exportWeights()
sk.importWeights()


from gameFace.ui.ui_main import showUI
showUI()