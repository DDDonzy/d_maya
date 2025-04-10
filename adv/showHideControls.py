# show adv hide controls
from maya import cmds


if __name__ == "__main__":
    objList = []
    for x in cmds.ls():
        udAttr = cmds.listAttr(x,ud=1)
        if not udAttr:
            continue
        for a in udAttr:
            if "Vis" in a:
                objList.append(f"{x}.{a}")
    for x in objList:
        cmds.setAttr(x,1)



    objList = []
    for x in cmds.ls():
        udAttr = cmds.listAttr(x,ud=1)
        if not udAttr:
            continue
        for a in udAttr:
            if "FKIKBlend" in a:
                objList.append(f"{x}.{a}")
    for x in objList:
        cmds.setAttr(x,5)
