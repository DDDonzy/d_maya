import maya.api.OpenMaya as om
import maya.cmds as cmds

# --- 组件 (Components) 相关函数 ---
def get_components_from_plug(plug):
    """从组件列表数据接口（plug）读取组件索引。"""
    component_list_data_obj = plug.asMObject()
    if component_list_data_obj.isNull():
        return []
    component_list_fn = om.MFnComponentListData(component_list_data_obj)
    all_indices = []
    for i in range(component_list_fn.length()):
        component_obj = component_list_fn.get(i)
        if component_obj.hasFn(om.MFn.kSingleIndexedComponent):
            component_fn = om.MFnSingleIndexedComponent(component_obj)
            indices = component_fn.getElements()
            all_indices.extend(list(indices))
    return all_indices

def get_components_obj_from_plug(plug):
    component_list_data_obj = plug.asMObject()
    return component_list_data_obj

def get_components_list_from_obj(obj):
    """从组件列表数据对象中获取组件索引列表。"""
    if obj.isNull():
        return []
    component_list_fn = om.MFnComponentListData(obj)
    all_indices = []
    for i in range(component_list_fn.length()):
        component_obj = component_list_fn.get(i)
        if component_obj.hasFn(om.MFn.kSingleIndexedComponent):
            component_fn = om.MFnSingleIndexedComponent(component_obj)
            indices = component_fn.getElements()
            all_indices.extend(list(indices))
    return all_indices

def components_to_mobject(components):
    """将组件列表转换为 MObject。"""
    component_fn = om.MFnSingleIndexedComponent()
    component_obj = component_fn.create(om.MFn.kMeshVertComponent)
    component_fn.addElements(components)
    component_list_fn = om.MFnComponentListData()
    component_list_data_obj = component_list_fn.create()
    component_list_fn.add(component_obj)
    return component_list_data_obj

def set_components(plug, obj):
    """将组件列表数据对象设置到指定的 plug 上。"""
    if obj.isNull() and obj.hasFn(om.MFn.kComponentListData):
        return
    plug.setMObject(obj)

def set_components_on_plug(plug, indices_to_set):
    """通过一个列表来设置组件索引。"""
    component_fn = om.MFnSingleIndexedComponent()
    component_obj = component_fn.create(om.MFn.kMeshVertComponent)
    component_fn.addElements(indices_to_set)
    component_list_fn = om.MFnComponentListData()
    component_list_data_obj = component_list_fn.create()
    component_list_fn.add(component_obj)
    plug.setMObject(component_list_data_obj)

# --- 点数据 (Points) 相关函数 ---
def get_points_from_plug(plug):
    """从点数组数据接口（plug）读取点的位置偏移。"""
    try:
        points_data_obj = plug.asMObject()
    except RuntimeError:
        raise RuntimeError("The plug does not contain valid point data.")
    point_array_fn = om.MFnPointArrayData(points_data_obj)
    point_array = point_array_fn.array()
    return point_array

def set_points_on_plug(plug, point_array):
    """
    新功能: 通过一个坐标列表来设置点的位置偏移。
    New Function: Sets the point position deltas from a list of coordinates.
    """

    # 2. 创建一个 MFnPointArrayData 函数集
    point_array_data_fn = om.MFnPointArrayData()
    
    # 3. 使用函数集创建一个包含 MPointArray 的数据对象
    points_data_obj = point_array_data_fn.create(point_array)
    
    # 4. 在接口上设置值
    plug.setMObject(points_data_obj)



# 获取 MPlug
comp_attr_name = 'myBlendShape.inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputComponentsTarget'
points_attr_name = 'myBlendShape.inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputPointsTarget'

selection_list_comp = om.MSelectionList()
selection_list_comp.add(comp_attr_name)
mPlug_comp = selection_list_comp.getPlug(0)

selection_list_points = om.MSelectionList()
selection_list_points.add(points_attr_name)
mPlug_points = selection_list_points.getPlug(0)


total_verts = cmds.polyEvaluate( 'base', vertex=True )
new_point_deltas = [(0.0, 0.0, 0.0)] * total_verts


new_point_deltas[10] = (0.0, 0.5, 0.0)  # 向上移动
new_point_deltas[20] = (0.0, 0.0, 0.5)  # 向前移动

set_points_on_plug(mPlug_points, new_point_deltas)


set_components_on_plug(mPlug_comp, [10, 20])

