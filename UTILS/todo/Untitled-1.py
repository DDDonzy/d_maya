"""
================================================================================
Maya 软选择组件获取工具
================================================================================
选择模型、点、边或面后，获取软选择组件及其权重信息。
现在支持在软选择关闭时，将选择的边或面转换为点。
================================================================================
"""

from maya.api import OpenMaya as om
from collections import OrderedDict


def get_soft_selection_component(sortByWeights=False):
    """获取软选择组件及其权重信息。

    该函数通过 Maya API 2.0 获取当前软选择状态下的组件信息。
    - 如果软选择开启，它将返回所有受影响的顶点及其权重。
    - 如果软选择关闭，它将：
        - 返回选择的顶点(权重1.0)。
        - 将选择的边或面转换为顶点(权重1.0)。
        - 如果选择的是整个对象，返回所有顶点(权重1.0)。

    Args:
        sortByWeights (bool, optional): 是否按权重值从高到低排序返回结果。
                                        默认为 False，保持原始顶点索引顺序。

    Returns:
        List[OrderedDict]: 包含组件权重信息的有序字典列表。每个字典的结构为：
                           {顶点索引(int): 权重值(float), ...}

                           示例：
                           [OrderedDict({0: 1.0, 1: 0.8, 2: 0.3})]
    """

    mRichSel = om.MGlobal.getRichSelection()
    sel: om.MSelectionList = mRichSel.getSelection()

    data = []
    
    # 我们需要按对象（DAG路径）来分组处理组件
    # 因为一次选择（比如带软选择选一个面）可能会为同一个物体返回多个组件
    # (例如, kMeshPolygonComponent 和 kMeshVertComponent)
    # 我们优先使用 kMeshVertComponent，因为它包含了权重信息。
    
    dag_components = OrderedDict()
    
    for i in range(sel.length()):
        try:
            mDag, comp = sel.getComponent(i)
            dag_path_name = mDag.fullPathName()
            
            if dag_path_name not in dag_components:
                dag_components[dag_path_name] = []
            dag_components[dag_path_name].append((mDag, comp))
        except:
            # 可能是选择了整个对象（Transform节点）
            try:
                mDag = sel.getDagPath(i)
                if mDag.hasFn(om.MFn.kMesh):
                    dag_path_name = mDag.fullPathName()
                    if dag_path_name not in dag_components:
                        dag_components[dag_path_name] = []
                    # 用 None 来标记这是一个完整的对象选择
                    dag_components[dag_path_name].append((mDag, None))
            except:
                continue # 忽略无法处理的选项

    # 遍历每个被选中的对象
    for dag_path_name, components in dag_components.items():
        
        softComponentDict = OrderedDict()
        fnMesh = None # 稍后按需初始化 MFnMesh
        
        # 优先级 1: 查找 kMeshVertComponent (它包含了软选择权重)
        vert_comp_data = None
        for mDag, comp in components:
            if comp and comp.apiType() == om.MFn.kMeshVertComponent:
                vert_comp_data = (mDag, comp)
                break # 找到了，这是最优先的
        
        if vert_comp_data:
            # 找到了顶点组件，使用你的原始逻辑
            mDag, comp = vert_comp_data
            fnComp = om.MFnSingleIndexedComponent(comp)
            for i in range(fnComp.elementCount):
                softComponentDict[fnComp.element(i)] = fnComp.weight(i).influence if fnComp.hasWeights else 1.0
        
        else:
            # 优先级 2: 没有找到顶点组件 (软选择关闭了)
            # 我们来手动转换 边(Edge) 和 面(Polygon)
            vertSet = set() # 使用 set 来自动处理重复的顶点
            processed_non_vtx = False

            for mDag, comp in components:
                if not comp: # 标记为 "None" 的完整对象选择
                    continue
                
                # 初始化 MFnMesh (仅在需要时)
                if fnMesh is None:
                    fnMesh = om.MFnMesh(mDag)

                if comp.apiType() == om.MFn.kMeshEdgeComponent:
                    processed_non_vtx = True
                    fnComp = om.MFnSingleIndexedComponent(comp)
                    for i in range(fnComp.elementCount):
                        edgeIndex = fnComp.element(i)
                        vtxIds = fnMesh.getEdgeVertices(edgeIndex) # 获取边的两个顶点
                        vertSet.add(vtxIds[0])
                        vertSet.add(vtxIds[1])
                        
                elif comp.apiType() == om.MFn.kMeshPolygonComponent:
                    processed_non_vtx = True
                    fnComp = om.MFnSingleIndexedComponent(comp)
                    for i in range(fnComp.elementCount):
                        faceIndex = fnComp.element(i)
                        vtxIds = fnMesh.getPolygonVertices(faceIndex) # 获取面的所有顶点
                        for vtxIndex in vtxIds:
                            vertSet.add(vtxIndex)

            if processed_non_vtx:
                # 如果我们处理了边或面，就从 set 中创建字典
                for vtxIndex in sorted(list(vertSet)):
                    softComponentDict[vtxIndex] = 1.0 # 权重为 1.0
            
            else:
                # 优先级 3: 既没有顶点组件，也没有边/面组件
                # 这说明是选择了整个对象
                mDag, _ = components[0] # 获取DAG路径
                if mDag.hasFn(om.MFn.kMesh):
                    if fnMesh is None:
                        fnMesh = om.MFnMesh(mDag)
                    for i in range(fnMesh.numVertices):
                        softComponentDict[i] = 1.0

        # 应用排序
        if sortByWeights and softComponentDict:
            softComponentDict = OrderedDict(sorted(softComponentDict.items(), key=lambda x: x[1], reverse=True))

        if softComponentDict:
            data.append(softComponentDict)

    return data


if __name__ == "__main__":
    # 现在你可以测试选择面或边（在关闭软选择的情况下）
    # 也可以测试开启软选择
    print(get_soft_selection_component(sortByWeights=True))