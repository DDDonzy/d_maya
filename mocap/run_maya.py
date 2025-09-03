import sys
import time  # noqa: E402
from maya import cmds  # noqa: E402
from pathlib import Path  # noqa: E402

import maya.standalone
from maya import mel

maya.standalone.initialize(name="python")


def replace_reference_by_path(node, old_path, new_path):
    ref_node_to_replace = node
    if ref_node_to_replace:
        print(f"找到了匹配的 Reference Node: {ref_node_to_replace}")
        try:
            cmds.file(query=True, reference=True)
            cmds.file(new_path, loadReference=ref_node_to_replace)
            print(f"成功将 '{old_path}' 替换为 '{new_path}'")
        except Exception as e:
            print(f"替换失败: {e}")
    else:
        print(f"错误：在场景中找不到对 '{old_path}' 的引用。")


def run_optimize_scene():
    """
    执行 Maya 的 "Optimize Scene Size" 命令，清理所有类型的冗余节点。
    这是一个非常全面的清理工具。
    """
    print(">>> Running Maya's full Optimize Scene Size command...")
    # cleanUpScene 是 "Optimize Scene Size" 窗口背后的 MEL 脚本
    # 参数 3 表示执行所有勾选的清理项
    mel.eval("cleanUpScene(3)")
    print(">>> Optimize Scene Size finished.")




# 加载 FBX 插件
plugin_name = "fbxmaya"
if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
    print(f"Loading plugin: {plugin_name}...")
    try:
        cmds.loadPlugin(plugin_name)
        print("Plugin loaded successfully.")
    except Exception as e:
        print(f"!!! FAILED to load plugin {plugin_name}. Error: {e}")
        # 如果插件加载失败，后续操作很可能会失败，可以选择退出
        sys.exit(1)


print("------------------------------")
print("启动maya环境完成")


sys.path.insert(0, str(Path(__file__).parent))
from mocap_bake_rig import bakeAnimations  # noqa: E402


source_namespace = "MOCAP"
source_ref_node = "MOCAPRN"
rig_namespace = "RIG"
rig_ref_node = "RIGRN"
rig_file = r"N:\SourceAssets\Characters\TestCharacter\Rigs\TestCharacter_rig.ma"
done = []
error = []


scan_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap\clip_preprocessing")
output_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap")


file_list = list(scan_dir.glob("*.ma"))
out_list = [x.name for x in output_dir.glob("*.ma")]



num_clip = len(file_list)
for i, x in enumerate(file_list):
    try:
        if x.name in out_list:
            print(x)
            continue
        
        print("\n" * 5)
        print(f"============= Processing file {i + 1} of {num_clip} =============")
        if "old" in x.name:
            print("跳过旧文件:", x)
            continue
        maya_file_path = str(x)
        maya_file_name = x.stem

        print(f"OPEN: {maya_file_path}")
        try:
            cmds.file(maya_file_path, o=1, f=1, loadNoReferences=1)
        except RuntimeError as e:
            print("Error opening file:", e)

        if cmds.objExists(source_ref_node):
            old_path = Path(cmds.referenceQuery(source_ref_node, filename=True))
            if not (Path(r"N:\SourceAssets\Characters\Hero\Mocap\ue_retarget") / old_path.name).exists():
                print("跳过不存在的文件:", old_path)
                break
            
            replace_reference_by_path(source_ref_node, old_path, Path(r"N:\SourceAssets\Characters\Hero\Mocap\ue_retarget") / old_path.name)
        else:
            cmds.file(Path(r"N:\SourceAssets\Characters\Hero\Mocap\ue_retarget") / f"{maya_file_name}.fbx", reference=True, namespace=source_namespace)

        if cmds.objExists(rig_ref_node):
            cmds.file(removeReference=1, referenceNode=rig_ref_node)
        print("FILE OPENED!")

        run_optimize_scene()

        exporter_node = "_ANIM_EXPORTER_"
        num_clip = len(cmds.ls(f"{exporter_node}.ac[*]"))
        playback_start_frame = 0
        playback_end_frame = 100000000000
        for x in range(num_clip):
            s = cmds.getAttr(f"{exporter_node}.ac[0].acs")
            e = cmds.getAttr(f"{exporter_node}.ac[{num_clip - 1}].ace")
            playback_start_frame = s if s > playback_start_frame else playback_start_frame
            playback_end_frame = e if e < playback_end_frame else playback_end_frame

        print(f"当前播放范围: {playback_start_frame} - {playback_end_frame}")

        print("加载RIG 文件 Reference")
        cmds.file(rig_file, reference=True, namespace="RIG")
        print("Reference 加载完成")

        print("开始烘焙动画...")
        bakeAnimations(target_namespace=rig_namespace, source_namespace=source_namespace, time=(playback_start_frame, playback_end_frame))
        print("烘焙动画完成")

        print("取消加载 FBX REFERENCE")
        cmds.file(unloadReference=source_ref_node)
        print("FBX REFERENCE 删除完成")

        print("删除‘delete’")
        try:
            cmds.delete("delete")
        except Exception as e:
            print(e)

        cmds.playbackOptions(ast=playback_start_frame)
        cmds.playbackOptions(aet=playback_end_frame)
        print("设置播放范围为:", playback_start_frame)

        new_ma_path = output_dir / f"{maya_file_name}.ma"

        cmds.file(rename=new_ma_path)
        cmds.file(save=True, type="mayaAscii", f=1)
        print(f"场景文件已保存: {new_ma_path}")

        done.append(maya_file_path)
    except Exception as e:
        print("处理文件时出错:", e)
        print(x)
        error.append(maya_file_path)

print("\n" * 3)
print(f"============={len(done)} 个文件处理成功===============")
for x in done:
    print(x)

print("\n" * 3)
print(f"============={len(error)} 个文件处理失败===============")
for x in error:
    print(x)
