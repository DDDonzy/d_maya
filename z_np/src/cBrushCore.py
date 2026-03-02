from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from z_np.src.cSkinDeform import CythonSkinDeformer

from z_np.src.cMemoryView import CMemoryManager
import z_np.src.cBrushCython as cBrushCython


# ==========================================
# 📦 数据结构定义区 (可以放在这，或者统一定义在总线文件里)
# ==========================================
@dataclass
class BrushSettings:
    """UI 面板直接修改此对象的属性，控制器通过引用实时读取。"""

    radius: float = 0.5
    strength: float = 0.1
    falloff_type: int = 0
    mode: int = 0
    use_surface: bool = True


class BrushHitState:
    """笔刷计算输出的渲染信箱，供 displayNode 读取绘制"""

    __slots__ = (
        "hit_count",
        "hit_indices_mgr",
        "hit_weights_mgr",
        "hit_center_position",
        "hit_center_normal",
    )

    def __init__(self, vertex_count):
        self.hit_count: int = 0
        self.hit_indices_mgr: "CMemoryManager" = CMemoryManager.allocate("i", (vertex_count,))
        self.hit_weights_mgr: "CMemoryManager" = CMemoryManager.allocate("f", (vertex_count,))

        self.hit_center_position: tuple = (0.0, 0.0, 0.0)
        self.hit_center_normal: tuple = (0.0, 0.0, 1.0)

    def clear(self):
        self.hit_count = 0
        self.hit_center_position = (0.0, 0.0, 0.0)
        self.hit_center_normal = (0.0, 0.0, 1.0)


# ==========================================
# 🧠 核心控制器
# ==========================================
class WeightBrushCore:
    """
    纯粹的无状态逻辑控制器 (Stateless Controller)
    配置来自引用注入，渲染通过总线提交。
    """

    def __init__(self, cSkin: "CythonSkinDeformer"):
        self.cSkin = cSkin

        # ==========================================
        # 🔽 1. 输入对接 (Input): 引用总线上的 UI 配置
        # ==========================================
        if getattr(self.cSkin.DATA, "brush_settings", None) is None:
            self.cSkin.DATA.brush_settings = BrushSettings()

        self.settings: BrushSettings = self.cSkin.DATA.brush_settings

        # ==========================================
        # 🔼 2. 输出挂载 (Output): 自身实例化，并发布到总线
        # ==========================================
        v_count = self.cSkin.DATA.vertex_count
        # 💥 由 WeightBrushCore 全权实例化自己的物理计算结果
        self.hit_state = BrushHitState(v_count)
        # 💥 挂载到总线，供 displayNode 和 Undo 读取！
        self.cSkin.DATA.brush_hit_state = self.hit_state

        # ==========================================
        # ⚙️ 3. 模型环境数据: 兜底初始化锁定状态
        # ==========================================
        i_count = self.cSkin.DATA.influences_count
        if getattr(self.cSkin.DATA, "influences_locks_mgr", None) is None or len(self.cSkin.DATA.influences_locks_mgr.view) != i_count:
            self.cSkin.DATA.influences_locks_mgr = CMemoryManager.allocate("B", (i_count,))
            for i in range(i_count):
                self.cSkin.DATA.influences_locks_mgr.view[i] = 0

    def teardown(self):
        """生命周期终结，彻底物理销毁"""
        # 1. 把自己的数据从总线上摘除 (断开对外广播)
        if hasattr(self.cSkin.DATA, "brush_hit_state"):
            self.cSkin.DATA.brush_hit_state = None

        # 2. 销毁内部对象引用
        self.hit_state = None
        self.settings = None
        self.cSkin = None

    def clear_hit_state(self):
        """替代原来的 clear_preview_registry"""
        if self.hit_state:
            self.hit_state.clear()

    def detect_range(self, center_xyz: tuple, hit_tri: int):
        """调用 Cython 检测笔刷衰减范围 (侦察兵)"""
        if self.cSkin.DATA.rawPoints2D_output is None:
            return 0

        # 💥 全部改为从 self.hit_state 中写入数据
        self.cSkin.DATA.brush_epoch += 1

        self.hit_state.hit_count = cBrushCython.compute_brush_weights_god_mode(
            center_xyz,
            self.cSkin.DATA.rawPoints2D_output.view,
            self.cSkin.DATA.tri_indices_2D.view,
            hit_tri,
            self.cSkin.DATA.adj_offsets.view,
            self.cSkin.DATA.adj_indices.view,
            self.settings.radius,
            self.settings.falloff_type,
            self.settings.use_surface,
            self.cSkin.DATA.brush_epoch,
            self.cSkin.DATA.pool_node_epochs.view,
            self.cSkin.DATA.pool_dist.view,
            self.cSkin.DATA.pool_queue.view,
            self.cSkin.DATA.pool_in_queue.view,
            self.hit_state.hit_indices_mgr.view,
            self.hit_state.hit_weights_mgr.view,
        )

        self.hit_state.hit_center_position = center_xyz
        return self.hit_state.hit_count

    def apply_weight_math(self) -> bool:
        """
        调度 Cython 数学核心，修改实际权重 (炮兵)
        返回: bool (True 表示成功修改了内存，False 表示未作任何修改)
        """
        if self.hit_state.hit_count == 0:
            return False

        modify_weights2D, target_inf, is_mask = self.cSkin.DATA.active_paint_target

        if modify_weights2D is None:
            return False

        if is_mask:
            safe_locks_view = CMemoryManager.allocate("B", (1,)).view
        else:
            safe_locks_view = self.cSkin.DATA.influences_locks_mgr.view

        cBrushCython.skin_weight_brush(
            self.settings.strength,
            self.settings.mode,
            target_inf,
            safe_locks_view,
            self.hit_state.hit_indices_mgr.view,
            self.hit_state.hit_weights_mgr.view,
            self.hit_state.hit_count,
            modify_weights2D.view,
        )
        return True
