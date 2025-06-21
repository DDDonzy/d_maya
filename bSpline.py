from maya.api import OpenMaya as om
from typing import List


class CurveData:
    def __init__(self, controlPoints: List[om.MVector], degree: int = 3):
        self.degree = degree
        self.controlPoints = controlPoints  # 修正了原始代码中的变量名笔误
        self.controlPointsCount = len(controlPoints)
        # 确保有足够的控制点来定义曲线
        if self.controlPointsCount <= self.degree:
            raise ValueError("Control points count must be greater than the degree.")
        self.knots = self.generateKnots()

    def generateKnots(self) -> List[float]:
        """
        生成一个标准的(clamped) B-样条结向量。
        曲线将在参数 0 到 1 之间定义。
        """
        d = self.degree
        count = self.controlPointsCount

        # 结的总数是 m = n + p + 1，其中 n 是控制点索引(0 to count-1), p 是阶数
        # m = (count - 1) + d + 1 + 1 = count + d + 1
        num_knots = count + d + 1

        knots: list = [0.0] * (d + 1)

        # 中间的结
        # 修正了原始的计算方式，使其更通用和准确
        # 内部结点的数量是 count - d - 1
        middle_knot_count = count - d - 1
        if middle_knot_count > 0:
            # 此处的分母应该是 count - d
            knots.extend([i / (count - d) for i in range(1, count - d)])

        knots.extend([1.0] * (d + 1))

        # 这是一个小修正，确保即使在 count-d=0 的情况下也能正确生成
        if len(knots) != num_knots:
            knots = [0.0] * (d + 1)
            knots.extend([1.0] * (d + 1))

        return knots

    def basisFunction(self, controlPointIdx: int, parameter: float, degree: int) -> float:
        """
        递归计算第 i 个 d 次的B样条基函数 N_{i,d}(t) 的值。
        """
        d = degree
        t = parameter
        i = controlPointIdx
        knots = self.knots

        if d == 0:
            # 特殊情况处理：当 t=1.0 时，它应该落在最后一个区间内。
            is_last_knot = knots[i] < knots[i + 1] and knots[i + 1] == 1.0
            if (knots[i] <= t < knots[i + 1]) or (t == 1.0 and is_last_knot):
                return 1.0
            else:
                return 0.0
        else:
            denom1 = knots[i + d] - knots[i]
            denom2 = knots[i + d + 1] - knots[i + 1]

            term1 = 0.0
            if denom1 > 1e-9:  # 避免除以零
                term1 = (t - knots[i]) / denom1 * self.basisFunction(i, t, d - 1)

            term2 = 0.0
            if denom2 > 1e-9:  # 避免除以零
                term2 = (knots[i + d + 1] - t) / denom2 * self.basisFunction(i + 1, t, d - 1)

            return term1 + term2

    def get_weights_by_parameter(self, parameter: float) -> List[float]:
        return [self.basisFunction(i, parameter, self.degree) for i in range(self.controlPointsCount)]

    def get_position_by_parameter(self, parameter: float) -> om.MVector:
        t = parameter
        d = self.degree
        pos = om.MVector()
        for i, cp in enumerate(self.controlPoints):
            w = self.basisFunction(i, t, d)
            pos += cp * w
        return pos
