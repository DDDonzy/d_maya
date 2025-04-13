from maya import cmds
from UTILS.ui.showMessage import showMessage


def zeroPivot(objList: list = []):
    if not objList:
        objList = cmds.ls(sl=1, type="transform")
    if not objList:
        return showMessage("No object selected")
    cmds.select(objList)
    cmds.move(0, 0, 0, ".rotatePivot", ".scalePivot", rpr=1)
    cmds.makeIdentity(a=1)
    showMessage("Zero Pivot")
    
if __name__ == "__main__":
    zeroPivot()
