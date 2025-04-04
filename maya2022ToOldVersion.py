"""
Maya 2022+ deform to old Version Compatibility Script
==============================================

This script modifies deformers created in Maya 2022+ to make them compatible with older Maya versions.
It achieves compatibility by creating groupParts nodes for each deformer in the scene.

Features:
- Removes existing groupParts nodes (if present)
- Creates new groupId and groupParts nodes for deformers
- Properly connects input and output attributes for the deformer

Supported deformer types:
- skinCluster
- blendShape
- proximityWrap
- deltaMush
- wrap
- cluster

Usage:
1. Load the script in Maya
2. Run createGroupPartsForAllDeformers() to process all supported deformers
3. Or use createGroupParts(deformName) for a specific deformer
"""

from maya import cmds
import maya.api.OpenMaya as om


def createGroupParts(deformName):
    if not cmds.objExists(deformName):
        om.MGlobal.displayError(f"'{deformName}' is not exists!")
        return
    # delete old groupParts node
    iter_bool = True
    while iter_bool:
        orig_attr = cmds.listConnections(f"{deformName}.input[0].inputGeometry", s=1, sh=1, p=1)[0]
        orig_node = cmds.ls(orig_attr, o=1)[0]
        if cmds.objectType(orig_node) == "groupParts":
            cmds.delete(orig_node)
        else:
            iter_bool = False

    # create groupParts node
    cmds.undoInfo(ock=1)
    try:
        groupId = cmds.createNode("groupId", name=f"{deformName}GroupId", skipSelect=1)
        groupParts = cmds.createNode("groupParts", name=f"{deformName}GroupParts", skipSelect=1)
        cmds.setAttr(f"{groupParts}.isHistoricallyInteresting", 0)
        cmds.setAttr(f"{groupId}.isHistoricallyInteresting", 0)

        cmds.connectAttr(f"{groupId}.groupId", f"{groupParts}.groupId")
        cmds.connectAttr(orig_attr, f"{groupParts}.inputGeometry")
        cmds.setAttr(f"{groupParts}.ic", 1, "vtx[*]", type="componentList")

        cmds.connectAttr(f"{groupParts}.outputGeometry", f"{deformName}.input[0].inputGeometry", f=1)
        cmds.connectAttr(f"{groupId}.groupId", f"{deformName}.input[0].groupId", f=1)
    except Exception as e:
        cmds.undoInfo(cck=1)
        cmds.undo()
        om.MGlobal.displayError(f"'{deformName}' create groupParts error! undo it !")
        om.MGlobal.displayError(str(e))
    else:
        cmds.undoInfo(cck=1)

    om.MGlobal.displayInfo(f"'{deformName}' create groupParts success!")
    return groupParts, groupId


def createGroupPartsForAllDeformers():
    deformTypeList = ["skinCluster", "blendShape", "proximityWrap", "deltaMush", "wrap", "cluster"]
    for deformType in deformTypeList:
        for deformNode in cmds.ls(type=deformType):
            createGroupParts(deformNode)


if __name__ == "__main__":
    createGroupPartsForAllDeformers()
