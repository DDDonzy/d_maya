# Author:   Donzy.xu
# CreateTime:   2022/6/30 - 14:06
# FileName:  savePose.py


import json
import maya.cmds as cmds
import m_utils.transform as t


def export_poseData():
    json_path = cmds.fileDialog2(dialogStyle=2, caption="Export pose", fileFilter="Pose Files (*.json)")
    if json_path:
        json_path = json_path[0]
        with open(json_path, "w") as json_file:
            selection_list = cmds.ls(sl=1)
            pose_dataDict = {}
            for obj in selection_list:
                obj_TRS = t.get_trs(obj)
                pose_dataDict.update({obj: obj_TRS})
            pose_dataDict = json.dumps(pose_dataDict, sort_keys=True, indent=4, separators=(",", ": "))
            json_file.write(pose_dataDict)
        cmds.inViewMessage(amg="save pose\n%s" % json_path, pos="midCenterBot", fade=True)


def import_poseDate():
    json_path = cmds.fileDialog2(dialogStyle=2, caption="Load pose", fileFilter="Pose Files (*.json)", fileMode=1)
    if json_path:
        json_path = json_path[0]
        with open(json_path, "r") as json_file:
            pose_dataDict = json.load(json_file)
            for obj in pose_dataDict:
                if cmds.objExists(obj):
                    try:
                        t.set_trs(obj, pose_dataDict[obj])
                    except:
                        pass
        cmds.inViewMessage(amg="load pose\n%s" % json_path, pos="midCenterBot", fade=True)


# export_poseData()
# import_poseDate()
