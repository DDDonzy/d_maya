import maya.api.OpenMaya as om
import maya.OpenMaya as om1
import maya.OpenMayaMPx as ompx

import z_np.src.cSkinDeform as cSkinDeform

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
