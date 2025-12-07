"""
================================================================================
Maya Python Environment - Batch Package Installer
================================================================================
[ 脚本目的 ]
该脚本是一个自动化工具，用于为 Maya 的 Python 环境 (mayapy.exe) 批量安装
在 `requirements.txt` 文件中定义的第三方库。它解决了在 Maya 封闭的 Python
环境中手动安装依赖包的繁琐问题。

[ 工作流程 ]
1.  定位 `mayapy.exe`:
    - 脚本首先通过 `sys.executable` 获取当前运行的 Python 解释器路径。
    - 它假定 `mayapy.exe` 与当前解释器（通常是 `python.exe`）位于同一目录下，
      从而精确地定位到 Maya 的 Python 执行文件。

2.  定位 `requirements.txt`:
    - 脚本会自动查找与自身 (`installPackage.py`) 位于同一目录下的
      `requirements.txt` 文件。

3.  执行安装命令:
    - 它会构建一个类似于以下的命令行指令：
      `mayapy.exe -m pip install -r path/to/requirements.txt`
    - 使用 Python 的 `subprocess` 模块，在后台执行这个命令。

4.  处理输出与结果:
    - 实时捕获 `pip` 命令的输出流（包括标准输出和错误输出）。
    - 如果安装成功，则打印成功信息和 `pip` 的日志。
    - 如果安装过程中发生任何错误（如网络问题、包不兼容等），则打印失败信息
      和详细的错误日志，方便排查问题。

5.  刷新 Python 路径缓存:
    - 在成功安装新库后，调用 `importlib.invalidate_caches()` 和 `site.main()`
      来强制 Python 重新加载其模块搜索路径。这确保了新安装的库可以被立即
      `import`，而无需重启 Maya。

[ 如何使用 ]
1.  将此脚本 (`installPackage.py`) 和一个包含所需库列表的 `requirements.txt`
    文件放在同一个目录下。
2.  在 Maya 的脚本编辑器中打开并执行此脚本，或者直接将此脚本文件拖拽到
    Maya 的视口中。
================================================================================
"""

import sys
import subprocess
from pathlib import Path


def install_requirements(requirements_file, executable_path=sys.executable):
    """# Runs the 'pip install -r' command to install packages."""
    command = [str(executable_path), "-m", "pip", "install", "-r", str(requirements_file)]

    print(f"{'':=^{120}}")
    print(f"Executing command: \n{' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,  # Will raise CalledProcessError on non-zero exit codes
            encoding="utf-8",
        )
        print(f"{' SUCCESS ':=^{120}}")
        print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print(f"{' ERROR ':=^{120}}")
        print(e.stderr)


def install_package():
    """Main execution function."""
    print("\n" * 4)
    print(f"{'':=^{120}}")
    print(f"{' Starting Installer ':=^{120}}")
    print(f"{'':=^{120}}")

    # Locate the requirements.txt file relative to this script
    try:
        script_path = Path(__file__).resolve()
        script_dir = script_path.parent
        requirements_file = script_dir / "requirements.txt"

        print(f"\nScriptPath: {script_dir}\n")

        if not requirements_file.is_file():
            print(f"{'':=^{120}}")
            print("ERROR: 'requirements.txt' not found in the script's directory.")
            print("Please ensure 'install.py' and 'requirements.txt' are in the same folder.")
            print(f"{'':=^{120}}")
            return

    except NameError:
        print(f"{'':=^{120}}")
        print("ERROR: Could not determine script path.")
        print("Please run this by dragging the .py file into the Maya viewport instead of copy-pasting.")
        print(f"{'':=^{120}}")
        return

    # Run the installation process
    if install_requirements(requirements_file, Path(sys.executable).parent / "mayapy.exe"):
        import site
        import importlib

        importlib.invalidate_caches()
        site.main()

        print("\n")
        print(f"{'':=^{120}}")
        print("SUCCESS All dependencies installed or up-to-date!")
        print(f"{'':=^{120}}")

    else:
        print("\n")
        print(f"{'':=^{120}}")
        print("ERROR: Some or all dependencies failed to install.")
        print(f"{'':=^{120}}")


if __name__ == "__main__":
    install_package()
