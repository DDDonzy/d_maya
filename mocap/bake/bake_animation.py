"""
================================================================================
Animation Baking Core Functions
================================================================================

[ 脚本目的 ]
该文件提供了将动画从一个源骨骼（UE 标准骨骼）烘焙到 绑定（Advanced Skeleton）的核心功能。
它通过创建一系列动态约束，将源骨骼的运动实时传递给目标绑定控制器，然后将这些运动的关键帧烘焙下来。

[ 核心组件 ]
1.  bake_dict:
    - 定义了目标绑定中 FK/IK 控制器与源骨骼关节的一对一映射关系。
    - 用于创建直接的矩阵约束（Matrix Constraint）。

2.  bake_pv_dict:
    - 定义了目标绑定中极向量（Pole Vector）控制器与源骨骼中对应 IK 链
      （如上臂、小臂、手）的映射关系。
    - 用于驱动极向量的动态计算。

[ 主要函数与工作流程 ]
1.  bakeAnimations(target_namespace, source_namespace, time):
    - 这是供外部调用的主入口函数。
    - 工作流程:
        a. 调用 `pre_bakeAnimations` 来创建所有的约束和计算节点。
        b. 调用 Maya 的 `bakeResults` 命令，对所有受约束的控制器在指定时间
           范围内进行烘焙，将动态的运动转化为静态的关键帧。
        c. 调用 `cmds.delete` 删除在预处理阶段创建的所有临时约束节点，
           保持场景干净。

2.  pre_bakeAnimations(...):
    - 烘焙前的预处理函数，负责搭建所有的“桥梁”。
    - 遍历 `bake_dict`，计算每个控制器相对于其驱动关节的初始偏移矩阵，
      并创建 `matrixConstraint` 将源关节的运动传递给目标控制器。
    - 遍历 `bake_pv_dict`，为每个 IK 链调用 `cal_pv` 函数，创建一套
      用于实时计算极向量位置的节点网络，并将计算结果约束到对应的极向量
      控制器上。
    - 返回所有被约束的控制器列表，供 `bakeResults` 使用。

3.  cal_pv(name):
    - 极向量位置的数学计算函数。
    - 它不使用简单的约束，而是通过创建一套 Maya 节点（如 plusMinusAverage,
      vectorProduct, multiplyDivide 等）来精确地、动态地计算出在 IK 链
      运动过程中，极向量应该处于的正确空间位置，以防止膝盖或手肘发生翻转。

[ 依赖项 ]
- 该脚本依赖于一系列自定义的工具函数，位于 `UTILS` 模块下，如
  `get_worldMatrix`, `matrixConstraint` 等。

================================================================================
"""

from maya import cmds
from maya.api import OpenMaya as om
from m_utils.compounds import matrixConstraint
from m_utils.create.assetCallback import AssetCallback
from mocap.bake.cal_pv import do_cal_pv
from mocap.bake.retargetConstraint import do_constraint
from mocap.bake.set_global import do_set_global


def find_object_ignoring_namespace(obj_name):
    """
    查找物体，忽略 Namespace 层级
    """
    # 查找所有 transform 节点
    all_transforms = cmds.ls(type="transform")
    # 筛选
    result = [o for o in all_transforms if o == obj_name or o.endswith(":" + obj_name)]
    return result


def pre_bakeAnimations(
    target_namespace="TestCharacter_rig",
    source_namespace="Retarget_M_Blade_Stand_Idle",
    main_t=True,
    main_r=True,
):
    """
    烘焙预处理，生成约束等
    """
    # pre
    with AssetCallback(name="bakeConstraint", isDagAsset=False) as asset:
        bake_list = []  # bake动画属性列表

        # 约束
        bake_list += do_constraint(
            source_namespace=source_namespace,
            target_namespace=target_namespace,
        )
        # 计算极限量位置
        bake_list += do_cal_pv(
            source_namespace=source_namespace,
            target_namespace=target_namespace,
        )
        # 设置 global
        bake_list += do_set_global(target_namespace=target_namespace)
        
        # 烘焙root运动
        rootMotion = find_object_ignoring_namespace("rootMotion")
        if rootMotion:
            matrixConstraint(rootMotion[0], f"{target_namespace}:FKRootGround_M", mo=False)
            bake_list.append(f"{target_namespace}:FKRootGround_M" if target_namespace else "FKRootGround_M")

    return asset, bake_list


def bakeAnimations(target_namespace, source_namespace, time=(0, 1000)):
    asset, bake_list = pre_bakeAnimations(
        target_namespace=target_namespace,
        source_namespace=source_namespace,
        main_t=True,
        main_r=True,
    )

    cmds.bakeResults(
        bake_list,
        at=["t", "r", "s"],
        t=time,
        sb=1,
        simulation=1,
    )

    cmds.delete(asset)
