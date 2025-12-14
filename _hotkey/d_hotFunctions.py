
from functools import partial

from maya import cmds

import m_utils.other.attr as attr
from m_utils.control.cvShape import mirror_cvShape_cmd, replace_cvShape_cmd, select_cvControlVertex_cmd, import_cvData, export_cvData
from m_utils.compounds import matrixConstraint, uvPin
from m_utils.other.zeroPivot import zeroPivot
from m_utils.transform import reset_transform_cmd, align_transform_cmd
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


#
RENAME_CMD = partial(renameShowUI)
MIRROR_CONFIG_CMD = partial(MIRROR_CONFIG.switch_mode)
DELETE_BIND_POSE_CMD = partial(deleteBindPose)
DELETE_NAMESPACE_CMD = partial(removeNamespace)
DELETE_UNKNOWN_PLUGIN_CMD = partial(removeUnknownPlugin)


# Note: The original lambda for DISPLAY_AFFECTED_CMD was:
# lambda *args, **kwargs: cmds.displayPref(displayAffected=not cmds.displayPref(q=1, displayAffected=1))
# Since 'partial' cannot handle the logic, we must keep it as a full function or a lambda.
# I will keep the existing pattern as it is a common Maya utility function.
# Alternatively, it could be wrapped in a function, but I'll stick to the original logic style for this specific case.
def toggle_display_affected():
    """
    Toggles the 'Display Affected' preference in Maya.

    This preference shows the downstream objects that are affected by
    the selected item (e.g., if a constraint source is selected, its targets are highlighted).
    """
    # Query the current state of 'displayAffected'
    is_visible = cmds.displayPref(query=True, displayAffected=True)

    # Set 'displayAffected' to the opposite of the current state
    cmds.displayPref(displayAffected=not is_visible)


DISPLAY_AFFECTED_CMD = partial(toggle_display_affected)


# transform
RESET_CMD = partial(reset_transform_cmd, transform=True, userDefined=False)
RESET_UD_CMD = partial(reset_transform_cmd, transform=True, userDefined=True)
ALIGN_TRANSFORM_CMD = partial(align_transform_cmd)
LOCK_ATTR_CMD = partial(attr.lockAttr)
LOCK_PIVOT_CMD = partial(attr.lockPivot)
SHOW_JOINT_ORIENT_CMD = partial(attr.showJointOrient)
SHOW_LOCAL_AXES_CMD = partial(attr.showLocalAxes)
SHOW_LOCKED_CMD = partial(attr.showLockAttr)
ZERO_PIVOT_CMD = partial(zeroPivot)

# curve
MIRROR_CURVE_SHAPE_CMD = partial(mirror_cvShape_cmd)
REPLACE_CURVE_SHAPE_CMD = partial(replace_cvShape_cmd)
SELECT_CVS_CMD = partial(select_cvControlVertex_cmd)
EXPORT_CURVE_SHAPE_CMD = partial(export_cvData)
IMPORT_CURVE_SHAPES_CMD = partial(import_cvData)
RAINBOW_CMD = partial(rainbow_win)

# select
SELECT_MIRROR_CMD = partial(mirror_selected)
SELECT_MIRROR_ADDON_CMD = partial(mirror_selected, True)  # Note: Passing True as the first positional argument
SELECT_HIERARCHY_CMD = partial(selectHierarchy_cmd)

# skin
GET_SKIN_INFLUENCE_CMD = partial(get_skinJoint_cmd)
COPY_SKIN_ONE_TO_N_CMD = partial(copyWeightsOneToN_cmd)
UPDATE_BIND_SKIN_CMD = partial(updateBindSkin_cmd)

# constraint
MATRIX_CONSTRAINT_CMD = partial(matrixConstraint, mo=False)
MATRIX_CONSTRAINT_OFFSET_CMD = partial(matrixConstraint, mo=True)
UV_PIN_CONSTRAINT_CMD = partial(uvPin)


def toggleJointOption():
    panel = cmds.getPanel(withFocus=True)
    if cmds.getPanel(typeOf=panel) == "modelPanel":
        is_visible = cmds.modelEditor(panel, query=True, joints=True)
        cmds.modelEditor(panel, edit=True, joints=(not is_visible))


TOGGLE_JOINT_OPTION_CMD = partial(toggleJointOption)
