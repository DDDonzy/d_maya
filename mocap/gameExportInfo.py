"""
================================================================================
Game Export Info - Animation Metadata Handler
================================================================================

该脚本提供了一套核心工具函数，用于在 Maya 场景中创建、读取和管理动画导出
所需的元数据 (Metadata)。它通过一个自定义的 "gameFbxExporter" 节点来持久化
存储这些信息，使得动画数据可以在不同的 Maya 文件和处理阶段之间被精确、可靠
地传递。


- 节点中心化: 所有元数据都存储在一个名为 "_ANIM_EXPORTER_" 的
  "gameFbxExporter" 类型的节点上。这种方法比使用场景变量或外部文件更
  加健壮，因为数据与 Maya 场景文件本身绑定在一起。
- 数据结构: 存储的数据主要包括：
    - 导出的 FBX 文件路径 (`exportPath`)。
    - 导出的 FBX 文件名 (`exportName`)。
    - 一个或多个动画片段 (`clip`) 的信息，每个片段包含名称、开始帧和结束帧。


1.  get_exportData(exportNode="_ANIM_EXPORTER_"):
    - 功能: 从场景中指定的 `exportNode` 上读取所有动画元数据。
    - 工作流程:
        a. 检查场景中是否存在该节点。
        b. 使用 `cmds.getAttr` 逐一获取 `exportPath` 和 `exportFilename` 属性。
        c. 遍历节点上的 `animClips` 复合属性，读取每一个片段的名称、开始帧和
           结束帧。
        d. 将读取到的片段数据按开始帧进行排序，确保数据的一致性。
        e. 将所有数据组织成一个有序字典 (OrderedDict) 并返回。

2.  create_exportData(data, name="_ANIM_EXPORTER_"):
    - 功能: 将一个包含元数据的字典写入到场景中的一个新节点上。
    - 工作流程:
        a. 如果场景中已存在同名节点，则先删除它以确保数据的全新写入。
        b. 创建一个新的 "gameFbxExporter" 节点。
        c. 使用 `cmds.setAttr` 将传入的 `data` 字典中的每一项（路径、名称、
           各个动画片段）逐一设置到新节点的对应属性上。
        d. 返回新创建的节点。

这个模块是整个自动化管线的“数据中枢”。例如：
- 在 Mocap 数据预处理阶段，使用 `create_exportData` 将切分好的动画片段信息
  写入文件。
- 在后续的烘焙阶段，使用 `get_exportData` 从文件中读出这些信息，以确定
  正确的烘焙范围和输出路径。

================================================================================
"""

from collections import OrderedDict
from maya import cmds


EXPORT_NODE = "_ANIM_EXPORTER_"


def get_exportData(exportNode=EXPORT_NODE):
    """
    从场景中指定的 `exportNode` 上读取所有动画元数据。
    Returns:
        data (dict): 一个包含导出元数据的字典，其结构和样式案例如下:
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
    if not cmds.objExists(exportNode):
        return export_data
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
    """
    根据传入的字典数据，在场景中创建一个 `gameFbxExporter` 节点并填充其属性。
    Args:
        data (dict): 一个包含导出元数据的字典，其结构和样式案例如下:
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
        name (str, optional): 要创建的节点名称。默认为 "_ANIM_EXPORTER_"。

    Returns:
        str: 新创建的节点的名称。
    """
    if cmds.objExists(name):
        cmds.delete(name)
    node = cmds.createNode("gameFbxExporter", name=name)
    cmds.setAttr(f"{node}.pn", name, type="string")
    cmds.setAttr(f"{node}.eti", 2)
    cmds.setAttr(f"{node}.ils", 1)
    cmds.setAttr(f"{node}.ilu", 1)
    cmds.setAttr(f"{node}.spt", 2)
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
