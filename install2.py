# -*- coding: utf-8 -*-

"""
Maya 插件依赖自动安装脚本 (从 requirements.txt 读取) - 修正版

功能:
1. 自动检测当前 Maya 的版本和路径。
2. 查找与本脚本位于同一目录下的 'requirements.txt' 文件。
3. **正确地从 maya.exe 推断出 mayapy.exe 的路径。**
4. 使用与当前 Maya 版本匹配的 mayapy 来安装文件中列出的所有 Python 依赖包。
5. 提供清晰的安装过程反馈。
"""

import sys
import subprocess
import os
from pathlib import Path

def get_maya_info():
    """
    获取当前 Maya 环境的关键信息。
    此函数经过修正，可以正确地在 Maya GUI 环境中找到 mayapy。
    """
    try:
        import maya.cmds as cmds
        
        # --- 关键修正 ---
        # 在 Maya GUI 中, sys.executable 指向 maya.exe 或 Maya (macOS)
        current_executable = Path(sys.executable)
        # bin 目录是当前可执行文件的父目录
        bin_dir = current_executable.parent
        
        # 根据操作系统构建 mayapy 的名称
        mayapy_name = "mayapy.exe" if sys.platform == "win32" else "mayapy"
        
        # 在同一个 bin 目录下构建 mayapy 的完整路径
        mayapy_path = bin_dir / mayapy_name

        print(f"当前可执行文件: {current_executable}")
        print(f"推断出的 'bin' 目录: {bin_dir}")
        print(f"定位到的 'mayapy' 路径: {mayapy_path}")
        
        # 安全检查：确保推断出的 mayapy 路径是真实存在的
        if not mayapy_path.is_file():
            print(f"错误：无法在预期的位置找到 'mayapy' ({mayapy_path})")
            print("脚本无法继续。")
            return None
            
        maya_version = cmds.about(version=True)
        is_windows = sys.platform == "win32"
        
        return {
            "mayapy_path": mayapy_path,
            "version": maya_version,
            "is_windows": is_windows,
        }
    except ImportError:
        print("错误: 此脚本似乎没有在 Maya 环境中运行。")
        return None

def check_admin_rights():
    """检查在 Windows 上是否具有管理员权限"""
    if os.name == 'nt':
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    return True

def run_pip_install_from_reqs(mayapy_path, requirements_file):
    """
    运行 pip install -r 命令来安装文件中的所有包。
    """
    print(f"\n准备从文件 '{requirements_file.name}' 安装依赖包...")
    
    command = [
        str(mayapy_path),
        "-m",
        "pip",
        "install",
        "-r",
        str(requirements_file)
    ]

    print("-" * 50)
    print(f"将要执行的命令: \n{' '.join(command)}")
    print("-" * 50)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        print("--- 安装成功 ---")
        print(result.stdout)
        return True

    except FileNotFoundError:
        print(f"错误: 无法找到命令 '{mayapy_path}'。请确认路径是否正确。")
        return False
        
    except subprocess.CalledProcessError as e:
        print("--- 安装失败 ---")
        print("错误信息:")
        print(e.stderr)
        
        if "Permission denied" in e.stderr or "Access is denied" in e.stderr:
            print("\n检测到权限问题！")
            if sys.platform == "win32":
                print("请尝试 '以管理员身份运行' Maya，然后再次拖拽此脚本进行安装。")
            else:
                print("你可能需要手动在终端中运行上述命令（可能需要 sudo 权限）。")
        return False

def main():
    """主执行函数"""
    print("=" * 70)
    print("开始执行 Maya 插件依赖自动安装程序 (修正版)")
    print("=" * 70)

    try:
        script_path = Path(__file__).resolve()
        script_dir = script_path.parent
        requirements_file = script_dir / "requirements.txt"
        print(f"脚本所在目录: {script_dir}")
        print(f"正在查找依赖文件: {requirements_file}")

        if not requirements_file.is_file():
            print(f"\n错误: 未能在脚本所在目录中找到 'requirements.txt' 文件。")
            print("请确保 'install.py' 和 'requirements.txt' 放在同一个文件夹下。")
            return
            
    except NameError:
        print("\n错误: 无法确定脚本路径。")
        print("请不要直接复制粘贴代码到脚本编辑器，而是将 .py 文件拖拽到 Maya 视口来运行。")
        return
    
    maya_info = get_maya_info()
    if not maya_info:
        return

    if maya_info["is_windows"]:
        print("\n正在检查管理员权限...")
        if not check_admin_rights():
            print("警告: 当前 Maya 未以管理员身份运行。安装过程可能会因权限不足而失败。")
        else:
            print("成功: 当前是以管理员权限运行。")

    if run_pip_install_from_reqs(maya_info["mayapy_path"], requirements_file):
        print("\n🎉 所有依赖已成功安装或已是最新版本！")
        print("插件环境已准备就绪。")
    else:
        print("\n❌ 部分或全部依赖安装失败。")
        print("请检查上面的错误信息以了解详情。")
    
    print("\n" + "=" * 70)
    print("安装程序执行完毕。")
    print("=" * 70)

if __name__ == "__main__":
    main()