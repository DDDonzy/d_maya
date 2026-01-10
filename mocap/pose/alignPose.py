import m_utils.transform as transform
import maya.cmds as cmds
import functools
import log

root = "FKRootGround_M"
move_controls = ["IKLeg_R", "IKLeg_L", "RootX_M", "IKArm_L", "IKArm_R", "PoleArm_R", "PoleArm_L", "PoleLeg_R", "PoleLeg_L"]

offset_matrix = []
func_list = []


def copyPose():
    try:
        namespace = cmds.ls(sl=1)[-1].split(":")[0]
    except Exception:
        log.error("请选择Root控制器")
        return

    root_matrix = transform.get_worldMatrix(f"{namespace}:{root}")
    offset_matrix.clear()
    func_list.clear()
    for x in move_controls:
        offset_matrix.append(transform.get_relativesMatrix(transform.get_worldMatrix(f"{namespace}:{x}"), root_matrix))
        func_list.append(functools.partial(transform.set_worldMatrix, f"{namespace}:{x}"))


def pastePose():
    try:
        namespace = cmds.ls(sl=1)[-1].split(":")[0]
    except Exception:
        log.error("请选择Root控制器")
        return

    root_matrix = transform.get_worldMatrix(f"{namespace}:{root}")
    for i, func in enumerate(func_list):
        func(offset_matrix[i] * root_matrix)
