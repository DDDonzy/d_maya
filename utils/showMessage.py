from maya import cmds


def showMessage(msg):
    message = f"<hl> {msg} </hl>"
    cmds.inViewMessage(amg=message, pos='botRight', fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)
