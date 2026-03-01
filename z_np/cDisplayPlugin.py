from maya.api import OpenMaya as om
from maya.api import OpenMayaRender as omr

import z_np.src2.cDisplayNode2 as cDisplay


def maya_useNewAPI():
    pass


NODE_NAME = "WeightPreviewShape"
NODE_ID = om.MTypeId(0x80005)  # 确保这个 ID 是你申请的或测试用的独立 ID
DRAW_CLASSIFICATION = "drawdb/geometry/WeightPreview"
DRAW_REGISTRAR = "WeightPreviewShapeRegistrar"


def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "Custom", "1.0", "Any")
    plugin.registerShape(
        NODE_NAME,
        NODE_ID,
        cDisplay.WeightPreviewShape.creator,
        cDisplay.WeightPreviewShape.initialize,
        cDisplay.WeightPreviewShapeUI.creator,
        DRAW_CLASSIFICATION,
    )
    omr.MDrawRegistry.registerGeometryOverrideCreator(
        DRAW_CLASSIFICATION,
        DRAW_REGISTRAR,
        cDisplay.WeightGeometryOverride.creator,
    )


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    omr.MDrawRegistry.deregisterGeometryOverrideCreator(
        DRAW_CLASSIFICATION,
        DRAW_REGISTRAR,
    )
    plugin.deregisterNode(NODE_ID)
