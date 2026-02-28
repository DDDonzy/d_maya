import cython


# =====================================================================
# 模块 1：纯粹的空间碰撞与衰减引擎 (终极优化版)
# =====================================================================
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.initializedcheck(False)  # 进一步关闭变量初始化检查，压榨最后一点性能
@cython.ccall
def calculate_brush_falloff_volume(
                                    points      : cython.float[:, ::1],  
                                    hit_xyz     : tuple,                 
                                    radius      : cython.float,
                                    falloff_mode: cython.int,            
                                    out_indices : cython.int[:],
                                    out_weights : cython.float[:],
) -> cython.int:
    i        : cython.int
    hit_count: cython.int = 0
    num_verts: cython.int = points.shape[0]

    hit_x    : cython.float = hit_xyz[0]
    hit_y    : cython.float = hit_xyz[1]
    hit_z    : cython.float = hit_xyz[2]

    # 💥 优化 1：预先计算 AABB 包围盒边界 (极速剔除用)
    min_x: cython.float = hit_x - radius
    max_x: cython.float = hit_x + radius
    min_y: cython.float = hit_y - radius
    max_y: cython.float = hit_y + radius
    min_z: cython.float = hit_z - radius
    max_z: cython.float = hit_z + radius

    vx     : cython.float
    vy     : cython.float
    vz     : cython.float
    dx     : cython.float
    dy     : cython.float
    dz     : cython.float
    dist_sq: cython.float
    dist   : cython.float
    weight : cython.float
    t      : cython.float

    radius_sq: cython.float = radius * radius

    for i in range(num_verts):
        vx = points[i, 0]
        # 💥 极速剔除：如果 X 轴超出包围盒，直接跳过！(下同)
        if vx < min_x or vx > max_x: 
            continue
        vy = points[i, 1]
        if vy < min_y or vy > max_y: 
            continue
        vz = points[i, 2]
        if vz < min_z or vz > max_z: 
            continue

        # 能活到这里的点，说明已经在这个正方体包围盒里了，命中率极高
        dx = vx - hit_x
        dy = vy - hit_y
        dz = vz - hit_z

        dist_sq = dx * dx + dy * dy + dz * dz

        # 进一步判断是否在精确的球体内部
        if dist_sq <= radius_sq:
            
            # 💥 优化 3：实心笔刷短路计算，直接给 1.0，连开方都不用做！
            if falloff_mode == 2:  # Solid
                weight = 1.0
            else:
                # 💥 优化 2：调用纯 C 的单精度开方，比 **0.5 快得多
                dist = dist_sq ** 0.5
                t = dist / radius  

                if falloff_mode == 0:    # Linear
                    weight = 1.0 - t
                else:                    # SmoothStep (假设 falloff_mode == 1)
                    weight = 1.0 - (t * t * (3.0 - 2.0 * t))

            out_indices[hit_count] = i
            out_weights[hit_count] = weight
            hit_count += 1

    return hit_count


# =====================================================================
# 模块 2：纯粹的 1D 数学笔刷
# =====================================================================
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def brush_math(
    hit_indices   : cython.int[:],     
    hit_weights   : cython.float[:],   
    hit_count     : cython.int,        
    brush_strength: cython.float,      
    brush_mode    : cython.int,        
    modify_view   : cython.float[:],   
):
    """
    通用一维数组修改引擎。
    执行具体的加/减/替换运算。它只负责修改传入的 1D 数据。

    Args:
        hit_indices (cython.int[:]): 被笔刷影响的顶点 ID 数组 (由模块1输出)。
        hit_weights (cython.float[:]): 对应顶点的笔刷空间衰减遮罩 (由模块1输出)。
        hit_count (cython.int): 实际命中的顶点数量，用于限制遍历范围。
        brush_strength (cython.float): 笔刷设定的基础力道/强度。在 Replace 模式下代表目标权重。
        brush_mode (cython.int): 运算模式。0: Add(相加), 1: Subtract(相减), 2: Replace(插值替换), 3: Multiply(相乘)。
        modify_view (cython.float[:]): [输入/输出] 待修改的目标数据 1D 视图。
    """
    i    : cython.int
    v_idx: cython.int
    mask : cython.float
    val  : cython.float

    for i in range(hit_count):
        v_idx = hit_indices[i]
        mask = hit_weights[i]

        if mask <= 0.0:
            continue

        val = modify_view[v_idx]

        if brush_mode == 0:    # Add
            val += brush_strength * mask
        elif brush_mode == 1:  # Sub
            val -= brush_strength * mask
        elif brush_mode == 2:  # Replace
            val += (brush_strength - val) * mask
        elif brush_mode == 3:  # Mult
            val *= brush_strength * mask

        if val < 0.0:
            val = 0.0
        elif val > 1.0:
            val = 1.0

        modify_view[v_idx] = val


