import math
from re import T
from maya import cmds

# --- 常量定义 (单位基于秒) ---
FPS = 60
SPEED_F = 500  # 最大前进速度 (单位/秒)
SPEED_B = 300
SPEED_L = 350
SPEED_R = 350
ACCEL_SPEED = 800  # 加速度 (单位/秒^2)
DECEL_SPEED = 2000  # 减速度 (单位/秒^2)


# --- 内部辅助函数 (仍然使用“秒”作为单位) ---
def get_accel_time_in_seconds(speed):
    """(内部使用) 计算加速到指定速度所需的时间(秒)。"""
    if ACCEL_SPEED == 0:
        return float("inf")
    return speed / ACCEL_SPEED


def get_decel_time_in_seconds(speed):
    """(内部使用) 计算减速到0所需的时间(秒)。"""
    if DECEL_SPEED == 0:
        return float("inf")
    return speed / DECEL_SPEED


# --- 用户接口函数 (使用“帧”作为单位) ---


def get_pos(frames, max_speed, accel=False, decel=False):
    """
    根据给定的**帧数**、是否加减速，计算位移。

    Args:
        frames (int): 总运动帧数。
        accel (bool): 是否计算加速。
        decel (bool): 是否计算减速。

    Returns:
        float or str: 计算出的总位移。
    """
    # **【单位转换】** 将输入的帧数转换为秒，用于物理计算
    time_in_seconds = frames / FPS

    time_to_accel = get_accel_time_in_seconds(max_speed)
    time_to_decel = get_decel_time_in_seconds(max_speed)

    # 情况 1: 匀速
    if not accel and not decel:
        return max_speed * time_in_seconds

    # 情况 2: 只有加速
    if accel and not decel:
        if time_in_seconds < time_to_accel:
            return 0.5 * ACCEL_SPEED * (time_in_seconds**2)
        else:
            dist_accel = 0.5 * ACCEL_SPEED * (time_to_accel**2)
            time_at_max_speed = time_in_seconds - time_to_accel
            return dist_accel + max_speed * time_at_max_speed

    # 情况 3: 只有减速
    if not accel and decel:
        if time_in_seconds < time_to_decel:
            return max_speed * time_in_seconds - 0.5 * DECEL_SPEED * (time_in_seconds**2)
        else:
            dist_decel = max_speed * time_to_decel - 0.5 * DECEL_SPEED * (time_to_decel**2)
            time_at_max_speed = time_in_seconds - time_to_decel
            return max_speed * time_at_max_speed + dist_decel

    # 情况 4: 加速和减速
    if accel and decel:
        if time_in_seconds < time_to_accel + time_to_decel:
            return "错误：帧数不足以完成加速和减速。"
        else:
            dist_accel = 0.5 * ACCEL_SPEED * (time_to_accel**2)
            dist_decel = max_speed * time_to_decel - 0.5 * DECEL_SPEED * (time_to_decel**2)
            time_at_max_speed = time_in_seconds - time_to_accel - time_to_decel
            return dist_accel + max_speed * time_at_max_speed + dist_decel


def get_time_in_frames(pos, max_speed, accel=False, decel=False):
    """
    根据位移、是否加减速，反推所需的**帧数**。

    Args:
        pos (float): 目标位移。
        accel (bool): 是否计算加速。
        decel (bool): 是否计算减速。

    Returns:
        float or str: 计算出的总帧数。
    """
    if pos < 0:
        return "错误：距离不能为负数。"

    time_to_accel = get_accel_time_in_seconds(max_speed)
    # 调用 get_pos 时，它的输入是帧数，所以需要转换
    dist_accel = get_pos(time_to_accel * FPS, max_speed, accel=True)

    time_to_decel = get_decel_time_in_seconds(max_speed)
    dist_decel = max_speed * time_to_decel - 0.5 * DECEL_SPEED * (time_to_decel**2)

    time_in_seconds = 0  # 先计算出总秒数

    # 情况 1: 匀速
    if not accel and not decel:
        time_in_seconds = pos / max_speed

    # 情况 2: 只有加速
    elif accel and not decel:
        if pos < dist_accel:
            time_in_seconds = math.sqrt(2 * pos / ACCEL_SPEED)
        else:
            pos_at_max_speed = pos - dist_accel
            time_at_max_speed = pos_at_max_speed / max_speed
            time_in_seconds = time_to_accel + time_at_max_speed

    # 情况 3: 只有减速
    elif not accel and decel:
        if pos < dist_decel:
            discriminant = (max_speed**2) - 2 * DECEL_SPEED * pos
            if discriminant < 0:
                return "错误: 在物理上不可能的减速距离。"
            time_in_seconds = (max_speed - math.sqrt(discriminant)) / DECEL_SPEED
        else:
            pos_at_max_speed = pos - dist_decel
            time_at_max_speed = pos_at_max_speed / max_speed
            time_in_seconds = time_to_decel + time_at_max_speed

    # 情况 4: 加速和减速
    elif accel and decel:
        dist_accel_and_decel = dist_accel + dist_decel
        if pos < dist_accel_and_decel:
            v_peak_sq = 2 * pos / (1 / ACCEL_SPEED + 1 / DECEL_SPEED)
            v_peak = math.sqrt(v_peak_sq)
            time_in_seconds = get_accel_time_in_seconds(v_peak) + get_decel_time_in_seconds(v_peak)
        else:
            pos_at_max_speed = pos - dist_accel_and_decel
            time_at_max_speed = pos_at_max_speed / max_speed
            time_in_seconds = time_to_accel + time_to_decel + time_at_max_speed

    # **【单位转换】** 将计算出的秒数转换为帧数返回
    return time_in_seconds * FPS


speed = SPEED_B
accel = True
decel = False
axis = "z"
max_fps = cmds.playbackOptions(q=True, max=True)
min_fps = cmds.playbackOptions(q=True, min=True)
time = max_fps - min_fps
end_pos = abs(cmds.getAttr(f"RIG:FKRootControls_M.t{axis}", t=max_fps))


true_time = get_time_in_frames(end_pos, speed, accel, decel)

accel_time = get_accel_time_in_seconds(speed * 60)
print("true_time: ", true_time)
print("end_time: ", min_fps + true_time)
print("accel_time: ", accel_time)
for x in range(int(true_time+1)):
    p = get_pos(x, speed, accel)
    print(f"fps: {min_fps + x} ", get_pos(x, speed, accel))
    cmds.setKeyframe(
        "RIG:FKRootControls_M",  # 物体
        attribute="t" + axis,  # 属性
        time=min_fps + x,  # 帧
        value=-p,  # 值
    )
