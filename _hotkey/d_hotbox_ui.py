from maya import cmds


def menuItem(*args, **kwargs):
    sourceType = kwargs.get("sourceType") or kwargs.get("stp") or "mel"
    boldFont = kwargs.get("boldFont") or kwargs.get("blf") or True
    kwargs.update({"sourceType": sourceType,
                   "boldFont": boldFont})
    cmds.menuItem(*args, **kwargs)


def addUI(*args, **kwargs):
    cmds.popupMenu(*args, **kwargs)
# Transform Menu
    menuItem(label="Transform",
             subMenu=True,
             radialPosition="E")
    menuItem(label="Reset Transform",
             radialPosition="SE",
             sourceType="python",
             command="from UTILS.transform import reset_transformObjectValue_cmd\nreset_transformObjectValue_cmd(True,False)")
    menuItem(label="Reset User Defined Attr",
             radialPosition="E",
             sourceType="python",
             command="from UTILS.transform import reset_transformObjectValue_cmd\nreset_transformObjectValue_cmd(True,True)")
    menuItem(label="Lock Attributes",
             radialPosition="W",
             sourceType="python",
             command="import UTILS.other.attr as attr\nattr.lockAttr()")
    menuItem(label="Show JointOrient",
             radialPosition="SW",
             sourceType="python",
             command="import UTILS.other.attr as attr\nattr.showJointOrient()")
    # menuItem(label="Lock Translate",
    #          radialPosition="NW",
    #          sourceType="python",
    #          command="import UTILS.other.attr as attr\nattr.lockAttr(attr=attr.TRANSLATE_ATTR)")
    menuItem(label="Show Local Axes",
             radialPosition="S",
             sourceType="python",
             command="import UTILS.other.attr as attr\nattr.showLocalAxes()")
    # menuItem(label="Lock Scale",
    #          radialPosition="NE",
    #          sourceType="python",
    #          command="import UTILS.other.attr as attr\nattr.lockAttr(attr=attr.SCALE_ATTR)")
    menuItem(label="Show Locked",
             radialPosition="NW",
             sourceType="python",
             command="import UTILS.other.attr as attr\nattr.showLockAttr()")
    cmds.setParent("..", menu=True)
    # Curve Menu
    menuItem(label="Curve",
             subMenu=True,
             radialPosition="W")
    menuItem(label="Mirror Curve Shape",
             radialPosition="W",
             sourceType="python",
             command="from UTILS.control.cvShape import mirror_cvShape_cmd\nmirror_cvShape_cmd()")
    menuItem(label="Replace Curve Shape",
             radialPosition="E",
             sourceType="python",
             command="from UTILS.control.cvShape import replace_cvShape_cmd\nreplace_cvShape_cmd()")
    menuItem(label="Select CVs",
             radialPosition="S",
             sourceType="python",
             command="from UTILS.control.cvShape import select_cvControlVertex_cmd\nselect_cvControlVertex_cmd()")
    menuItem(label="Export Curve Shape",
             radialPosition="NE",
             sourceType="python",
             command="from UTILS.control.cvShape import import_cvData,export_cvData\nexport_cvData()")
    menuItem(label="Import Curve Shapes",
             radialPosition="NW",
             sourceType="python",
             command="from UTILS.control.cvShape import import_cvData,export_cvData\nimport_cvData()")
    menuItem(label="Rainbow",
             radialPosition="N",
             sourceType="python",
             command="from Rainbow.rainbow_UI import *\nrainbow_win()")
    cmds.setParent("..", menu=True)
    # Select Menu
    menuItem(label="Select",
             subMenu=True,
             radialPosition="SE")
    menuItem(label="Mirror Selected",
             radialPosition="S",
             sourceType="python",
             command="from UTILS.mirrorEnv import mirror_selected\nmirror_selected()")
    menuItem(label="Mirror Selected Addon",
             radialPosition="SE",
             sourceType="python",
             command="from UTILS.mirrorEnv import mirror_selected\nmirror_selected(True)")
    menuItem(label="Duplicate And Mirror Selected",
             radialPosition="N")
    cmds.setParent("..", menu=True)
    # Skin Menu
    menuItem(label="Skin",
             subMenu=True,
             radialPosition="N")
    menuItem(label="Get Skin Influence",
             radialPosition="SE",
             sourceType="python",
             command="from UTILS.skin.getSkinJoint import get_skinJoint_cmd\nget_skinJoint_cmd()")
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
             sourceType="python",
             command="from UTILS.skin.copyWeightsOneToN import copyWeightsOneToN_cmd\ncopyWeightsOneToN_cmd()")
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
             sourceType="python",
             command="from UTILS.rename import showUI as renameShowUI\nrenameShowUI()")
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
             sourceType="python",
             command="from UTILS.transform import matrixConstraint \nmatrixConstraint()")
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
             sourceType="python",
             command="from UTILS.transform.uvPin import create_uvPin \ncreate_uvPin()")
    cmds.setParent("..", menu=True)
    # Mirror Config
    menuItem(label="MIRROR_CONFIG",
             sourceType="python",
             command="from UTILS.mirrorEnv import MIRROR_CONFIG\nMIRROR_CONFIG.switch_mode()")
    # Separator
    menuItem(label="separator",
             divider=True,
             dividerLabel="separator")
    # Delete Bind Pose
    menuItem(label="Delete Bind Pose",
             sourceType="python",
             command="from UTILS.scene.deleteBindPose import deleteBindPose \ndeleteBindPose()")
    # Delete Namespace
    menuItem(label="Delete Namespace",
             sourceType="python",
             command="from UTILS.scene.removeNamespace import removeNamespace\nremoveNamespace()")
    # Delete Unknown Plugin
    menuItem(label="Delete Unknown Plugin",
             sourceType="python",
             command="from UTILS.scene.removeUnknownPlugin import removeUnknownPlugin\nremoveUnknownPlugin()")
    # Separator
    menuItem(label="separator",
             divider=True,
             dividerLabel="separator")
    # Display Affected
    menuItem(label="Display Affected",
             checkBox=cmds.displayPref(q=1, displayAffected=1),
             sourceType="python",
             command="import maya.cmds \nmaya.cmds.displayPref(displayAffected = not maya.cmds.displayPref(q=1,displayAffected=1))")
    cmds.setParent("..", menu=True)
