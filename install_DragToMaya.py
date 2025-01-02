import os
import sys
from importlib import reload
from maya import cmds, mel

ENV_LIB = {
    "MAYA_NO_HOME": 1,
    "MAYA_NO_HOME_ICON": 1,
    "MAYA_SKIP_BLOCK_CHECK": 1
}

THIS_Path = os.path.dirname(__file__)

path = r"E:/d_maya"
if path not in sys.path:
    sys.path.append(path)


def reload_modules_in_path(path):
    reload_list = []
    for modules_name in sys.modules:
        try:
            modules_path = sys.modules[modules_name].__file__
            common_path = os.path.commonpath([path, modules_path])
            if os.path.samefile(path, common_path):
                reload_list.append(sys.modules[modules_name])
        except:
            pass
    for x in reload_list:
        reload(x)
        print(f"Reload: {x}")


def get_mayaEnvFile():
    maya_env_file = "Maya.env"
    env_path = mel.eval('getenv "MAYA_APP_DIR"')
    maya_version = cmds.about(v=1)
    env_path = os.path.join(env_path, maya_version, maya_env_file)
    env_path = os.path.normpath(env_path)
    return env_path


def modify_mayaEnvFile():
    with open(get_mayaEnvFile(), 'w') as file:
        pass

    with open(get_mayaEnvFile(), 'r') as file:
        content = file.read()

    with open(get_mayaEnvFile(), 'a') as file:
        for key, value in ENV_LIB.items():
            if key in content:
                continue
            additional_text = f"\n{key} = {value};"
            file.write(additional_text)


def modify_mayaUserSetup():
    user_setup_file = "usersetup.py"
    userSetup_path = mel.eval('getenv "MAYA_APP_DIR"')
    maya_version = cmds.about(v=1)
    userSetup_path = os.path.join(userSetup_path, maya_version, "scripts", user_setup_file)
    userSetup_path = os.path.normpath(userSetup_path)

    with open(userSetup_path, 'w') as file:
        pass

    with open(userSetup_path, 'r') as file:
        content = file.read()

    with open(userSetup_path, 'a') as file:
        additional_text = f"\nimport sys\nif r'{THIS_Path}' not in sys.path:\n    sys.path.append(r'{THIS_Path}')"
        if additional_text in content:
            return
        file.write(additional_text)
        print(f"Modify: {userSetup_path}")


def show_message(msg):
    message = f"<hl> {msg} </hl>"
    cmds.inViewMessage(amg=message, pos='botCenter', fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)


# reload_modules_in_path(path)
modify_mayaEnvFile()
modify_mayaUserSetup()
show_message("Setup Done")
