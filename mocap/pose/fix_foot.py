from maya import cmds
from maya.api import OpenMaya as om
import log

dict = {
    "l": {
        "ik": "IKLeg_L",
        "toe": "IKToesHandle_L",
        "heel": "RollHeel_L",
    },
    "r": {
        "ik": "IKLeg_R",
        "toe": "IKToesHandle_R",
        "heel": "RollHeel_R",
    },
}


def condition_left_right(ctrl: str):
    ctrl = ctrl.lower()
    if "l" in ctrl.split("_"):
        return "l"
    if "r" in ctrl.split("_"):
        return "r"


def get_select_time_range():
    start = int(cmds.playbackOptions(q=1, sst=1))
    end = int(cmds.playbackOptions(q=1, set=1))
    return start, end


def get_namespace(name_str: str):
    if ":" not in name_str:
        return ""
    namespace = ":".join(name_str.split(":")[0:-1])
    if namespace:
        namespace = f"{namespace}:"
    return namespace


def pin_foot(loc="heel"):
    try:
        ctrl = cmds.ls(sl=1)[0]
    except Exception:
        log.exception("请先选择一个控制器")
        return

    namespace = get_namespace(ctrl)
    side = condition_left_right(ctrl)
    if not side:
        return

    ik_ctrl = f"{namespace}{dict[side]['ik']}"
    loc_ctrl = f"{namespace}{dict[side][loc]}"

    start, end = get_select_time_range()
    loc_ws = om.MVector(list(om.MMatrix(cmds.getAttr(f"{loc_ctrl}.worldMatrix", t=start)))[12:15])
    for frame in range(start + 1, end + 1):
        cmds.currentTime(frame)
        ik_ws = om.MVector(list(om.MMatrix(cmds.getAttr(f"{loc_ctrl}.worldMatrix", t=frame)))[12:15])
        offset = loc_ws - ik_ws
        cmds.move(offset.x, offset.y, offset.z, ik_ctrl, r=1)


def pin_by_heel():
    pin_foot("heel")


def pin_by_toe():
    pin_foot("toe")
