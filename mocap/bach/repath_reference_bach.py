"""
================================================================================
Maya Batch Reference Repath Tool
================================================================================

[ 脚本目的 ]
该脚本是一个在 Maya 独立模式 (mayapy.exe) 下运行的自动化工具，其核心功能是
批量打开指定的 Maya 文件，并将其中的一个或多个引用 (Reference) 的路径更新为
新的、正确的路径。

这在项目文件迁移、资产库更新或修复损坏的引用路径时非常有用。

[ 工作流程 ]
1.  初始化:
    - 启动一个无界面的 Maya 独立环境。
    - 定义一个任务目录，扫描其中所有待处理的 `.ma` 文件。
    - 定义一个目标绑定文件 (`rig_file`) 和它在场景中对应的引用节点名
      (`rig_ref_node`)。

2.  批量处理 (循环):
    - 脚本会遍历所有待处理的 Maya 文件。
    - 对于每一个文件，它会执行以下操作：
        a. **打开文件**: 以“不加载任何引用”(`loadNoReferences=True`) 的方式
           强制打开文件。这可以加快文件打开速度，并避免因引用路径错误而
           导致的弹窗或卡死。
        b. **定位引用**: 使用 `repath_reference` 函数，根据预设的引用节点名
           (如 "RIGRN") 在场景中找到对应的引用。
        c. **更新路径**: 调用 `cmds.file(new_path, loadReference=...)` 命令，
           将该引用的文件路径修改为新的、正确的目标文件路径。
        d. **保存文件**: 将修改后的文件以相同的名称覆盖保存在指定的输出目录中。

3.  完成:
    - 循环处理所有文件，并在控制台打印出每一步的处理信息。

[ 核心函数 ]
-   list_all_references():
    遍历场景，返回一个包含所有引用节点、路径和加载状态的列表。

-   repath_reference(reference_node, new_path):
    接收一个引用节点名和一个新路径作为参数，执行实际的路径替换操作，并包含
    详细的成功/失败日志记录。

[ 如何运行 ]
在命令行中执行:
mayapy.exe "path/to/this/script/repath_reference.py"

================================================================================
"""

import os
from pathlib import Path

from maya import cmds

import log
from mocap.mayapy import init_maya
from mocap.suppress_maya_logs import suppress_maya_logs
from mocap.reference import list_all_references, repath_reference


def repath_reference_bach(
    task_dir,  # dir of maya files to process
    rig_file,  # path of the rig file to repath
    output_dir,  # dir to save processed maya files
    ref_filter_func=None,  # function to filter which reference to repath   Example: lambda path: "Rigs" in path
):
    task_dir = Path(task_dir)
    rig_file = Path(rig_file)
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 初始化maya独立环境
    init_maya()

    success_task = []  # 处理成功的文件列表
    error_task = []  # 处理失败的文件列表

    completed_task = [x.name for x in output_dir.glob("*.ma")]  # 已处理的文件列表
    task_list = list(task_dir.glob("*.ma"))  # 扫描目录
    for maya_file in task_list:
        file_name = maya_file.name  # 获取文件名

        # skip already completed file
        if file_name in completed_task:
            log.info(f"Already Completed: '{maya_file}'")
            continue

        # Process File
        log.info(f"Process : {maya_file}")
        try:
            # Open File
            with suppress_maya_logs():
                log.debug(f"Open File: '{file_name}'")
                cmds.file(maya_file, open=1, force=1, loadNoReferences=True)  # 打开，不加载引用
                log.debug(f"File Opened: '{file_name}'")

            # Repath Reference
            log.debug("change reference path...")
            ref_data = list_all_references()
            for ref in ref_data:
                old_path = ref["path"]
                if ref_filter_func(old_path):
                    rig_ref_node = ref["node"]
                    break
            repath_reference(rig_ref_node, rig_file)  # 重新指定 引用路径
            log.debug("Reference path changed.")

            # rename reference node
            log.debug("Rename reference node name.")
            cmds.lockNode(rig_ref_node, lock=False)  # 解锁引用节点
            cmds.rename(rig_ref_node, "RIGRN")  # 重命名引用节点
            log.debug("Reference node name renamed.")

            # save file
            log.debug(f"Try Save File: '{output_dir / file_name}'")
            cmds.file(rename=str(output_dir / file_name))  # 另存为
            cmds.file(save=True, force=True, type="mayaAscii")  # 保存
            log.debug(f"File Saved: '{output_dir / file_name}'")

            # add to success list
            success_task.append(maya_file)
            log.success(f"Completed: '{maya_file}' saved to '{output_dir / file_name}'")

        except Exception as e:
            error_task.append(maya_file)
            log.exception(f"Process Failed: '{maya_file}'\n{e}")
            continue
    
    #
    log.success(f"Total {len(success_task)} files processed successfully.")
    for ref in success_task:
        log.success(f"Completed File: {ref}")

    log.error(f"Total {len(error_task)} files failed.")
    for ref in error_task:
        log.error(f"Failed File: {ref}")


if __name__ == "__main__":
    task_dir = r"N:\SourceAssets\Characters\Hero\Mocap"  # 扫描目录
    rig_file = r"N:\SourceAssets\Characters\Hero\Rigs\RIG_Hero.ma"  # 绑定角色文件
    output_dir = r"N:\SourceAssets\Characters\Hero\Mocap\xxxxxx"  # 输出目录

    repath_reference_bach(
        task_dir=task_dir,
        rig_file=rig_file,
        output_dir=output_dir,
        ref_filter_func=lambda path: "Rigs" in path or "TestCharacter" in path,
    )
