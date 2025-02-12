from maya import cmds

MUTE_MESSAGE = False

def showMessage(msg):
    if MUTE_MESSAGE:
        return
    message = "<hl> %s </hl>" % msg  
    cmds.inViewMessage(amg=message, pos='botRight', fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)

def muteMessage(mute):
    global MUTE_MESSAGE
    MUTE_MESSAGE = mute
    return MUTE_MESSAGE
