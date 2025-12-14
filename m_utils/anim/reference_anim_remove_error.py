import maya.cmds as cmds


def removeDisConnectAttr(refNode):
    targetCommand = "disconnectAttr"
    refEdits = cmds.referenceQuery(refNode, editStrings=True, editCommand=targetCommand)  # 查询 disconnectAttr 的编辑字符串
    nodeName = cmds.referenceQuery(refNode, en=True, editCommand=targetCommand)  # 查询 disconnectAttr 引用节点的名称
    sk_nodeList = set()
    for x in nodeName:
        if cmds.objExists(x) and cmds.objectType(x) == "skinCluster":
            sk_nodeList.add(x)

    editList = []
    for x in refEdits:
        for sk in sk_nodeList:
            if sk in x:
                editList.append(x)

    for line in editList:
        strings = line.replace("\"", "").split(" ")
        destination = strings[2]
        cmds.referenceEdit(destination, removeEdits=True, failedEdits=True, successfulEdits=True, editCommand=targetCommand)
        print("remove disconnectAttr: ", destination)


def removeSetAttr(refNode):
    targetCommand = "setAttr"
    refEdits = cmds.referenceQuery(refNode, editStrings=True, editCommand=targetCommand)
    nodeName = cmds.referenceQuery(refNode, en=True, editCommand=targetCommand)
    sk_nodeList = set()
    for x in nodeName:
        if cmds.objExists(x) and cmds.objectType(x) == "skinCluster":
            sk_nodeList.add(x)

    editList = []
    for x in refEdits:
        for sk in sk_nodeList:
            if sk in x:
                editList.append(x)

    for line in editList:
        strings = line.replace("\"", "").split(" ")
        source = strings[1]
        cmds.referenceEdit(source, removeEdits=True, failedEdits=True, successfulEdits=True, editCommand=targetCommand)
        print("remove setAttr: ", source)


referenceList = cmds.ls(type="reference")
for ref in referenceList:
    try:
        removeDisConnectAttr(ref)
    except:
        pass
    try:
        removeSetAttr(ref)
    except:
        pass
