"""
注册全局内存

`cSkinDeform`,`cDisplayNode`,`cBrushCore` 共享数据，避开maya数据传递开销，尽最大可能避免数据复制。
"""

import sys


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cSkinDeform import CythonSkinDeformer


# 变形器数据
if not hasattr(sys, "GLOBAL_DEFORMER_REGISTRY"):
    sys.GLOBAL_DEFORMER_REGISTRY = {}
GLOBAL_DEFORMER_REGISTRY: dict[int, "CythonSkinDeformer"] = sys.GLOBAL_DEFORMER_REGISTRY


# 笔刷数据
if not hasattr(sys, "GLOBAL_BRUSH_REGISTRY"):
    sys.GLOBAL_BRUSH_REGISTRY = {}
GLOBAL_BRUSH_REGISTRY: dict = sys.GLOBAL_BRUSH_REGISTRY
