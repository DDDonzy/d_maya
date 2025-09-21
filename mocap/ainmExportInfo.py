""" """

from collections import OrderedDict
from maya import cmds


EXPORT_NODE = "_ANIM_EXPORTER_"


def get_exportData(exportNode=EXPORT_NODE):
    """
    {"exportPath": "N:/SourceAssets/Characters/Hero/Animations/FBX",
     "exportName": "M_Blade_Stand_Turn_",
     "clip"      : {"L_045": ( 673.0,  811.0),
                    "R_045": (1171.0, 1294.0),
                    "L_090": (1642.0, 1796.0),
                    "R_090": (2175.0, 2360.0),
                    "L_135": (2644.0, 2823.0),
                    "R_135": (3153.0, 3323.0),
                    "L_180": (3652.0, 3822.0),
                    "R_180": (4146.0, 4337.0)}}
    """
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
