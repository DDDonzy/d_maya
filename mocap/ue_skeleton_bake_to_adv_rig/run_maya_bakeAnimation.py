"""
================================================================================
Mocap to Rig - Batch Animation Baking Pipeline
================================================================================

该脚本是一个在 Maya 独立模式 (mayapy.exe) 下运行的自动化工具，用于将预处理
过的动作捕捉 (Mocap) 动画片段，批量烘焙到一个标准化的角色绑定 (Rig) 上。

[ 工作流程 ]
1.  初始化:
    - 启动一个无界面的 Maya 独立环境。
    - 加载处理 FBX 和动画数据所必需的插件。
    - 定义源 Mocap 片段目录、最终输出目录、角色绑定文件等关键路径。

2.  扫描与过滤:
    - 脚本会扫描指定的任务目录 (`task_file`)，获取所有待处理的 `.ma` 文件列表。
    - 它会检查输出目录 (`output_dir`)，自动跳过已经处理完成的文件，支持任务中断和续跑。

3.  文件预处理 (循环内):
    - 打开每一个 Mocap 片段文件。
    - 从文件中一个名为 `_ANIM_EXPORTER_` 的特定节点上，读取并提取动画片段的元数据
      (如起止帧、片段名等)。
    - 对该文件执行深度清理，移除未知节点、垃圾数据结构等，并覆盖保存，确保源文件
      的“纯净性”。

4.  烘焙流程 (循环内):
    - 创建一个全新的、干净的 Maya 场景。
    - 将上一步提取的动画元数据写入到新场景的一个节点中，用于精确控制后续流程。
    - 将标准角色绑定文件 (`rig_file`) 作为引用加载到场景中 (命名空间: "RIG")。
    - 将刚刚被清理过的 Mocap 片段文件作为引用加载到场景中 (命名空间: "CLIP")。
    - 根据动画设置正确的动画播放范围。
    - 调用核心的 `bakeAnimations` 函数，将 `CLIP:MOCAP` 命名空间下骨骼的动画，
      烘焙到 `RIG` 命名空间下的角色控制器上。

5.  收尾与输出 (循环内):
    - 动画数据烘焙完成后，卸载 (Unload) Mocap 片段的引用，以减小文件体积。
    - 再次清理场景，确保没有冗余数据。
    - 将这个只包含已烘焙动画的 Rig 的场景，重命名并保存到最终的输出目录 (`output_dir`)。

6.  完成:
    - 循环处理所有文件，并在最后打印出成功处理的文件列表。
================================================================================
"""

from maya import cmds
import maya.standalone


from pathlib import Path

from mocap.ue_skeleton_bake_to_adv_rig.fn_bake_animation import bakeAnimations
from mocap.gameExportInfo import get_exportData, create_exportData
from mocap.mayapy import init_maya
from mocap.suppress_maya_logs import suppress_maya_logs
from UTILS.scene.removeUnknownPlugin import removeUnknownPlugin


def info(title: str, total_length: int = 200) -> None:
    formatted_title = f"{f' {title} ':=^{total_length}}"
    print(formatted_title)


