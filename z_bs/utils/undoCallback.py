from maya import cmds


class BaseCallBack(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class UndoCallback(BaseCallBack):
    def __call__(self, *args):
        cmds.undoInfo(openChunk=1)
        try:
            return self.func(*self.args, **self.kwargs)
        finally:
            cmds.undoInfo(closeChunk=1)
