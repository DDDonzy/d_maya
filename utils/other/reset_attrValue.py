from maya import cmds

def reset_value(obj, transform=True, userDefined=True):
    if transform:
        for t in "trs":
            v = 0
            if t == "s":
                v = 1
            for a in "xyz":
                try:
                    cmds.setAttr(f"{obj}.{t}{a}", v)
                except:
                    print(f"{obj}.{t}{a} ---> can't reset")
    if userDefined:
        user_defined = cmds.listAttr(obj, ud=1, u=1)
        if user_defined is not None:
            for x in user_defined:
                x = f"{obj}.{x}"
                v = cmds.addAttr(x, q=1, dv=1)
                if v is not None:
                    try:
                        cmds.setAttr(x, v)
                    except:
                        print(f"{x} ---> can't reset")


if __name__ == "__main__":
    obj_list = cmds.ls(sl=1)
    for obj in obj_list:
        reset_value(obj=obj, transform=True, userDefined=True)
