from __future__ import annotations
from typing import TYPE_CHECKING
from .cBrushCore2 import BrushSettings, BrushHitState

if TYPE_CHECKING:
    import maya.OpenMaya as om1  # type: ignore
    from z_np.src.cMemoryView import CMemoryManager
    from z_np.src.cWeightsHandle import WeightsLayerData


class SkinMemoryContext:
    """
    蒙皮与笔刷的全局物理内存上下文 (Model / Data)
    所有数据全局存放在此，方便调用。
    """

    __slots__ = (
        # 模型基础拓扑数据
        "topology",
        "tri_indices_2D",
        "tri_to_face_map",
        "vertex_count",
        "rawPoints_original",
        "rawPoints2D_original",
        "rawPoints_output",
        "rawPoints2D_output",
        # 蒙皮矩阵数据
        "influences_count",
        "influences_locks_mgr",
        "_influencesMatrix_mgr",
        "_bindPreMatrix_mgr",
        "_rotateMatrix_mgr",
        "_translateVector_mgr",
        # API 缓存对象
        "hashCode",
        "mObject",
        "mFnDep",
        "mFnMesh_original",
        "mFnMesh_output",
        "weightsLayer",
        # 笔刷专用的动态内存与状态
        "brush_hit_state",                 # 🎨 笔刷渲染总线 (由笔刷写入，displayNode 只读)
        # 用户交互参数 (UI 层直接读写)
        "brush_settings",                  # ⚙️ 笔刷配置总线 (由 UI 或快捷键修改，笔刷只读)
        # 绘制权重的数据源
        "paintLayerIndex",
        "paintInfluenceIndex",
        "paintMask",
    )

    def __init__(self):
        # fmt:off
        # ==========================================
        # 📐 1. 模型基础拓扑与空间数据
        # ==========================================
        self.vertex_count          : int             = 0     # 模型总顶点数 (N)
        self.topology              : list[int]       = None  # 模型的面拓扑数据缓存 (多边形边数列表)
        self.tri_indices_2D        : CMemoryManager  = None  # 三角化后的顶点索引 (用于 Cython 射线检测碰撞)
        self.tri_to_face_map       : CMemoryManager  = None  # 三角面 ID 映射回 Maya 原生多边形 Face ID 的查找表
        # 顶点坐标内存池 (1D 与 2D 视图绑定同一块物理内存)
        self.rawPoints_original  : CMemoryManager    = None  # 蒙皮前的原始顶点坐标 (1D 展平，长 N*3)
        self.rawPoints2D_original: CMemoryManager    = None  # 蒙皮前的原始顶点坐标 (2D 视图，形状 N x 3)
        self.rawPoints_output    : CMemoryManager    = None  # 蒙皮形变后的顶点坐标 (1D 展平，用于推给 GPU)
        self.rawPoints2D_output  : CMemoryManager    = None  # 蒙皮形变后的顶点坐标 (2D 视图，用于笔刷计算距离)
        # ==========================================
        # 🦴 2. 蒙皮矩阵与变换数据
        # ==========================================
        self.influences_count     : int            = 0     # 参与蒙皮的骨骼/影响物总数
        self.influences_locks_mgr : CMemoryManager = None  # 骨骼的锁定状态
        self._influencesMatrix_mgr: CMemoryManager = None  # 骨骼的当前世界矩阵 (World Matrix)
        self._bindPreMatrix_mgr   : CMemoryManager = None  # 骨骼的绑定逆矩阵 (Bind Pre Matrix)
        self._rotateMatrix_mgr    : CMemoryManager = None  # 提取出的骨骼纯旋转矩阵 (用于法线计算或封套计算)
        self._translateVector_mgr : CMemoryManager = None  # 提取出的骨骼平移向量
        # ==========================================
        # 📦 3. Maya API 对象缓存 (避免每帧重复实例化带来的开销)
        # ==========================================
        self.hashCode        : int                             = None  # 当前 cSkinDeform 节点的全局唯一哈希值 (替代原本的字典 Key)
        self.mObject         : om1.MObject                     = None  # 变形器自身的 MObject
        self.mFnDep          : om1.MFnDependencyNode           = None  # 变形器自身的 Dependency Node 函数集
        self.mFnMesh_original: om1.MFnMesh                     = None  # 连入变形器的原始网格 (Input Mesh) 函数集
        self.mFnMesh_output  : om1.MFnMesh                     = None  # 变形器输出的网格 (Output Mesh) 函数集
        self.weightsLayer    : dict[int, WeightsLayerData]     = {}    # 多层权重系统的数据字典 {层级ID: 权重数据句柄}
        # ==========================================
        # 🖌️ 4. 笔刷系统专用的动态内存与参数
        # ==========================================
        # --- 运行时动态指针 ---
        self.brush_hit_state    : BrushHitState    = None                 # 🎨 笔刷渲染总线 (由笔刷写入，displayNode 只读)
        self.brush_settings     : BrushSettings    = BrushSettings()      # ⚙️ 笔刷配置总线 (由 UI 或快捷键修改，笔刷只读)
        # --- 绘制权重的数据源 ---
        self.paintLayerIndex    : int = -1               # 当前正在绘制的权重层 ID (-1 通常代表 Base 层)
        self.paintInfluenceIndex: int = 0                # 当前正在绘制权重的目标骨骼 ID
        self.paintMask          : bool = False           # 是否开启了遮罩绘制模式
        # fmt:on

    def get_active_weights2D(self) -> CMemoryManager | None:
        """
        根据当前 UI 设置的图层目标，安全地返回 2D 权重的 C 内存视图。
        """
        # 1. 越界保护
        if self.paintLayerIndex < 0 or self.paintLayerIndex >= len(self.weightsLayer):
            return None

        # 2. 提取当前图层
        active_layer = self.weightsLayer[self.paintLayerIndex]
        if not active_layer.weightsHandle.is_valid:
            return None

        # 3. 塑形并返回纯 C 视图
        return active_layer.weightsHandle.memory.reshape((self.vertex_count, self.influences_count))