# =====================================================================
# 模块 3：蒙皮专用的后处理模块
# =====================================================================
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.ccall
def post_process_skin_weights(
    modify_bone : cython.int,    
    bone_locks  : cython.uchar[:],
    hit_indices : cython.int[:],
    hit_count   : cython.int,
    weights_view: cython.float[:, ::1],   
):
    """
    蒙皮权重归一化后处理引擎 (Interactive Normalization)。
    在目标骨骼权重被修改后，负责按比例自动缩放 (吸血/反哺) 该顶点上其他未锁定的骨骼权重，确保顶点总权重始终维持在 1.0。

    Args:
        modify_bone (cython.int): 刚才被画笔修改的目标骨骼索引 (它是归一化的基准点，不能被缩放)。
        bone_locks (cython.uchar[:]): 全局骨骼锁定状态数组。形状为 [骨骼总数]。(0: 未锁定, 1: 锁定)。
        hit_indices (cython.int[:]): 刚才被笔刷影响的顶点 ID 数组。只对这些脏顶点进行归一化。
        hit_count (cython.int): 命中的顶点数量。
        weights_view (cython.float[:, ::1]): 完整的 2D 蒙皮权重底图视图。形状为 [顶点总数, 骨骼总数]。
    """
    i                 : cython.int
    j                 : cython.int
    v_idx             : cython.int
    num_bones         : cython.int = weights_view.shape[1]
    locked_sum        : cython.float
    target_w          : cython.float
    sum_other_unlocked: cython.float
    remaining         : cython.float
    ratio             : cython.float
    unlocked_count    : cython.int

    for i in range(hit_count):
        v_idx = hit_indices[i]

        locked_sum = 0.0
        sum_other_unlocked = 0.0
        unlocked_count = 0

        for j in range(num_bones):
            if j == modify_bone:
                continue

            if bone_locks[j] == 1:
                locked_sum += weights_view[v_idx, j]
            else:
                sum_other_unlocked += weights_view[v_idx, j]
                unlocked_count += 1

        target_w = weights_view[v_idx, modify_bone]

        if target_w > 1.0 - locked_sum:
            target_w = 1.0 - locked_sum
            weights_view[v_idx, modify_bone] = target_w

        remaining = 1.0 - locked_sum - target_w

        if unlocked_count == 0:
            weights_view[v_idx, modify_bone] = 1.0 - locked_sum
            continue

        if sum_other_unlocked > 0.000001:
            ratio = remaining / sum_other_unlocked
            for j in range(num_bones):
                if j != modify_bone and bone_locks[j] == 0:
                    weights_view[v_idx, j] *= ratio
        else:
            if remaining > 0.000001:
                ratio = remaining / unlocked_count
                for j in range(num_bones):
                    if j != modify_bone and bone_locks[j] == 0:
                        weights_view[v_idx, j] = ratio


# =====================================================================
# 模块 4：总调度枢纽
# =====================================================================
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def skin_weight_brush(
    points_view   : cython.float[:, ::1],
    hit_xyz       : tuple,
    radius        : cython.float,
    falloff_mode  : cython.int,
    brush_strength: cython.float,
    brush_mode    : cython.int,
    modify_bone   : cython.int,
    bone_locks    : cython.uchar[:],
    weights_view  : cython.float[:, ::1],
    modify_indices   : cython.int[:],
    modify_weights   : cython.float[:],
) -> cython.int:
    """
    蒙皮权重笔刷总入口 (Pipeline Orchestrator)。
    一键式调用，顺序执行：空间碰撞检测 -> 目标骨骼权重计算 -> 全局归一化修正。

    Args:
        points_view (cython.float[:, ::1]): 模型顶点坐标 2D 连续视图 [N, 3]。
        hit_xyz (tuple): 笔刷击中模型的 3D 空间坐标 (x, y, z)。
        radius (cython.float): 笔刷绝对空间半径。
        falloff_mode (cython.int): 笔刷衰减模式 (0: Linear, 1: Smooth, 2: Solid)。
        brush_strength (cython.float): 笔刷强度 / 目标权重值。
        brush_mode (cython.int): 绘制模式 (0: Add, 1: Sub, 2: Replace, 3: Mult)。
        modify_bone (cython.int): 当前选择绘制的目标骨骼索引。
        bone_locks (cython.uchar[:]): 全局骨骼锁定状态 1D 数组 [M]。
        weights_view (cython.float[:, ::1]): 被修改图层的完整权重 2D 连续视图 [N, M]。
        out_indices (cython.int[:]): [缓存] 用于存储命中的顶点 ID 的一维数组。长度需满足最大潜在命中数 (通常等于总顶点数 N)。
        out_weights (cython.float[:]): [缓存] 用于存储对应顶点遮罩权重的一维数组。

    Returns:
        cython.int: 成功修改的顶点数量 (hit_count)。若为 0 代表笔刷落空或目标骨骼被锁定。
    """
    hit_count: cython.int

    if bone_locks[modify_bone] == 1:
        return 0

    hit_count = calculate_brush_falloff_volume(
        points_view,         
        hit_xyz,
        radius,
        falloff_mode,
        modify_indices,
        modify_weights
    )

    if hit_count == 0:
        return 0

    brush_math(
        modify_indices,
        modify_weights,
        hit_count,
        brush_strength,
        brush_mode,
        weights_view[:, modify_bone]  
    )

    post_process_skin_weights(
        modify_bone,
        bone_locks,
        modify_indices,
        hit_count,
        weights_view,
    )

    return hit_count