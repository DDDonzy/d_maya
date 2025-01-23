import cProfile
import time
from maya.api import OpenMaya as om
from maya import cmds
import numpy as np


sel = cmds.ls(sl=1, fl=1)
int_sel = set([int(x.split("[")[1].split("]")[0]) for x in sel])


mesh = "Common_Hair_Mesh"

mSel = om.MSelectionList()
mSel.add(mesh)
mDag: om.MDagPath = mSel.getDagPath(0)
fnMesh = om.MFnMesh(mDag)
mIterMesh = om.MItMeshVertex(mDag)
neighbor_vtx_list = {}
position_vtx_list = {}
while not mIterMesh.isDone():
    vtx_id = mIterMesh.index()
    connected_vtx = mIterMesh.getConnectedVertices()
    neighbor_vtx_list[vtx_id] = set(connected_vtx)
    position_vtx_list[vtx_id] = set(mIterMesh.position())
    mIterMesh.next()


s = time.time()


def test():

    out = set(int_sel)
    iter_l = int_sel
    iter_num = 0

    while iter_l:
        iter_num += 1
        add = set()

        for x in iter_l:
            new_neighbors = neighbor_vtx_list[x] - out
            add.update(new_neighbors)
        out.update(add)
        iter_l = add
        cmds.select([f"Common_Hair_Mesh.vtx[{x}]" for x in add])
        cmds.cluster()


test()
print(time.time()-s)
