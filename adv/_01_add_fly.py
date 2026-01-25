import m_utils.transform as t
from maya import cmds

fly_ref_pos = "RootX_M"
main = "Main"
main = cmds.rename(main, main + "Base")
new_main = cmds.createNode("transform", name="Main", parent="MainSystem")
fly_offset = cmds.createNode("transform", name="FlyOffset", parent=new_main)
fly = cmds.createNode("transform", name="Fly", parent=fly_offset)
cmds.createNode("nurbsCurve", name="FlyShape", parent=fly, skipSelect=True)
t.set_worldMatrix(fly_offset, t.get_worldMatrix(fly_ref_pos))
main_offset = cmds.createNode("transform", name="MainOffset", parent="Fly")
t.set_worldMatrix(main_offset, t.get_worldMatrix(main))
cmds.parent(main, main_offset)

for x in cmds.listAttr(main, ud=1, cb=1):
    at = cmds.addAttr(f"{main}.{x}", q=1, at=1)
    cmds.getAttr(f"{main}.{x}", l=1)
    cmds.addAttr(new_main, ln=x, at=at, pxy=f"{main}.{x}", k=cmds.getAttr(f"{main}.{x}", k=1))
    cmds.setAttr(f"{new_main}.{x}", cb=cmds.getAttr(f"{main}.{x}", cb=1))
    cmds.setAttr(f"{new_main}.{x}", l=cmds.getAttr(f"{main}.{x}", l=1))
for x in cmds.listRelatives(main, s=1):
    cmds.parent(x, new_main, r=1, s=1)
    cmds.rename(x, f"{new_main}Shape")
