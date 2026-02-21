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
from pathlib import Path


import log

from mocap.bake.bake_animation import bakeAnimations
from mocap.gameExportInfo import create_exportData
from mocap.mayapy import init_maya
from mocap.suppress_maya_logs import suppress_maya_logs


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
                except Exception as e:
                    log.trace(e)

        cmds.dataStructure(removeAll=True)
        log.trace("Clear unknown data complete.")

    except Exception as e:
        log.trace(f"Clear unknown error: {e}")


def loadHandPose():
    """加载手部姿势"""
    import sys

    if r"C:\Users\Donzy\Downloads\studiolibrary-2.20.2\src" not in sys.path:
        sys.path.insert(0, r"C:\Users\Donzy\Downloads\studiolibrary-2.20.2\src")
    import mutils  # type: ignore

    mutils.loadPose(r"C:\Users\Donzy\Desktop\pose\Hero\Hand\Hand_R_Weapon.pose\pose.json", namespaces=":", key=True)


if __name__ == "__main__":
    task_file = list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\Xsens\UE_Retarget").glob("*.fbx"))  # 扫描目录
    output_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap\Xsens\Bake")  # 输出目录
    fbx_output_dir = Path(r"N:\SourceAssets\Characters\Hero\Animations\FBX")  # FBX 输出目录，用于配置Game Exporter节点，不导出fbx
    rig_file = r"N:\SourceAssets\Characters\Hero\Rigs\Rig_Hero.ma"  # 绑定角色文件

    rig_namespace = "RIG:"  # 绑定角色命名空间
    mocap_namespace = "MOCAP:"  # 动作源命名空间

    # 初始化maya独立环境
    init_maya()

    succeeded_list = []  # 处理成功的文件列表
    failed_list = []  # 处理失败的文件列表
    already_completed_list = [x.name for x in output_dir.glob("*.ma")]  # 已处理的文件列表
    skip_list = []  # 跳过的文件列表

    for mocap_file in task_file:
        file_name = mocap_file.name  # 获取文件名
        # 如果文件已处理，跳过
        if file_name in already_completed_list:
            skip_list.append(file_name)
            log.info(f"Skip (already done): '{mocap_file}'")
            continue

        # 开始处理文件
        log.info(f"Process : '{mocap_file}'")
        try:
            cmds.file(file_name, new=1, force=1)  # 新建文件
            log.debug(f"New File Created:{file_name}")
            cmds.currentUnit(time="ntscf")  # 设置时间单位为 60 FPS
            log.debug("Set Time Unit to ntscf ----- 60 FPS")

            # 引用 绑定 和 Mocap
            log.debug("Reference Mocap and Rig")
            with suppress_maya_logs():
                log.debug("Referencing Files...")
                cmds.file(rig_file, reference=True, namespace="RIG", force=1)  # 引用绑定角色
                log.debug("Rig Reference Complete")
                cmds.file(mocap_file, reference=True, namespace="MOCAP", force=1)  # 引用MOCAP
                log.debug("Clip Reference Complete")

            # 获取FBX文件开始结束时间
            keyframes = cmds.keyframe(f"{mocap_namespace}pelvis", query=True, timeChange=True)
            start = keyframes[0]
            end = keyframes[-1]
            cmds.playbackOptions(ast=start, aet=end, min=2, max=4)  # 设置播放范围开始时间
            log.debug(f"Set Playback Range: {start} - {end}")

            log.debug("Load hand Pose.")
            loadHandPose()  # 加载手部姿势
            log.debug("Load Hand Pose complete.")

            # bake Animation
            log.debug("Baking...")
            # 烘焙动画
            bakeAnimations(
                target_namespace=rig_namespace,
                source_namespace=mocap_namespace,
                time=(start, end),
            )
            log.debug("Baking Animation Complete")

            export_node = {
                "exportPath": str(fbx_output_dir),
                "exportName": "",
                "clip": {
                    "Name": (start, end),
                },
            }
            create_exportData(export_node)
            log.debug("Set Export Path Complete")

            cmds.file(unloadReference=f"{mocap_namespace.replace(':', '')}RN")  # 卸载Mocap引用
            log.debug("Unload Mocap Reference Complete")

            clean_unknown_data()  # 清理场景
            log.debug("Clean Unknown Data Complete")

            log.debug("Save Fils...")
            cmds.file(rename=str(output_dir / f"{mocap_file.stem}.ma"))  # 重命名文件
            cmds.file(save=True, force=True, type="mayaAscii")  # 保存文件
            log.debug("Save File Complete")

        except Exception as e:
            log.exception(e)
            failed_list.append(mocap_file)  # 添加到失败列表
            raise

        succeeded_list.append(mocap_file)  # 添加到成功列表
        log.success(f"Completed: {str(output_dir / f'{mocap_file.stem}.ma')}")

    log.info("----" * 10)
    log.info("Complete All Tasks.")
    log.info("----" * 10)

    log.success(f"Total {len(succeeded_list)} files processed successfully.")
    for x in succeeded_list:
        log.success(f"Completed File: {x}")
    if failed_list:
        log.error(f"Total {len(failed_list)} files failed.")
    else:
        log.success("All files processed successfully without errors.")
    for x in failed_list:
        log.error(f"Failed File: {x}")
