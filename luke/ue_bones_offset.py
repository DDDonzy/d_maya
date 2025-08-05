from maya import cmds

ue_offset = {}
for x in cmds.ls(sl=1):
    matrix = [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    ue_offset.update(
        {
            x: {
                "driver": "",
                "driven": x,
                "offsetMatrix": matrix,
            }
        },
    )
