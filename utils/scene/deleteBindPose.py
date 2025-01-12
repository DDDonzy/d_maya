from maya import cmds
from utils.showMessage import showMessage

def deleteBindPose():
    cmds.delete(cmds.ls(type="dagPose"))
    showMessage("DELETE BIND POSE DONE")