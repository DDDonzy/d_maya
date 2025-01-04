from maya import cmds
from maya.api import OpenMaya as om
from utils.generate_unique_name import generate_unique_name
from utils.create_assets import create_assets
from utils.transform.transform import get_local_matrix, get_offset_matrix, get_world_matrix


def parentspaceConstraint(control_obj: str,
                          target_obj: str,
                          nice_name: str = None,
                          translate=True,
                          rotate=True,
                          scale=True,
                          shear=True):
    parentspace_attrName = "parentSpace"

    def _parentspace_constraint_pre(target_obj):
        # assets box
        assets_name = generate_unique_name(f"{target_obj}_parentspace")
        all_parentspace_assets = create_assets("parentspaceAssets", parent_assets=create_assets("RigAssets"))
        parentspace_assets = create_assets(assets_name, parent_assets=all_parentspace_assets)

        node_bw = cmds.createNode("blendMatrix", name=f"{target_obj}_spaceBW")
        node_getLocalMatrix = cmds.createNode("multMatrix", name=f"{target_obj}_getLocalMatrix")
        node_decMatrix = cmds.createNode("decomposeMatrix", name=f"{target_obj}_decomposeMatrix")
        node_parentMult = cmds.createNode("multMatrix", name=f"{target_obj}_parentMult")
        # parent connect
        cmds.setAttr(f"{node_parentMult}.matrixIn[0]",
                     get_local_matrix(target_obj),
                     type="matrix")
        cmds.connectAttr(f"{target_obj}.parentMatrix[0]",
                         f"{node_parentMult}.matrixIn[1]")
        cmds.connectAttr(f"{node_parentMult}.matrixSum",
                         f"{node_bw}.inputMatrix")
        # blend world matrix to local matrix
        cmds.connectAttr(f"{node_bw}.outputMatrix",
                         f"{node_getLocalMatrix}.matrixIn[0]")
        cmds.connectAttr(f"{target_obj}.parentInverseMatrix[0]",
                         f"{node_getLocalMatrix}.matrixIn[1]")
        cmds.connectAttr(f"{node_getLocalMatrix}.matrixSum",
                         f"{node_decMatrix}.inputMatrix")
        # decomposeMatrix
        cmds.connectAttr(f"{target_obj}.rotateOrder",
                         f"{node_decMatrix}.inputRotateOrder")
        cmds.connectAttr(f"{node_decMatrix}.outputTranslate",
                         f"{target_obj}.translate")
        cmds.connectAttr(f"{node_decMatrix}.outputRotate",
                         f"{target_obj}.rotate")
        cmds.connectAttr(f"{node_decMatrix}.outputScale",
                         f"{target_obj}.scale")
        cmds.connectAttr(f"{node_decMatrix}.outputShear",
                         f"{target_obj}.shear")
        cmds.connectAttr(f"{node_decMatrix}.outputQuat",
                         f"{target_obj}.rotateQuaternion")

        # assets
        cmds.container(parentspace_assets, e=1, addNode=[node_bw, node_getLocalMatrix, node_decMatrix, node_parentMult])
        cmds.container(parentspace_assets, e=1, publishName='inputBlendTarget')
        cmds.container(parentspace_assets, e=1, bindAttr=[f"{node_bw}.target", 'inputBlendTarget'])
        cmds.addAttr(parentspace_assets, ln=parentspace_attrName, at="enum", en="Parent", k=1)
        cmds.addAttr(parentspace_assets, ln=name_info, at="message")
        # add message info to obj
        if not cmds.objExists(f"{target_obj}.{name_info}"):
            cmds.addAttr(target_obj, ln=name_info, at="message")
        cmds.connectAttr(f"{parentspace_assets}.{name_info}",
                         f"{target_obj}.{name_info}")
        # add parentspace attr to obj
        if not cmds.objExists(f"{target_obj}.{parentspace_attrName}"):
            cmds.addAttr(target_obj, ln=parentspace_attrName, pxy=f"{parentspace_assets}.{parentspace_attrName}", k=1)
        else:
            cmds.addAttr(f"{target_obj}.{parentspace_attrName}", e=1, en="Parent", k=1)

        return parentspace_assets

    name_info = "parentspaceConstraint"
    # get parentspace assets
    if not cmds.objExists(f"{target_obj}.{name_info}"):
        parentspace_assets = _parentspace_constraint_pre(target_obj)
    else:
        parentspace_assets = cmds.listConnections(f"{target_obj}.{name_info}", s=1, d=0)[0]
    # nice name enum
    if not nice_name:
        nice_name = control_obj
    enum_str = cmds.addAttr(f"{parentspace_assets}.{parentspace_attrName}", q=1, en=1)
    nice_name_list = enum_str.split(":")
    nice_name_list.append(nice_name)
    enum_str = ":".join(nice_name_list)
    parent_indices = len(nice_name_list)-1
    # update parentspace enum
    cmds.addAttr(f"{parentspace_assets}.{parentspace_attrName}", e=1, en=enum_str)
    cmds.addAttr(f"{target_obj}.{parentspace_attrName}", e=1, en=enum_str)
    # get node blendMatrix
    bind_attr_list = cmds.container(parentspace_assets, q=1, bindAttr=1)
    node_bw_target_attr = bind_attr_list[bind_attr_list.index("inputBlendTarget")-1]
    # control_obj constraint target_obj
    offset_matrix = get_offset_matrix(get_world_matrix(target_obj),
                                      get_world_matrix(control_obj))
    node_multMatrix = cmds.createNode("multMatrix", name=f"{control_obj}_{target_obj}_multMatrix")
    cmds.setAttr(f"{node_multMatrix}.matrixIn[0]",
                 offset_matrix,
                 type="matrix")
    cmds.connectAttr(f"{control_obj}.worldMatrix[0]",
                     f"{node_multMatrix}.matrixIn[1]")
    # connect to blendMatrix
    cmds.connectAttr(f'{node_multMatrix}.matrixSum',
                     f"{node_bw_target_attr}[{parent_indices}].targetMatrix")
    # version switch
    if cmds.about(api=True) >= 20230000:
        status = [translate, rotate, scale, shear]
        for i, attr in enumerate(["translateWeight", "rotateWeight", "scaleWeight", "shearWeight"]):
            cmds.addAttr(parentspace_assets, ln=f"{attr}_{parent_indices}", at="double", min=0, max=1, k=1, dv=float(status[i]))
            cmds.connectAttr(f"{parentspace_assets}.{attr}_{parent_indices}",
                             f"{node_bw_target_attr}[{parent_indices}].{attr}", f=1)
    else:
        status = [translate, rotate, scale, shear]
        for i, attr in enumerate(["useTranslate", "useRotate", "useScale", "useShear"]):
            cmds.addAttr(parentspace_assets, ln=f"{attr}_{parent_indices}", at="bool", min=0, max=1, k=1, dv=status[i])
            cmds.connectAttr(f"{parentspace_assets}.{attr}_{parent_indices}",
                             f"{node_bw_target_attr}[{parent_indices}].{attr}", f=1)

    # sdk
    cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                           cd=f"{parentspace_assets}.{parentspace_attrName}",
                           dv=parent_indices - 1, v=0)
    cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                           cd=f"{parentspace_assets}.{parentspace_attrName}",
                           dv=parent_indices, v=1)
    cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                           cd=f"{parentspace_assets}.{parentspace_attrName}",
                           dv=parent_indices + 1, v=0)

    node_sdk = cmds.listConnections(f"{node_bw_target_attr}[{parent_indices}].weight", s=1, d=0)
    cmds.container(parentspace_assets, e=1, addNode=[node_multMatrix]+node_sdk)
