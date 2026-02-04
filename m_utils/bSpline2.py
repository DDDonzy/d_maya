from maya.api import OpenMaya as om


class CurveData(om.MFnNurbsCurve):
    """
    B-样条曲线数据类
    继承自 Maya OpenMaya 的 MFnNurbsCurve，提供 B-样条曲线的创建和操作功能
    """

    def __init__(self, controlPoints, degree):
        """
        Args:
            controlPoints (MPointArray or list): 控制点
            degree (int): 曲线度数
        """
        super().__init__()

        # 确保控制点是 MPointArray 格式
        if not isinstance(controlPoints, om.MPointArray):
            temp_pts = om.MPointArray()
            for p in controlPoints:
                temp_pts.append(om.MPoint(p))
            controlPoints = temp_pts

        # 1. 生成符合数学定义的完整节点向量 (n+d+1)
        full_knots = self.generate_knots(len(controlPoints), degree)
        self._cache_knots = full_knots

        # 2. 创建 NURBS 数据存储器
        self.data = om.MFnNurbsCurveData().create()

        # Maya API 要求传入 n+d-1 个节点，即去掉 full_knots 的首尾各一个
        maya_knots = om.MDoubleArray(full_knots[1:-1])

        self.create(controlPoints, maya_knots, degree, om.MFnNurbsCurve.kOpen, False, True, self.data)

    @staticmethod
    def generate_knots(count, degree):
        """生成标准 Clamped 节点向量 (n+d+1)"""
        knots = [0.0] * (degree + 1)
        interior_count = count - degree - 1
        if interior_count > 0:
            for i in range(1, interior_count + 1):
                knots.append(i / (interior_count + 1))
        knots.extend([1.0] * (degree + 1))
        return knots

    def get_tWeights(self, t):
        """
        使用迭代 Cox-de Boor 算法计算权重
        """
        degree = self.degree
        knots = self._cache_knots
        num_cvs = self.numCVs

        # 初始化权重矩阵 [degree + 1][num_cvs + degree]
        # 使用填表法代替递归
        n_table = [[0.0] * (num_cvs + degree) for _ in range(degree + 1)]

        # Step 1: 计算 0 度基函数 (找到 t 所在的区间)
        for i in range(len(knots) - 1):
            if i < len(n_table[0]):
                if knots[i] <= t < knots[i + 1]:
                    n_table[0][i] = 1.0
                elif t == knots[-1] and knots[i] < t <= knots[i + 1]:
                    n_table[0][i] = 1.0

        # Step 2: 迭代计算至目标度数
        for d in range(1, degree + 1):
            for i in range(num_cvs + degree - d):
                denom1 = knots[i + d] - knots[i]
                term1 = ((t - knots[i]) / denom1 * n_table[d - 1][i]) if denom1 > 0 else 0.0

                denom2 = knots[i + d + 1] - knots[i + 1]
                term2 = ((knots[i + d + 1] - t) / denom2 * n_table[d - 1][i + 1]) if denom2 > 0 else 0.0

                n_table[d][i] = term1 + term2

        return n_table[degree][:num_cvs]

    def build(self):
        """在场景中生成实际节点"""
        dag_mod = om.MDagModifier()
        new_obj = dag_mod.createNode("transform", name="bSplineCurve")
        dag_mod.doIt()

        # 使用原始数据重新创建
        self.create(self.cvPositions(), om.MDoubleArray(self.knots()), self.degree, self.form, False, True, new_obj)

        return om.MFnDependencyNode(new_obj).name()
