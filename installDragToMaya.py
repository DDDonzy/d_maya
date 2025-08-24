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
