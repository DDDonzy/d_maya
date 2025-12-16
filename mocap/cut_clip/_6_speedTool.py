import maya.cmds as cmds
import functools  # <-- 我们需要这个来实现简洁的按钮命令

# -----------------------------------------------------------------
# 1. 定义你的主脚本逻辑 (与之前相同)
# -----------------------------------------------------------------
"""
运动学计算脚本
基于基本的物理公式，计算角色在加速、匀速和减速阶段的运动数据。

cal: p = v*t + 0.5*a*t^2
p: 位移
v: 初始速度
t: 时间
a: 加速度
"""

import math
from typing import Dict, List

from maya import cmds


class UESpeed:
    FPS = 60
    # sprint
    sprint = 700
    sprint_accel = 1000
    sprint_decel = 1000

    # run speeds
    run_f = 475
    run_b = 320
    run_lp = 400
    run_ln = 400
    run_rp = 400
    run_rn = 400
    run_accel = 800
    run_decel = 1000

    # walk speeds
    walk_f = 170
    walk_b = 150
    walk_lp = 160
    walk_ln = 150
    walk_rp = 160
    walk_rn = 150
    walk_accel = 400
    walk_decel = 800


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


def fn_loop(
    speed=500,
    loop_frames=60,
    initial_pos=0.0,
    initial_frame=0,
    sample_fps=60,
):
    """
    计算匀速运动的位移数据。

    Args:
        speed (int, optional): 运动速度。默认为 500。
        loop_frames (int, optional): 匀速运动持续的帧数。默认为 60。
        initial_pos (float, optional): 起始位置。默认为 0.0。
        initial_frame (int, optional): 起始帧。默认为 0。
        sample_fps (int, optional): 采样帧率。默认为 FPS。

    Returns:
        dict ({str: list}): 包含运动数据的字典，具有以下键：
            - "frames_range" (list): [start_frame, end_frame]
            - "motion_data" (list): 包含 [frame, position] 嵌套列表。
    """
    motion_info: Dict[str, list] = {
        "frames_range": [initial_frame, initial_frame + loop_frames],
        "motion_data": [],
    }

    for frame in range(loop_frames + 1):
        current_time = frame / float(sample_fps)
        # 位移 = 初始位置 + 速度 * 时间
        position = (abs(initial_pos) + speed * current_time) * (1 if initial_pos >= 0 else -1)
        motion_info["motion_data"].append([initial_frame + frame, position])

    timeSliderBookmark(name="loop", time=[initial_frame, initial_frame + loop_frames + 1], color=[0.6, 0.263, 0.431])
    return motion_info


def fn_accel(
    initial_speed=0.0,
    accel=1000.0,
    max_speed=500.0,
    initial_pos=0.0,
    initial_frame=0,
    sample_fps=60,
):
    """
    计算匀加速运动的位移数据。

    Args:
        initial_speed (float, optional): 初始速度。默认为 0.0。
        accel (float, optional): 加速度（正数）。默认为 1000.0。
        max_speed (float, optional): 达到的最大速度。默认为 500.0。
        initial_pos (float, optional): 初始位置。默认为 0.0。
        initial_frame (int, optional): 初始帧。默认为 0。
        sample_fps (int, optional): 采样帧率。默认为 FPS。

    Returns:
        dict ({str: list}): 包含运动数据的字典，具有以下键：
            - "frames_range" (list): [start_frame, end_frame]
            - "motion_data" (list): 包含 [frame, position] 嵌套列表。
    """
    if accel <= 0:
        raise ValueError("加速度必须为正数。")
    if initial_speed >= max_speed:
        raise ValueError("初始速度必须小于最大速度。")

    # 计算加速到最大速度所需的时间和帧数
    accel_times = (max_speed - initial_speed) / accel
    accel_frames = math.ceil(accel_times * sample_fps)

    motion_info: Dict[str, list] = {
        "frames_range": [initial_frame, initial_frame + accel_frames],
        "motion_data": [],
    }
    for frame in range(accel_frames + 1):
        current_time = frame / float(sample_fps)
        current_speed = initial_speed + accel * current_time
        # 防止速度超过最大速度
        if current_speed > max_speed:
            current_speed = max_speed
        # 位移 = 初始位置 + 初始速度*时间 + 0.5*加速度*时间^2
        current_pos = initial_pos + initial_speed * current_time + 0.5 * accel * current_time**2
        motion_info["motion_data"].append([initial_frame + frame, current_pos])

    timeSliderBookmark(name="accel", time=[initial_frame, initial_frame + accel_frames + 1], color=[0.67, 0.235, 0.235])
    return motion_info