def debug(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ DEBUG ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


def error(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ ERROR ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


def clean_unknown_data():
    """清理场景中的 unknown 节点和未加载的引用"""
    try:
        unknown_nodes = cmds.ls(type="unknown")
        if unknown_nodes:
            cmds.delete(unknown_nodes)

        unknown_plugin_nodes = cmds.ls(type="unknownPlugin")
        if unknown_plugin_nodes:
            cmds.delete(unknown_plugin_nodes)

        unknown_transforms = cmds.ls(type="unknownTransform")
        if unknown_transforms:
            cmds.delete(unknown_transforms)

        refs = cmds.ls(references=True)
        for ref in refs:
            if not cmds.referenceQuery(ref, isLoaded=True):
                try:
                    cmds.file(removeReference=True, referenceNode=ref)
                except Exception:
                    pass

        cmds.dataStructure(removeAll=True)
        print("Clear unknown data complete.")

    except Exception as e:
        print(f"Clear unknown error: {e}")


if __name__ == "__main__":
    task_file = list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\clip_preprocessing").glob("*.ma"))  # 扫描目录
    fbx_output_dir = Path(r"N:\SourceAssets\Characters\Hero\Animations\FBX")  # FBX 输出目录，用于配置Game Exporter节点，不导出fbx
    output_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap\xx")  # 输出目录

    rig_file = r"N:\SourceAssets\Characters\Hero\Rigs\Rig_Hero.ma"  # 绑定角色文件
    rig_namespace = "RIG"  # 绑定角色命名空间
    mocap_namespace = "MOCAP"  # 动作源命名空间
    clip_namespace = "CLIP"  # 动作片段命名空间 

    # 初始化maya独立环境
    init_maya()

    success_list = []  # 处理成功的文件列表
    already_done = [x.name for x in output_dir.glob("*.ma")]  # 已处理的文件列表
    for maya_file in task_file:  # 遍历任务文件
        file_name = maya_file.name  # 获取文件名
        if file_name in already_done:  # 如果文件已处理，跳过
            info(f"Skip (already done): {maya_file}")
            continue
        info(f"Process : {maya_file}")
        try:
            # Open File
            debug(f"Open File: {file_name}")
            with suppress_maya_logs():
                cmds.file(maya_file, open=1, force=1)
            # Get Clip Data
            clip_data = get_exportData()  # 获取导出数据
            # 如果没有导出数据，跳过
            if clip_data:
                debug("Get Clip Success")
            else:
                debug("No Clip Data Found, Skip!")
                continue
            # data structure clear
            cmds.dataStructure(removeAll=True)
            removeUnknownPlugin()
            debug("Clear Data Structure Complete And Remove Unknown Plugin")
            cmds.file(rename=maya_file)
            cmds.file(save=True, force=True)
            debug("Cleaned File Saved")

            # Create New File
            cmds.file(file_name, new=1, force=1)
            debug("New File Created")

            cmds.currentUnit(time="ntscf")  # 设置时间单位为 60 FPS
            debug("Set Time Unit to ntscf-----60 FPS")

            export_node = create_exportData(clip_data)  # 创建导出节点
            debug("Create Export Node Complete")

            # reference Rig and Mocap
            debug("Reference Clip and Rig")
            with suppress_maya_logs():
                cmds.file(rig_file, reference=True, namespace="RIG", force=1)  # 引用绑定角色
                debug("Rig Reference Complete")
                cmds.file(maya_file, reference=True, namespace="CLIP", force=1)  # 引用片段
                debug("Clip Reference Complete")
            print(cmds.ls(type="skinCluster"))

            # bake Animation
            clips_attrs = cmds.ls(f"{export_node}.animClips[*]")  # 获取所有动画片段属性
            start = cmds.getAttr(f"{clips_attrs[0]}.animClipStart")  # 获取第一个片段的开始时间
            end = cmds.getAttr(f"{clips_attrs[-1]}.animClipEnd")  # 获取最后一个片段的结束时间

            cmds.playbackOptions(ast=start)  # 设置播放范围开始时间
            cmds.playbackOptions(aet=end)  # 设置播放范围结束时间
            debug(f"Set Playback Range: {start} - {end}")
            debug("Baking Animation...")
            # 烘焙动画
            bakeAnimations(
                target_namespace=rig_namespace,
                source_namespace=":".join([clip_namespace, mocap_namespace]),
                time=(start, end),
            )
            debug("Baking Animation Complete")

            cmds.setAttr(f"{export_node}.exportPath", str(fbx_output_dir), type="string")  # 设置导出路径
            debug("Set Export Path Complete")
            clean_unknown_data()  # 清理 unknown 数据
            debug("Clean Unknown Data Complete")
            cmds.file(unloadReference=f"{clip_namespace}RN")  # 卸载片段引用
            debug("Unload Clip Reference Complete")
            cmds.file(rename=str(output_dir / file_name))  # 重命名文件
            cmds.file(save=True, force=True, type="mayaAscii")  # 保存文件
            debug("Save File Complete")

        except Exception:
            error(maya_file)
            raise
        success_list.append(maya_file)  # 添加到成功列表
        info(f"Complate: {str(output_dir / file_name)}")
        break

    info(f"Total {len(success_list)} files processed successfully.")
    for x in success_list:
        info(x)
