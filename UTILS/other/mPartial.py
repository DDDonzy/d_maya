import maya.cmds as cmds
from functools import partial as original_partial


def partial(func, *args, **kwargs):
    """
    Replaced functools.partial to support Maya undo/redo
    """
    def wrapped(*inner_args, **inner_kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            result = func(*args, *inner_args, **kwargs, **inner_kwargs)
            return result
        finally:
            cmds.undoInfo(closeChunk=True)
    return wrapped
