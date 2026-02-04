def get_nurbs_weights_iterative(t, degree, knots, cp_count):
    """
    使用迭代 Cox-de Boor 算法计算指定参数 t 处的所有控制点权重
    
    Args:
        t (float): 参数值 [0, 1]
        degree (int): 曲线度数 (p)
        knots (list): 节点向量 (长度应为 cp_count + degree + 1)
        cp_count (int): 控制点数量 (n+1)
        
    Returns:
        list: 每个控制点的权重值，长度为 cp_count
    """
    # 1. 初始化基础层 (degree = 0)
    # n_matrix[d][i] 表示 d 度时第 i 个基函数的值
    # 为了节省内存，我们只需要保留当前度和上一度的结果
    # 但为了逻辑清晰，这里展示完整的矩阵思路
    n_matrix = [[0.0] * (cp_count + degree) for _ in range(degree + 1)]

    # 2. 计算 0 度基函数 (阶梯函数)
    # 注意：B-样条定义在半开半闭区间 [t_i, t_{i+1})
    for i in range(len(knots) - 1):
        if i < len(n_matrix[0]):
            if knots[i] <= t < knots[i+1]:
                n_matrix[0][i] = 1.0
            # 特殊处理闭区间末端 t = 1.0 的情况
            elif t == knots[-1] and knots[i] < t <= knots[i+1]:
                 n_matrix[0][i] = 1.0
    # 3. 迭代计算更高阶的基函数
    for d in range(1, degree + 1):
        print(n_matrix)
        for i in range(cp_count + degree - d):
            # 第一项系数计算
            denom1 = knots[i + d] - knots[i]
            term1 = 0.0
            if denom1 > 0:
                term1 = ((t - knots[i]) / denom1) * n_matrix[d-1][i]

            # 第二项系数计算
            denom2 = knots[i + d + 1] - knots[i + 1]
            term2 = 0.0
            if denom2 > 0:
                term2 = ((knots[i + d + 1] - t) / denom2) * n_matrix[d-1][i+1]

            n_matrix[d][i] = term1 + term2

    # 返回最高度数 d=degree 的前 cp_count 个权重
    return n_matrix[degree][:cp_count]

# 1. 设置参数
degree = 3
cp_count = 6
t = 0.5  # 我们想获取曲线中点位置的权重

# 2. 生成节点向量 (Maya 标准的 Clamped 节点向量)
# 对于 degree=3, cp_count=6，节点数 = 6 + 3 + 1 = 10 个
# 形状通常是 [0, 0, 0, 0, 0.33, 0.66, 1, 1, 1, 1]
knots = [0.0] * degree + [i / (cp_count - degree) for i in range(cp_count - degree + 1)] + [1.0] * degree

# 3. 调用函数
weights = get_nurbs_weights_iterative(t, degree, knots, cp_count)

# 4. 查看结果
for i, w in enumerate(weights):
    print(f"控制点 {i} 的权重: {w:.4f}")

print(f"总权重之和: {sum(weights)}") # 结果应为 1.0