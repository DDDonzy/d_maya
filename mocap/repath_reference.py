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

from pathlib import Path

from maya import cmds

from mocap.mayapy import init_maya
from mocap.suppress_maya_logs import suppress_maya_logs
from mocap.reference import list_all_references, repath_reference


def info(title: str, total_length: int = 200) -> None:
    formatted_title = f"{f' {title} ':=^{total_length}}"
    print(formatted_title)


def debug(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ DEBUG ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


def error(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ ERROR ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


if __name__ == "__main__":
    task_file = list(Path(r"N:\SourceAssets\Characters\Hero\Mocap").glob("*.ma"))  # 扫描目录
    output_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap\xx")  # 输出目录

    rig_file = r"N:\SourceAssets\Characters\Hero\Rigs\RIG_Hero.ma"  # 绑定角色文件

    # 初始化maya独立环境
    init_maya()

    success_list = []  # 处理成功的文件列表
    error_list = []  # 处理失败的文件列表
    already_done = [x.name for x in output_dir.glob("*.ma")]  # 已处理的文件列表
    for maya_file in task_file:
        file_name = maya_file.name  # 获取文件名
        if file_name in already_done:
            info(f"Skip Already Done: {maya_file}")
            continue  # 跳过已处理的文件

        info(f"Process : {maya_file}")
        try:
            # Open File
            debug(f"Open File: {file_name}")
            with suppress_maya_logs():
                try:
                    cmds.file(maya_file, open=1, force=1, loadNoReferences=True)  # 打开，不加载引用
                except Exception:
                    pass
            debug(f"File Opened: {file_name}")

            ref_data = list_all_references()
            for x in ref_data:
                if "Rigs" in x["path"] or "TestCharacter" in x["path"]:
                    rig_ref_node = x["node"]
                    break
            repath_reference(rig_ref_node, rig_file)  # 重新指定 引用路径
            cmds.lockNode(rig_ref_node, lock=False)  # 解锁引用节点
            cmds.rename(rig_ref_node, "RIGRN")  # 重命名引用节点
            debug(f"Repath Reference: {rig_ref_node} -> {rig_file}")

            cmds.file(rename=str(output_dir / file_name))  # 另存为
            cmds.file(save=True, force=True, type="mayaAscii")  # 保存
            success_list.append(maya_file)
            debug(f"File Saved: {output_dir / file_name}")

        except Exception as e:
            error(f"Process Failed: {maya_file} | Error: {e}")
            error_list.append(maya_file)

    info(f"Total {len(success_list)} files processed successfully.")
    for x in success_list:
        info(x)
    info(f"Total {len(error_list)} files failed.")
    for x in error_list:
        error(x)
