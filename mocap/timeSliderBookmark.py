from maya import cmds


def timeSliderBookmark(name, time, color):
    # name = "idle"
    # time = (10,50)
    # color = (0.5,0.5,0.5)
    bookmark = cmds.createNode("timeSliderBookmark", name=f"timeSliderBookmark_{name}")
    cmds.setAttr(f"{bookmark}.name", name, type="string")
    cmds.setAttr(f"{bookmark}.color", *color)
    cmds.setAttr(f"{bookmark}.timeRangeStart", time[0])
    cmds.setAttr(f"{bookmark}.timeRangeStop", time[1])
