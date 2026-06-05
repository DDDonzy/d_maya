from maya import cmds

transform_list = ["FKSystem", "IKSystem", "FKIKSystem", "BendSystem", "AimSystem", "RootSystem", "TwistSystem", "GlobalSystem", "ConstraintSystem", "DynamicSystem", "DrivingSystem", "MicroSystem", "buildPose"]
for x in transform_list:
    try:
        cmds.setAttr(f"{x}.inheritsTransform", l=0)
        cmds.setAttr(f"{x}.inheritsTransform", 0)
        cmds.parent(x, "Main")
    except:
        pass
