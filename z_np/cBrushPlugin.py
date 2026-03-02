import maya.api.OpenMaya as om
from z_np.src.cBrush import WeightBrushContextCmd


def maya_useNewAPI():
    pass


def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "Donzy", "1.0", "Any")
    plugin.registerContextCommand(
        WeightBrushContextCmd.COMMAND_NAME,
        WeightBrushContextCmd.creator,
    )


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    plugin.deregisterContextCommand(
        WeightBrushContextCmd.COMMAND_NAME,
    )
