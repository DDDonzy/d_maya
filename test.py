from maya.api import OpenMaya as om


def test():
mSel: om.MSelectionList = om.MGlobal.getActiveSelectionList()
if mSel.length() == 0:
    raise RuntimeError("Please select meshes!")
mDag: om.MDagPath = mSel.getDagPath(0).extendToShape()
if not mDag.hasFn(om.MFn.kMesh):
    om.MGlobal.displayError("Please select meshes!")
    raise RuntimeError("daf")
