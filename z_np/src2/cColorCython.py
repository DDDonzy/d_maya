# ==============================================================================
# 🎨 cColor.py - 纯 Python 语法版 (支持 Cython 极限编译)
# ==============================================================================
import cython


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def render_heatmap(
    weights_1d: cython.float[:],
    color_view: cython.float[:, :],
):
    """冷暖色谱渲染 (带绝对 0/1 极值高亮提示)"""
    N: cython.int = color_view.shape[0]
    i: cython.int
    w: cython.float
    r: cython.float
    g: cython.float
    b: cython.float
    t: cython.float

    with cython.nogil:
        for i in range(N):
            w = weights_1d[i]

            # 💥 1. 绝对为 0 (或低于0)：显示为纯黑！
            if w <= 0.0:
                r, g, b = 0.0, 0.0, 0.0

            # 💥 2. 只要大于 0，哪怕是 0.000001，也会走这里的插值
            # 当 w = 0.000001 时，t 几乎等于 0，计算结果为 (0, 近乎0, 近乎1) -> 视觉上依然是绝对的纯蓝！
            elif w < 0.40:
                t = w / 0.40
                r, g, b = 0.0, t, 1.0 - t

            elif w < 0.60:
                t = (w - 0.40) / 0.20
                r, g, b = t, 1.0, 0.0

            elif w < 0.80:
                t = (w - 0.60) / 0.20
                r, g, b = 1.0, 1.0 - (0.5 * t), 0.0

            # 💥 3. 只要小于 1.0，哪怕是 0.999999，也会走这里的插值
            # 当 w = 0.999999 时，t 几乎等于 1，计算结果为 (1, 近乎0, 0) -> 视觉上依然是绝对的纯红！
            elif w < 1.0:
                t = (w - 0.80) / 0.20
                r, g, b = 1.0, 0.5 - (0.5 * t), 0.0

            # 💥 4. 绝对为 1.0 (或大于1.0)：显示为纯白！
            else:
                r, g, b = 1.0, 1.0, 1.0

            color_view[i, 0] = r
            color_view[i, 1] = g
            color_view[i, 2] = b
            color_view[i, 3] = 0.0


@cython.boundscheck(False)
@cython.wraparound(False)
def render_gradient(weights_1d: cython.float[:], color_view: cython.float[:, :], color_a: tuple, color_b: tuple):
    """通用双色插值器 (纯 Python 语法)"""
    N: cython.int = color_view.shape[0]
    i: cython.int
    w: cython.float

    # 在进入 C 循环前，解包 tuple 为单精度浮点数
    bg_r: cython.float = color_a[0]
    bg_g: cython.float = color_a[1]
    bg_b: cython.float = color_a[2]
    bg_a: cython.float = color_a[3]

    fg_r: cython.float = color_b[0]
    fg_g: cython.float = color_b[1]
    fg_b: cython.float = color_b[2]
    fg_a: cython.float = color_b[3]

    with cython.nogil:
        for i in range(N):
            w = weights_1d[i]
            color_view[i, 0] = bg_r + w * (fg_r - bg_r)
            color_view[i, 1] = bg_g + w * (fg_g - bg_g)
            color_view[i, 2] = bg_b + w * (fg_b - bg_b)
            color_view[i, 3] = bg_a + w * (fg_a - bg_a)


@cython.boundscheck(False)
@cython.wraparound(False)
def render_fill(color_view: cython.float[:, :], color: tuple):
    """纯色填充器 (纯 Python 语法)"""
    N: cython.int = color_view.shape[0]
    i: cython.int

    r: cython.float = color[0]
    g: cython.float = color[1]
    b: cython.float = color[2]
    a: cython.float = color[3]

    with cython.nogil:
        for i in range(N):
            color_view[i, 0] = r
            color_view[i, 1] = g
            color_view[i, 2] = b
            color_view[i, 3] = a


@cython.boundscheck(False)
@cython.wraparound(False)
def render_brush_gradient(
    color_view: cython.float[:, :],
    hit_indices: cython.int[:],
    hit_weights: cython.float[:],
    hit_count: cython.int,
    color_a: tuple,
    color_b: tuple,
):
    """散点渐变器：专门用于通过顶点ID精准映射笔刷衰减颜色"""
    i: cython.int
    v_idx: cython.int
    w: cython.float

    bg_r: cython.float = color_b[0]
    bg_g: cython.float = color_b[1]
    bg_b: cython.float = color_b[2]
    bg_a: cython.float = color_b[3]
    fg_r: cython.float = color_a[0]
    fg_g: cython.float = color_a[1]
    fg_b: cython.float = color_a[2]
    fg_a: cython.float = color_a[3]

    with cython.nogil:
        # 💥 核心：只循环 hit_count 次，绝不多算一点！
        for i in range(hit_count):
            v_idx = hit_indices[i]  # 拿到真实的顶点 ID
            w = hit_weights[i]  # 拿到对应的衰减权重

            # 精准投放到对应的显存位置
            color_view[v_idx, 0] = bg_r + w * (fg_r - bg_r)
            color_view[v_idx, 1] = bg_g + w * (fg_g - bg_g)
            color_view[v_idx, 2] = bg_b + w * (fg_b - bg_b)
            color_view[v_idx, 3] = bg_a + w * (fg_a - bg_a)


# =====================================================================
# 3. 渲染管线辅助函数 (直接向 Maya VP2 缓冲区写入数据)
# =====================================================================
@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nogil
def _offset_indices_direct(
    src_ptr: cython.p_uint,
    dst_ptr: cython.p_uint,
    count: cython.int,
    offset: cython.uint,
) -> cython.void:
    # 👆 💥 加上 -> cython.void:
    i: cython.int
    for i in range(count):
        dst_ptr[i] = src_ptr[i] + offset


def offset_indices_direct(
    src_addr: cython.Py_ssize_t,
    dst_addr: cython.Py_ssize_t,
    count: cython.int,
    offset: cython.int,
):
    """Python 包装器：接收整型地址，强转为 unsigned int 指针"""
    src_ptr = cython.cast(cython.p_uint, src_addr)
    dst_ptr = cython.cast(cython.p_uint, dst_addr)

    _offset_indices_direct(src_ptr, dst_ptr, count, cython.cast(cython.uint, offset))
