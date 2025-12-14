import maya.cmds as cmds

import m_utils.other.attr as attr
from m_utils.control.cvShape import mirror_cvShape_cmd, replace_cvShape_cmd, select_cvControlVertex_cmd, import_cvData, export_cvData
from m_utils.compounds import matrixConstraint, uvPin
from m_utils.other.zeroPivot import zeroPivot
from m_utils.transform import align_transform_cmd
from m_utils.mirrorEnv import mirror_selected, MIRROR_CONFIG
from m_utils.deform.skin.getSkinJoint import get_skinJoint_cmd
from m_utils.deform.skin.copyWeightsOneToN import copyWeightsOneToN_cmd
from m_utils.deform.skin.updateBindSkin import updateBindSkin_cmd
from m_utils.rename import showUI as renameShowUI
from m_utils.scene.deleteBindPose import deleteBindPose
from m_utils.scene.removeNamespace import removeNamespace
from m_utils.scene.removeUnknownPlugin import removeUnknownPlugin
from m_utils.dag.selectHierarchy import selectHierarchy_cmd
from Rainbow.rainbow_UI import rainbow_win


class Callback(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *ui_args):
        return self.func(*self.args, **self.kwargs)


def toggle_display_affected():
    is_visible = cmds.displayPref(query=True, displayAffected=True)
    cmds.displayPref(displayAffected=not is_visible)


def menuItem(*args, **kwargs):
    sourceType = kwargs.get("sourceType") or kwargs.get("stp") or "mel"
    boldFont = kwargs.get("boldFont") or kwargs.get("blf") or True
    kwargs.update({"sourceType": sourceType, "boldFont": boldFont})
    cmds.menuItem(*args, **kwargs)


