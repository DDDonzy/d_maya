
import maya.standalone
maya.standalone.initialize()
#
from time import time
from utils.generateUniqueName import generateUniqueName
from utils.transform import transform as t
from maya import cmds


a = cmds.polyCube()[0]
b = cmds.polyCube()[0]
t.set_trs(a,[1,2,3,4,5,6,1,1,1])
t.set_trs(b,[2,1,4,4,5,0,1,1,1])

s = time()
temp = ""
for x in range(200):
    if not temp:
        temp = cmds.createNode("transform", name=f"test{x}")
    else:
        temp = cmds.createNode("transform", name=f"test{x}", parent=temp)
    if x%2 ==0:
        #t.matrixConstraint(a,temp)
        cmds.parentConstraint(a,temp,mo=1)
        cmds.scaleConstraint(a,temp,mo=1)
    if x%2 ==1:
        #t.matrixConstraint(b,temp)
        cmds.parentConstraint(b,temp,mo=1)
        cmds.scaleConstraint(b,temp,mo=1)
sphere = cmds.polySphere()[0]
cmds.parent(sphere,temp)

print(time()-s)




a = cmds.polyCube()[0]
b = cmds.polyCube()[0]
t.set_trs(a,[1,2,3,4,5,6,1,1,1])
t.set_trs(b,[2,1,4,4,5,0,1,1,1])

s = time()
temp = ""
for x in range(200):
    if not temp:
        temp = cmds.createNode("transform", name=f"te1st{x}")
    else:
        temp = cmds.createNode("transform", name=f"te1st{x}", parent=temp)
    if x%2 ==0:
        t.matrixConstraint(a,temp)

    if x%2 ==1:
        t.matrixConstraint(b,temp)

sphere = cmds.polySphere()[0]
cmds.parent(sphere,temp)

print(time()-s)