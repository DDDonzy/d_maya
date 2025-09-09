from maya.api import OpenMaya as om
from maya import cmds, mel
from UTILS.transform import matrix_to_trs

# 选择clip，矫正方向和位置
pelvis = "MOCAP:pelvis"


clip = None
for x in cmds.ls(sl=1):
    if cmds.objectType(x,isa="timeEditorClip"):
        clip = x
        break
if not clip:
    raise RuntimeError ("Please Select clip")
    
start_time = cmds.getAttr(f"{clip}.clipStart")
end_time = start_time + cmds.getAttr(f"{clip}.clipDuration")


matrix_a = om.MMatrix(cmds.getAttr(f"{pelvis}.worldMatrix", t=start_time))
matrix_b = om.MMatrix(cmds.getAttr(f"{pelvis}.worldMatrix", t=end_time))
vector_a = om.MTransformationMatrix(matrix_a).translation(om.MSpace.kWorld)
vector_b = om.MTransformationMatrix(matrix_b).translation(om.MSpace.kWorld)
vector_a.y = 0
vector_b.y = 0
y = om.MVector([0, 1, 0])
x = (vector_b - vector_a).normal()
z = (x ^ y).normal()
matrix = [*x, 0, *y, 0, *z, 0, 0, 0, 0, 0]

mel.eval("teCreateRelocator(-1)")
loc = cmds.ls(sl=1)[0]
cmds.xform(loc, t=vector_a * -1, ws=1)


loc_ro = cmds.spaceLocator(name=loc.replace("Relocator", "Rerotate"))[0]
cmds.setAttr(f"{loc_ro}.localScale", 500, 500, 500)
cmds.setAttr(f"{loc_ro}.r", *matrix_to_trs(om.MMatrix(matrix))[3:6])
cmds.parentConstraint(loc_ro, loc, mo=1)
cmds.setAttr(f"{loc_ro}.r", 0, 0, 0)
cmds.parent(loc, loc_ro)
cmds.setAttr(f"{loc}.inheritsTransform", 0)
cmds.select(loc_ro)
cmds.refresh()
