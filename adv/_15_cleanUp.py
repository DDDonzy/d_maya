from maya import cmds

cmds.delete([x for x in cmds.ls(type="displayLayer") if x != "defaultLayer"])
char = cmds.createNode("transform", name="Character")
rig = cmds.createNode("transform", name="Rig_Group", parent=char)
mesh = cmds.createNode("transform", name="Meshes_Group", parent=char)

bones = cmds.listRelatives("joints_grp", c=1)
cmds.parent("headRig_grp", rig)
cmds.parent("body_grp", mesh)
cmds.parent("head_grp", mesh)
cmds.parent(bones, w=1)
cmds.parent("RIG_ASSET", rig)
cmds.parent("Group", rig)
cmds.parent("CAM:CAMERA", rig)
cmds.delete("rig")


# display layer
cmds.select(rig)
cmds.createDisplayLayer(name="Rig", nr=1)

cmds.select(bones)
cmds.createDisplayLayer(name="Bones", nr=1)

cmds.select("body_grp", "head_grp")
cmds.createDisplayLayer(name="Meshes_Body", nr=1)
