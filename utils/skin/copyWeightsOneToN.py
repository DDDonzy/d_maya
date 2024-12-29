import maya.cmds as cmds


def copyWeightsOneToN(sour="", target=None):
    if sour == None or sour == "":
        sour = cmds.ls(sl=1)[0]
    if type(sour) == str:
        sour = sour
    if target == None or target == "":
        target = cmds.ls(sl=1)[1:]
    elif type(target) is not list:
        target = [target]
    influenceList = cmds.skinCluster(sour, q=1, inf=1)
    his = cmds.listHistory(sour, pdo=1, il=1)
    for node in his:
        if cmds.objectType(node) == 'skinCluster':
            ss = node
    newSkin_List = []
    skinningMethod = cmds.getAttr(ss+'.skinningMethod')
    for geo in target:
        ds = cmds.skinCluster(geo, influenceList, tsb=1)[0]
        cmds.setAttr(ds+".skinningMethod", skinningMethod)
        cmds.copySkinWeights(ss=ss, ds=ds, noMirror=1, surfaceAssociation="closestPoint",
                             influenceAssociation="closestJoint")
        newSkin_List.append(ds)
    return newSkin_List


if __name__ == "__main__":
    copyWeightsOneToN()
