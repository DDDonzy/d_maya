"""
================================================================================
Maya Component Selection Utilities
================================================================================

[ 脚本目的 ]
该脚本提供了一套核心工具函数，用于在 Maya 中获取组件（如顶点、边、面）
的选择信息。它特别专注于使用 Maya Python API 2.0 (`OpenMaya`) 来高效地
处理标准的组件选择和更为复杂的软选择 (Soft Selection)。

[ 核心技术 ]
- Maya Python API 2.0: 脚本完全使用 `OpenMaya` API，这在处理大量组件数据时，
  比传统的 `maya.cmds` 提供了显著的性能优势。
- Rich Selection: `get_soft_selection_component` 函数通过 `MGlobal.getRichSelection`
  来访问软选择的权重信息，这是标准 `cmds` 命令无法直接获取的。

[ 主要函数 ]
1.  `get_soft_selection_component(sortByWeights=False)`:
    - 功能: 获取当前激活的软选择中的所有组件及其对应的权重值。
    - 工作流程:
        a. 使用 `MGlobal.getRichSelection` 获取包含权重信息的“富选择”对象。
        b. 遍历选择集中的所有元素，提取每个组件的索引 (index) 和其影响权重
           (influence)。
        c. 将结果存储在一个有序字典 (OrderedDict) 中，键为组件索引，值为权重。
    - 参数:
        - `sortByWeights`: 如果为 `True`，则返回的字典会按权重值从高到低排序。
    - 返回:
        - 一个 `OrderedDict`，包含了组件索引到权重的映射。

2.  `get_selection_component()`:
    - 功能: 获取标准的（非软选择）组件选择，并返回其索引。
    - 工作流程:
        a. 使用 `MGlobal.getActiveSelectionList` 获取当前的选择列表。
        b. 从选择列表中提取组件对象。
        c. 使用 `MFnSingleIndexedComponent` 函数集来获取所有选中组件的索引。
    - 返回:
        - 一个 `MIntArray` 对象，包含了所有选中组件的索引列表。

[ 应用场景 ]
这些函数是开发高级建模、绑定或权重工具的基础。例如：
- 在一个自定义的权重工具中，使用 `get_soft_selection_component` 来根据软选择
  的衰减来平滑或设置权重。
- 在一个程序化建模工具中，使用 `get_selection_component` 来确定在哪些顶点上
  执行挤出或倒角操作。

================================================================================
"""

from maya.api import OpenMaya as om
from collections import OrderedDict


def get_soft_selection_component(sortByWeights=False):
    """Get the soft selected component and its weights.

    Returns:
        Dict: List of tuples containing component index and its weight.
    """
    softComponentDict = OrderedDict()

    mRichSel = om.MGlobal.getRichSelection()
    sel = mRichSel.getSelection()

    _, comp = sel.getComponent(0)

    fnComp = om.MFnSingleIndexedComponent(comp)
    if fnComp.hasWeights is False:
        raise RuntimeError("Component has no weights, Please use soft selection.")

    for i in range(fnComp.elementCount):
        softComponentDict[fnComp.element(i)] = fnComp.weight(i).influence

    if sortByWeights:
        return OrderedDict(sorted(softComponentDict.items(), key=lambda x: x[1], reverse=True))
    else:
        return softComponentDict


def get_selection_component():
    """
    Get the selected component.
    Returns:
        MIntArray: List of component index.
    """

    selection = om.MGlobal.getActiveSelectionList()
    _, comp = selection.getComponent(0)
    fnComp: om.MFnSingleIndexedComponent = om.MFnSingleIndexedComponent(comp)
    return fnComp.getElements()


if __name__ == "__main__":
    print(get_soft_selection_component(True))
    print(get_selection_component())
