# Author:   Donzy.xu
# CreateTime:   2023/3/16 - 21:27
# FileName:  parentSpace.py

import maya.cmds as cmds
import maya.api.OpenMaya as om
from . import transform as t


def parentSpace(enum_name='Parent',
                driver_object=None,
                target_object=None,
                skip=None):
    if not driver_object:
        driver_object = cmds.ls(sl=1)[0]
        target_object = cmds.ls(sl=1)[1]
    name_split = target_object.split("_")
    name_split[-1] = "parentSpace"
    parent_constraint_grp = "_".join(name_split)
    if not cmds.objExists(parent_constraint_grp):
        parent_object = cmds.listRelatives(target_object, p=1)[0]
        parent_constraint_grp = cmds.createNode('transform', name=parent_constraint_grp)
        cmds.delete(cmds.parentConstraint(target_object, parent_constraint_grp))
        cmds.parent(parent_constraint_grp, parent_object)
        cmds.parent(target_object, parent_constraint_grp)

    else:
        parent_object = cmds.listRelatives(parent_constraint_grp, p=1)[0]

    c_matrix = om.MMatrix(cmds.getAttr("{}.worldInverseMatrix".format(driver_object)))
    t_matrix = om.MMatrix(cmds.getAttr("{}.worldMatrix".format(target_object)))

    fbf_node = t.createNode_FBF(t_matrix * c_matrix, name="{}_CON_{}_FBF".format(driver_object, target_object))
    mult_node = cmds.createNode('multMatrix', name="{}_CON_{}_MultMatrix".format(driver_object, target_object))
    cmds.connectAttr("{}.output".format(fbf_node), "{}.matrixIn[0]".format(mult_node))
    cmds.connectAttr("{}.worldMatrix".format(driver_object), "{}.matrixIn[1]".format(mult_node))
    cmds.connectAttr("{}.worldInverseMatrix".format(parent_object), "{}.matrixIn[2]".format(mult_node))
    blend_matrix = '{}_MatrixBW'.format(target_object)
    if not cmds.objExists(blend_matrix):
        blend_matrix = cmds.createNode('wtAddMatrix', name='{}_MatrixBW'.format(target_object))
        array_index = len(cmds.ls("{}.wtMatrix[*]".format(blend_matrix)))
        cmds.connectAttr("{}.matrixSum".format(mult_node), "{}.wtMatrix[{}].matrixIn".format(blend_matrix, array_index))
        cmds.setAttr("{}.wtMatrix[{}].weightIn".format(blend_matrix, array_index), 1)
        decompose_node = cmds.createNode('decomposeMatrix', name="{}_decomposeMatrix".format(target_object))
        cmds.connectAttr("{}.matrixSum".format(blend_matrix), "{}.inputMatrix".format(decompose_node))
        cmds.connectAttr("{}.outputTranslate".format(decompose_node), "{}.translate".format(parent_constraint_grp))
        cmds.connectAttr("{}.outputRotate".format(decompose_node), "{}.rotate".format(parent_constraint_grp))
        cmds.connectAttr("{}.outputScale".format(decompose_node), "{}.scale".format(parent_constraint_grp))
        cmds.connectAttr("{}.outputShear".format(decompose_node), "{}.shear".format(parent_constraint_grp))
        cmds.addAttr(target_object, ln="parentSpace", at="enum", en=enum_name, k=1)
        cmds.setDrivenKeyframe("{}.wtMatrix[{}].weightIn".format(blend_matrix, array_index),
                               cd="{}.parentSpace".format(target_object),
                               dv=array_index - 1, v=0)
        cmds.setDrivenKeyframe("{}.wtMatrix[{}].weightIn".format(blend_matrix, array_index),
                               cd="{}.parentSpace".format(target_object),
                               dv=array_index, v=1)
        cmds.setDrivenKeyframe("{}.wtMatrix[{}].weightIn".format(blend_matrix, array_index),
                               cd="{}.parentSpace".format(target_object),
                               dv=array_index + 1, v=0)
    else:
        array_index = len(cmds.ls("{}.wtMatrix[*]".format(blend_matrix)))
        print(array_index)
        cmds.connectAttr("{}.matrixSum".format(mult_node), "{}.wtMatrix[{}].matrixIn".format(blend_matrix, array_index))
        new_enum_name = "{}:{}".format(cmds.addAttr(target_object + ".parentSpace", q=1, en=1), enum_name)
        print(new_enum_name)
        enum_list = new_enum_name.split(":")
        print(enum_list)
        cmds.addAttr(target_object + ".parentSpace", e=1, en=new_enum_name)

        cmds.setDrivenKeyframe("{}.wtMatrix[{}].weightIn".format(blend_matrix, array_index),
                               cd="{}.parentSpace".format(target_object),
                               dv=enum_list.index(enum_name) - 1, v=0)
        cmds.setDrivenKeyframe("{}.wtMatrix[{}].weightIn".format(blend_matrix, array_index),
                               cd="{}.parentSpace".format(target_object),
                               dv=enum_list.index(enum_name), v=1)
        cmds.setDrivenKeyframe("{}.wtMatrix[{}].weightIn".format(blend_matrix, array_index),
                               cd="{}.parentSpace".format(target_object),
                               dv=enum_list.index(enum_name) + 1, v=0)


if __name__ == "__main__":
    parentSpace(enum_name="Chest")
