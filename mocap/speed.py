import math
from maya import cmds

from mocap.gameExportInfo import get_exportData, create_exportData

# --- 常量定义 (单位基于秒) ---
FPS = 60
SPRINT = 700
RUN_F = 500  # 最大前进速度 (单位/秒)
RUN_B = 300
RUN_L = 350
RUN_R = 350
ACCEL_SPEED = 800  # 加速度 (单位/秒^2)
DECEL_SPEED = 1000  # 减速度 (单位/秒^2)


def get_accel_time_to_speed(target_speed):
    """计算加速到目标速度所需的时间(秒)"""
    return target_speed / ACCEL_SPEED


def get_decel_time_from_speed(initial_speed):
    """计算从初始速度减速到0所需的时间(秒)"""
    return initial_speed / DECEL_SPEED


def get_position_at_time(time_in_seconds, total_motion_duration, max_speed, accel=False, decel=False):
    """
    根据总运动信息，计算在特定时间点的瞬时位移

    Args:
        time_in_seconds (float): 要求值的当前时间点(秒)
        max_speed (float): 最大速度
        total_motion_duration (float): 整个运动的总持续时间(秒)
        accel (bool): 是否包含加速阶段
        decel (bool): 是否包含减速阶段

    Returns:
        float: 在 time_in_seconds 时的位移
    """
    time_to_max_speed = get_accel_time_to_speed(max_speed) if accel else 0
    time_to_stop = get_decel_time_from_speed(max_speed) if decel else 0

    # 情况1: 匀速运动
    if not accel and not decel:
        return max_speed * time_in_seconds

    # 情况2: 只有加速 (加速 -> 匀速)
    elif accel and not decel:
        if time_in_seconds <= time_to_max_speed:
            return 0.5 * ACCEL_SPEED * (time_in_seconds**2)
        else:
            accel_distance = 0.5 * ACCEL_SPEED * (time_to_max_speed**2)
            constant_time = time_in_seconds - time_to_max_speed
            constant_distance = max_speed * constant_time
            return accel_distance + constant_distance

    # 情况3: 只有减速 (匀速 -> 减速)
    elif not accel and decel:
        # 减速阶段开始的时间点
        decel_start_time = total_motion_duration - time_to_stop

        if time_in_seconds <= decel_start_time:
            # 仍在匀速阶段
            return max_speed * time_in_seconds
        else:
            # 进入减速阶段
            constant_distance = max_speed * decel_start_time
            time_into_decel = time_in_seconds - decel_start_time
            # 使用减速公式计算减速阶段的位移
            decel_distance = max_speed * time_into_decel - 0.5 * DECEL_SPEED * (time_into_decel**2)
            return constant_distance + decel_distance

    # 情况4: 既有加速又有减速 (加速 -> 匀速 -> 减速)
    elif accel and decel:
        constant_duration = total_motion_duration - time_to_max_speed - time_to_stop

        # 判断当前时间处于哪个阶段
        if time_in_seconds <= time_to_max_speed:
            # 1. 加速阶段
            return 0.5 * ACCEL_SPEED * (time_in_seconds**2)
        elif time_in_seconds <= time_to_max_speed + constant_duration:
            # 2. 匀速阶段
            accel_distance = 0.5 * ACCEL_SPEED * (time_to_max_speed**2)
            constant_time = time_in_seconds - time_to_max_speed
            constant_distance = max_speed * constant_time
            return accel_distance + constant_distance
        else:
            # 3. 减速阶段
            accel_distance = 0.5 * ACCEL_SPEED * (time_to_max_speed**2)
            constant_distance = max_speed * constant_duration

            decel_start_time = time_to_max_speed + constant_duration
            time_into_decel = time_in_seconds - decel_start_time
            decel_distance = max_speed * time_into_decel - 0.5 * DECEL_SPEED * (time_into_decel**2)
            return accel_distance + constant_distance + decel_distance

    return 0


