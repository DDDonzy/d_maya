from __future__ import annotations

from functools import partial

from z_np.src2.cBrushCore2 import BrushSettings, BrushHitState

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maya.OpenMaya as om1  # type: ignore
    import maya.api.OpenMaya as om2  # type: ignore
    from z_np.src2.cMemoryView import CMemoryManager
    from z_np.src2.cWeightsHandle import WeightsLayerData


class SkinMemoryContext:
    """
    蒙皮与笔刷的全局物理内存上下文 (Model / Data)
    所有数据全局存放在此，方便调用。
    """

    __slots__ = (
        # 模型基础拓扑数据
        "vertex_count",
        "tri_indices_2D",
        "tri_to_face_map",
        "base_edge_indices",  # 💥 新增：纯净的边索引 [v1, v2, v1, v2...]
        "adj_offsets",        # 💥 新增：顶点邻接表偏移 (CSR 格式)
        "adj_indices",        # 💥 新增：顶点邻接表数据 (CSR 格式)
        # 顶点坐标数据
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
        "brush_hit_state",  # 🎨 笔刷渲染总线 (由笔刷写入，displayNode 只读)
        # 用户交互参数 (UI 层直接读写)
        "brush_settings",  # ⚙️ 笔刷配置总线 (由 UI 或快捷键修改，笔刷只读)
        # 绘制权重的数据源
        "paintLayerIndex",
        "paintInfluenceIndex",
        "paintMask",
        # -----------------
        "brush_epoch",           # 世代计数器
        "pool_node_epochs",      # 顶点的世代标记簿
        "pool_dist",             # 距离缓存
        "pool_queue",            # 环形队列
        "pool_in_queue",         # 是否在队列中的布尔标记
        "pool_touched",          # 记录不重复的顶点 
        #  ------------------
        # 显示权重物体
        "preview_shape_mObj",
        # 色彩与显示配置
        "color_wire",
        "color_point",
        "color_mask_remapA",
        "color_mask_remapB",
        "color_weights_remapA",
        "color_weights_remapB",
        "color_brush_remapA",
        "color_brush_remapB",
        # 渲染模式
        
        "render_mode",
    )

    def __init__(self):
        # fmt:off
        # ==========================================
        # 📐 1. 模型基础拓扑与空间数据
        # ==========================================
        self.vertex_count          : int             = 0     # 模型总顶点数 (N)
        self.tri_indices_2D        : CMemoryManager  = None  # 三角化后的顶点索引 (用于 Cython 射线检测碰撞)
        self.tri_to_face_map       : CMemoryManager  = None  # 三角面 ID 映射回 Maya 原生多边形 Face ID 的查找表
        self.base_edge_indices     : CMemoryManager  = None  # 用于 GPU 画线
        self.adj_offsets           : CMemoryManager  = None  # 用于 Cython 极速查找邻接点
        self.adj_indices           : CMemoryManager  = None  # 用于 Cython 极速查找邻接点
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
        # ----------------------
        self.brush_epoch        : int = 1
        self.pool_node_epochs   : CMemoryManager = None
        self.pool_dist          : CMemoryManager = None
        self.pool_queue         : CMemoryManager = None
        self.pool_in_queue      : CMemoryManager = None
        self.pool_touched       : CMemoryManager = None 
        # --------------------------
        # --- 渲染 ---
        self.preview_shape_mObj : om2.MObject = None     # 显示权重物体
        # ==========================================
        # 🎨 色彩与显示配置 (灵活到可以做皮肤主题)
        # ==========================================
        self.color_wire     = (0.0, 1.0, 1.0, 1.0)      # 线框色
        self.color_point    = (1.0, 0.0, 0.0, 1.0)      # 笔刷红点
        
        # 遮罩模式配色
        self.color_mask_remapA  = (0.1, 0.1, 0.1, 0.0)      
        self.color_mask_remapB  = (0.1, 1.0, 0.1, 0.0)      
        
        # 黑白权重配色 (替代了原来的 render_black_white)
        self.color_weights_remapA    = (0.0, 0.0, 0.0, 0.0)      # 纯黑
        self.color_weights_remapB    = (1.0, 1.0, 1.0, 0.0)      # 纯白
        # 笔刷渐变范围，红黄
        self.color_brush_remapA = (1.0, 0.0, 0.0, 1.0)
        self.color_brush_remapB = (1.0, 1.0, 0.0, 1.0)
        
        self.render_mode    = 0

        # fmt:on

    @property
    def active_paint_target(self) -> tuple["CMemoryManager", int, bool] | tuple[None, None, None]:
        """
        🎨 [Property] 活跃绘制目标 (只读)
        Controller 直接读取此属性，即可获取当前正确的物理内存、靶心索引，以及是否为遮罩。
        返回: (memory_view, target_influence_index, is_mask)
        """
        if self.paintLayerIndex not in self.weightsLayer:
            return None, None, None

        active_layer = self.weightsLayer[self.paintLayerIndex]

        if self.paintMask:
            if not active_layer.maskHandle or not active_layer.maskHandle.is_valid:
                return None, None, None
            # Mask 模式：单通道视图，靶心 0，is_mask=True
            return active_layer.maskHandle.memory.reshape((self.vertex_count, 1)), 0, True

        else:
            if not active_layer.weightsHandle or not active_layer.weightsHandle.is_valid:
                return None, None, None
            # 权重模式：多通道视图，靶心为用户选择的骨骼，is_mask=False
            return active_layer.weightsHandle.memory.reshape((self.vertex_count, self.influences_count)), self.paintInfluenceIndex, False


