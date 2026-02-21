"""
查找前后5帧内，pelvis 最低帧
"""

from maya import cmds

pelvis = cmds.ls("pelvis", r=1)
if pelvis:
    pelvis = pelvis[0]
else:
    raise RuntimeError("'pelvis' not found")

current_time = cmds.currentTime(q=1)
time_range = range(int(current_time - 5), int(current_time + 5))
min = 0.0
min_time = None
for t in time_range:
    dis = cmds.getAttr(f"{pelvis}.worldMatrix", t=t)[13]
    if min == 0.0 or dis < min:
        min = dis
        min_time = t
cmds.currentTime(min_time)