def get_time_from_distance(distance, max_speed, accel=False, decel=False):
    """
    根据位移距离计算所需运动时间

    Args:
        distance (float): 位移距离
        max_speed (float): 最大速度
        accel (bool): 是否包含加速阶段
        decel (bool): 是否包含减速阶段

    Returns:
        float: 运动时间(秒)
    """
    if distance < 0:
        raise ValueError("距离不能为负数")

    # 情况1: 匀速运动
    if not accel and not decel:
        return distance / max_speed

    # 情况2: 只有加速
    elif accel and not decel:
        # 计算加速到最大速度所需的距离
        time_to_max_speed = get_accel_time_to_speed(max_speed)
        distance_to_max_speed = 0.5 * ACCEL_SPEED * (time_to_max_speed**2)

        if distance <= distance_to_max_speed:
            # 整个运动都在加速阶段
            return math.sqrt(2 * distance / ACCEL_SPEED)
        else:
            # 加速到最大速度后保持匀速
            constant_distance = distance - distance_to_max_speed
            constant_time = constant_distance / max_speed
            return time_to_max_speed + constant_time

    # 情况3: 只有减速
    elif not accel and decel:
        # 计算从最大速度减速到0所需的距离
        time_to_stop = get_decel_time_from_speed(max_speed)
        distance_to_stop = 0.5 * DECEL_SPEED * (time_to_stop**2)

        if distance <= distance_to_stop:
            # 整个运动都在减速阶段
            # 解方程: distance = max_speed * t - 0.5 * DECEL_SPEED * t^2
            discriminant = max_speed**2 - 2 * DECEL_SPEED * distance
            if discriminant < 0:
                raise ValueError("在物理上不可能的减速距离")

            # 选择合理的解 (时间应该小于减速到0所需的时间)
            t1 = (max_speed - math.sqrt(discriminant)) / DECEL_SPEED
            t2 = (max_speed + math.sqrt(discriminant)) / DECEL_SPEED

            return min(t1, t2) if t1 > 0 else t2
        else:
            # 先匀速后减速
            constant_distance = distance - distance_to_stop
            constant_time = constant_distance / max_speed
            return constant_time + time_to_stop

    # 情况4: 既有加速又有减速
    elif accel and decel:
        # 计算加速和减速阶段的总距离
        time_to_max_speed = get_accel_time_to_speed(max_speed)
        time_to_stop = get_decel_time_from_speed(max_speed)

        distance_accel = 0.5 * ACCEL_SPEED * (time_to_max_speed**2)
        distance_decel = 0.5 * DECEL_SPEED * (time_to_stop**2)
        total_accel_decel_distance = distance_accel + distance_decel

        if distance <= total_accel_decel_distance:
            # 无法达到最大速度，需要计算实际峰值速度
            # 根据距离计算峰值速度
            peak_speed = math.sqrt(2 * distance * (ACCEL_SPEED * DECEL_SPEED) / (ACCEL_SPEED + DECEL_SPEED))
            accel_time = peak_speed / ACCEL_SPEED
            decel_time = peak_speed / DECEL_SPEED
            return accel_time + decel_time
        else:
            # 完整的加速-匀速-减速过程
            constant_distance = distance - total_accel_decel_distance
            constant_time = constant_distance / max_speed
            return time_to_max_speed + constant_time + time_to_stop



