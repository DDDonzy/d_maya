from maya import cmds


def connect_to_sdk_cmd():
    bsNode = cmds.ls(sl=1)[0]
    for x in cmds.channelBox("mainChannelBox", q=1, sma=1):
        attr = f"{bsNode}.{x}"
        sour = cmds.listConnections(attr, p=1, s=1, d=0)[0]
        cmds.disconnectAttr(sour, attr)
        cmds.setDrivenKeyframe(attr, cd=sour, dv=0, v=0, inTangentType="linear", outTangentType="linear")
        cmds.setDrivenKeyframe(attr, cd=sour, dv=1, v=1, inTangentType="linear", outTangentType="linear")
        animCurve = cmds.listConnections(attr, s=1, d=0)[0]
        cmds.setAttr(f"{animCurve}.preInfinity", 4)
        cmds.setAttr(f"{animCurve}.postInfinity", 4)

if __name__ == "__main__":
    connect_to_sdk_cmd()
