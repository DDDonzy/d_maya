from maya import cmds


def choseFile(path=None, *args, **kwargs):
    if not path:
        path = (cmds.fileDialog2(*args, **kwargs) or [None])[0]
    return path
