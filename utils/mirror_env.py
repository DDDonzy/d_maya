# Author:   Donzy.xu
# CreateTime:   2022/6/22 - 5:05
# FileName:  mirror_env

import maya.cmds as cmds


def set_string_operation():
    global mirror_dict
    global mirror_clickCount
    if mirror_clickCount % 2 == 0:
        left_string = "_L"
        right_string = "_R"
        mirror_dict = {"L": left_string,
                       "R": right_string}
        message = '<hl> %s <----> %s </hl>' % (left_string, right_string)
        cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)
    elif mirror_clickCount % 2 == 1:
        left_string = "L_"
        right_string = "R_"
        mirror_dict = {"L": left_string,
                       "R": right_string}
        message = '<hl> %s <----> %s </hl>' % (left_string, right_string)
        cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)
    mirror_clickCount += 1
    return mirror_dict


def get_oppositeString(input_string):
    if mirror_dict["L"] in input_string:
        return input_string.replace(mirror_dict["L"], mirror_dict["R"])
    if mirror_dict["R"] in input_string:
        return input_string.replace(mirror_dict["R"], mirror_dict["L"])


try:
    set_string_operation()
except Exception:
    mirror_dict = {}
    mirror_clickCount = 0
    set_string_operation()