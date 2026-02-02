import json
from pathlib import Path
from maya import cmds
from m_utils.dag.getHistory import get_history

MAYA_TEMP_DIR = Path.home() / "AppData" / "Local" / "Temp" / "maya_cache"
MAYA_TEMP_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = MAYA_TEMP_DIR / "maya_skin_influences.json"


def _save_influences(influences):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(influences, f)
    except Exception as e:
        print(f"Save failed: {e}")


def _load_influences():
    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Load failed: {e}")
    return []


def get_skinJoint(obj_list=None):
    if type(obj_list) is str:
        obj_list = [obj_list]
    skin_joint_list = []
    for obj in obj_list:
        if not cmds.objExists(obj):
            continue

        history_list = get_history(obj, "skinCluster")
        if not history_list:
            skin_joint_list.extend([])
            continue

        for his in history_list:
            skin_joint_list.extend(cmds.skinCluster(his, q=1, inf=1))
    seen = set()
    skin_joint_list = [x for x in skin_joint_list if not (x in seen or seen.add(x))]
    return skin_joint_list


def get_skinJoint_cmd(createSet=False):
    obj_list = cmds.ls(sl=1)
    skin_joint_list = get_skinJoint(obj_list)
    if createSet and skin_joint_list:
        cmds.sets(skin_joint_list, n="skinJointSet")
    cmds.select(skin_joint_list)
    _save_influences(skin_joint_list)
    return skin_joint_list


def select_laster_influences_cmd():
    influences = _load_influences()
    if influences:
        cmds.select(influences)
    return influences


if __name__ == "__main__":
    get_skinJoint_cmd(True)