def fn_decel(
    initial_speed=500.0,
    decel=1000.0,
    min_speed=0.0,
    initial_pos=0.0,
    initial_frame=0,
    sample_fps=60,
):
    """
    计算匀减速运动的位移数据。

    Args:
        initial_speed (float, optional): 初始速度。默认为 500.0。
        decel (float, optional): 减速度（正数）。默认为 1000.0。
        min_speed (float, optional): 减速后的最小速度。默认为 0.0。
        initial_pos (float, optional): 初始位置。默认为 0.0。
        initial_frame (int, optional): 初始帧。默认为 0。
        sample_fps (int, optional): 采样帧率。默认为 FPS。

    Returns:
        dict ({str: list}): 包含运动数据的字典，具有以下键：
            - "frames_range" (list): [start_frame, end_frame]
            - "motion_data" (list): 包含 [frame, position] 嵌套列表。
    """
    if decel <= 0:
        raise ValueError("减速度比如为正数")
    if initial_speed <= min_speed:
        raise ValueError("初始速度必须大于最小速度。")

    # 计算减速到最小速度所需的时间和帧数
    decel_times = (initial_speed - min_speed) / decel
    decel_frames = math.ceil(decel_times * sample_fps)

    motion_info: Dict[str, list] = {
        "frames_range": [initial_frame, initial_frame + decel_frames],
        "motion_data": [],
    }
    for frame in range(decel_frames + 1):
        current_time = frame / float(sample_fps)
        # 位移 = 初始位置 + 初始速度*时间 - 0.5*减速度*时间^2
        current_pos = initial_pos + initial_speed * current_time - 0.5 * decel * (current_time**2)
        motion_info["motion_data"].append([initial_frame + frame, current_pos])

    timeSliderBookmark(name="decel", time=[initial_frame, initial_frame + decel_frames + 1], color=[0.749, 0.4, 0.235])
    return motion_info


def pre_motion_data(motion_data: Dict[str, list]) -> Dict[str, list]:
    """
    预处理运动数据，将整个运动片段在时间和空间上向前移动一个自身的长度。

    比如 现在有一段 减速运动数据，帧范围是 `[0, 30]`，位置是 `[0, 250]`，
    那么处理后，帧范围变为 `[-30, 0]`，位置变为 `[-250cm, 0cm]`。

    适用于在运动前后，再次插入运动，比如 accel -> loop 这种连续运动，
    我们可以先生成 loop 数据，然后再生成 accel 数据，
    使用 pre_motion_data 将 accel 数据向前移动，实现在loop之前插入 accel 动作。

    Args:
        motion_data ({str: list}): 输入的运动数据字典。
            - "frames_range" (list): [start_frame, end_frame]
            - "motion_data" (list): 包含 [frame, position] 嵌套列表。
    Returns:
        dict ({str: list}): 处理后的运动数据字典，其帧范围和位置数据都已向前平移。
            - "frames_range" (list): [start_frame, end_frame]
            - "motion_data" (list): 包含 [frame, position] 嵌套列表。
    """

    if not motion_data:
        raise ValueError("Please input motion data")

    # 获取原始运动的起止帧和位置信息
    start_frame = motion_data["frames_range"][0]
    end_frame = motion_data["frames_range"][-1]
    motion_frames = end_frame - start_frame
    start_pos = motion_data["motion_data"][0][-1]
    end_pos = motion_data["motion_data"][-1][-1]
    motion_pos = end_pos - start_pos

    motion_data["frames_range"] = [start_frame - motion_frames, start_frame]
    # 重新计算每一帧的帧号和位置
    for frame in motion_data["motion_data"]:
        current_frame = frame[0]
        current_pos = frame[1]
        frame[0] = current_frame - motion_frames
        frame[1] = current_pos - motion_pos
    return motion_data


def key_motion_data(
    motion_data: Dict[str, list],
    object: str,
    attr: str,
    negative: bool = False,
):
    """
    将运动数据应用为目标对象的关键帧动画。

    Args:
        motion_data (dict): 包含运动数据的字典，具有以下键：
            - "frames_range" (list): [start_frame, end_frame]
            - "motion_data" (list): 包含 [frame, position] 嵌套列表。
        object_attribute (str): 目标属性名称（如 "translateX"）。
        negative (bool, optional): 是否将位置取反。默认为 False。
    """
    if not motion_data:
        raise ValueError("Please input motion data")

    if negative:
        negative = -1
    else:
        negative = 1
    for frame in motion_data["motion_data"]:
        cmds.setKeyframe(object, attribute=attr, value=frame[1] * negative, time=frame[0])


