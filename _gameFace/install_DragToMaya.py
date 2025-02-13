from __future__ import print_function
import os
import sys
from maya import cmds, mel

path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.append(path)


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
    modify_mayaUserSetup()
    import face.main
    face.main.show_UI()
    show_message("Setup Done")
