# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# distutils: language = c++

import cython
from cython.parallel import prange  # type: ignore


# =====================================================================
# 1. 纯 C 级别底层内核 (nogil, 极限狂飙, 只接收裸指针)
# =====================================================================
@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.exceptval(check=False)
@cython.nogil
def _compute_deform_matrices(
    geo_arr: cython.p_double,
    geo_inv_arr: cython.p_double,
    bind_arr: cython.p_double,
    influences_arr: cython.p_double,
    rotate_arr: cython.p_float,
    translate_arr: cython.p_float,
    influences_count: cython.int,
    is_geo_identity: cython.bint,  # 💥 新增开关
) -> cython.void:

    b: cython.int
    i: cython.int
    j: cython.int
    k: cython.int

    T1: cython.double[4][4] = cython.declare(cython.double[4][4])
    T2: cython.double[4][4] = cython.declare(cython.double[4][4])
    Final: cython.double[4][4] = cython.declare(cython.double[4][4])

    for b in range(influences_count):
        # 👑 通道 A：极限狂飙通道 (99%的情况，模型 Transform 为空)
        if is_geo_identity:
            # 既然 Geo 和 GeoInv 都是空气，直接 Final = BindPre * BoneWorld
            for i in range(4):
                for j in range(4):
                    Final[i][j] = 0.0
                    for k in range(4):
                        Final[i][j] += bind_arr[b * 16 + i * 4 + k] * influences_arr[b * 16 + k * 4 + j]

        # 🐌 通道 B：全能兼容通道 (模型 Transform 被瞎挪动了，必须严谨计算)
        else:
            # 1. T1 = Geo * Bind
            for i in range(4):
                for j in range(4):
                    T1[i][j] = 0.0
                    for k in range(4):
                        T1[i][j] += geo_arr[i * 4 + k] * bind_arr[b * 16 + k * 4 + j]

            # 2. T2 = T1 * Bone
            for i in range(4):
                for j in range(4):
                    T2[i][j] = 0.0
                    for k in range(4):
                        T2[i][j] += T1[i][k] * influences_arr[b * 16 + k * 4 + j]

            # 3. Final = T2 * GeoInv
            for i in range(4):
                for j in range(4):
                    Final[i][j] = 0.0
                    for k in range(4):
                        Final[i][j] += T2[i][k] * geo_inv_arr[k * 4 + j]

        # 🎯 提取 3x3 旋转和 1x3 位移 (这部分代码共享)
        for i in range(3):
            for j in range(3):
                rotate_arr[b * 9 + i * 3 + j] = cython.cast(cython.float, Final[i][j])

        translate_arr[b * 3 + 0] = cython.cast(cython.float, Final[3][0])
        translate_arr[b * 3 + 1] = cython.cast(cython.float, Final[3][1])
        translate_arr[b * 3 + 2] = cython.cast(cython.float, Final[3][2])


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.exceptval(check=False)  # 等同于 noexcept
@cython.nogil
def _run_skinning_core(
    ori_pts: cython.p_float,
    out_pts: cython.p_float,
    weights: cython.p_float,
    m_rot: cython.p_float,
    m_trans: cython.p_float,
    num_verts: cython.int,
    num_bones: cython.int,
    envelope: cython.float,
) -> cython.void:

    v: cython.int  # vertex index
    b: cython.int  # bone index
    w: cython.float  # weight
    x: cython.float  # original x
    y: cython.float  # original y
    z: cython.float  # original z
    out_x: cython.float  # output x
    out_y: cython.float  # output y
    out_z: cython.float  # output z

    for v in prange(num_verts):
        x = ori_pts[v * 3 + 0]
        y = ori_pts[v * 3 + 1]
        z = ori_pts[v * 3 + 2]
        out_x = 0.0
        out_y = 0.0
        out_z = 0.0

        for b in range(num_bones):
            w = weights[v * num_bones + b]
            if w < 0.000001:
                continue

            out_x += w * (x * m_rot[b * 9 + 0] + y * m_rot[b * 9 + 3] + z * m_rot[b * 9 + 6] + m_trans[b * 3 + 0])
            out_y += w * (x * m_rot[b * 9 + 1] + y * m_rot[b * 9 + 4] + z * m_rot[b * 9 + 7] + m_trans[b * 3 + 1])
            out_z += w * (x * m_rot[b * 9 + 2] + y * m_rot[b * 9 + 5] + z * m_rot[b * 9 + 8] + m_trans[b * 3 + 2])

        if envelope != 1.0:
            out_x = (out_x - x) * envelope + x
            out_y = (out_y - y) * envelope + y
            out_z = (out_z - z) * envelope + z

        out_pts[v * 3 + 0] = out_x
        out_pts[v * 3 + 1] = out_y
        out_pts[v * 3 + 2] = out_z


# =====================================================================
# 2. Python 接口包装器 (智能提纯：接收视图 -> 提取指针 -> 喂给内核)
# =====================================================================
def compute_deform_matrices(
    geo_matrix: cython.Py_ssize_t,     
    geo_matrix_i: cython.Py_ssize_t,  
    bind_view: cython.double[:, :],
    dyn_view: cython.double[:, :],
    rot_view: cython.float[:, :],
    trans_view: cython.float[:, :],
    geo_matrix_is_identity: cython.bint,
):
    """供 Python 调用的矩阵混合入口，完全基于 MemoryView"""

    # 自动从视图获取长度，无需手动传参
    num_bones: cython.int = bind_view.shape[0]

    # 获取底层原生 C 指针
    geo_mat_ptr = cython.cast(cython.p_double, geo_matrix)
    geo_mat_inv_ptr = cython.cast(cython.p_double, geo_matrix_i)

    bind_ptr = cython.cast(cython.p_double, cython.address(bind_view[0, 0]))
    dyn_ptr = cython.cast(cython.p_double, cython.address(dyn_view[0, 0]))
    rot_ptr = cython.cast(cython.p_float, cython.address(rot_view[0, 0]))
    trans_ptr = cython.cast(cython.p_float, cython.address(trans_view[0, 0]))

    _compute_deform_matrices(
        geo_mat_ptr,
        geo_mat_inv_ptr,
        bind_ptr,
        dyn_ptr,
        rot_ptr,
        trans_ptr,
        num_bones,
        geo_matrix_is_identity,
    )


def run_skinning_core(
    ori_pts_view: cython.float[:],
    out_pts_view: cython.float[:],
    weights_view: cython.float[:],
    rot_view: cython.float[:, :],
    trans_view: cython.float[:, :],
    envelope: cython.float,
):
    """供 Python 调用的蒙皮核心解算入口，完全基于 MemoryView"""

    # 自动从视图获取顶点和骨骼数
    num_verts: cython.int = ori_pts_view.shape[0] // 3
    num_bones: cython.int = trans_view.shape[0]

    # 提取底层原生 C 指针
    ori_ptr = cython.cast(cython.p_float, cython.address(ori_pts_view[0]))
    out_ptr = cython.cast(cython.p_float, cython.address(out_pts_view[0]))
    w_ptr = cython.cast(cython.p_float, cython.address(weights_view[0]))
    rot_ptr = cython.cast(cython.p_float, cython.address(rot_view[0, 0]))
    trans_ptr = cython.cast(cython.p_float, cython.address(trans_view[0, 0]))

    _run_skinning_core(
        ori_ptr,
        out_ptr,
        w_ptr,
        rot_ptr,
        trans_ptr,
        num_verts,
        num_bones,
        envelope,
    )
