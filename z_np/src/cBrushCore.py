from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from z_np.src.cSkinDeform import CythonSkinDeformer

from z_np.src.cMemoryView import CMemoryManager
import z_np.src.cBrushCython as cBrushCython
from z_np.src._cRegistry import GLOBAL_BRUSH_REGISTRY


class WeightBrushCore:
    # ==========================================
    # 🎨 1. 笔刷全局设置 (类属性：UI 随时修改，常驻内存)
    # ==========================================
    radius: float = 0.5
    strength: float = 0.1
    falloff_type: int = 0
    mode: int = 0

    paintLayerIndex: int = -1
    paintInfluenceIndex: int = 0
    paintMask: bool = False

    # ==========================================
    # ⚙️ 2. 运行时内存状态 (纯指针，绝对私有)
    # ==========================================
    cSkin: "CythonSkinDeformer" = None

    _hit_indices_mgr: CMemoryManager = None
    _hit_weights_mgr: CMemoryManager = None
    _hit_count: int = 0

    # ==========================================
    # ⚙️ 3. 权重源数据指针
    # ==========================================

    @classmethod
    def setup_memory_pool(cls, cSkin: "CythonSkinDeformer"):
        """注入依赖并申请内存池：接管来自 Maya 的坐标数据"""
        cls.cSkin = cSkin
        # 申请笔刷专用的内存池
        cls._hit_indices_mgr = CMemoryManager.allocate("i", (cls.cSkin.DATA.vertex_count,))
        cls._hit_weights_mgr = CMemoryManager.allocate("f", (cls.cSkin.DATA.vertex_count,))
        cls._hit_count = 0

    @classmethod
    def teardown_memory_pool(cls):
        """工具退出时，立刻斩断野指针，防止崩溃！"""
        cls._hit_indices_mgr = None
        cls._hit_weights_mgr = None
        cls._hit_count = 0

    @classmethod
    def detect_range(cls, center_xyz: tuple):
        """
        范围检测：将纯 Python 元组 (x, y, z) 传递给 Cython
        输入射线检测的点，暴力迭代所有模型点，进行权重衰减计算
        `cls.cSkin.DATA.output_rawPoints_mgr2D.view` 模型点数据
        cython会把计算结果输出到 `cls._hit_indices_mgr` 和 `cls._hit_weights_mgr`
        """
        if cls.cSkin.DATA.output_rawPoints_mgr2D is None:
            return 0

        cls._hit_count = cBrushCython.calculate_brush_falloff_volume(
            cls.cSkin.DATA.output_rawPoints_mgr2D.view,
            center_xyz,
            cls.radius,
            cls.mode,
            cls._hit_indices_mgr.view,
            cls._hit_weights_mgr.view,
        )

        return cls._hit_count

    @classmethod
    def write_preview_registry(cls):
        """专递数据指针到全局内存中"""
        if cls._hit_count > 0:
            GLOBAL_BRUSH_REGISTRY["brush_preview"] = {
                "hit_count": cls._hit_count,
                "indices_mgr": cls._hit_indices_mgr,
                "weights_mgr": cls._hit_weights_mgr,
            }
        else:
            GLOBAL_BRUSH_REGISTRY.clear()

    @classmethod
    def clear_preview_registry(cls):
        GLOBAL_BRUSH_REGISTRY.clear()
        cls._hit_count = 0

    # ==========================================
    # 核心算法调度区 (加/减/乘 预留)
    # ==========================================
    @classmethod
    def apply_weight_math(cls, center_xyz):
        """根据当前的 cls.mode 调度不同的 Cython 数学计算"""
        if cls._hit_count == 0:
            return

        lock_list = [0 for _ in range(cls.cSkin.DATA.influences_count)]
        bone_locks_mgr = CMemoryManager.from_list(lock_list, "B")
        modify_weights = cls.cSkin.DATA.weightsLayer[WeightBrushCore.paintLayerIndex].weightsHandle
        modify_weights2D_view = modify_weights.memory.reshape((cls.cSkin.DATA.vertex_count, cls.cSkin.DATA.influences_count)).view

        cBrushCython.skin_weight_brush(
            cls.cSkin.DATA.output_rawPoints_mgr2D.view,
            center_xyz,
            cls.radius,
            cls.falloff_type,
            cls.strength,
            cls.mode,
            cls.paintInfluenceIndex,
            bone_locks_mgr.view,
            modify_weights2D_view,
            cls._hit_indices_mgr.view,
            cls._hit_weights_mgr.view,
        )
