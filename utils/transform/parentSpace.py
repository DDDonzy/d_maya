from maya import cmds
from maya.api import OpenMaya as om


def get_spaceBox(object):
    return cmds.listConnections(f"{object}.parentSpace_node", s=1, d=0)[0]


def get_blendMatrix(object):
    return cmds.listConnections(f"{object}.blendMatrix_node", s=1, d=0)[0]


def create_spaceBox(object):
    asset_box = cmds.container(type="dagContainer", name=f"{object}_spaceBox")
    cmds.parent(asset_box, object)
    node_bw = cmds.createNode("blendMatrix", name=f"{object}_spaceBW")
    cmds.setAttr(f"{node_bw}.isHistoricallyInteresting",0)
    cmds.addAttr(object, ln="parentSpace_node", at="message")
    cmds.addAttr(asset_box, ln="blendMatrix_node", at="message")
    cmds.connectAttr(f"{asset_box}.message",
                     f"{object}.parentSpace_node")
    cmds.connectAttr(f"{node_bw}.message",
                     f"{asset_box}.blendMatrix_node")
    node_multMatrix = cmds.createNode("multMatrix", name=f"{object}_spaceLocalMultMatrix")
    cmds.setAttr(f"{node_multMatrix}.isHistoricallyInteresting",0)
    p_list = cmds.listRelatives(object, p=1)
    if p_list:
        p = p_list[0]
        cmds.connectAttr(f"{p}.worldMatrix[0]",
                         f"{node_bw}.inputMatrix")
        cmds.connectAttr(f"{p}.worldInverseMatrix[0]",
                         f"{node_multMatrix}.matrixIn[1]")

    cmds.connectAttr(f"{node_bw}.outputMatrix",
                     f"{node_multMatrix}.matrixIn[0]")
    cmds.connectAttr(f"{node_multMatrix}.matrixSum",
                     f"{object}.offsetParentMatrix")

    cmds.container(asset_box, e=1, addNode=[node_bw, node_multMatrix])
    cmds.addAttr(asset_box, ln="parentSpace", at="enum", en="Parent", k=1)
    cmds.addAttr(object, ln="parentSpace", pxy=f"{asset_box}.parentSpace", k=1)
    return node_bw


def parentSpace(object: str,
                parent: str,
                nice_name: str,
                translate=True,
                rotate=True,
                scale=True,
                shear=True):

    if not cmds.objExists(f"{object}.parentSpace_node"):
        asset_box = create_spaceBox(object)

    asset_box = get_spaceBox(object)
    node_bw = get_blendMatrix(asset_box)

    enum_str = cmds.addAttr(f"{asset_box}.parentSpace", q=1, en=1)
    nice_name_list = enum_str.split(":")
    nice_name_list.append(nice_name)
    enum_str = ":".join(nice_name_list)
    parent_indices = len(nice_name_list)-1

    cmds.addAttr(f"{asset_box}.parentSpace", e=1, en=enum_str)
    cmds.addAttr(f"{object}.parentSpace", e=1, en=enum_str)

    object_worldMatrix = om.MMatrix(cmds.getAttr(f"{object}.worldMatrix[0]"))
    parent_worldMatrix = om.MMatrix(cmds.getAttr(f"{parent}.worldMatrix[0]"))
    offset_matrix = object_worldMatrix * parent_worldMatrix.inverse()
    offset_matrix_attr_name = f"offsetMatrix_{parent_indices}"
    cmds.addAttr(asset_box, ln=offset_matrix_attr_name, at="matrix")
    cmds.setAttr(f"{asset_box}.{offset_matrix_attr_name}", offset_matrix, type="matrix", l=1)

    node_multMatrix = cmds.createNode("multMatrix", name=f"{parent}_{object}_multMatrix")
    cmds.setAttr(f"{node_multMatrix}.isHistoricallyInteresting",0)
    cmds.connectAttr(f"{asset_box}.{offset_matrix_attr_name}",
                     f"{node_multMatrix}.matrixIn[0]")
    cmds.connectAttr(f"{parent}.worldMatrix[0]",
                     f"{node_multMatrix}.matrixIn[1]")
    cmds.connectAttr(f'{node_multMatrix}.matrixSum',
                     f"{node_bw}.target[{parent_indices}].targetMatrix")
    if cmds.about(api=True)>=20230000:
        status = [translate,rotate,scale,shear]
        for i,attr in enumerate(["translateWeight","rotateWeight","scaleWeight","shearWeight"]):
            cmds.addAttr(asset_box,ln=f"{attr}_{parent_indices}",at="double",min=0,max=1,k=1,dv=float(status[i]))
            cmds.connectAttr(f"{asset_box}.{attr}_{parent_indices}",
                             f"{node_bw}.target[{parent_indices}].{attr}", f=1)
    else:
        status = [translate,rotate,scale,shear]
        for i,attr in enumerate(["useTranslate","useRotate","useScale","useShear"]):
            cmds.addAttr(asset_box,ln=f"{attr}_{parent_indices}",at="bool",min=0,max=1,k=1,dv=status[i])
            cmds.connectAttr(f"{asset_box}.{attr}_{parent_indices}",
                             f"{node_bw}.target[{parent_indices}].{attr}", f=1)

    # sdk
    cmds.setDrivenKeyframe(f"{node_bw}.target[{parent_indices}].weight",
                           cd=f"{asset_box}.parentSpace",
                           dv=parent_indices - 1, v=0)
    cmds.setDrivenKeyframe(f"{node_bw}.target[{parent_indices}].weight",
                           cd=f"{asset_box}.parentSpace",
                           dv=parent_indices, v=1)
    cmds.setDrivenKeyframe(f"{node_bw}.target[{parent_indices}].weight",
                           cd=f"{asset_box}.parentSpace",
                           dv=parent_indices + 1, v=0)

    node_sdk = cmds.listConnections(f"{node_bw}.target[{parent_indices}].weight", s=1, d=0)
    cmds.container(asset_box, e=1, addNode=[node_multMatrix]+node_sdk)


def parentSpace_cmd(nice_name="",
                    translate=True,
                    rotate=True,
                    scale=True,
                    shear=True):
    sel = cmds.ls(sl=1)
    if not nice_name:
        nice_name = sel[1]
    parentSpace(object=sel[1], parent=sel[0], nice_name=nice_name,translate=translate,rotate=rotate,scale=scale,shear=shear)


# parentSpace_cmd()
