import maya.cmds as mc
from maya import cmds
try:
    value = 0
    status = mc.getAttr("time1.isHistoricallyInteresting")
    if status == 0:
        value = 2
    else:
        value = 0
    for each in mc.ls():
        if mc.nodeType(each) in ["groupParts", "groupId", "animCurveUU", "unitConversion"]:
            mc.setAttr((each+".isHistoricallyInteresting"), 0)
        else:
            mc.setAttr((each+'.isHistoricallyInteresting'), value)
except:
    pass
