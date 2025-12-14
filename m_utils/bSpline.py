"""
B-样条曲线工具类
用于在 Maya 中创建和操作 NURBS 曲线的 B-样条实现
"""
from maya.api import OpenMaya as om
from maya import cmds


class CurveData(om.MFnNurbsCurve):
    """
    B-样条曲线数据类
    继承自 Maya OpenMaya 的 MFnNurbsCurve，提供 B-样条曲线的创建和操作功能
    """

    def __init__(self, controlPoints, degree):
        """
        初始化 B-样条曲线

        Args:
            controlPoints (list): 控制点列表，每个点为 MPoint 对象
            degree (int): 曲线的度数（阶数-1）
        """
        super().__init__()

        # 创建 NURBS 曲线数据对象
        self.data = om.MFnNurbsCurveData().create()
        # 生成节点向量
        self._knots = self.generateKnots(controlPoints, degree)
        # 创建 NURBS 曲线
        # 注意：传入的节点向量需要去掉首尾重复的节点
        self.create(controlPoints,
                    self._knots[1:-1],  # 去掉首尾重复节点
                    degree,
                    om.MFnNurbsCurve.kOpen,  # 开放型曲线
                    False,  # 不是理性曲线
                    True,   # 三维曲线
                    self.data)

    def build(self):
        """
        重建曲线
        使用当前的控制点位置和参数重新创建曲线
        """
        cv = cmds.createNode("transform", name="bSplineCurve")
        sel: om.MSelectionList = om.MGlobal.getSelectionListByName(cv)
        self.create(self.cvPositions(om.MFn.kWorld),  # 获取世界坐标系下的控制点
                    self.knots(),    # 当前节点向量
                    self.degree,     # 当前度数
                    self.form,       # 当前形式（开放/封闭）
                    False,
                    True,
                    sel.getDependNode(0))
        for x in cmds.listRelatives(cv, shapes=1) or []:
            cmds.rename(x, f"{cv}Shape")
        return cv

    def t_length(self, t=1.0):
        """
        根据参数 t 获取曲线长度

        Args:
            t (float): 参数值，范围 [0, 1]

        Returns:
            float: 从曲线起点到参数 t 位置的弧长
        """
        return self.findLengthFromParam(t)

    def parameter(self, length=0):
        """
        根据长度获取对应的parameter参数值

        Args:
            length (float): 从曲线起点开始的长度

        Returns:
            float: 对应的参数值 t
        """
        return self.findParamFromLength(length)

    def get_tWeights(self, t):
        """
        获取参数 t 处所有控制点的基函数权重

        Args:
            t (float): 参数值

        Returns:
            list: 每个控制点对应的基函数值列表
        """
        return [self.basisFunction(i, t, self.degree) for i in range(len(self.cvPositions()))]

    def generateKnots(self, controlPoints, degree):
        """
        为 B-样条曲线生成均匀分布的节点向量

        Args:
            controlPoints (list): 控制点列表
            degree (int): 曲线度数

        Returns:
            list: 节点向量，首尾重复度数次

        Note:
            对于度数为 d 的 B-样条曲线，需要 n+d+1 个节点值
            其中 n 是控制点数量
        """
        d = degree
        count = len(controlPoints)

        # 起始节点：重复度数次的 0.0
        knots = [0.0] * d
        # 内部节点：均匀分布的参数值
        knots += [i / (count - d) for i in range(count - d + 1)]
        # 结束节点：重复度数次的 1.0
        knots += [1.0] * d
        return knots

    def basisFunction(self, i, t, d):
        """
        计算 B-样条基函数值 (Cox-de Boor 递归公式)

        Args:
            i (int): 基函数索引
            t (float): 参数值
            d (int): 度数

        Returns:
            float: 基函数 N_{i,d}(t) 的值

        Note:
            使用 Cox-de Boor 递归公式：
            - 当 d=0 时，N_{i,0}(t) = 1 if t_i <= t < t_{i+1}, else 0
            - 当 d>0 时，N_{i,d}(t) = (t-t_i)/(t_{i+d}-t_i) * N_{i,d-1}(t) + 
                                     (t_{i+d+1}-t)/(t_{i+d+1}-t_{i+1}) * N_{i+1,d-1}(t)
        """
        knots = self._knots

        # 递归终止条件：0度基函数
        if d == 0:
            # 特殊处理边界情况：t=1时包含右端点
            if (knots[i] <= t < knots[i + 1]) or (t == 1 and knots[i] <= t <= knots[i + 1]):
                return 1
            else:
                return 0
        else:
            # 递归计算：Cox-de Boor 公式
            denom1 = knots[i + d] - knots[i]
            denom2 = knots[i + d + 1] - knots[i + 1]

            # 第一项：避免除零错误
            term1 = 0.0 if denom1 == 0.0 else (t - knots[i]) / denom1 * self.basisFunction(i, t, d-1)

            # 第二项：避免除零错误
            term2 = 0.0 if denom2 == 0.0 else (knots[i + d + 1] - t) / denom2 * self.basisFunction(i + 1, t, d-1)

            return term1 + term2
