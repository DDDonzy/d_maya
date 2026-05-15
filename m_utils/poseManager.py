import json
from pathlib import Path

import log
from m_utils import transform

from maya import cmds
from maya.api import OpenMaya as om


def get_poseData_by_selected():
    mSel: om.MSelectionList = om.MGlobal.getActiveSelectionList()
    if mSel.length() == 0:
        raise RuntimeError("No object selected")

    pose_data = {}
    for x in range(mSel.length()):
        dag: om.MDagPath = mSel.getDagPath(x)
        name = dag.partialPathName()
        pose_data[name] = list(transform.get_worldMatrix(name))

    return pose_data


def get_poseData():
    return get_poseData_by_selected()


def set_poseData(pose_data):
    todo_dict = {}
    for name, matrix in pose_data.items():
        try:
            mSel: om.MSelectionList = om.MGlobal.getSelectionListByName(name)  # Check if the object exists
        except RuntimeError:
            log.warning("Object '{}' does not exist. Skipping.", name)
            continue

        dag: om.MDagPath = mSel.getDagPath(0)  # Get the DAG path of the object
        i_todo_data = todo_dict.get(dag.length(), [])
        i_todo_data.append((dag.partialPathName(), matrix))
        todo_dict[dag.length()] = i_todo_data

    current_selected = cmds.ls(sl=1) or pose_data.keys()
    for i in sorted(todo_dict.keys(), reverse=False):
        for name, matrix in todo_dict[i]:
            if name not in current_selected:
                continue
            try:
                transform.set_worldMatrix(name, om.MMatrix(matrix))
            except RuntimeError as e:
                log.error("Failed to set pose for '{}': {}", name, e)
                continue
    return True


def export_poseData():
    json_path = cmds.fileDialog2(dialogStyle=2, caption="Export pose", fileFilter="Pose Files (*.json)")
    if not json_path:
        return None
    json_path = Path(json_path[0])
    pose_data = get_poseData()
    with json_path.open("w") as json_file:
        json.dump(pose_data, json_file, indent=4)
    log.success("Pose data exported to '{}'", json_path)
    return True


def import_poseData():
    json_path = cmds.fileDialog2(dialogStyle=2, caption="Load pose", fileFilter="Pose Files (*.json)", fileMode=1)
    if not json_path:
        return None
    json_path = Path(json_path[0])
    with json_path.open("r") as json_file:
        pose_data = json.load(json_file)
    set_poseData(pose_data)
    log.success("Pose data imported from '{}'", json_path)
    return True