def run_script_with_ui_values(attr, is_positive, max_speed, accel, decel):
    print(attr, is_positive, max_speed, accel, decel)
    if not cmds.objExists("rootMotion"):
        cmds.spaceLocator(name="rootMotion")
        cmds.setAttr("rootMotion.localScale", *(100, 100, 100))

    loop_frames = abs(int(cmds.playbackOptions(q=1, sst=1)) - int(cmds.playbackOptions(q=1, set=1)))
    start_frame = int(cmds.playbackOptions(q=1, sst=1))

    loop_data = fn_loop(
        speed=max_speed,
        loop_frames=loop_frames,
        initial_pos=cmds.getAttr(f"rootMotion.{attr}"),
        initial_frame=start_frame,
        sample_fps=60,
    )

    key_motion_data(loop_data, object="rootMotion", attr=attr, negative=not is_positive)


def run_accel_script(attr, is_positive, max_speed, accel, decel):
    print(attr, is_positive, max_speed, accel, decel)
    if not cmds.objExists("rootMotion"):
        cmds.spaceLocator(name="rootMotion")

    start_frame = int(cmds.currentTime(q=1))

    data = fn_accel(
        initial_speed=0.0,
        accel=accel,
        max_speed=max_speed,
        initial_pos=cmds.getAttr(f"rootMotion.{attr}"),
        initial_frame=start_frame,
        sample_fps=60,
    )

    key_motion_data(data, object="rootMotion", attr=attr, negative=not is_positive)


def run_decel_script(attr, is_positive, max_speed, accel, decel):
    print(attr, is_positive, max_speed, accel, decel)
    if not cmds.objExists("rootMotion"):
        cmds.spaceLocator(name="rootMotion")

    start_frame = int(cmds.currentTime(q=1))

    data = fn_decel(
        initial_speed=max_speed,
        decel=decel,
        min_speed=0.0,
        initial_pos=cmds.getAttr(f"rootMotion.{attr}"),
        initial_frame=start_frame,
        sample_fps=60,
    )

    key_motion_data(data, object="rootMotion", attr=attr, negative=not is_positive)


# -----------------------------------------------------------------
# 2. UI 回调
# -----------------------------------------------------------------

ui_elements = {}
window_name = "simpleAxisUI"


def _query_common_ui_values():
    """辅助函数，查询所有UI字段"""

    selected_axis = cmds.radioCollection(ui_elements["axis_collection"], query=True, select=True)
    if selected_axis == "x_rb":
        attr = "tx"
    elif selected_axis == "y_rb":
        attr = "ty"
    elif selected_axis == "z_rb":
        attr = "tz"
    else:
        attr = "tx"

    selected_dir = cmds.radioCollection(ui_elements["dir_collection"], query=True, select=True)
    is_positive = selected_dir == "plus_rb"

    max_speed = cmds.floatFieldGrp(ui_elements["maxSpeed_field"], query=True, value1=True)
    accel = cmds.floatFieldGrp(ui_elements["accel_field"], query=True, value1=True)
    decel = cmds.floatFieldGrp(ui_elements["decel_field"], query=True, value1=True)

    return attr, is_positive, max_speed, accel, decel


# --- 主要运行按钮的回调 ---


def on_loop_click(*args):
    """当 'Loop' 按钮被点击时调用"""
    attr, is_positive, max_speed, accel, decel = _query_common_ui_values()
    run_script_with_ui_values(attr, is_positive, max_speed, accel, decel)


def on_accel_click(*args):
    """当 'Accel' 按钮被点击时调用"""
    attr, is_positive, max_speed, accel, decel = _query_common_ui_values()
    run_accel_script(attr, is_positive, max_speed, accel, decel)


def on_decel_click(*args):
    """当 'Decel' 按钮被点击时调用"""
    attr, is_positive, max_speed, accel, decel = _query_common_ui_values()
    run_decel_script(attr, is_positive, max_speed, accel, decel)


# --- 新增：预设按钮的回调 ---


