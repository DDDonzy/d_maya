import maya.standalone 
maya.standalone.initialize( name='python' )


from maya import cmds  # noqa: E402
import os  # noqa: E402
from pathlib import Path  # noqa: E402

import maya.mel as mel


from maya import cmds
from maya.api import OpenMaya as om
from UTILS.transform import get_worldMatrix, get_relativesMatrix
from UTILS.compounds import matrixConstraint
from UTILS.create.assetCallback import AssetCallback

from mocap_bake_rig import *


def replace_reference_by_path(node, old_path, new_path):
    ref_node_to_replace = node
    if ref_node_to_replace:
        print(f"找到了匹配的 Reference Node: {ref_node_to_replace}")
        try:
            cmds.file(new_path, loadReference=ref_node_to_replace)
            print(f"成功将 '{old_path}' 替换为 '{new_path}'")
        except Exception as e:
            print(f"替换失败: {e}")
    else:
        print(f"错误：在场景中找不到对 '{old_path}' 的引用。")


ma = {}
fbx = {}
ref_node = "MOCAPRN"


for x in list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\clip2").glob("*.ma")):
    source = x.stem
    new = "".join(char for char in source if char.isalnum())
    ma.update({new: x})
    print(new)


for x in list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\retarget_source").glob("*.fbx")):
    source = x.stem
    new = "".join(char for char in source if char.isalnum()).replace("Retarget", "")
    fbx.update({new: x})


for k, v in ma.items():
    if k in fbx.keys():
        ma_file = ma[k]
        new_ma_name = ma_file.stem.replace("(", "_").replace(")", "_")

        new_ref_path = fbx[k]

        print(f"正在处理: {k} - {ma_file} -> {new_ref_path}")
        print(f"正在加载场景文件...{ma_file}")
        cmds.file(ma_file, o=1, f=1, loadNoReferences=1)
        print(f"加载完成: {ma_file}")

        exporter_node = "_ANIM_EXPORTER_"

        old_ref_path = cmds.referenceQuery(ref_node, filename=True)
        print("当前引用路径:", old_ref_path)

        num_clip = len(cmds.ls(f"{exporter_node}.ac[*]"))
        playback_start_frame = cmds.getAttr(f"{exporter_node}.ac[0].acs")
        playback_end_frame = cmds.getAttr(f"{exporter_node}.ac[{num_clip - 1}].ace")
        print(f"当前播放范围: {playback_start_frame} - {playback_end_frame}")

        replace_reference_by_path(ref_node, old_ref_path, new_ref_path)
        print(f"引用路径已替换: {new_ref_path}")

        cmds.playbackOptions(ast=playback_start_frame)
        cmds.playbackOptions(aet=playback_end_frame)
        print("设置播放范围为:", playback_start_frame)

        export_file_name = cmds.getAttr(f"{exporter_node}.exportFilename")

        cmds.setAttr(f"{exporter_node}.ac[{num_clip}].acn", "All", type="string")
        cmds.setAttr(f"{exporter_node}.ac[{num_clip}].acs", playback_start_frame)
        cmds.setAttr(f"{exporter_node}.ac[{num_clip}].ace", playback_end_frame)

        for x in range(num_clip):
            cmds.setAttr(f"{exporter_node}.ac[{x}].exportAnimClip", False)
        cmds.setAttr(f"{exporter_node}.ac[{num_clip}].exportAnimClip", True)
        cmds.setAttr(f"{exporter_node}.exportFilename", f"{new_ma_name}_", type="string")
        cmds.setAttr(f"{exporter_node}.exportPath", r"N:\SourceAssets\Characters\Hero\Mocap\clip3\sourceRetarget_clip", type="string")

        print("设置导出ALL")

        # print("开始导出")
        # if cmds.window("gameExporterWindow", q=1, ex=1):
        #     cmds.deleteUI("gameExporterWindow")
        # mel.eval("gameFbxExporter")
        # mel.eval("gameExp_DoExport;")

        print("导出结束")

        for x in range(num_clip):
            cmds.setAttr(f"{exporter_node}.ac[{x}].exportAnimClip", True)
        cmds.setAttr(f"{exporter_node}.ac[{num_clip}].exportAnimClip", False)
        cmds.setAttr(f"{exporter_node}.exportFilename", export_file_name, type="string")
        cmds.setAttr(f"{exporter_node}.exportPath", r"N:\SourceAssets\Characters\Hero\Mocap\clip3\FBX", type="string")
        new_ma_path = Path(r"N:\SourceAssets\Characters\Hero\Mocap\clip3") / f"{new_ma_name}.ma"
        
        cmds.file(r"N:\SourceAssets\Characters\TestCharacter\Rigs\TestCharacter_rig.ma", reference=True, namespace="RIG")
        
        cmds.playbackOptions(ast=playback_start_frame)
        cmds.playbackOptions(aet=playback_end_frame)
        print("设置播放范围为:", playback_start_frame)



        bakeAnimations(target_namespace="RIG", source_namespace="MOCAP", time=(playback_start_frame, playback_end_frame))
        
        cmds.file(removeReference=True, referenceNode=ref_node)
        
        
        
        cmds.playbackOptions(ast=playback_start_frame)
        cmds.playbackOptions(aet=playback_end_frame)
        print("设置播放范围为:", playback_start_frame)

        cmds.file(rename=new_ma_path)
        cmds.file(save=True, type="mayaAscii", f=1)
        print(f"场景文件已保存: {ma_file}")
