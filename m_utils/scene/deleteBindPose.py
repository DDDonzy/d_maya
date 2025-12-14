from maya import cmds

import log


def deleteBindPose():
    cmds.delete(cmds.ls(type="dagPose"))
    log.success("DELETE BIND POSE DONE")
