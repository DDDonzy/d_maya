import _hotkey.d_hotFunctions as hotFn
from maya import cmds


def menuItem(*args, **kwargs):
    sourceType = kwargs.get("sourceType") or kwargs.get("stp") or "mel"
    boldFont = kwargs.get("boldFont") or kwargs.get("blf") or True
    kwargs.update({"sourceType": sourceType, "boldFont": boldFont})
    cmds.menuItem(*args, **kwargs)


def addUI(*args, **kwargs):
    cmds.popupMenu(*args, **kwargs)
    # Transform Menu
    menuItem(label="Transform", subMenu=True, radialPosition="E")
    menuItem(label="Align Transform", radialPosition="E", sourceType="python", command=hotFn.ALIGN_TRANSFORM_CMD)
    menuItem(label="Lock Attributes", radialPosition="W", sourceType="python", command=hotFn.LOCK_ATTR_CMD)
    menuItem(label="Show JointOrient", radialPosition="SW", sourceType="python", command=hotFn.SHOW_JOINT_ORIENT_CMD)
    menuItem(label="Show Locked", radialPosition="NW", sourceType="python", command=hotFn.SHOW_LOCKED_CMD)
    menuItem(label="Lock Pivot", radialPosition="N", sourceType="python", command=hotFn.LOCK_PIVOT_CMD)
    menuItem(label="Show Local Axes", radialPosition="S", sourceType="python", command=hotFn.SHOW_LOCAL_AXES_CMD)
    menuItem(label="separator", divider=True, dividerLabel="separator")
    menuItem(label="Zero Pivot", sourceType="python", command=hotFn.ZERO_PIVOT_CMD)

    cmds.setParent("..", menu=True)
    # Curve Menu
    menuItem(label="Curve", subMenu=True, radialPosition="W")
    menuItem(label="Mirror Curve Shape", radialPosition="W", sourceType="python", command=hotFn.MIRROR_CURVE_SHAPE_CMD)
    menuItem(label="Replace Curve Shape", radialPosition="E", sourceType="python", command=hotFn.REPLACE_CURVE_SHAPE_CMD)
    menuItem(label="Select CVs", radialPosition="S", sourceType="python", command=hotFn.SELECT_CVS_CMD)
    menuItem(label="Export Curve Shape", radialPosition="NE", sourceType="python", command=hotFn.EXPORT_CURVE_SHAPE_CMD)
    menuItem(label="Import Curve Shapes", radialPosition="NW", sourceType="python", command=hotFn.IMPORT_CURVE_SHAPES_CMD)
    menuItem(label="Rainbow", radialPosition="N", sourceType="python", command=hotFn.RAINBOW_CMD)
    cmds.setParent("..", menu=True)
    # Select Menu
    menuItem(label="Select", subMenu=True, radialPosition="SE")
    menuItem(label="Mirror Selected", radialPosition="SE", sourceType="python", command=hotFn.SELECT_MIRROR_CMD)
    menuItem(label="Mirror Selected Addon", radialPosition="E", sourceType="python", command=hotFn.SELECT_MIRROR_ADDON_CMD)
    menuItem(label="Select Hierarchy", radialPosition="S", sourceType="python", command=hotFn.SELECT_HIERARCHY_CMD)
    cmds.setParent("..", menu=True)
    # Skin Menu
    menuItem(label="Skin", subMenu=True, radialPosition="N")
    menuItem(label="Bind Skin", radialPosition="N", image="smoothSkin.png", command="SmoothBindSkin")
    menuItem(label="menuEditorMenuItem1", optionBox=True, command="SmoothBindSkinOptions")
    menuItem(label="Unbind Skin", radialPosition="S", image="detachSkin.png", command="DetachSkin")
    menuItem(label="Go to Bind Pose", radialPosition="W", image="goToBindPose.png", command="GoToBindPose")
    menuItem(label="Copy Skin One To N", radialPosition="E", sourceType="python", command=hotFn.COPY_SKIN_ONE_TO_N_CMD)
    menuItem(label="Copy Skin Weights", radialPosition="NE", image="copySkinWeight.png", sourceType="python", command="CopySkinWeights")
    menuItem(label="Copy Skin Weights Options", optionBox=True, command="CopySkinWeightsOptions")
    menuItem(label="Get Skin Influence", radialPosition="SE", sourceType="python", command=hotFn.GET_SKIN_INFLUENCE_CMD)

    menuItem(label="Add Influence", image="addWrapInfluence.png", command="AddInfluence")
    menuItem(label="Add Influence Options", optionBox=True, command="AddInfluenceOptions")
    menuItem(label="Remove Influence", image="removeWrapInfluence.png", command="RemoveInfluence")
    menuItem(label="Remove Unused Influences", command="RemoveUnusedInfluences")
    menuItem(label="separator", divider=True, dividerLabel="separator")
    menuItem(label="Update Bind Pose", sourceType="python", command=hotFn.UPDATE_BIND_SKIN_CMD)

    cmds.setParent("..", menu=True)
    # Rename Menu
    menuItem(label="Rename", radialPosition="NW", sourceType="python", command=hotFn.RENAME_CMD)
    # Set Menu
    menuItem(label="Set", radialPosition="SW", command="CreateSet")
    # Constraint Menu
    menuItem(label="Constraint", subMenu=True, radialPosition="NE")
    menuItem(label="Matrix Constraint", subMenu=True, radialPosition="NE")
    menuItem(label="Matrix Constraint", radialPosition="NE", sourceType="python", command=hotFn.MATRIX_CONSTRAINT_CMD)
    menuItem(label="Matrix Constraint(Keep Offset)", radialPosition="E", sourceType="python", command=hotFn.MATRIX_CONSTRAINT_OFFSET_CMD)
    cmds.setParent("..", menu=True)
    menuItem(label="Parent Constraint", radialPosition="N", image="parentConstraint.png", command="ParentConstraint")
    menuItem(label="menuEditorMenuItem3", optionBox=True, command="ParentConstraintOptions")
    menuItem(label="Scale Constraint", radialPosition="SE", image="scaleConstraint.png", command="ScaleConstraint")
    menuItem(label="menuEditorMenuItem6", optionBox=True, command="ScaleConstraintOptions")
    menuItem(label="Orient Constraint", radialPosition="E", image="orientConstraint.png", command="OrientConstraint")
    menuItem(label="menuEditorMenuItem9", optionBox=True, command="OrientConstraintOptions")
    menuItem(label="UV Pin Constraint", radialPosition="W", sourceType="python", command=hotFn.UV_PIN_CONSTRAINT_CMD)
    cmds.setParent("..", menu=True)
    # Mirror Config
    menuItem(label="MIRROR_CONFIG", sourceType="python", command=hotFn.MIRROR_CONFIG_CMD)
    # Separator
    menuItem(label="separator", divider=True, dividerLabel="separator")
    # Delete Bind Pose
    menuItem(label="Delete Bind Pose", sourceType="python", command=hotFn.DELETE_BIND_POSE_CMD)
    # Delete Namespace
    menuItem(label="Delete Namespace", sourceType="python", command=hotFn.DELETE_NAMESPACE_CMD)
    # Delete Unknown Plugin
    menuItem(label="Delete Unknown Plugin", sourceType="python", command=hotFn.DELETE_UNKNOWN_PLUGIN_CMD)
    # Separator
    menuItem(label="separator", divider=True, dividerLabel="separator")
    # Display Affected
    menuItem(label="Display Affected", checkBox=cmds.displayPref(q=1, displayAffected=1), sourceType="python", command=hotFn.DISPLAY_AFFECTED_CMD)
    cmds.setParent("..", menu=True)
