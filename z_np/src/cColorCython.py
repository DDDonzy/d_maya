# cython_core.py
import cython


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall  # 允许 Python 和 C 双向极速调用
def compute_colors_fast(
    weights: cython.float[:, :],  # 💥 明确指定输入权重视图必须是单精度 float32
    colors: cython.float[:, :],  # 明确指定输出颜色视图也是单精度 float32
    bone_index: cython.int,
    r: cython.float,
    g: cython.float,
    b: cython.float,
    a: cython.float,
):
    """
    极速核心：将 2D 权重矩阵映射为 RGBA 颜色矩阵 (纯 Python 语法模式，极致单精度版)
    """
    # 静态类型声明
    num_verts: cython.int = weights.shape[0]
    num_bones: cython.int = weights.shape[1]
    v: cython.int = 0
    w: cython.float = 0.0  # 💥 权重变量明确为 float

    # 防呆保护：防止骨骼索引越界
    if bone_index < 0 or bone_index >= num_bones:
        bone_index = 0

    # 纯 C 级别的极速循环
    for v in range(num_verts):
        w = weights[v, bone_index]

        colors[v, 0] = w * r
        colors[v, 1] = w * g
        colors[v, 2] = w * b
        colors[v, 3] = a




# ------------------------------------------------------------------------------------
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def inject_brush_color_to_vram(
    vram_color_view: cython.float[:, :], # 目标：GPU 显存的二维视图 (N, 4)
    indices_view: cython.int[:],         # 源：笔刷算出来的顶点 ID
    weights_view: cython.float[:],       # 源：笔刷算出来的衰减权重
    hit_count: cython.int                # 命中数量
):
    """
    极速显存染色：直接在 GPU 映射内存中将笔刷范围涂红 (纯 Python 语法版)
    """
    # ==========================================
    # 静态类型声明区 (完全摒弃 cdef)
    # ==========================================
    i: cython.int = 0
    v_idx: cython.int = 0
    w: cython.float = 0.0

    # ==========================================
    # 极速内存覆写
    # ==========================================
    for i in range(hit_count):
        v_idx = indices_view[i]
        w = weights_view[i]
        
        # 强制覆写显存！红色通道为衰减权重，透明度拉满
        vram_color_view[v_idx, 0] = w        # R
        vram_color_view[v_idx, 1] = 0.0      # G
        vram_color_view[v_idx, 2] = 0.0      # B
        vram_color_view[v_idx, 3] = 1.0      # Alpha



# ------------------------------------------------------------------------------------
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def generate_offset_indices(
    target_idx_view: cython.uint[:],   # 目标：点阵的 Index Buffer
    start_offset: cython.int,          # 起始偏移量 (也就是 N)
    count: cython.int                  # 顶点数量
):
    """极速生成带偏移量的连续 Index 数组"""
    i: cython.int = 0
    for i in range(count):
        target_idx_view[i] = start_offset + i




# ------------------------------------------------------------------------------------
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def fill_solid_color(
    target_color_view: cython.float[:, :], # 目标：显存颜色视图
    count: cython.int,                     # 填充数量
    r: cython.float,
    g: cython.float,
    b: cython.float,
    a: cython.float
):
    """极速用统一纯色填满目标显存 (替换 np.full)"""
    i: cython.int = 0
    for i in range(count):
        target_color_view[i, 0] = r
        target_color_view[i, 1] = g
        target_color_view[i, 2] = b
        target_color_view[i, 3] = a



# ------------------------------------------------------------------------------------
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def apply_brush_colors(
    target_color_view: cython.float[:, :], # 目标：后半段显存颜色视图
    indices_view: cython.int[:],           # 源：笔刷算出的顶点 ID
    weights_view: cython.float[:],         # 源：笔刷算出的衰减权重
    hit_count: cython.int
):
    """给笔刷命中的顶点上色，颜色随权重衰减"""
    i: cython.int = 0
    v_idx: cython.int = 0
    w: cython.float = 0.0
    for i in range(hit_count):
        v_idx = indices_view[i]
        w = weights_view[i]
        
        # 亮黄色 (R=1, G=w, B=0)
        target_color_view[v_idx, 0] = 1.0
        target_color_view[v_idx, 1] = w
        target_color_view[v_idx, 2] = 0.0
        target_color_view[v_idx, 3] = 1.0


# ------------------------------------------------------------------------------------
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def generate_brush_indices(
    target_idx_view: cython.uint[:],   # 目标：专门给笔刷点的 Index Buffer
    source_indices_view: cython.int[:],# 源：笔刷算出来的真实顶点 ID
    offset: cython.int,                # 偏移量 (也就是顶点总数 N)
    hit_count: cython.int
):
    """将圈中的顶点 ID 加上偏移量，提取出来给显卡"""
    i: cython.int = 0
    for i in range(hit_count):
        target_idx_view[i] = source_indices_view[i] + offset