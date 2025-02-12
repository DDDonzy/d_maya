from __future__ import print_function
import os
import sys
from maya import cmds, mel
from imp import reload

# path = r"E:\\d_maya"
path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.append(path)

ENV_LIB = {
    "MAYA_NO_HOME": 1,
    "MAYA_NO_HOME_ICON": 1,
    "MAYA_SKIP_BLOCK_CHECK": 1
}


def reloadALL(path=path):
    """Reload all modules in the specified path."""
    reload_list = []
    for modules_name in sys.modules:
        try:
            modules_path = sys.modules[modules_name].__file__
            common_path = os.path.commonpath([path, modules_path])
        except:
            continue
        if os.path.samefile(path, common_path):
            reload_list.append(sys.modules[modules_name])
    for x in reload_list:
        reload(x)
        print("Reload: {}".format(x))


def get_mayaEnvFile():
    """Get .env file path"""
    maya_env_file = "Maya.env"
    env_path = mel.eval('getenv "MAYA_APP_DIR"')
    maya_version = cmds.about(v=1)
    env_path = os.path.join(env_path, maya_version, maya_env_file)
    env_path = os.path.normpath(env_path)
    return env_path


def modify_mayaEnvFile():
    """Add path to maya usersetup.py """
    env_file = get_mayaEnvFile()
    try:
        with open(env_file, 'r') as file:
            content = file.read()
    except:
        content = ""

    with open(env_file, 'a') as file:
        for key, value in ENV_LIB.items():
            if key in content:
                continue
            additional_text = "\n{} = {};".format(key, value)
            file.write(additional_text)
    print("Modify: {}".format(env_file))


def modify_mayaUserSetup():
    """Add some env set"""
    this_path = os.path.dirname(__file__)
    user_setup_file = "usersetup.py"
    userSetup_path = mel.eval('getenv "MAYA_APP_DIR"')
    maya_version = cmds.about(v=1)
    userSetup_path = os.path.join(userSetup_path, maya_version, "scripts", user_setup_file)
    userSetup_path = os.path.normpath(userSetup_path)
    try:
        with open(userSetup_path, 'r') as file:
            content = file.read()
    except:
        content = ""

    with open(userSetup_path, 'a') as file:
        additional_text = "\nimport sys\nif r'{}' not in sys.path:\n    sys.path.append(r'{}')".format(this_path, this_path)
        if additional_text in content:
            return
        file.write(additional_text)
        print("Modify: {}".format(userSetup_path))


def show_message(msg):
    message = "<hl> {} </hl>".format(msg)
    cmds.inViewMessage(amg=message, pos='botCenter', fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)


def onMayaDroppedPythonFile(*args, **kwargs):
    """Dropped to maya functions"""
    modify_mayaEnvFile()
    modify_mayaUserSetup()
    reloadALL(path)
    show_message("Setup Done")
