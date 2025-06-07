from maya import cmds


MUTE_MESSAGE = False


def showMessage(msg, time=1000):
    if MUTE_MESSAGE:
        return
    message = f"<hl> {msg} </hl>"
    cmds.inViewMessage(amg=message, pos='botRight', fade=True, fadeInTime=100, fadeStayTime=time, fadeOutTime=100)


def muteMessage(mute: bool):
    global MUTE_MESSAGE
    MUTE_MESSAGE = mute
    return MUTE_MESSAGE
