from maya import cmds


MUTE_MESSAGE = False


def showMessage(msg, time=1000):
    if MUTE_MESSAGE:
        return
    message = f"{msg}"
    cmds.inViewMessage(amg=message, pos='botRight', fade=True, fadeInTime=200, fadeStayTime=time, fadeOutTime=200)


def muteMessage(mute: bool):
    global MUTE_MESSAGE
    MUTE_MESSAGE = mute
    return MUTE_MESSAGE
