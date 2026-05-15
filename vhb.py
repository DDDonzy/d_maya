from maya import mel
import maya.cmds as cmds

# ==========================================
# 算法全局常量 (控制 BVH 分裂的甜点参数)
# ==========================================
MAX_FACES_PER_LEAF = 4   # 甜点参数1：叶子节点最多容纳的三角形数量 (通常为 4~16)
MAX_DEPTH = 32           # 甜点参数2：树的最大深度，防止堆栈溢出 (通常为 32 或 64)

# ==========================================
# 1. 核心数据结构
# ==========================================
class AABB:
    def __init__(self, min_pt, max_pt):
        self.min = [min_pt[0], min_pt[1], min_pt[2]]
        self.max = [max_pt[0], max_pt[1], max_pt[2]]
        
    def merge(self, other):
        new_min = [min(self.min[i], other.min[i]) for i in range(3)]
        new_max = [max(self.max[i], other.max[i]) for i in range(3)]
        return AABB(new_min, new_max)
        
    def get_center_and_size(self):
        center = [(self.max[i] + self.min[i]) * 0.5 for i in range(3)]
        size = [self.max[i] - self.min[i] for i in range(3)]
        size = [max(0.01, s) for s in size] # 防止极薄的面片导致视觉不可见
        return center, size

class BVHNode:
    def __init__(self, level=0):
        self.aabb = None
        self.left = None
        self.right = None
        self.faces = [] 
        self.is_leaf = False
        self.level = level    
        self.vis_cube = None 

    def compute_bounds(self, faces, mesh_name):
        min_pt = [float('inf')] * 3
        max_pt = [-float('inf')] * 3
        
        for face in faces:
            vtx_list = cmds.polyInfo(f"{mesh_name}.f[{face}]", faceToVertex=True)[0].split()[2:]
            for v_idx in vtx_list:
                pos = cmds.xform(f"{mesh_name}.vtx[{v_idx}]", q=True, t=True, ws=True)
                min_pt = [min(min_pt[i], pos[i]) for i in range(3)]
                max_pt = [max(max_pt[i], pos[i]) for i in range(3)]
        return AABB(min_pt, max_pt)

    def get_face_centroid(self, face, mesh_name):
        """新增：获取单个三角形(面)的中心点坐标"""
        vtx_list = cmds.polyInfo(f"{mesh_name}.f[{face}]", faceToVertex=True)[0].split()[2:]
        centroid = [0.0, 0.0, 0.0]
        for v_idx in vtx_list:
            pos = cmds.xform(f"{mesh_name}.vtx[{v_idx}]", q=True, t=True, ws=True)
            centroid[0] += pos[0]
            centroid[1] += pos[1]
            centroid[2] += pos[2]
        num_vtx = len(vtx_list)
        return [centroid[0]/num_vtx, centroid[1]/num_vtx, centroid[2]/num_vtx]

    def build(self, faces, mesh_name):
        self.aabb = self.compute_bounds(faces, mesh_name)
        
        if len(faces) <= MAX_FACES_PER_LEAF or self.level >= MAX_DEPTH:
            self.is_leaf = True
            self.faces = faces
            self.create_visual_cube(is_leaf=True)
            return
            
        # ==========================================
        # 🚀 核心优化：空间排序 (沿最长轴)
        # ==========================================
        # 1. 找出当前包围盒的最长轴 (0:X, 1:Y, 2:Z)
        size_x = self.aabb.max[0] - self.aabb.min[0]
        size_y = self.aabb.max[1] - self.aabb.min[1]
        size_z = self.aabb.max[2] - self.aabb.min[2]
        
        longest_axis = 0
        if size_y > size_x and size_y > size_z:
            longest_axis = 1
        elif size_z > size_x and size_z > size_y:
            longest_axis = 2
            
        # 2. 根据面中心点在最长轴上的坐标，对 faces 数组进行排序
        faces.sort(key=lambda f: self.get_face_centroid(f, mesh_name)[longest_axis])
        
        # 3. 再进行中点切割（此时切开的已经是空间上相邻的面了）
        mid = len(faces) // 2
        
        self.left = BVHNode(self.level + 1)
        self.left.build(faces[:mid], mesh_name)
        
        self.right = BVHNode(self.level + 1)
        self.right.build(faces[mid:], mesh_name)
        
        self.create_visual_cube(is_leaf=False)
        
        if self.left and self.left.vis_cube:
            cmds.parent(self.left.vis_cube, self.vis_cube)
        if self.right and self.right.vis_cube:
            cmds.parent(self.right.vis_cube, self.vis_cube)
            
        if self.level == 0 and cmds.objExists("BVH_Visualization_Grp"):
            cmds.parent(self.vis_cube, "BVH_Visualization_Grp")

    def create_visual_cube(self, is_leaf):
        node_type = "Leaf" if is_leaf else "Node"
        self.vis_cube = cmds.polyCube(name=f"BVH_{node_type}_Lvl{self.level}_#", ch=False)[0]
        
        cmds.setAttr(f"{self.vis_cube}.overrideEnabled", 1)
        cmds.setAttr(f"{self.vis_cube}.overrideShading", 0)
        cmds.setAttr(f"{self.vis_cube}.inheritsTransform", 0)
        
        color = 14 if is_leaf else (13 if self.level == 0 else 17)
        cmds.setAttr(f"{self.vis_cube}.overrideColor", color)
        
        self.update_visual_cube()

    def update_visual_cube(self):
        center, size = self.aabb.get_center_and_size()
        cmds.xform(self.vis_cube, t=center, s=size, ws=True)

    def refit(self, mesh_name):
        if self.is_leaf:
            self.aabb = self.compute_bounds(self.faces, mesh_name)
        else:
            self.left.refit(mesh_name)
            self.right.refit(mesh_name)
            self.aabb = self.left.aabb.merge(self.right.aabb)
            
        self.update_visual_cube()

