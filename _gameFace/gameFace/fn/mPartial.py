import maya.cmds as cmds
from functools import partial as original_partial



def partial(func, *args, **kwargs):
    """
    Replaces functools.partial to support Maya undo/redo in Python 2.7.
    """
    def wrapped(*inner_args, **inner_kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            all_args = args + inner_args
            all_kwargs = kwargs.copy()
            all_kwargs.update(inner_kwargs)
            return func(*all_args, **all_kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
    return wrapped


