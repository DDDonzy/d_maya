import UTILS.skin.fnSkin as sk

from gameFace.ui import ui_main as ui
from gameFace import createControls as cc
from gameFace import fit
from gameFace import build

from maya import cmds


fit.importFit()
fit.exportFit()
fit.hideClass()
fit.autoCalClassPosition()
fit.mirrorDuplicateTransform_cmd()
fit.get_fitJointByLabel()

cc.get_controlsByLabel()

build.build("Face")


sk.exportWeights()
sk.importWeights()


ui.showUI()
