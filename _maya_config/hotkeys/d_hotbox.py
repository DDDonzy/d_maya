from functools import partial

from maya import cmds, mel


class UI_Command:
    @staticmethod
    def toggle_joint_option():
        panel = cmds.getPanel(withFocus=True)
        if cmds.getPanel(typeOf=panel) == "modelPanel":
            is_visible = cmds.modelEditor(panel, query=True, joints=True)
            cmds.modelEditor(panel, edit=True, joints=(not is_visible))

    @staticmethod
    def toggle_display_affected(*args, **kwargs):
        is_visible = cmds.displayPref(query=True, displayAffected=True)
        cmds.displayPref(displayAffected=not is_visible)

    # --- Transform Tools ---
    @staticmethod
    def reset_transform(*args, **kwargs):
        from m_utils.transform import reset_transform_cmd

        reset_transform_cmd(transform=True, userDefined=False)

    @staticmethod
    def reset_transform_user_defined(*args, **kwargs):
        from m_utils.transform import reset_transform_cmd

        reset_transform_cmd(transform=True, userDefined=True)

    @staticmethod
    def align_transform(*args, **kwargs):
        from m_utils.transform import align_transform_cmd

        align_transform_cmd()

    @staticmethod
    def mirror_transform(*args, **kwargs):
        from m_utils.transform import mirror_transform_cmd

        mirror_transform_cmd()

    @staticmethod
    def lock_attr(*args, **kwargs):
        from m_utils.other import attr

        attr.lockAttr()

    @staticmethod
    def show_jo(*args, **kwargs):
        from m_utils.other import attr

        attr.showJointOrient()

    @staticmethod
    def show_locked(*args, **kwargs):
        from m_utils.other import attr

        attr.showLockAttr()

    @staticmethod
    def lock_pivot(*args, **kwargs):
        from m_utils.other import attr

        attr.lockPivot()

    @staticmethod
    def show_local_axes(*args, **kwargs):
        from m_utils.other import attr

        attr.showLocalAxes()

    @staticmethod
    def zero_pivot(*args, **kwargs):
        from m_utils.other.zeroPivot import zeroPivot

        zeroPivot()

    # --- Curve Tools ---
    @staticmethod
    def mirror_cv_shape(*args, **kwargs):
        from m_utils.control.cvShape import mirror_cvShape_cmd

        mirror_cvShape_cmd()

    @staticmethod
    def replace_cv_shape(*args, **kwargs):
        from m_utils.control.cvShape import replace_cvShape_cmd

        replace_cvShape_cmd()

    @staticmethod
    def select_cv(*args, **kwargs):
        from m_utils.control.cvShape import select_cvControlVertex_cmd

        select_cvControlVertex_cmd()

    @staticmethod
    def export_cv(*args, **kwargs):
        from m_utils.control.cvShape import export_cvData

        export_cvData()

    @staticmethod
    def import_cv(*args, **kwargs):
        from m_utils.control.cvShape import import_cvData

        import_cvData()

    @staticmethod
    def rainbow_ui(*args, **kwargs):
        from Rainbow.rainbow_UI import rainbow_win

        rainbow_win()

    # --- Select Tools ---
    @staticmethod
    def mirror_selected(*args, **kwargs):
        from m_utils.mirrorEnv import mirror_selected

        mirror_selected()

    @staticmethod
    def mirror_selected_addon(*args, **kwargs):
        from m_utils.mirrorEnv import mirror_selected

        mirror_selected(True)

    @staticmethod
    def select_hierarchy(*args, **kwargs):
        from m_utils.dag.selectHierarchy import selectHierarchy_cmd

        selectHierarchy_cmd()

    # --- Skin Tools ---
    @staticmethod
    def bind_skin(*args, **kwargs):
        selected = cmds.ls(sl=1)
        selected_joints = []
        selected_meshes = []
        for obj in selected:
            if cmds.objectType(obj, isAType="joint"):
                selected_joints.append(obj)
            if cmds.objectType(obj, isAType="transform"):
                selected_meshes += cmds.ls(cmds.listRelatives(obj, shapes=1), ni=1, g=1)

        if not selected_joints:
            from m_utils.deform.skin.autoProp import autoProp

            autoProp(autoSkin=True)
        else:
            from m_utils.dag.getHistory import get_history

            for x in selected_meshes:
                cmds.select(selected_joints, x, r=1)
                if get_history(x, type="skinCluster"):
                    mel.eval("AddInfluence")
                else:
                    mel.eval("SmoothBindSkin")

    @staticmethod
    def go_to_bind_pose(*args, **kwargs):
        from m_utils.deform.skin.goToBindPose import go_to_bind_pose

        go_to_bind_pose()

    @staticmethod
    def copy_weights_1_to_n(*args, **kwargs):
        from m_utils.deform.skin.copyWeightsOneToN import copyWeightsOneToN_cmd

        copyWeightsOneToN_cmd()

    @staticmethod
    def get_skin_joint(*args, **kwargs):
        from m_utils.deform.skin.getSkinJoint import get_skinJoint_cmd

        get_skinJoint_cmd()

    @staticmethod
    def select_laster_influences(*args, **kwargs):
        from m_utils.deform.skin.getSkinJoint import select_laster_influences_cmd

        select_laster_influences_cmd()

    @staticmethod
    def update_bind_skin(*args, **kwargs):
        from m_utils.deform.skin.updateBindSkin import updateBindSkin_cmd

        updateBindSkin_cmd()

    @staticmethod
    def update_orig_mesh(*args, **kwargs):
        from m_utils.deform.update_orig import update_orig_cmd

        update_orig_cmd()

    # --- Rename / Scene Tools ---
    @staticmethod
    def rename_ui(*args, **kwargs):
        from m_utils.rename import showUI

        showUI()

    @staticmethod
    def delete_bind_pose(*args, **kwargs):
        from m_utils.scene.deleteBindPose import deleteBindPose

        deleteBindPose()

    @staticmethod
    def remove_namespace(*args, **kwargs):
        from m_utils.scene.removeNamespace import removeNamespace

        removeNamespace()

    @staticmethod
    def remove_unknown_plugin(*args, **kwargs):
        from m_utils.scene.removeUnknownPlugin import removeUnknownPlugin

        removeUnknownPlugin()

    # --- Constraint Tools ---
    @staticmethod
    def matrix_constraint_mo_false(*args, **kwargs):
        from m_utils.compounds import matrixConstraint

        matrixConstraint(mo=False)

    @staticmethod
    def matrix_constraint_mo_true(*args, **kwargs):
        from m_utils.compounds import matrixConstraint

        matrixConstraint(mo=True)

    @staticmethod
    def uv_pin(*args, **kwargs):
        from m_utils.compounds import uvPin

        uvPin()

    # --- Global Config ---
    @staticmethod
    def mirror_config_switch(*args, **kwargs):
        from m_utils.mirrorEnv import MIRROR_CONFIG

        MIRROR_CONFIG.switch_mode()


