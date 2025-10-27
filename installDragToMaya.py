"""
================================================================================
Maya Environment - One-Click Installer via Drag-and-Drop
================================================================================

[ 脚本目的 ]
该脚本是一个为 Maya 设计的“一键式”环境配置工具。它通过利用 Maya 的
`onMayaDroppedPythonFile` 拖拽执行特性，自动完成一系列复杂的设置任务，
包括安装第三方库、配置环境变量、设置启动脚本和安装自定义热键。

用户只需将此文件拖拽到 Maya 的视口中，即可完成所有配置。

[ 工作流程 ]
当该文件被拖拽到 Maya 视口时，`onMayaDroppedPythonFile` 函数会被触发，并
依次执行以下操作：

1.  安装第三方库:
    - 导入并调用 `installPackage.install_package()` 函数。
    - 该函数会读取项目根目录下的 `requirements.txt` 文件，并使用 `mayapy.exe`
      为 Maya 的 Python 环境批量安装所有必需的第三方库。

2.  修改 Maya.env 文件:
    - 调用 `modify_mayaEnvFile()` 函数。
    - 该函数会自动定位到当前 Maya 版本的 `Maya.env` 文件。
    - 向文件中添加一系列预设的环境变量（如 `MAYA_NO_HOME`），用于优化 Maya
      的启动行为和禁用不必要的功能。

3.  修改 userSetup.py 文件:
    - 调用 `modify_mayaUserSetup()` 函数。
    - 该函数会自动定位到当前 Maya 版本的 `scripts/userSetup.py` 文件。
    - 向文件中添加一段 Python 代码，该代码会在 Maya 每次启动时，自动将
      本项目的根目录添加到 `sys.path` 中。这确保了项目中的所有模块都
      可以被 Maya 正确导入。

4.  安装自定义热键:
    - 导入并调用 `_hotkey.d_hotkey.install_hotkey()` 函数。
    - 该函数会读取热键配置文件，并在 Maya 中创建或更新用户的自定义热键设置。

5.  热重载模块:
    - 调用 `reloadALL()` 函数。
    - 该函数会智能地查找并重新加载所有属于本项目的、已经导入到 Maya 内存中
      的模块。这确保了所有的修改和新安装的库都能立即生效，而无需重启 Maya。

6.  显示完成信息:
    - 在 Maya 视口的底部中央显示一条 "Setup Done" 的提示信息，告知用户
      安装过程已成功完成。

[ 如何使用 ]
1.  确保此文件与 `installPackage.py`, `requirements.txt`, `_hotkey` 目录等
    位于正确的项目结构中。
2.  打开 Maya。
3.  将 `installDragToMaya.py` 这个文件直接从文件浏览器拖拽到 Maya 的视口中。
4.  等待视口下方出现 "Setup Done" 提示。

================================================================================
"""

import os
import sys
from importlib import reload
from maya import cmds, mel

# path = r"E:\\d_maya"
path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.append(path)


ENV_LIB = {
    "MAYA_NO_HOME": 1,
    "MAYA_NO_HOME_ICON": 1,
    "MAYA_SKIP_BLOCK_CHECK": 1,
    "MAYA_NO_WARNING_FOR_MISSING_DEFAULT_RENDERER": 1,
}


def reloadALL(path=path):
    """Reload all modules in the specified path."""
    reload_list = []
    for modules_name in sys.modules:
        try:
            modules_path = sys.modules[modules_name].__file__
            common_path = os.path.commonpath([path, modules_path])
        except:  # noqa: E722
            continue
        if os.path.samefile(path, common_path):
            reload_list.append(sys.modules[modules_name])
    for x in reload_list:
        reload(x)
        print(f"Reload: {x}")


def get_mayaEnvFile():
    """Get .env file path"""
    maya_env_file = "Maya.env"
    env_path = mel.eval('getenv "MAYA_APP_DIR"')
    maya_version = cmds.about(v=1)
    env_path = os.path.join(env_path, maya_version, maya_env_file)
    env_path = os.path.normpath(env_path)
    return env_path


def modify_mayaEnvFile():
    """Add path to maya usersetup.py"""
    env_file = get_mayaEnvFile()
    try:
        with open(env_file, "a+") as file:
            file.seek(0)
            content = file.read()
            for key, value in ENV_LIB.items():
                if key not in content:
                    additional_text = f"\n{key} = {value};"
                    file.write(additional_text)

        print(f"Modify: {env_file}")
    except Exception as e:
        print(e)


def modify_mayaUserSetup():
    """Add some env set"""
    this_path = os.path.dirname(__file__)
    user_setup_file = "usersetup.py"
    userSetup_path = mel.eval('getenv "MAYA_APP_DIR"')
    maya_version = cmds.about(v=1)
    userSetup_path = os.path.join(userSetup_path, maya_version, "scripts", user_setup_file)
    userSetup_path = os.path.normpath(userSetup_path)

    try:
        with open(userSetup_path, "a+") as file:
            file.seek(0)
            content = file.read()
            additional_text = f"\nimport sys\nif r'{this_path}' not in sys.path:\n    sys.path.append(r'{this_path}')"
            if additional_text not in content:
                file.write(additional_text)
                print(f"Modify: {userSetup_path}")
    except Exception as e:
        print(e)


def show_message(msg):
    message = f"<hl> {msg} </hl>"
    cmds.inViewMessage(amg=message, pos="botCenter", fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)


def onMayaDroppedPythonFile(*args, **kwargs):
    """Dropped to maya functions"""
    import installPackage  # noqa: E402

    installPackage.install_package()

    modify_mayaEnvFile()
    modify_mayaUserSetup()

    from _hotkey.d_hotkey import install_hotkey  # noqa: E402

    install_hotkey()

    reloadALL(path)
    show_message("Setup Done")
