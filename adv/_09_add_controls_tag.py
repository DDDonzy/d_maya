from maya import cmds
from m_utils.dag.iterHierarchy import IterHierarchy
from m_utils.control.controllerTag import create_controllerTag

rig_group = r"MotionSystem"


def isController(obj):
    for shape in cmds.listRelatives(obj, s=1) or []:
        if cmds.objectType(shape, isa="nurbsCurve"):
            return True
    return False


controls_list = []
for obj, dag in IterHierarchy(rig_group):
    # 排除 骨骼 以及 非变换节点
    if cmds.objectType(obj, isAType="joint") or not cmds.objectType(obj, isAType="transform"):
        continue
    # 如果是 控制器 则锁定指定属性
    elif isController(obj):
        controls_list.append(obj)

create_controllerTag(controls_list)
