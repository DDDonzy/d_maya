from maya import cmds
from maya.api import OpenMaya as om
import mutils.transform as t


def get_adv_extra_controls(control: str):
    parent = cmds.listRelatives(control, parent=True)[0]
    if "Extra" in parent:
        return parent
    else:
        return None


def get_adv_controls_data_from_scene(controls_set="ControlSet"):
    controls_list = cmds.sets(controls_set, query=True)
    controls_dict = {}
    for x in controls_list:
        extra = get_adv_extra_controls(x)
        if extra:
            controls_dict[x] = extra
    return controls_dict


def zero_pose(control, zero_control):
    control_world_matrix = t.get_worldMatrix(control)
    zero_parent_matrix = t.get_parentMatrix(zero_control)
    offset_matrix = t.get_relativesMatrix(control_world_matrix, zero_parent_matrix)
    if offset_matrix.isEquivalent(om.MMatrix()):
        return
    if not cmds.objExists(f"{control}.tPoseMatrix"):
        cmds.addAttr(control, ln="tPoseMatrix", dt="matrix")
        bwm_node = cmds.createNode("blendMatrix", name=f"{control}_tPoseBlendMatrix", skipSelect=1)
        cmds.connectAttr(f"{control}.tPoseMatrix", f"{bwm_node}.target[0].targetMatrix")
        cmds.connectAttr(f"{bwm_node}.outputMatrix", f"{zero_control}.offsetParentMatrix")
        if not cmds.objExists("Main.tPose"):
            cmds.addAttr("Main", ln="tPose", at="double", min=0, max=1, dv=1, keyable=True)
        cmds.connectAttr("Main.tPose", f"{bwm_node}.target[0].weight")

    cmds.setAttr(f"{control}.tPoseMatrix", offset_matrix, type="matrix")

    t.set_localMatrix(control, om.MMatrix())
    t.set_localMatrix(zero_control, om.MMatrix())


def zero_all_controls():
    controls_data = get_adv_controls_data_from_scene()
    for control, zero_control in controls_data.items():
        zero_pose(control, control)


if __name__ == "__main__":
    zero_all_controls()


