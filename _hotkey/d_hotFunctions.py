
from maya import cmds

from UTILS.control.cvShape import (mirror_cvShape_cmd,
                                   replace_cvShape_cmd,
                                   select_cvControlVertex_cmd,
                                   import_cvData,
                                   export_cvData)
from UTILS.compounds import matrixConstraint, uvPin
import UTILS.other.attr as attr
from UTILS.other.zeroPivot import zeroPivot
from UTILS.transform import reset_transformObjectValue_cmd, alignTransform_cmd
from UTILS.mirrorEnv import mirror_selected, MIRROR_CONFIG
from Rainbow.rainbow_UI import rainbow_win
from UTILS.skin.getSkinJoint import get_skinJoint_cmd
from UTILS.skin.copyWeightsOneToN import copyWeightsOneToN_cmd
from UTILS.skin.updateBindSkin import updateBindSkin_cmd
from UTILS.rename import showUI as renameShowUI
from UTILS.scene.deleteBindPose import deleteBindPose
from UTILS.scene.removeNamespace import removeNamespace
from UTILS.scene.removeUnknownPlugin import removeUnknownPlugin
from UTILS.dag.selectHierarchy import selectHierarchy_cmd

#
RENAME_CMD = lambda *args, **kwargs: renameShowUI()
MIRROR_CONFIG_CMD = lambda *args, **kwargs: MIRROR_CONFIG.switch_mode()
DELETE_BIND_POSE_CMD = lambda *args, **kwargs: deleteBindPose()
DELETE_NAMESPACE_CMD = lambda *args, **kwargs: removeNamespace()
DELETE_UNKNOWN_PLUGIN_CMD = lambda *args, **kwargs: removeUnknownPlugin()
DISPLAY_AFFECTED_CMD = lambda *args, **kwargs: cmds.displayPref(displayAffected=not cmds.displayPref(q=1, displayAffected=1))

# transform
RESET_CMD = lambda *args, **kwargs: reset_transformObjectValue_cmd(transform=True, userDefined=False)
RESET_UD_CMD = lambda *args, **kwargs: reset_transformObjectValue_cmd(transform=True, userDefined=True)
ALIGN_TRANSFORM_CMD = lambda *args, **kwargs: alignTransform_cmd()
LOCK_ATTR_CMD = lambda *args, **kwargs: attr.lockAttr()
LOCK_PIVOT_CMD = lambda *args, **kwargs: attr.lockPivot()
SHOW_JOINT_ORIENT_CMD = lambda *args, **kwargs: attr.showJointOrient()
SHOW_LOCAL_AXES_CMD = lambda *args, **kwargs: attr.showLocalAxes()
SHOW_LOCKED_CMD = lambda *args, **kwargs: attr.showLockAttr()
ZERO_PIVOT_CMD = lambda *args, **kwargs: zeroPivot()

# curve
MIRROR_CURVE_SHAPE_CMD = lambda *args, **kwargs: mirror_cvShape_cmd()
REPLACE_CURVE_SHAPE_CMD = lambda *args, **kwargs: replace_cvShape_cmd()
SELECT_CVS_CMD = lambda *args, **kwargs: select_cvControlVertex_cmd()
EXPORT_CURVE_SHAPE_CMD = lambda *args, **kwargs: export_cvData()
IMPORT_CURVE_SHAPES_CMD = lambda *args, **kwargs: import_cvData()
RAINBOW_CMD = lambda *args, **kwargs: rainbow_win()

# select
SELECT_MIRROR_CMD = lambda *args, **kwargs: mirror_selected()
SELECT_MIRROR_ADDON_CMD = lambda *args, **kwargs: mirror_selected(True)
SELECT_HIERARCHY_CMD = lambda *args, **kwargs: selectHierarchy_cmd()

# skin
GET_SKIN_INFLUENCE_CMD = lambda *args, **kwargs: get_skinJoint_cmd()
COPY_SKIN_ONE_TO_N_CMD = lambda *args, **kwargs: copyWeightsOneToN_cmd()
UPDATE_BIND_SKIN_CMD = lambda *args, **kwargs: updateBindSkin_cmd()

# constraint
MATRIX_CONSTRAINT_CMD = lambda *args, **kwargs: matrixConstraint()
UV_PIN_CONSTRAINT_CMD = lambda *args, **kwargs: uvPin()


def toggleJointOption():
    panel = cmds.getPanel(withFocus=True)
    if cmds.getPanel(typeOf=panel) == 'modelPanel':
        is_visible = cmds.modelEditor(panel, query=True, joints=True)
        cmds.modelEditor(panel, edit=True, joints=(not is_visible))


TOGGLE_JOINT_OPTION_CMD = lambda *args, **kwargs: toggleJointOption()