def log_info():
    print("\n" * 2)
    print("=" * 120)
    print("Original Animation Info:")
    print(f"    - Animation Duration:           {time:.2f} frames ({time / FPS:.2f} sec)")
    print(f"    - Animation Frame Range:        [{min_fps:.2f} - {max_fps:.2f}] frames")
    print("-" * 120)
    print("Motion Analysis Results:")
    print(f"    - Distance:                     {dis:.2f} units (Axis-{axis.upper()})")
    print(f"    - Has Accel:                    {accel}")
    print(f"    - Has Decel:                    {decel}")
    if accel:
        print(f"    - Accel:                        {speed} units/sec²")
        print(f"    - Accel Time:                   {accel_time:.2f} frames ({accel_time / FPS:.2f} sec)")
        print(f"    - Accel Frames Range:           [{min_fps} - {min_fps + accel_time:.2f}] frames")

    print(f"    - Max Speed:                    {speed:.2f} units/sec")
    print(f"    - Duration:                     {motion_time:.2f} frames ({motion_time / FPS:.2f} sec)")
    print(f"    - Max Speed Frames Range:       [{min_fps + accel_time:.2f} - {modify_end_time - decel_time:.2f}] frames")

    if decel:
        print(f"    - Decel:                        {DECEL_SPEED} units/sec²")
        print(f"    - Decel Time:                   {decel_time:.2f} frames ({decel_time / FPS:.2f} sec)")
        print(f"    - Decel Frames Range:           [{modify_end_time - decel_time:.2f} - {modify_end_time:.2f}] frames")

    print("-" * 120)
    print("Modify: ")

    print(f"    - Animation Duration:           {motion_time:.2f} frames ({motion_time / FPS:.2f} sec)")
    print(f"    - Animation Frame Range:        [{min_fps:.2f} - {modify_end_time:.2f}] frames")
    print("=" * 120)


def do():
    # cmds.scaleKey(find_animCurveNode(), time=(min_fps, max_fps), newStartTime=min_fps, newEndTime=modify_end_time)
    # merge_animLayers()
    cmds.select(clear=True)

    rootMotionLayer = "RootMotion"
    if not cmds.objExists(rootMotionLayer):
        rootMotionLayer = cmds.animLayer(rootMotionLayer)

    cmds.setAttr(f"{rootMotionLayer}.rotationAccumulationMode", 0)
    cmds.setAttr(f"{rootMotionLayer}.scaleAccumulationMode", 1)
    cmds.animLayer(rootMotionLayer, edit=True, override=True)

    target_object = "RIG:FKRootControls_M"
    cmds.select(target_object)
    cmds.animLayer(rootMotionLayer, edit=True, addSelectedObjects=True)
    cmds.animLayer(rootMotionLayer, edit=True, selected=True)

    for x in range(int(motion_time + 1)):
        current_time_sec = x / FPS
        total_motion_sec = motion_time / FPS

        p = dis_s + get_position_at_time(current_time_sec, total_motion_sec, speed, accel, decel)

        cmds.setKeyframe(
            target_object,  # 物体
            attribute="t" + axis,  # 属性
            time=min_fps + x,  # 帧
            value=p * p_or_n,  # 值
        )

    target_attribute = f"{target_object}.t{axis}"
    cmds.keyTangent(target_attribute, itt="clamped", ott="clamped")

    cmds.setInfinity(target_attribute, pri="constant")
    if not decel:
        cmds.setInfinity(target_attribute, poi="linear")
    else:
        cmds.setInfinity(target_attribute, poi="constant")

    data = get_exportData()
    if data and "clip" in data:
        for k, v in data["clip"].items():
            data["clip"][k] = (min_fps, modify_end_time)
            break
        create_exportData(data)


speed = RUN_L
accel = False
decel = False
axis = "x"


axis = axis.lower()
min_fps = cmds.playbackOptions(q=True, min=True)
max_fps = cmds.playbackOptions(q=True, max=True)
time = max_fps - min_fps
dis_s = cmds.getAttr(f"RIG:FKRootControls_M.t{axis}", t=min_fps)
dis_e = cmds.getAttr(f"RIG:FKRootControls_M.t{axis}", t=max_fps)
dis = dis_e - dis_s
p_or_n = 1 if dis >= 0 else -1
dis = abs(dis)
motion_time = round(get_time_from_distance(dis, speed, accel, decel) * FPS)
accel_time = round(get_accel_time_to_speed(speed) * FPS if accel else 0)
decel_time = round(get_decel_time_from_speed(speed) * FPS if decel else 0)
#
modify_end_time = min_fps + motion_time


log_info()

do()
