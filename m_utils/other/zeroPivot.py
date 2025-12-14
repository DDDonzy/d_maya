from maya import cmds
import log


def zeroPivot(objList: list = []):
    if not objList:
        objList = cmds.ls(sl=1, type="transform")
    if not objList:
        log.warning("No object selected")
        return
    cmds.select(objList)
    cmds.move(0, 0, 0, ".rotatePivot", ".scalePivot", rpr=1)
    cmds.makeIdentity(a=1)
    log.success("Zero Pivot")


if __name__ == "__main__":
    zeroPivot()
