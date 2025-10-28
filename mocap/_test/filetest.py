from mocap.mayapy import init_maya

from mocap.suppress_maya_logs import suppress_maya_logs
from maya import cmds

init_maya()


with suppress_maya_logs():
    cmds.file("N:\SourceAssets\Characters\Hero\Mocap\M_Blade_Stand_Turn.ma", o=1, f=1, resetError=False)
print("打开文件完成")
print(cmds.ls())
cmds.file(new=1, f=1)