class UI_Logic:
    sys_hotBox = "modelPanel4ObjectPop"
    d_hotBox_LMB = "d_hotbox_LMB"
    d_hotBox_RMB = "d_hotbox_RMB"

    PRESS_COUNT = 0
    DISPLAY_COUNT = 0

    def menuItem(self, *args, **kwargs):
        sourceType = kwargs.get("sourceType") or kwargs.get("stp") or "mel"
        boldFont = kwargs.get("boldFont") or kwargs.get("blf") or True
        kwargs.update({"sourceType": sourceType, "boldFont": boldFont})
        cmds.menuItem(*args, **kwargs)

    def addUI(self, *args, **kwargs):
        cmds.popupMenu(*args, **kwargs)

        # --- Transform Menu ---
        self.menuItem(label="Transform", subMenu=True, radialPosition="E")
        self.menuItem(label="Align Transform", radialPosition="NE", sourceType="python", command=UI_Command.align_transform)
        self.menuItem(label="Mirror Transform", radialPosition="E", sourceType="python", command=UI_Command.mirror_transform)
        self.menuItem(label="Lock Attributes", radialPosition="W", sourceType="python", command=UI_Command.lock_attr)
        self.menuItem(label="Show JointOrient", radialPosition="SW", sourceType="python", command=UI_Command.show_jo)
        self.menuItem(label="Show Locked", radialPosition="NW", sourceType="python", command=UI_Command.show_locked)
        self.menuItem(label="Lock Pivot", radialPosition="N", sourceType="python", command=UI_Command.lock_pivot)
        self.menuItem(label="Show Local Axes", radialPosition="S", sourceType="python", command=UI_Command.show_local_axes)
        self.menuItem(label="separator", divider=True, dividerLabel="separator")
        self.menuItem(label="Zero Pivot", sourceType="python", command=UI_Command.zero_pivot)
        cmds.setParent("..", menu=True)

        # --- Curve Menu ---
        self.menuItem(label="Curve", subMenu=True, radialPosition="W")
        self.menuItem(label="Mirror Curve Shape", radialPosition="W", sourceType="python", command=UI_Command.mirror_cv_shape)
        self.menuItem(label="Replace Curve Shape", radialPosition="E", sourceType="python", command=UI_Command.replace_cv_shape)
        self.menuItem(label="Select CVs", radialPosition="S", sourceType="python", command=UI_Command.select_cv)
        self.menuItem(label="Export Curve Shape", radialPosition="NE", sourceType="python", command=UI_Command.export_cv)
        self.menuItem(label="Import Curve Shapes", radialPosition="NW", sourceType="python", command=UI_Command.import_cv)
        self.menuItem(label="Rainbow", radialPosition="N", sourceType="python", command=UI_Command.rainbow_ui)
        cmds.setParent("..", menu=True)

        # --- Select Menu ---
        self.menuItem(label="Select", subMenu=True, radialPosition="SE")
        self.menuItem(label="Mirror Selected", radialPosition="SE", sourceType="python", command=UI_Command.mirror_selected)
        self.menuItem(label="Mirror Selected Addon", radialPosition="E", sourceType="python", command=UI_Command.mirror_selected_addon)
        self.menuItem(label="Select Hierarchy", radialPosition="S", sourceType="python", command=UI_Command.select_hierarchy)
        cmds.setParent("..", menu=True)

        # --- Skin Menu ---
        self.menuItem(label="Skin", subMenu=True, radialPosition="N")
        self.menuItem(label="Bind Skin", radialPosition="N", image="smoothSkin.png", sourceType="python", command=UI_Command.bind_skin)
        self.menuItem(label="menuEditorMenuItem1", optionBox=True, command="SmoothBindSkinOptions")
        self.menuItem(label="Unbind Skin", radialPosition="S", image="detachSkin.png", command="DetachSkin")
        self.menuItem(label="Go to Bind Pose", radialPosition="W", image="goToBindPose.png", sourceType="python", command=UI_Command.go_to_bind_pose)

        self.menuItem(label="Copy Skin One To N", radialPosition="E", sourceType="python", command=UI_Command.copy_weights_1_to_n)

        self.menuItem(label="Copy Skin Weights", radialPosition="NE", image="copySkinWeight.png", sourceType="python", command="CopySkinWeights")
        self.menuItem(label="Copy Skin Weights Options", optionBox=True, command="CopySkinWeightsOptions")

        self.menuItem(label="Get Skin Influence", radialPosition="SE", sourceType="python", command=UI_Command.get_skin_joint)
        self.menuItem(label="Select Last Influences", radialPosition="SW", sourceType="python", command=UI_Command.select_laster_influences)

        self.menuItem(label="Add Influence", image="addWrapInfluence.png", command="AddInfluence")
        self.menuItem(label="Add Influence Options", optionBox=True, command="AddInfluenceOptions")
        self.menuItem(label="Remove Influence", image="removeWrapInfluence.png", command="RemoveInfluence")
        self.menuItem(label="Remove Unused Influences", command="RemoveUnusedInfluences")
        self.menuItem(label="separator", divider=True, dividerLabel="separator")
        self.menuItem(label="Update Bind Pose", sourceType="python", command=UI_Command.update_bind_skin)
        self.menuItem(label="Update Original Mesh", sourceType="python", command=UI_Command.update_orig_mesh)
        cmds.setParent("..", menu=True)

        # --- Rename Menu ---
        self.menuItem(label="Rename", radialPosition="NW", sourceType="python", command=UI_Command.rename_ui)

        # --- Set Menu ---
        self.menuItem(label="Set", radialPosition="SW", command="CreateSet")

        # --- Constraint Menu ---
        self.menuItem(label="Constraint", subMenu=True, radialPosition="NE")

        # Matrix Submenu
        self.menuItem(label="Matrix Constraint", subMenu=True, radialPosition="NE")
        self.menuItem(label="Matrix Constraint", radialPosition="NE", sourceType="python", command=UI_Command.matrix_constraint_mo_false)
        self.menuItem(label="Matrix Constraint(Keep Offset)", radialPosition="E", sourceType="python", command=UI_Command.matrix_constraint_mo_true)
        cmds.setParent("..", menu=True)

        self.menuItem(label="Parent Constraint", radialPosition="N", image="parentConstraint.png", command="ParentConstraint")
        self.menuItem(label="menuEditorMenuItem3", optionBox=True, command="ParentConstraintOptions")
        self.menuItem(label="Scale Constraint", radialPosition="SE", image="scaleConstraint.png", command="ScaleConstraint")
        self.menuItem(label="menuEditorMenuItem6", optionBox=True, command="ScaleConstraintOptions")
        self.menuItem(label="Orient Constraint", radialPosition="E", image="orientConstraint.png", command="OrientConstraint")
        self.menuItem(label="menuEditorMenuItem9", optionBox=True, command="OrientConstraintOptions")

        self.menuItem(label="UV Pin Constraint", radialPosition="W", sourceType="python", command=UI_Command.uv_pin)
        cmds.setParent("..", menu=True)

        # --- Global Tools ---
        self.menuItem(label="MIRROR_CONFIG", sourceType="python", command=UI_Command.mirror_config_switch)

        self.menuItem(label="separator", divider=True, dividerLabel="separator")

        self.menuItem(label="Delete Bind Pose", sourceType="python", command=UI_Command.delete_bind_pose)
        self.menuItem(label="Delete Namespace", sourceType="python", command=UI_Command.remove_namespace)
        self.menuItem(label="Delete Unknown Plugin", sourceType="python", command=UI_Command.remove_unknown_plugin)

        self.menuItem(label="separator", divider=True, dividerLabel="separator")

        # Display Affected
        self.menuItem(label="Display Affected", checkBox=cmds.displayPref(q=1, displayAffected=1), sourceType="python", command=UI_Command.toggle_display_affected)

        cmds.setParent("..", menu=True)

    def createUI(self):
        if cmds.popupMenu(UI_Logic.d_hotBox_LMB, q=1, ex=1):
            cmds.deleteUI(UI_Logic.d_hotBox_LMB)
        if cmds.popupMenu(UI_Logic.d_hotBox_RMB, q=1, ex=1):
            cmds.deleteUI(UI_Logic.d_hotBox_RMB)
        # set sys_hotBox button = 2
        cmds.popupMenu(UI_Logic.sys_hotBox, e=1, button=2)
        # add ui as mouser button 3
        self.addUI(UI_Logic.d_hotBox_LMB, button=3, parent=mel.eval("findPanelPopupParent"), aob=0, mm=1, pmc=lambda *args, **kwargs: self.changeDisplayCount())
        # add ui as mouser button 1
        self.addUI(UI_Logic.d_hotBox_RMB, button=1, parent=mel.eval("findPanelPopupParent"), aob=0, mm=1, pmc=lambda *args, **kwargs: self.changeDisplayCount())

    def deleteUI(self):
        if cmds.popupMenu(UI_Logic.d_hotBox_LMB, q=1, ex=1):
            cmds.deleteUI(UI_Logic.d_hotBox_LMB)
        if cmds.popupMenu(UI_Logic.d_hotBox_RMB, q=1, ex=1):
            cmds.deleteUI(UI_Logic.d_hotBox_RMB)
        # set sys_hotBox button = 3
        cmds.popupMenu(UI_Logic.sys_hotBox, e=1, button=3)

    def d_hotbox_press(self):
        UI_Logic.PRESS_COUNT += 1
        self.createUI()

    def d_hotbox_release(self):
        if UI_Logic.PRESS_COUNT != UI_Logic.DISPLAY_COUNT:
            UI_Command.reset_transform()
        UI_Logic.PRESS_COUNT = 0
        UI_Logic.DISPLAY_COUNT = 0
        cmds.evalDeferred(partial(self.deleteUI))

    def changeDisplayCount(self):
        UI_Logic.DISPLAY_COUNT += 1
        cmds.evalDeferred(partial(self.deleteUI))


ui_logic = UI_Logic()
