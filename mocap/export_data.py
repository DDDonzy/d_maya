"""
"""
from collections import OrderedDict
from maya import cmds


EXPORT_NODE = "_ANIM_EXPORTER_"


def get_exportData(exportNode=EXPORT_NODE):
    export_data = OrderedDict()
    export_data["exportPath"] = cmds.getAttr(f"{exportNode}.exportPath")
    export_data["exportName"] = cmds.getAttr(f"{exportNode}.exportFilename")

    clip_data = OrderedDict()
    for clip in cmds.ls(f"{exportNode}.animClips[*]"):
        clipName = cmds.getAttr(f"{clip}.animClipName")
        start = cmds.getAttr(f"{clip}.animClipStart")
        end = cmds.getAttr(f"{clip}.animClipEnd")
        clip_data[clipName] = (start, end)

    clip_items = clip_data.items()
    sorted_clip_items = sorted(clip_items, key=lambda item: item[1][0])
    sorted_clip = OrderedDict(sorted_clip_items)
    export_data["clip"] = sorted_clip
    return export_data


def create_exportData(data, name=EXPORT_NODE):
    if cmds.objExists(name):
        cmds.delete(name)
    node = cmds.createNode("gameFbxExporter", name=name)
    cmds.setAttr(f"{node}.pn", name, type="string")
    cmds.setAttr(f"{node}.eti", 2)
    cmds.setAttr(f"{node}.ils", 1)
    cmds.setAttr(f"{node}.ilu", 1)
    cmds.setAttr(f"{node}.exportPath", data["exportPath"], type="string")
    cmds.setAttr(f"{node}.exportFilename", data["exportName"], type="string")
    i = 0
    for k, v in data["clip"].items():
        clipAttr = f"{node}.animClips[{i}]"
        cmds.setAttr(f"{clipAttr}.animClipName", k, type="string")
        cmds.setAttr(f"{clipAttr}.animClipStart", v[0])
        cmds.setAttr(f"{clipAttr}.animClipEnd", v[1])
        i += 1
    return node
