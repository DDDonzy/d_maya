# Author:   Donzy.xu
# CreateTime:   2024/1/27 - 3:52
# FileName:  addGroup_new.py


import re
import maya.cmds as cmds
from functools import partial


def addGroupNew(obj, add_string, replaceString):
    add_string = re.sub(r"\W", ",", add_string)
    add_list = add_string.split(",")

    if replaceString == "":
        replaceString = None

    # add group
    iter_index = 0
    grp_list = []
    for x in add_list:
        if replaceString:
            grp_name = obj.replace(replaceString, x)
        else:
            grp_name = "{}_{}".format(obj, x)
        grp = cmds.createNode("transform", name=grp_name)
        grp_list.append(grp)

        if iter_index != 0:
            cmds.parent(grp, grp_list[-2])
        iter_index += 1

    # align group
    cmds.delete(cmds.parentConstraint(obj, grp_list[0]))
    cmds.delete(cmds.scaleConstraint(obj, grp_list[0]))

    # connect logic
    cmds.parentConstraint(grp_list[-1], obj)
    cmds.scaleConstraint(grp_list[-1], obj)

    obj_parent = cmds.listRelatives(obj, parent=1)
    if obj_parent:
        obj_parent = obj_parent[0]
        obj_parent_group = "{}_{}".format(obj_parent, add_list[-1])
        if cmds.objExists(obj_parent_group):
            cmds.parent(grp_list[0], obj_parent_group)
        else:
            cmds.parentConstraint(obj_parent, grp_list[0], mo=1)
            cmds.scaleConstraint(obj_parent, grp_list[0], mo=1)


class addGroup_ui:
    def __init__(self):
        self.winName = "AddGroupTool"
        if cmds.window(self.winName, ex=1):
            cmds.deleteUI(self.winName)
        self.win = cmds.window(self.winName, tlb=1)
        root_Layout = cmds.columnLayout(p=self.win, adj=1)
        cmds.separator(p=root_Layout, style="none", height=5)
        self.searchTFBG = cmds.textFieldButtonGrp(p=root_Layout, text="", label="SearchSuffix :", buttonLabel="Clear", bc=partial(self.clearSearchTFBG))
        self.groupTFBG = cmds.textFieldButtonGrp(p=root_Layout, text="GRP,CTL", label="GroupSuffix :", buttonLabel="Clear", bc=partial(self.clearGroupTFBG))
        cmds.button(p=root_Layout, label="Add Group", height=40, c=partial(self.addGroupButtonCommand))

    def show(self):
        cmds.window(self.win, e=1, wh=[500, 100], s=0)
        cmds.showWindow(self.win)

    def clearSearchTFBG(self):
        cmds.textFieldButtonGrp(self.searchTFBG, e=1, text="")

    def clearGroupTFBG(self):
        cmds.textFieldButtonGrp(self.groupTFBG, e=1, text="")

    def addGroupButtonCommand(self, *args):
        objList = cmds.ls(sl=1)
        objSuffix = str(cmds.textFieldButtonGrp(self.searchTFBG, q=1, text=1))
        grpSuffix = str(cmds.textFieldButtonGrp(self.groupTFBG, q=1, text=1))
        for obj in objList:
            addGroupNew(obj=obj, replaceString=objSuffix, add_string=grpSuffix)


if __name__ == "__main__":
    win = addGroup_ui()
    win.show()
