from maya import cmds
from UTILS.showMessage import showMessage

CHANNELBOX_NAME = "mainChannelBox"

TRANSLATE_ATTR = ["tx", "ty", "tz"]
ROTATE_ATTR = ["rx", "ry", "rz"]
SCALE_ATTR = ["sx", "sy", "sz",]
VIS_ATTR = ["v"]


def _getSelectionFliteShapes():
    obj = cmds.ls(sl=1)
    shapes = cmds.ls(sl=1, s=1)
    [obj.remove(x) for x in shapes]
    return obj


def isAverageTrue(bool_list):
    average = sum(bool_list) / len(bool_list)
    return average >= 0.5


def lockAttr(obj: list = [], attr: list = []):
    boolList = []
    if isinstance(obj, str):
        obj = [obj]
    obj = obj or _getSelectionFliteShapes() or []
    attr = attr or cmds.channelBox(CHANNELBOX_NAME, q=1, sma=1) or TRANSLATE_ATTR+ROTATE_ATTR+SCALE_ATTR+VIS_ATTR

    for x in obj:
        for a in attr:
            boolList.append(cmds.getAttr(f"{x}.{a}", l=1))
    if boolList:
        lock = isAverageTrue(bool_list=boolList)
        for x in obj:
            for a in attr:
                cmds.setAttr(f"{x}.{a}", l=not lock)
                cmds.setAttr(f"{x}.{a}", k=lock)
        showMessage(f"LOCK ATTR: {not lock}".upper())


def getLockedAttr(obj: list = [], userDefine=True):
    attrList = []
    if isinstance(obj, str):
        obj = [obj]
    obj = obj or _getSelectionFliteShapes() or []

    for x in obj:
        lockedAttr = cmds.listAttr(x, l=1) or []
        if not userDefine:
            userDefineAttr = cmds.listAttr(x, ud=1, l=1) or []
            for udAttr in userDefineAttr:
                lockedAttr.remove(udAttr)
        lockedAttr = [f"{x}.{a}" for a in lockedAttr]
        attrList.extend(lockedAttr)
    return attrList


def showLockAttr(obj: list = [], userDefine=True):
    boolList = []
    lockedAttrList = []
    if isinstance(obj, str):
        obj = [obj]
    obj = obj or _getSelectionFliteShapes() or []

    lockedAttrList = getLockedAttr(obj=obj, userDefine=userDefine)
    for a in lockedAttrList:
        boolList.append(cmds.getAttr(a, k=1))

    if lockedAttrList:
        hide = not isAverageTrue(bool_list=boolList)
        for x in lockedAttrList:
            cmds.setAttr(x, k=hide)
        showMessage(f"SHOW HIDE ATTR: {hide}".upper())
