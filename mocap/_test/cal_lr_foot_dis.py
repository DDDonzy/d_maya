from maya.api import OpenMaya as om
from maya import cmds


r_foot = "RIG:IKLeg_R"
l_foot = "RIG:IKLeg_L"

current_time = cmds.currentTime(q=1)
time_range = range(int(current_time - 5), int(current_time + 5))
min_distance = 0.0
min_distance_time = None
for t in time_range:
    matrix_a = om.MMatrix(cmds.getAttr(f"{l_foot}.worldMatrix", t=t))
    matrix_b = om.MMatrix(cmds.getAttr(f"{r_foot}.worldMatrix", t=t))
    vector_a = om.MTransformationMatrix(matrix_a).translation(om.MSpace.kWorld)
    vector_b = om.MTransformationMatrix(matrix_b).translation(om.MSpace.kWorld)
    dis = (vector_a - vector_b).length()
    if min_distance == 0.0 or dis < min_distance:
        min_distance = dis
        min_distance_time = t
cmds.currentTime(min_distance_time)
