import cython
from cython.parallel import prange  # type: ignore


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.exceptval(check=False)
@cython.nogil
def _accumulate_layer_weights(
    in_out_weights: cython.p_float,
    layer_weights: cython.p_float,
    layer_mask: cython.p_float,
    num_verts: cython.int,
    num_bones: cython.int,
) -> cython.void:
    """
    纯 C 内核：将 Layer 的权重乘以 Mask 后，累加 (+=) 到 in_out_weights 中。
    """
    v: cython.int
    b: cython.int
    idx: cython.int
    m: cython.float

    for v in prange(num_verts):
        m = layer_mask[v]

        # 🚀 极致优化 1：完全无遮罩 (Mask == 0) -> 直接跳过
        if m < 0.000001:
            continue

        # 🚀 极致优化 2：完全生效 (Mask == 1) -> 纯粹的向量加法
        if m > 0.999999:
            for b in range(num_bones):
                idx = v * num_bones + b
                in_out_weights[idx] += layer_weights[idx]

        # 🚀 常规计算：半透明遮罩 (0 < Mask < 1) -> 乘加融合 (FMA)
        else:
            for b in range(num_bones):
                idx = v * num_bones + b
                in_out_weights[idx] += layer_weights[idx] * m


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.exceptval(check=False)
@cython.nogil
def _fill_float_array(
    arr: cython.float[:],
    length: cython.int,
    value: cython.float,
) -> cython.void:
    """纯 C 内核：直接接收类型化内存视图，安全且极速"""
    i: cython.int
    for i in range(length):
        arr[i] = value


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.nogil
@cython.exceptval(check=False)  # 1. 消除 GIL 异常检查警告
def _normalize_weights(
    weights: cython.p_float,
    num_verts: cython.int,
    num_bones: cython.int,
) -> cython.void:
    """
    [纯 C 内核] 并行归一化权重数组
    """
    v: cython.int
    b: cython.int
    total: cython.float
    scale: cython.float
    idx: cython.int
    base_idx: cython.int

    # 使用 OpenMP 并行加速
    for v in prange(num_verts, nogil=True):
        # 必须在循环内部初始化 total
        total = 0.0
        base_idx = v * num_bones

        # 第一轮：计算总和
        for b in range(num_bones):
            # 🚀 2. 关键修改！
            # 不要用 total += ...，这会触发 Cython 的 Reduction 误判
            # 改用 total = total + ...，编译器就会知道这是个普通的局部累加
            total = total + weights[base_idx + b]

        # 第二轮：执行归一化
        if total > 0.000001:
            if (total - 1.0 > 0.0001) or (1.0 - total > 0.0001):
                scale = 1.0 / total
                for b in range(num_bones):
                    # 同理，虽然这里乘法没问题，但保持一致性
                    idx = base_idx + b
                    weights[idx] = weights[idx] * scale
        else:
            # 孤立点处理
            weights[base_idx] = 1.0


# =====================================================================
# 暴露给 Python 的包装器
# =====================================================================
def accumulate_layer_weights(
    in_out_view: cython.float[:],
    layer_view: cython.float[:],
    mask_view: cython.float[:],
    num_verts: cython.int,
    num_bones: cython.int,
):
    out_ptr = cython.cast(cython.p_float, cython.address(in_out_view[0]))
    layer_ptr = cython.cast(cython.p_float, cython.address(layer_view[0]))
    mask_ptr = cython.cast(cython.p_float, cython.address(mask_view[0]))
    _accumulate_layer_weights(
        out_ptr,
        layer_ptr,
        mask_ptr,
        num_verts,
        num_bones,
    )


def normalize_weights(
    weights_view: cython.float[:],
    num_verts: cython.int,
    num_bones: cython.int,
):

    if weights_view.shape[0] == 0:
        return

    weights_ptr: cython.p_float = cython.cast(cython.p_float, cython.address(weights_view[0]))

    _normalize_weights(weights_ptr, num_verts, num_bones)


def fill_float_array(
    arr_view: cython.float[:],
    value: cython.float,
):
    """供 Python 调用的数组填充包装器"""
    if arr_view.shape[0] == 0:
        return

    length: cython.int = arr_view.shape[0]

    _fill_float_array(arr_view, length, value)