def set_speed_values(max_speed, accel, decel, *args):
    """
    这个函数会被所有预设按钮调用。
    它会更新UI中的 float fields。
    """
    try:
        cmds.floatFieldGrp(ui_elements["maxSpeed_field"], edit=True, value1=max_speed)
        cmds.floatFieldGrp(ui_elements["accel_field"], edit=True, value1=accel)
        cmds.floatFieldGrp(ui_elements["decel_field"], edit=True, value1=decel)
        print(f"Preset set: MaxSpeed={max_speed}, Accel={accel}, Decel={decel}")
    except KeyError:
        cmds.warning("UI elements not found. Cannot set preset values.")
    except RuntimeError:
        # 这通常意味着窗口已被关闭
        pass


# -----------------------------------------------------------------
# 3. UI 创建
# -----------------------------------------------------------------


def create_simple_ui():
    """
    创建UI窗口
    """
    global ui_elements, window_name

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)

    # 增加窗口高度以容纳新按钮
    cmds.window(window_name, title="Select Axis", widthHeight=(260, 600), s=False)

    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    # --- Axis (X, Y, Z) ---
    ui_elements["axis_collection"] = cmds.radioCollection()
    cmds.rowLayout(numberOfColumns=3)
    cmds.radioButton("x_rb", label="X")
    cmds.radioButton("z_rb", label="Z", select=True)
    cmds.setParent(main_layout)

    # --- Direction (+, -) ---
    ui_elements["dir_collection"] = cmds.radioCollection()
    cmds.rowLayout(numberOfColumns=2)
    cmds.radioButton("plus_rb", label="+ (Positive)", select=True)
    cmds.radioButton("minus_rb", label="- (Negative)")
    cmds.setParent(main_layout)

    cmds.separator(h=10, style="in")

    # --- 数值输入框 ---
    ui_elements["maxSpeed_field"] = cmds.floatFieldGrp(label="Max Speed", numberOfFields=1, value1=500.0, columnWidth2=[80, 100])

    ui_elements["accel_field"] = cmds.floatFieldGrp(label="Accel", numberOfFields=1, value1=1000.0, columnWidth2=[80, 100])

    ui_elements["decel_field"] = cmds.floatFieldGrp(label="Decel", numberOfFields=1, value1=1000.0, columnWidth2=[80, 100])

    cmds.setParent(main_layout)

    cmds.separator(h=10, style="in")

    # 布局参数: 4列, 间距为5, 每列宽度60
    btn_width = 60
    btn_spacing = 5

    # --- Row 1: Run ---
    cmds.rowLayout(numberOfColumns=4)
    cmds.button(label="Run_F", w=60, command=functools.partial(set_speed_values, 500, 1000, 1000))
    cmds.button(label="Run_LRP", w=60, command=functools.partial(set_speed_values, 450, 1000, 1000))
    cmds.button(label="Run_LRN", w=60, command=functools.partial(set_speed_values, 400, 1000, 1000))
    cmds.button(label="Run_B", w=60, command=functools.partial(set_speed_values, 400, 1000, 1000))
    cmds.setParent(main_layout)

    # --- Row 2: Walk ---
    cmds.rowLayout(numberOfColumns=4)
    cmds.button(label="Walk_F", w=60, command=functools.partial(set_speed_values, 170, 400, 800))
    cmds.button(label="Walk_LRP", w=60, command=functools.partial(set_speed_values, 160, 400, 800))
    cmds.button(label="Walk_LRN", w=60, command=functools.partial(set_speed_values, 150, 400, 800))
    cmds.button(label="Walk_B", w=60, command=functools.partial(set_speed_values, 150, 400, 800))
    cmds.setParent(main_layout)

    # --- Row 3: Sprint ---
    cmds.rowLayout(numberOfColumns=1, adjustableColumn=1)
    # 让这个按钮填满宽度
    full_width = (btn_width * 4) + (btn_spacing * 3)
    cmds.button(label="Sprint", command=functools.partial(set_speed_values, 700, 1000, 1000), width=full_width)
    cmds.setParent(main_layout)

    # --- 最终运行按钮 ---
    cmds.separator(h=15, style="in")
    cmds.button(label="Loop", command=on_loop_click, height=30)
    cmds.button(label="Accel", command=on_accel_click, height=30)
    cmds.button(label="Decel", command=on_decel_click, height=30)

    cmds.showWindow(window_name)


# -----------------------------------------------------------------
# 4. 运行脚本
# -----------------------------------------------------------------
if __name__ == "__main__":
    # 假设你的 loop 和 key_motion_data 已经定义好了
    # (如果还没有，你需要先 source 或执行定义它们的脚本)

    # 启动UI
    create_simple_ui()
