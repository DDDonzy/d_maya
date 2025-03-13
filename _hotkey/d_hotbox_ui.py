from maya import cmds

from UTILS.control.cvShape import (mirror_cvShape_cmd,
                                   replace_cvShape_cmd,
                                   select_cvControlVertex_cmd,
                                   import_cvData,
                                   export_cvData)
from UTILS.compounds import (matrixConstraint,
                             uvPin)


import UTILS.other.attr as attr
from UTILS.transform import reset_transformObjectValue_cmd
from UTILS.mirrorEnv import mirror_selected, MIRROR_CONFIG
from Rainbow.rainbow_UI import rainbow_win
from UTILS.skin.getSkinJoint import get_skinJoint_cmd
from UTILS.skin.copyWeightsOneToN import copyWeightsOneToN_cmd
from UTILS.rename import showUI as renameShowUI
from UTILS.scene.deleteBindPose import deleteBindPose
from UTILS.scene.removeNamespace import removeNamespace
from UTILS.scene.removeUnknownPlugin import removeUnknownPlugin


def menuItem(*args, **kwargs):
    sourceType = kwargs.get("sourceType") or kwargs.get("stp") or "mel"
    boldFont = kwargs.get("boldFont") or kwargs.get("blf") or True
    kwargs.update({"sourceType": sourceType,
                   "boldFont": boldFont})
    cmds.menuItem(*args, **kwargs)


RESET_CMD = lambda *args, **kwargs: reset_transformObjectValue_cmd(transform=True, userDefined=False)
RESET_UD_CMD = lambda *args, **kwargs: reset_transformObjectValue_cmd(transform=True, userDefined=True)
LOCK_ATTR_CMD = lambda *args, **kwargs: attr.lockAttr()
SHOW_JOINT_ORIENT_CMD = lambda *args, **kwargs: attr.showJointOrient()
SHOW_LOCAL_AXES_CMD = lambda *args, **kwargs: attr.showLocalAxes()
SHOW_LOCKED_CMD = lambda *args, **kwargs: attr.showLockAttr()
MIRROR_CURVE_SHAPE_CMD = lambda *args, **kwargs: mirror_cvShape_cmd()
REPLACE_CURVE_SHAPE_CMD = lambda *args, **kwargs: replace_cvShape_cmd()
SELECT_CVS_CMD = lambda *args, **kwargs: select_cvControlVertex_cmd()
EXPORT_CURVE_SHAPE_CMD = lambda *args, **kwargs: export_cvData()
IMPORT_CURVE_SHAPES_CMD = lambda *args, **kwargs: import_cvData()
RAINBOW_CMD = lambda *args, **kwargs: rainbow_win()
MIRROR_SELECTED_CMD = lambda *args, **kwargs: mirror_selected()
MIRROR_SELECTED_ADDON_CMD = lambda *args, **kwargs: mirror_selected(True)
GET_SKIN_INFLUENCE_CMD = lambda *args, **kwargs: get_skinJoint_cmd()
COPY_SKIN_ONE_TO_N_CMD = lambda *args, **kwargs: copyWeightsOneToN_cmd()
RENAME_CMD = lambda *args, **kwargs: renameShowUI()
MATRIX_CONSTRAINT_CMD = lambda *args, **kwargs: matrixConstraint()
UV_PIN_CONSTRAINT_CMD = lambda *args, **kwargs: uvPin()
MIRROR_CONFIG_CMD = lambda *args, **kwargs: MIRROR_CONFIG.switch_mode()
DELETE_BIND_POSE_CMD = lambda *args, **kwargs: deleteBindPose()
DELETE_NAMESPACE_CMD = lambda *args, **kwargs: removeNamespace()
DELETE_UNKNOWN_PLUGIN_CMD = lambda *args, **kwargs: removeUnknownPlugin()
DISPLAY_AFFECTED_CMD = lambda *args, **kwargs: cmds.displayPref(displayAffected=not cmds.displayPref(q=1, displayAffected=1))


