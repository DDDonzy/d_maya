from gameFace.config import *

from maya import cmds


def choseFile(path=None, *args, **kwargs):
    if not path:
        if not kwargs.get("startingDirectory", None):
            kwargs.update({"startingDirectory": PROJECT_DIR})
        path = (cmds.fileDialog2(*args, **kwargs) or [None])[0]
    return path
