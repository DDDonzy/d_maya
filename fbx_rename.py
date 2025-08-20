# -*- coding: utf-8 -*-

"""
FBX批量重命名并转换为Binary格式的工具。

功能:
- 遍历指定文件夹下的所有 .fbx 文件。
- 对每个文件中的所有节点名称执行搜索和替换。
- 将修改后的文件以Binary格式覆盖保存。
"""

import sys
import os
from pathlib import Path

try:
    from fbx import *
except ImportError:
    print("错误: FBX Python模块无法导入。")
    print("请确保您的Python环境已正确配置FBX SDK路径。")
    sys.exit(1)

# --- 1. 自定义配置 ---
# 您可以在这里修改搜索和替换的字符串
SEARCH_STRING = "MOCAP:"
REPLACE_STRING = ""
OUTPUT_SUFFIX = "" # 注意：空后缀会覆盖原文件
# --------------------


def process_node_recursive(node, search_str, replace_str):
    """
    递归处理节点及其所有子节点，执行名称替换。
    """
    original_name = node.GetName()
    if search_str in original_name:
        new_name = original_name.replace(search_str, replace_str)
        node.SetName(new_name)
        print(f"    - Renamed: '{original_name}' -> '{new_name}'")

    # 递归遍历子节点
    for i in range(node.GetChildCount()):
        process_node_recursive(node.GetChild(i), search_str, replace_str)


# [修改] 函数重命名，并修改内部逻辑以保存为Binary
def save_scene_as_binary(manager, scene, file_path):
    """
    将场景以默认的Binary格式保存到文件。
    """
    exporter = FbxExporter.Create(manager, "")
    try:
        # 要保存为默认的二进制格式，文件格式ID传入-1即可
        # 无需再遍历查找ASCII格式
        if not exporter.Initialize(str(file_path), -1, manager.GetIOSettings()):
            error = exporter.GetStatus().GetErrorString()
            print(f"  错误: FbxExporter 初始化失败: {error}")
            return False

        if not exporter.Export(scene):
            print("  错误: 导出场景失败。")
            return False

    finally:
        # 确保导出器被销毁
        exporter.Destroy()
    return True


def process_fbx_file(fbx_path: Path):
    """
    处理单个FBX文件：加载、重命名、另存为Binary。
    """
    print(f"\n--- 正在处理文件: {fbx_path.name} ---")

    manager = FbxManager.Create()
    if not manager:
        print("  错误: 无法创建FBX管理器。")
        return

    try:
        scene = FbxScene.Create(manager, "scene")
        importer = FbxImporter.Create(manager, "")

        if not importer.Initialize(str(fbx_path), -1, manager.GetIOSettings()):
            print("  错误: FbxImporter 初始化失败。")
            return

        if not importer.Import(scene):
            print("  错误: 导入场景失败。")
            return
        importer.Destroy()

        # 执行重命名
        print("  正在搜索和替换节点名称...")
        process_node_recursive(scene.GetRootNode(), SEARCH_STRING, REPLACE_STRING)

        # 定义输出路径
        output_filename = f"{fbx_path.stem}{OUTPUT_SUFFIX}{fbx_path.suffix}"
        output_path = fbx_path.with_name(output_filename)

        # [修改] 更新日志和函数调用
        print(f"  正在将结果保存为Binary格式到: {output_path.name}")
        if not save_scene_as_binary(manager, scene, output_path):
             print(f"  未能成功保存文件: {output_path.name}")
        else:
             print(f"  成功保存文件!")

    finally:
        # 确保管理器及其所有对象被销毁
        manager.Destroy()


def process_directory(directory_path_str: str):
    """
    遍历指定目录下的所有FBX文件并处理它们。
    """
    directory_path = Path(directory_path_str)

    if not directory_path.is_dir():
        print(f"错误: 提供的路径不是一个有效的文件夹: {directory_path}")
        return

    print(f"开始扫描文件夹: {directory_path}")
    fbx_files = list(directory_path.glob('*.fbx'))

    if not fbx_files:
        print("未在该文件夹下找到任何 .fbx 文件。")
        return

    print(f"找到 {len(fbx_files)} 个 .fbx 文件，准备处理...")

    for fbx_file in fbx_files:
        process_fbx_file(fbx_file)

    print("\n--- 所有任务处理完毕 ---")


if __name__ == "__main__":

    input_folder = r"N:\SourceAssets\Characters\Hero\Mocap\clip3\sourceRetarget_clip"
    process_directory(input_folder)