def addUI(*args, **kwargs):
    cmds.popupMenu(*args, **kwargs)
    # Transform Menu
    menuItem(label="Transform", subMenu=True, radialPosition="E")
    menuItem(label="Reset Transform",
             radialPosition="SE",
             sourceType="python", command=RESET_CMD)
    menuItem(label="Reset User Defined Attr",
             radialPosition="E",
             sourceType="python", command=RESET_UD_CMD)
    menuItem(label="Lock Attributes",
             radialPosition="W",
             sourceType="python", command=LOCK_ATTR_CMD)
    menuItem(label="Show JointOrient",
             radialPosition="SW",
             sourceType="python", command=SHOW_JOINT_ORIENT_CMD)
    menuItem(label="Show Local Axes",
             radialPosition="S",
             sourceType="python", command=SHOW_LOCAL_AXES_CMD)
    menuItem(label="Show Locked",
             radialPosition="NW",
             sourceType="python", command=SHOW_LOCKED_CMD)
    cmds.setParent("..", menu=True)
    # Curve Menu
    menuItem(label="Curve",
             subMenu=True,
             radialPosition="W")
    menuItem(label="Mirror Curve Shape",
             radialPosition="W",
             sourceType="python", command=MIRROR_CURVE_SHAPE_CMD)
    menuItem(label="Replace Curve Shape",
             radialPosition="E",
             sourceType="python", command=REPLACE_CURVE_SHAPE_CMD)
    menuItem(label="Select CVs",
             radialPosition="S",
             sourceType="python", command=SELECT_CVS_CMD)
    menuItem(label="Export Curve Shape",
             radialPosition="NE",
             sourceType="python", command=EXPORT_CURVE_SHAPE_CMD)
    menuItem(label="Import Curve Shapes",
             radialPosition="NW",
             sourceType="python", command=IMPORT_CURVE_SHAPES_CMD)
    menuItem(label="Rainbow",
             radialPosition="N",
             sourceType="python", command=RAINBOW_CMD)
    cmds.setParent("..", menu=True)
    # Select Menu
    menuItem(label="Select",
             subMenu=True,
             radialPosition="SE")
    menuItem(label="Mirror Selected",
             radialPosition="S",
             sourceType="python", command=MIRROR_SELECTED_CMD)
    menuItem(label="Mirror Selected Addon",
             radialPosition="SE",
             sourceType="python", command=MIRROR_SELECTED_ADDON_CMD)
    menuItem(label="Duplicate And Mirror Selected",
             radialPosition="N")
    cmds.setParent("..", menu=True)
    # Skin Menu
    menuItem(label="Skin",
             subMenu=True,
             radialPosition="N")
    menuItem(label="Get Skin Influence",
             radialPosition="SE",
             sourceType="python", command=GET_SKIN_INFLUENCE_CMD)
    menuItem(label="Add Influence",
             radialPosition="NW",
             image="addWrapInfluence.png",
             command="AddInfluence")
    menuItem(label="menuEditorMenuItem3",
             optionBox=True,
             command="AddInfluenceOptions")
    menuItem(label="Remove Influence",
             radialPosition="W",
             image="removeWrapInfluence.png",
             command="RemoveInfluence")
    menuItem(label="Bind Skin",
             radialPosition="N",
             image="smoothSkin.png",
             command="SmoothBindSkin")
    menuItem(label="menuEditorMenuItem1",
             optionBox=True,
             command="SmoothBindSkinOptions")
    menuItem(label="Copy Skin One To N",
             radialPosition="E",
             sourceType="python", command=COPY_SKIN_ONE_TO_N_CMD)
    menuItem(label="Unbind Skin",
             radialPosition="S",
             image="detachSkin.png",
             command="DetachSkin")
    menuItem(label="Go to Bind Pose",
             radialPosition="NE",
             image="goToBindPose.png",
             command="GoToBindPose")
    menuItem(label="Remove Unused Influences",
             radialPosition="SW",
             command="RemoveUnusedInfluences")
    cmds.setParent("..", menu=True)
    # Rename Menu
    menuItem(label="Rename",
             radialPosition="NW",
             sourceType="python", command=RENAME_CMD)
    # Set Menu
    menuItem(label="Set",
             radialPosition="SW",
             command="CreateSet")
    # Constraint Menu
    menuItem(label="Constraint",
             subMenu=True,
             radialPosition="NE")
    menuItem(label="Matrix Constraint",
             radialPosition="NE",
             sourceType="python", command=MATRIX_CONSTRAINT_CMD)
    menuItem(label="Parent Constraint",
             radialPosition="N",
             image="parentConstraint.png",
             command="ParentConstraint")
    menuItem(label="menuEditorMenuItem3",
             optionBox=True,
             command="ParentConstraintOptions")
    menuItem(label="Scale Constraint",
             radialPosition="SE",
             image="scaleConstraint.png",
             command="ScaleConstraint")
    menuItem(label="menuEditorMenuItem6",
             optionBox=True,
             command="ScaleConstraintOptions")
    menuItem(label="Orient Constraint",
             radialPosition="E",
             image="orientConstraint.png",
             command="OrientConstraint")
    menuItem(label="menuEditorMenuItem9",
             optionBox=True,
             command="OrientConstraintOptions")
    menuItem(label="UV Pin Constraint",
             radialPosition="W",
             sourceType="python", command=UV_PIN_CONSTRAINT_CMD)
    cmds.setParent("..", menu=True)
    # Mirror Config
    menuItem(label="MIRROR_CONFIG",
             sourceType="python", command=MIRROR_CONFIG_CMD)
    # Separator
    menuItem(label="separator",
             divider=True,
             dividerLabel="separator")
    # Delete Bind Pose
    menuItem(label="Delete Bind Pose",
             sourceType="python", command=DELETE_BIND_POSE_CMD)
    # Delete Namespace
    menuItem(label="Delete Namespace",
             sourceType="python", command=DELETE_NAMESPACE_CMD)
    # Delete Unknown Plugin
    menuItem(label="Delete Unknown Plugin",
             sourceType="python", command=DELETE_UNKNOWN_PLUGIN_CMD)
    # Separator
    menuItem(label="separator",
             divider=True,
             dividerLabel="separator")
    # Display Affected
    menuItem(label="Display Affected",
             checkBox=cmds.displayPref(q=1, displayAffected=1),
             sourceType="python", command=DISPLAY_AFFECTED_CMD)
    cmds.setParent("..", menu=True)
