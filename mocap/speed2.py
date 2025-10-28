"""
运动学计算脚本
基于基本的物理公式，计算角色在加速、匀速和减速阶段的运动数据。

cal: p = v*t + 0.5*a*t^2
p: 位移
v: 初始速度
t: 时间
a: 加速度
"""

from functools import partial
import math
from typing import Dict

from maya import cmds

FPS = 60  # 动画帧率


class UESpeed:
    # sprint
    sprint = 700
    sprint_accel = 1000
    sprint_decel = 2000

    # run speeds
    run_f = 500
    run_b = 400
    run_lp = 450
    run_ln = 400
    run_rp = 450
    run_rn = 400
    run_accel = 1000
    run_decel = 2000

    # walk speeds
    walk_f = 170
    walk_b = 150
    walk_lp = 160
    walk_ln = 150
    walk_rp = 160
    walk_rn = 150
    walk_accel = 400
    walk_decel = 800


def loop(
    speed=500,
    loop_frames=60,
    initial_pos=0.0,
    initial_frame=0,
    sample_fps=FPS,
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
        position = initial_pos + speed * current_time
        motion_info["motion_data"].append([initial_frame + frame, position])

    return motion_info


def accel(
    initial_speed=0.0,
    accel=1000.0,
    max_speed=500.0,
    initial_pos=0.0,
    initial_frame=0,
    sample_fps=FPS,
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

    return motion_info


def decel(
    initial_speed=500.0,
    decel=2000.0,
    min_speed=0.0,
    initial_pos=0.0,
    initial_frame=0,
    sample_fps=FPS,
):
    """
    计算匀减速运动的位移数据。

    Args:
        initial_speed (float, optional): 初始速度。默认为 500.0。
        decel (float, optional): 减速度（正数）。默认为 2000.0。
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
    object_attr: str,
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

    for frame in motion_data["motion_data"]:
        cmds.currentTime(frame[0])
        cmds.setAttr(f"{object_attr}", frame[1] if not negative else -frame[1])


if __name__ == "__main__":
    # 1. 计算加速阶段的运动数据
    data = accel(initial_pos=0)
    # 2. 计算匀速阶段的运动数据，起始位置为加速阶段的结束位置
    data1 = loop(
        loop_frames=20,
        initial_pos=data["motion_data"][-1][-1],
    )
    # 3. 计算减速阶段的运动数据，起始位置为匀速阶段的结束位置
    data2 = decel(
        initial_pos=data1["motion_data"][-1][-1],
    )

    # 将加速数据应用到 pCube1
    for x in data["motion_data"]:
        cmds.currentTime(x[0])
        cmds.setAttr("pCube1.tz", x[1])
    # 将匀速数据应用到 pCube1，注意帧偏移
    for x in data1["motion_data"]:
        cmds.currentTime(x[0] + data["frames_range"][-1])
        cmds.setAttr("pCube1.tz", x[1])
    # 将减速数据应用到 pCube1，注意帧偏移
    for x in data2["motion_data"]:
        cmds.currentTime(x[0] + data1["frames_range"][-1] + data["frames_range"][-1])
        cmds.setAttr("pCube1.tz", x[1])
