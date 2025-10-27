# 0.5*a*t^2 加速/减速距离
# v 初始速度
# t 运动时间
# a 加速度
# dis = v*t + 0.5*a*t^2

import math
from typing import Dict

from maya import cmds

FPS = 60
SPRINT = 700
RUN_ACCEL = 1000
RUN_DECEL = 2000


def loop(
    speed=500,
    loop_frames=60,
    initial_pos=0.0,
    initial_frame=0,
    sample_fps=FPS,
):
    motion_info: Dict[str, list] = {
        "frames_range": [initial_frame, initial_frame + loop_frames],
        "motion_data": [],
    }
    for frame in range(loop_frames + 1):
        current_time = frame / float(sample_fps)
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
    if accel <= 0:
        raise ValueError("加速度必须为正数。")
    if initial_speed >= max_speed:
        raise ValueError("初始速度必须小于最大速度。")

    accel_times = (max_speed - initial_speed) / accel
    accel_frames = math.ceil(accel_times * sample_fps)

    motion_info: Dict[str, list] = {
        "frames_range": [initial_frame, initial_frame + accel_frames],
        "motion_data": [],
    }
    for frame in range(accel_frames + 1):
        current_time = frame / float(sample_fps)
        current_speed = initial_speed + accel * current_time
        if current_speed > max_speed:
            current_speed = max_speed
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
    if decel <= 0:
        raise ValueError("减速度比如为正数")
    if initial_speed <= min_speed:
        raise ValueError("初始速度必须大于最小速度。")

    decel_times = (initial_speed - min_speed) / decel
    decel_frames = math.ceil(decel_times * sample_fps)
    motion_info: Dict[str, list] = {
        "frames_range": [initial_frame, initial_frame + decel_frames],
        "motion_data": [],
    }
    for frame in range(decel_frames + 1):
        current_time = frame / float(sample_fps)
        current_pos = initial_pos + initial_speed * current_time - 0.5 * decel * (current_time**2)
        motion_info["motion_data"].append([initial_frame + frame, current_pos])

    return motion_info


def invert_motion_data(motion_data: Dict[str, list]) -> Dict[str, list]:
    if not motion_data:
        raise ValueError("Please input motion data")

    start_frame = motion_data["frames_range"][0]
    end_frames = motion_data["frames_range"][-1]
    motion_frames = end_frames - start_frame
    start_pos = motion_data["motion_data"][0][-1]
    end_pos = motion_data["motion_data"][-1][-1]
    motion_pos = end_pos - start_pos

    motion_data["frames_range"] = [start_frame - motion_frames, start_frame]
    for frame in motion_data["motion_data"]:
        current_frame = frame[0]
        current_pos = frame[1]
        frame[0] = current_frame - motion_frames
        frame[1] = current_pos - motion_pos

    return motion_data


data = accel(initial_pos=0)
data1 = loop(loop_frames=20, initial_pos=data["motion_data"][-1][-1])
data2 = decel(initial_pos=data1["motion_data"][-1][-1])
for x in data["motion_data"]:
    cmds.currentTime(x[0])
    cmds.setAttr("pCube1.tz", x[1])
for x in data1["motion_data"]:
    cmds.currentTime(x[0] + data["frames_range"][-1])
    cmds.setAttr("pCube1.tz", x[1])
for x in data2["motion_data"]:
    cmds.currentTime(x[0] + data1["frames_range"][-1] + data["frames_range"][-1])
    cmds.setAttr("pCube1.tz", x[1])
