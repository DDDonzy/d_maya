from enum import IntFlag, auto

# ==========================================
# 1. 底层定义：用 IntFlag 搞定掩码定义和可读性
# ==========================================
class RenderDirtyFlag(IntFlag):
    CLEAN = 0
    VTX_POS = auto()      # 1
    FACE_IDX = auto()     # 2
    FACE_COLOR = auto()   # 4

# ==========================================
# 2. 状态管理器：对外提供傻瓜接口，对内操作掩码
# ==========================================
class RenderState:
    __slots__ = ('_flags',) # 依然保持极致的内存优化

    def __init__(self):
        # 唯一的数据源：一个 IntFlag 变量
        self._flags = RenderDirtyFlag.CLEAN

    # --- 外部接口：傻瓜式布尔值操作 ---
    @property
    def isDirty_vtx(self):
        # 使用 in 关键字，直观且安全
        return RenderDirtyFlag.VTX_POS in self._flags

    @isDirty_vtx.setter
    def isDirty_vtx(self, value):
        if value:
            self._flags |= RenderDirtyFlag.VTX_POS
        else:
            self._flags &= ~RenderDirtyFlag.VTX_POS

    @property
    def isDirty_color(self):
        return RenderDirtyFlag.FACE_COLOR in self._flags

    @isDirty_color.setter
    def isDirty_color(self, value):
        if value:
            self._flags |= RenderDirtyFlag.FACE_COLOR
        else:
            self._flags &= ~RenderDirtyFlag.FACE_COLOR


# ==========================================
# 3. 任务绑定器
# ==========================================
class BoundTask:
    __slots__ = ('flag', 'action')
    def __init__(self, flag, action):
        self.flag = flag
        self.action = action


# ==========================================
# 4. 你的核心插件类 (总调度器)
# ==========================================
class TriangleOverride:
    def __init__(self):
        # 实例化状态管理器
        self.state = RenderState()
        
        # 定义流水线：将底层的 Flag 和具体的执行函数锁死
        self._update_pipeline = (
            BoundTask(RenderDirtyFlag.VTX_POS, self._update_vtx_positions),
            BoundTask(RenderDirtyFlag.FACE_COLOR, self._update_colors),
        )

    # --- 具体的业务逻辑 ---
    def _update_vtx_positions(self):
        print(">> 正在执行：搬运顶点显存...")

    def _update_colors(self):
        print(">> 正在执行：Cython 计算顶点颜色...")

    # --- 总调度器 ---
    def update(self):
        print("\n[调度器启动] 当前底层状态:", self.state._flags)
        
        # 批量执行管线
        for task in self._update_pipeline:
            # 检查底层 _flags 中是否包含该任务的标记
            if task.flag in self.state._flags:
                # 1. 执行具体的逻辑
                task.action()
                # 2. 自动清理该状态
                self.state._flags &= ~task.flag
                
        print("[调度器结束] 处理后状态:", self.state._flags)


plugin = TriangleOverride()

# 【场景：业务逻辑开发者/前端接线员】
# 你的同事完全不需要懂掩码，像往常一样赋值 True/False 即可
plugin.state.isDirty_vtx = True
plugin.state.isDirty_color = True

# 【场景：Maya 触发了下一帧的刷新】
# 调度器完美接管，不仅执行了代码，打印出来的日志也极其清晰
plugin.update()