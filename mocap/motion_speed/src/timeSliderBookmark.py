from maya import cmds
from typing import List


def timeSliderBookmark(name: str, time: List[int], color: List[float], priority: int = 1) -> str:
    """
    在Maya时间轴上创建一个书签标记

    Args:
        name (str): 书签的名称
        time (List[int]): 时间范围，包含开始帧和结束帧 [开始帧, 结束帧]
        color (List[float]): RGB颜色值，范围0-1 [R, G, B]
        priority (int, optional): 书签的优先级，默认为1

    Returns:
        str: 创建的timeSliderBookmark节点名称

    Example:
        # 创建一个名为"idle"的书签，时间范围10-50帧，颜色为灰色
        bookmark_node = timeSliderBookmark("idle", [10, 50], [0.5, 0.5, 0.5])
    """

    bookmark = cmds.createNode("timeSliderBookmark", name=f"timeSliderBookmark_{name}")
    cmds.setAttr(f"{bookmark}.name", name, type="string")
    cmds.setAttr(f"{bookmark}.color", *color)
    cmds.setAttr(f"{bookmark}.timeRangeStart", time[0])
    cmds.setAttr(f"{bookmark}.timeRangeStop", time[1])
    cmds.setAttr(f"{bookmark}.priority", priority)

    return bookmark
