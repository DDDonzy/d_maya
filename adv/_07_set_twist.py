from maya import cmds
for x in ['Hip_L', 'Hip_R', 'Shoulder_L', 'Shoulder_R']:
    cmds.setAttr(f"{x}.twistAmount", 1)