# ==========================================
# 2. 场景管理与 UI 绑定
# ==========================================
global_bvh_root = None
global_target_mesh = None

def cleanup_old_bvh():
    """清理旧的视觉包围盒组"""
    if cmds.objExists("BVH_Visualization_Grp"):
        cmds.delete("BVH_Visualization_Grp")

def setup_scene_from_selection(*args):
    global global_bvh_root, global_target_mesh
    
    # 1. 获取用户当前选择的模型
    selection = cmds.ls(selection=True, type="transform")
    if not selection:
        cmds.warning("请先在视图中选择一个多边形模型！")
        return
        
    mesh_transform = selection[0]
    
    # 检查是否有 polygon shape
    shapes = cmds.listRelatives(mesh_transform, shapes=True, type="mesh")
    if not shapes:
        cmds.warning("选择的物体不是一个有效的多边形网格！")
        return
        
    global_target_mesh = mesh_transform
    
    # 2. 获取网格的面数
    num_faces = cmds.polyEvaluate(global_target_mesh, face=True)
    
    # 【安全锁】防止 Maya 因生成过多包围盒而卡死
    if num_faces > 500:
        cmds.warning(f"模型面数（{num_faces}面）过高！为了防止 Maya 崩溃，请使用小于 500 面的低模进行可视化测试。")
        return
        
    faces = list(range(num_faces))
    
    # 3. 清理旧数据，创建存放包围盒的干净组
    cleanup_old_bvh()
    cmds.group(empty=True, name="BVH_Visualization_Grp")
    
    # 4. 构建动态 BVH
    print(f"正在为 {global_target_mesh} 构建 BVH，包含 {num_faces} 个面...")
    global_bvh_root = BVHNode(level=0)
    global_bvh_root.build(faces, global_target_mesh)
    
    # 展开 Outliner 中的组
    cmds.select("BVH_Visualization_Grp")
    import mel
    mel.eval('OutlinerWindow;')
    
    # 切换到顶点模式方便拖拽测试
    cmds.select(clear=True)
    cmds.hilite(global_target_mesh)
    cmds.selectType(vertex=True)
    print(">> BVH 构建完成！请拖拽顶点并点击 Refit 观察更新。")

def perform_refit(*args):
    global global_bvh_root, global_target_mesh
    if global_bvh_root and global_target_mesh:
        if cmds.objExists(global_target_mesh):
            global_bvh_root.refit(global_target_mesh)
            print(">> BVH 包围盒 Refit 完毕！")
        else:
            cmds.warning("原始模型已被删除，无法执行 Refit。")

# ==========================================
# 3. 创建极简操作 UI
# ==========================================
if cmds.window("BVH_Demo_UI", exists=True):
    cmds.deleteUI("BVH_Demo_UI")
    
window = cmds.window("BVH_Demo_UI", title="自定义网格 Dynamic BVH", widthHeight=(280, 160))
cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 10))

cmds.text(label=f"\n当前限制: 最大深度={MAX_DEPTH}, 叶子容量={MAX_FACES_PER_LEAF}", align="center", font="smallObliqueLabelFont")

cmds.text(label="1. 选中任意模型 (建议 <500 面)", align="center")
cmds.button(label="根据所选模型生成 BVH", command=setup_scene_from_selection, bgc=(0.2, 0.4, 0.6))

cmds.text(label="2. 在视图中随意拖拽模型的顶点\n3. 点击 Refit 观察包围盒瞬间更新", align="center")
cmds.button(label="✨ 执行 Refit (重构)", command=perform_refit, bgc=(0.6, 0.3, 0.2))

cmds.showWindow(window)