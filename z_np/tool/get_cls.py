from maya.api import OpenMaya as om
import numpy as np
import sys
from z_np.src.cMemoryView import CMemoryManager
sel = om.MSelectionList().add("cSkinDeformer1")
cls = sys.GLOBAL_DEFORMER_REGISTRY.get(om.MObjectHandle(sel.getDependNode(0)).hashCode())

print("="*50)
print(np.asarray(cls.DATA.output_rawPoints_mgr.reshape((cls.DATA.vertex_count,3)).view))
print("="*50)
ptr = int(cls.DATA.mFnMesh_output.getRawPoints())
print(np.asarray(CMemoryManager.from_ptr(ptr,"f",(cls.DATA.vertex_count,3)).view))
print("="*50)