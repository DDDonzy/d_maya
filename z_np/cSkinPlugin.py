import maya.api.OpenMaya as om
import maya.OpenMaya as om1  # type:ignore
import maya.OpenMayaMPx as ompx  # type:ignore

import z_np.src2.cSkinDeform2 as cSkinDeform

NODE_NAME = "cSkinDeformer"
NODE_ID = om1.MTypeId(0x00080033)


def nodeCreator():
    return ompx.asMPxPtr(cSkinDeform.CythonSkinDeformer())


def initializePlugin(mObj):
    mPlugin = ompx.MFnPlugin(mObj, "Donzy", "1.0", "Any")
    mPlugin.registerNode(
        NODE_NAME,
        NODE_ID,
        nodeCreator,
        cSkinDeform.CythonSkinDeformer.nodeInitializer,
        ompx.MPxNode.kDeformerNode,
    )
    om.MGlobal.displayInfo(f"{NODE_NAME} loaded successfully.")


def uninitializePlugin(mObj):
    mPlugin = ompx.MFnPlugin(mObj)
    mPlugin.deregisterNode(NODE_ID)
    om.MGlobal.displayInfo(f"{NODE_NAME} unloaded successfully.")