def addUI(*args, **kwargs):
    cmds.popupMenu(*args, **kwargs)

    # --- Transform Menu ---
    menuItem(label="Transform", subMenu=True, radialPosition="E")
    menuItem(label="Align Transform", radialPosition="E", sourceType="python", command=Callback(align_transform_cmd))
    menuItem(label="Lock Attributes", radialPosition="W", sourceType="python", command=Callback(attr.lockAttr))
    menuItem(label="Show JointOrient", radialPosition="SW", sourceType="python", command=Callback(attr.showJointOrient))
    menuItem(label="Show Locked", radialPosition="NW", sourceType="python", command=Callback(attr.showLockAttr))
    menuItem(label="Lock Pivot", radialPosition="N", sourceType="python", command=Callback(attr.lockPivot))
    menuItem(label="Show Local Axes", radialPosition="S", sourceType="python", command=Callback(attr.showLocalAxes))
    menuItem(label="separator", divider=True, dividerLabel="separator")
    menuItem(label="Zero Pivot", sourceType="python", command=Callback(zeroPivot))
    cmds.setParent("..", menu=True)

    # --- Curve Menu ---
    menuItem(label="Curve", subMenu=True, radialPosition="W")
    menuItem(label="Mirror Curve Shape", radialPosition="W", sourceType="python", command=Callback(mirror_cvShape_cmd))
    menuItem(label="Replace Curve Shape", radialPosition="E", sourceType="python", command=Callback(replace_cvShape_cmd))
    menuItem(label="Select CVs", radialPosition="S", sourceType="python", command=Callback(select_cvControlVertex_cmd))
    menuItem(label="Export Curve Shape", radialPosition="NE", sourceType="python", command=Callback(export_cvData))
    menuItem(label="Import Curve Shapes", radialPosition="NW", sourceType="python", command=Callback(import_cvData))
    menuItem(label="Rainbow", radialPosition="N", sourceType="python", command=Callback(rainbow_win))
    cmds.setParent("..", menu=True)

    # --- Select Menu ---
    menuItem(label="Select", subMenu=True, radialPosition="SE")
    menuItem(label="Mirror Selected", radialPosition="SE", sourceType="python", command=Callback(mirror_selected))
    menuItem(label="Mirror Selected Addon", radialPosition="E", sourceType="python", command=Callback(mirror_selected, True))
    menuItem(label="Select Hierarchy", radialPosition="S", sourceType="python", command=Callback(selectHierarchy_cmd))
    cmds.setParent("..", menu=True)

    # --- Skin Menu ---
    menuItem(label="Skin", subMenu=True, radialPosition="N")
    menuItem(label="Bind Skin", radialPosition="N", image="smoothSkin.png", command="SmoothBindSkin")
    menuItem(label="menuEditorMenuItem1", optionBox=True, command="SmoothBindSkinOptions")
    menuItem(label="Unbind Skin", radialPosition="S", image="detachSkin.png", command="DetachSkin")
    menuItem(label="Go to Bind Pose", radialPosition="W", image="goToBindPose.png", command="GoToBindPose")
    menuItem(label="Copy Skin One To N", radialPosition="E", sourceType="python", command=Callback(copyWeightsOneToN_cmd))
    menuItem(label="Copy Skin Weights", radialPosition="NE", image="copySkinWeight.png", sourceType="python", command="CopySkinWeights")
    menuItem(label="Copy Skin Weights Options", optionBox=True, command="CopySkinWeightsOptions")
    menuItem(label="Get Skin Influence", radialPosition="SE", sourceType="python", command=Callback(get_skinJoint_cmd))

    menuItem(label="Add Influence", image="addWrapInfluence.png", command="AddInfluence")
    menuItem(label="Add Influence Options", optionBox=True, command="AddInfluenceOptions")
    menuItem(label="Remove Influence", image="removeWrapInfluence.png", command="RemoveInfluence")
    menuItem(label="Remove Unused Influences", command="RemoveUnusedInfluences")
    menuItem(label="separator", divider=True, dividerLabel="separator")
    menuItem(label="Update Bind Pose", sourceType="python", command=Callback(updateBindSkin_cmd))
    cmds.setParent("..", menu=True)

    # --- Rename Menu ---
    menuItem(label="Rename", radialPosition="NW", sourceType="python", command=Callback(renameShowUI))

    # --- Set Menu ---
    menuItem(label="Set", radialPosition="SW", command="CreateSet")

    # --- Constraint Menu ---
    menuItem(label="Constraint", subMenu=True, radialPosition="NE")

    # Matrix Submenu
    menuItem(label="Matrix Constraint", subMenu=True, radialPosition="NE")
    menuItem(label="Matrix Constraint", radialPosition="NE", sourceType="python", command=Callback(matrixConstraint, mo=False))
    menuItem(label="Matrix Constraint(Keep Offset)", radialPosition="E", sourceType="python", command=Callback(matrixConstraint, mo=True))
    cmds.setParent("..", menu=True)

    menuItem(label="Parent Constraint", radialPosition="N", image="parentConstraint.png", command="ParentConstraint")
    menuItem(label="menuEditorMenuItem3", optionBox=True, command="ParentConstraintOptions")
    menuItem(label="Scale Constraint", radialPosition="SE", image="scaleConstraint.png", command="ScaleConstraint")
    menuItem(label="menuEditorMenuItem6", optionBox=True, command="ScaleConstraintOptions")
    menuItem(label="Orient Constraint", radialPosition="E", image="orientConstraint.png", command="OrientConstraint")
    menuItem(label="menuEditorMenuItem9", optionBox=True, command="OrientConstraintOptions")
    menuItem(label="UV Pin Constraint", radialPosition="W", sourceType="python", command=Callback(uvPin))
    cmds.setParent("..", menu=True)

    # --- Global Tools ---
    menuItem(label="MIRROR_CONFIG", sourceType="python", command=Callback(MIRROR_CONFIG.switch_mode))

    menuItem(label="separator", divider=True, dividerLabel="separator")

    menuItem(label="Delete Bind Pose", sourceType="python", command=Callback(deleteBindPose))
    menuItem(label="Delete Namespace", sourceType="python", command=Callback(removeNamespace))
    menuItem(label="Delete Unknown Plugin", sourceType="python", command=Callback(removeUnknownPlugin))

    menuItem(label="separator", divider=True, dividerLabel="separator")

    menuItem(label="Display Affected", checkBox=cmds.displayPref(q=1, displayAffected=1), sourceType="python", command=Callback(toggle_display_affected))

    cmds.setParent("..", menu=True)
