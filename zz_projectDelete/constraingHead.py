from maya import cmds
import UTILS.transform as transform

bodyHead = "Head_J"
target = "hair:Head_J_GRP"


headMatrix = transform.get_worldMatrix(bodyHead)
targetMatrix = transform.get_worldMatrix(target)
node_bm = cmds.createNode("blendMatrix")
cmds.connectAttr(f"{bodyHead}.worldMatrix", f"{node_bm}.inputMatrix")
cmds.setAttr(f"{node_bm}.target[0].targetMatrix", targetMatrix, type="matrix")
cmds.connectAttr(f"{node_bm}.outputMatrix", f"{target}.offsetParentMatrix")

transform.set_trs(target, [0, 0, 0, 0, 0, 0, 1, 1, 1])
cmds.addAttr(target,ln="lockToWorld",at="bool",k=1,dv=0)
cmds.setAttr(f"{target}.lockToWorld", k=0, cb=1)
cmds.connectAttr(f"{target}.lockToWorld", f"{node_bm}.target[0].weight", f=1)