# (您可以将这整块代码复制到您的文件中)

import maya.api.OpenMaya as om


class OctreeNode:
    """八叉树的节点(簇块)类。"""

    def __init__(self, bounds, depth):
        self.bounds = bounds          # 该节点的包围盒 (om.MBoundingBox)
        self.depth = depth            # 节点在树中的深度
        self.points_indices = []      # 如果是叶子节点，存储顶点索引
        self.children = []            # 存储八个子节点
        self.is_leaf = True           # 默认为叶子节点


class Octree:
    """
    八叉树加速结构主类。
    负责构建整个树，并提供查询方法。
    """

    def __init__(self,
                 points: om.MPointArray,
                 max_depth=10,
                 min_points_per_node=32):
        """
        初始化并构建八叉树。
        Args:
            points (om.MPointArray): 模型所有顶点的世界空间坐标数组。
            max_depth (int): 树的最大划分深度。
            min_points_per_node (int): 节点中包含的最少点数，低于此数目则不继续划分。
        """
        self.points = points
        self.max_depth = max_depth
        self.min_points_per_node = min_points_per_node

        # 计算根节点的包围盒，使其能包裹所有点
        root_bounds = om.MBoundingBox()
        for p in points:
            root_bounds.expand(p)

        # 创建根节点并开始递归划分
        self.root = OctreeNode(root_bounds, 0)
        all_points_indices = range(len(points))
        self._subdivide(self.root, all_points_indices)

    def _subdivide(self,
                   node: OctreeNode,
                   point_indices: list[int]):
        """
        (私有方法) 递归地划分节点。
        """
        # 终止条件：达到最大深度或节点内的点数过少
        if (node.depth >= self.max_depth) or (len(point_indices) <= self.min_points_per_node):
            node.points_indices = point_indices
            return

        node.is_leaf = False
        center = node.bounds.center

        # 为8个子象限创建临时的点索引列表
        child_point_indices = [[] for _ in range(8)]

        # 将当前节点的点分配到对应的子象限中
        for idx in point_indices:
            p = self.points[idx]
            octant = 0  # 通过位运算快速判断象限
            if p.x > center.x:
                octant |= 1
            if p.y > center.y:
                octant |= 2
            if p.z > center.z:
                octant |= 4
            child_point_indices[octant].append(idx)

        # 递归地为包含点的子节点进行划分
        for i in range(8):
            if not child_point_indices[i]:
                continue

            # 计算子节点的精确包围盒
            min_p, max_p = node.bounds.min, node.bounds.max
            c_min = om.MPoint(min_p)
            c_max = om.MPoint(center)

            if i & 1:
                c_min.x, c_max.x = center.x, max_p.x
            if i & 2:
                c_min.y, c_max.y = center.y, max_p.y
            if i & 4:
                c_min.z, c_max.z = center.z, max_p.z

            child_bounds = om.MBoundingBox(c_min, c_max)
            child_node = OctreeNode(child_bounds, node.depth + 1)
            node.children.append(child_node)
            self._subdivide(child_node, child_point_indices[i])

    def query_sphere(self, sphere_center: om.MPoint, sphere_radius: float) -> list[int]:
        """
        广阶段查询：返回所有可能在球体范围内的顶点的索引。
        """
        candidate_indices = []
        if self.root:
            self._query_sphere_recursive(self.root, sphere_center, sphere_radius, candidate_indices)
        return candidate_indices

    def _query_sphere_recursive(self, node: OctreeNode, sphere_center, sphere_radius, candidate_indices):
        # 检查球体是否与节点的包围盒相交
        if not self._sphere_intersects_aabb(sphere_center, sphere_radius, node.bounds):
            return  # 剪枝：如果不相交，则忽略此节点及其所有子节点

        if node.is_leaf:
            candidate_indices.extend(node.points_indices)
            return

        for child in node.children:
            self._query_sphere_recursive(child, sphere_center, sphere_radius, candidate_indices)

    def _sphere_intersects_aabb(self, sphere_center: om.MPoint, sphere_radius: float, box: om.MBoundingBox) -> bool:
        """
        (私有方法) 判断球体和轴对齐包围盒是否相交。
        """
        # 找到包围盒上离球心最近的点
        closest_point_in_box = om.MFloatPoint()
        closest_point_in_box.x = max(box.min.x, min(sphere_center.x, box.max.x))
        closest_point_in_box.y = max(box.min.y, min(sphere_center.y, box.max.y))
        closest_point_in_box.z = max(box.min.z, min(sphere_center.z, box.max.z))

        # 如果最近点到球心的距离的平方，小于半径的平方，则相交

        distance_squared = sphere_center.distanceTo(closest_point_in_box)
        return distance_squared < sphere_radius
