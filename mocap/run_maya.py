import sys  # noqa: E402
from maya import cmds  # noqa: E402
from pathlib import Path  # noqa: E402

import maya.standalone

maya.standalone.initialize(name="python")


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


ma = {}
fbx = {}
ref_node = "MOCAPRN"

done = []
error = []


for x in list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\20250830").glob("*.ma")):
    try:
        print("\n" * 5)
        maya_file_path = str(x)
        maya_file_name = x.stem

        print(f"OPEN: {maya_file_path}")
        cmds.file(maya_file_path, o=1, f=1)
        print("FILE OPENED!")

        exporter_node = "_ANIM_EXPORTER_"
        num_clip = len(cmds.ls(f"{exporter_node}.ac[*]"))
        playback_start_frame = cmds.getAttr(f"{exporter_node}.ac[0].acs")
        playback_end_frame = cmds.getAttr(f"{exporter_node}.ac[{num_clip - 1}].ace")
        print(f"当前播放范围: {playback_start_frame} - {playback_end_frame}")

        print("加载RIG 文件 Reference")
        cmds.file(r"N:\SourceAssets\Characters\TestCharacter\Rigs\TestCharacter_rig.ma", reference=True, namespace="RIG")
        print("Reference 加载完成")

        print("开始烘焙动画...")
        bakeAnimations(target_namespace="RIG", source_namespace="MOCAP", time=(playback_start_frame, playback_end_frame))
        print("烘焙动画完成")

        print("删除 FBX REFERENCE")
        cmds.file(removeReference=True, referenceNode=ref_node)
        print("FBX REFERENCE 删除完成")

        print("删除‘delete’")
        try:
            cmds.delete("delete")
        except Exception as e:
            print(e)

        cmds.playbackOptions(ast=playback_start_frame)
        cmds.playbackOptions(aet=playback_end_frame)
        print("设置播放范围为:", playback_start_frame)

        new_ma_path = Path(r"N:\SourceAssets\Characters\Hero\Mocap\20250830\test") / f"{maya_file_name}.ma"

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
