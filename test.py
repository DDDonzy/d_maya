<<<<<<< HEAD
import os
import shutil

# 定义路径
mvn_dir = r'N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260419\MVN'
base_dir = r'N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260419\FBX\base'
target_dir = r'N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260419\FBX'

def sync_fbx_files():
    # 1. 获取 MVN 目录下没有后缀的文件名
    print("正在扫描 MVN 目录...")
    missing_ext_files = []
    for f in os.listdir(mvn_dir):
        # 拼接完整路径以判断是否为文件
        full_path = os.path.join(mvn_dir, f)
        if os.path.isfile(full_path) and '.' not in f:
            missing_ext_files.append(f)
    
    if not missing_ext_files:
        print("未在 MVN 目录中找到无后缀的文件。")
        return

    print(f"找到 {len(missing_ext_files)} 个无后缀文件。开始匹配并复制...")

    # 2. 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 3. 寻找对应的 FBX 并复制
    copied_count = 0
    for file_name in missing_ext_files:
        # 构建 base 目录下的源文件路径 (文件名 + .fbx)
        source_fbx = os.path.join(base_dir, file_name + '.fbx')
        # 构建目标路径
        destination_fbx = os.path.join(target_dir, file_name + '.fbx')

        if os.path.exists(source_fbx):
            try:
                shutil.copy2(source_fbx, destination_fbx)
                print(f"已成功复制: {file_name}.fbx")
                copied_count += 1
            except Exception as e:
                print(f"复制 {file_name}.fbx 时出错: {e}")
        else:
            print(f"跳过: 在 base 目录中未找到 {file_name}.fbx")

    print(f"\n任务完成！共计复制 {copied_count} 个文件到 {target_dir}")

if __name__ == "__main__":
    sync_fbx_files()
=======
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
>>>>>>> 873e6e9bd66b0c897deff3b062b6e31ef64c7161
