# -----------------------------------------------------------------
# 1. 定义你的主脚本逻辑
# -----------------------------------------------------------------
"""
运动学计算脚本 (3D 向量版 + 动态 Root 管理)
"""

import math
import functools
from typing import Dict, List

import maya.cmds as cmds

# --- 全局配置常量 ---
# 这是默认创建的 Locator 名称，如果场景里没有指定物体，点击赋值按钮会创建这个
DEFAULT_ROOT_NAME = "rootMotion" 


class UESpeed:
    FPS = 60
    # sprint
    sprint = 700
    sprint_accel = 800
    sprint_decel = 800

    # run speeds
    run_f = 500
    run_b = 320
    run_lp = 400
    run_ln = 400
    run_rp = 400
    run_rn = 400
    run_accel = 800
    run_decel = 800

    # walk speeds
    walk_f = 170
    walk_b = 150
    walk_lp = 160
    walk_ln = 150
    walk_rp = 160
    walk_rn = 150
    walk_accel = 400
    walk_decel = 800


# --- 辅助工具函数 ---

def get_current_position(node: str) -> List[float]:
    """获取物体当前的世界坐标 [x, y, z]"""
    if not cmds.objExists(node):
        raise ValueError(f"Object '{node}' does not exist.")
    return cmds.xform(node, query=True, translation=True, worldSpace=True)


def get_direction_vector(axis_attr: str, is_positive: bool) -> List[float]:
    """
    根据UI选择的轴和方向，返回归一化的方向向量。
    """
    direction = 1.0 if is_positive else -1.0
    
    if axis_attr == "tx":
        return [direction, 0.0, 0.0]
    elif axis_attr == "ty":
        return [0.0, direction, 0.0]
    elif axis_attr == "tz":
        return [0.0, 0.0, direction]
    else:
        return [1.0, 0.0, 0.0] 


def timeSliderBookmark(name: str, time: List[int], color: List[float], priority: int = 1) -> str:
    """在Maya时间轴上创建一个书签标记"""
    bookmark_name = f"timeSliderBookmark_{name}"
    # 简单的防重名处理，实际项目中可以做更复杂的查找
    bookmark = cmds.createNode("timeSliderBookmark", name=bookmark_name)
    cmds.setAttr(f"{bookmark}.name", name, type="string")
    cmds.setAttr(f"{bookmark}.color", *color)
    cmds.setAttr(f"{bookmark}.timeRangeStart", time[0])
    cmds.setAttr(f"{bookmark}.timeRangeStop", time[1])
    cmds.setAttr(f"{bookmark}.priority", priority)
    return bookmark


# --- 核心计算函数 (纯数学计算，不依赖物体) ---

def fn_loop(
    speed=500,
    loop_frames=60,
    start_pos_vec=[0.0, 0.0, 0.0],
    direction_vec=[0.0, 0.0, 1.0],
    initial_frame=0,
    sample_fps=60,
):
    motion_info: Dict[str, list] = {
        "frames_range": [initial_frame, initial_frame + loop_frames],
        "motion_data": [],  # [frame, x, y, z]
    }

    for frame in range(loop_frames + 1):
        current_time = frame / float(sample_fps)
        scalar_dist = speed * current_time
        
        curr_x = start_pos_vec[0] + (direction_vec[0] * scalar_dist)
        curr_y = start_pos_vec[1] + (direction_vec[1] * scalar_dist)
        curr_z = start_pos_vec[2] + (direction_vec[2] * scalar_dist)

        motion_info["motion_data"].append([initial_frame + frame, curr_x, curr_y, curr_z])

    timeSliderBookmark(name="loop", time=[initial_frame, initial_frame + loop_frames + 1], color=[0.6, 0.263, 0.431])
    return motion_info


def fn_accel(
    initial_speed=0.0,
    accel=1000.0,
    max_speed=500.0,
    start_pos_vec=[0.0, 0.0, 0.0],
    direction_vec=[0.0, 0.0, 1.0],
    initial_frame=0,
    sample_fps=60,
):
    if accel <= 0:
        raise ValueError("加速度必须为正数。")

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
            
        scalar_dist = (initial_speed * current_time) + (0.5 * accel * (current_time**2))
        
        curr_x = start_pos_vec[0] + (direction_vec[0] * scalar_dist)
        curr_y = start_pos_vec[1] + (direction_vec[1] * scalar_dist)
        curr_z = start_pos_vec[2] + (direction_vec[2] * scalar_dist)

        motion_info["motion_data"].append([initial_frame + frame, curr_x, curr_y, curr_z])

    timeSliderBookmark(name="accel", time=[initial_frame, initial_frame + accel_frames + 1], color=[0.67, 0.235, 0.235])
    return motion_info


def fn_decel(
    initial_speed=500.0,
    decel=1000.0,
    min_speed=0.0,
    start_pos_vec=[0.0, 0.0, 0.0],
    direction_vec=[0.0, 0.0, 1.0],
    initial_frame=0,
    sample_fps=60,
):
    if decel <= 0:
        raise ValueError("减速度必须为正数")

    decel_times = (initial_speed - min_speed) / decel
    decel_frames = math.ceil(decel_times * sample_fps)

    motion_info: Dict[str, list] = {
        "frames_range": [initial_frame, initial_frame + decel_frames],
        "motion_data": [],
    }
    
    for frame in range(decel_frames + 1):
        current_time = frame / float(sample_fps)
        scalar_dist = (initial_speed * current_time) - (0.5 * decel * (current_time**2))
        
        curr_x = start_pos_vec[0] + (direction_vec[0] * scalar_dist)
        curr_y = start_pos_vec[1] + (direction_vec[1] * scalar_dist)
        curr_z = start_pos_vec[2] + (direction_vec[2] * scalar_dist)
        
        motion_info["motion_data"].append([initial_frame + frame, curr_x, curr_y, curr_z])

    timeSliderBookmark(name="decel", time=[initial_frame, initial_frame + decel_frames + 1], color=[0.749, 0.4, 0.235])
    return motion_info


def key_motion_data(motion_data: Dict[str, list], target_node: str):
    """
    将 3D 运动数据应用到指定的 target_node。
    """
    if not motion_data:
        raise ValueError("Please input motion data")

    if not cmds.objExists(target_node):
        raise RuntimeError(f"Target object '{target_node}' not found in scene.")
    
    for item in motion_data["motion_data"]:
        frame = item[0]
        val_x, val_y, val_z = item[1], item[2], item[3]
        
        cmds.setKeyframe(target_node, attribute="tx", value=val_x, time=frame)
        cmds.setKeyframe(target_node, attribute="ty", value=val_y, time=frame)
        cmds.setKeyframe(target_node, attribute="tz", value=val_z, time=frame)


# --- 脚本执行逻辑 (UI 对接层) ---

def run_loop_script(target_node, attr_axis, is_positive, max_speed, accel, decel):
    if not target_node:
        cmds.warning("No Root object specified!")
        return
        
    print(f"Loop -> Target:{target_node}, Axis:{attr_axis}, Speed:{max_speed}")
    
    loop_frames = abs(int(cmds.playbackOptions(q=1, sst=1)) - int(cmds.playbackOptions(q=1, set=1)))
    start_frame = int(cmds.playbackOptions(q=1, sst=1))
    
    start_pos = get_current_position(target_node)
    direction = get_direction_vector(attr_axis, is_positive)

    loop_data = fn_loop(
        speed=max_speed,
        loop_frames=loop_frames,
        start_pos_vec=start_pos,
        direction_vec=direction,
        initial_frame=start_frame,
        sample_fps=60,
    )

    key_motion_data(loop_data, target_node)


def run_accel_script(target_node, attr_axis, is_positive, max_speed, accel, decel):
    if not target_node:
        cmds.warning("No Root object specified!")
        return

    print(f"Accel -> Target:{target_node}, Speed:{max_speed}")
    
    start_frame = int(cmds.currentTime(q=1))
    start_pos = get_current_position(target_node)
    direction = get_direction_vector(attr_axis, is_positive)

    data = fn_accel(
        initial_speed=0.0,
        accel=accel,
        max_speed=max_speed,
        start_pos_vec=start_pos,
        direction_vec=direction,
        initial_frame=start_frame,
        sample_fps=60,
    )

    key_motion_data(data, target_node)


def run_decel_script(target_node, attr_axis, is_positive, max_speed, accel, decel):
    if not target_node:
        cmds.warning("No Root object specified!")
        return

    print(f"Decel -> Target:{target_node}, Speed:{max_speed}")
    
    start_frame = int(cmds.currentTime(q=1))
    start_pos = get_current_position(target_node)
    direction = get_direction_vector(attr_axis, is_positive)

    data = fn_decel(
        initial_speed=max_speed,
        decel=decel,
        min_speed=0.0,
        start_pos_vec=start_pos,
        direction_vec=direction,
        initial_frame=start_frame,
        sample_fps=60,
    )

    key_motion_data(data, target_node)


# -----------------------------------------------------------------
# 2. UI 回调
# -----------------------------------------------------------------

ui_elements = {}
window_name = "simpleAxisUI"


def on_assign_root_click(*args):
    """
    Root 栏目旁边的按钮回调：
    1. 如果选择了物体 -> 将其填入文本框
    2. 如果未选择物体 -> 创建默认 Locator (如果不存在) 并填入文本框
    """
    selection = cmds.ls(selection=True)
    
    target_name = ""
    
    if selection:
        # 情况1: 有选择，使用选择的第一个物体
        target_name = selection[0]
    else:
        # 情况2: 无选择，检查是否存在常量物体，不存在则创建
        if not cmds.objExists(DEFAULT_ROOT_NAME):
            cmds.spaceLocator(name=DEFAULT_ROOT_NAME)
            cmds.setAttr(f"{DEFAULT_ROOT_NAME}.localScale", *(100, 100, 100))
            print(f"Created default root: {DEFAULT_ROOT_NAME}")
        target_name = DEFAULT_ROOT_NAME
    
    # 更新 UI 文本框
    if target_name:
        cmds.textFieldButtonGrp(ui_elements["root_field"], edit=True, text=target_name)
        print(f"Root set to: {target_name}")


def _query_common_ui_values():
    """查询UI并返回: 目标物体名, 轴向, 方向, 速度参数"""
    
    # 获取 Root 物体名
    target_root = cmds.textFieldButtonGrp(ui_elements["root_field"], query=True, text=True)

    selected_axis = cmds.radioCollection(ui_elements["axis_collection"], query=True, select=True)
    if selected_axis == "x_rb":
        attr = "tx"
    elif selected_axis == "y_rb":
        attr = "ty"
    elif selected_axis == "z_rb":
        attr = "tz"
    else:
        attr = "tz"

    selected_dir = cmds.radioCollection(ui_elements["dir_collection"], query=True, select=True)
    is_positive = (selected_dir == "plus_rb")

    max_speed = cmds.floatFieldGrp(ui_elements["maxSpeed_field"], query=True, value1=True)
    accel = cmds.floatFieldGrp(ui_elements["accel_field"], query=True, value1=True)
    decel = cmds.floatFieldGrp(ui_elements["decel_field"], query=True, value1=True)

    return target_root, attr, is_positive, max_speed, accel, decel


def on_loop_click(*args):
    target, attr, is_pos, speed, acc, dec = _query_common_ui_values()
    run_loop_script(target, attr, is_pos, speed, acc, dec)


def on_accel_click(*args):
    target, attr, is_pos, speed, acc, dec = _query_common_ui_values()
    run_accel_script(target, attr, is_pos, speed, acc, dec)


def on_decel_click(*args):
    target, attr, is_pos, speed, acc, dec = _query_common_ui_values()
    run_decel_script(target, attr, is_pos, speed, acc, dec)


def set_speed_values(max_speed, accel, decel, *args):
    try:
        cmds.floatFieldGrp(ui_elements["maxSpeed_field"], edit=True, value1=max_speed)
        cmds.floatFieldGrp(ui_elements["accel_field"], edit=True, value1=accel)
        cmds.floatFieldGrp(ui_elements["decel_field"], edit=True, value1=decel)
        print(f"Preset set: MaxSpeed={max_speed}, Accel={accel}, Decel={decel}")
    except KeyError:
        pass
    except RuntimeError:
        pass


# -----------------------------------------------------------------
# 3. UI 创建
# -----------------------------------------------------------------

def create_simple_ui():
    global ui_elements, window_name

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)

    cmds.window(window_name, title="UE Speed Tools", widthHeight=(280, 600), s=True)

    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=['both', 5])

    # --- 1. Root 对象选择区域 (新增) ---
    cmds.frameLayout(label="Target Root Settings", collapsable=False)
    
    # 查找默认物体逻辑
    default_text = ""
    # 尝试查找 *:FKRootGround_M
    found_roots = cmds.ls("*:FKRootGround_M", recursive=True, long=False)
    if not found_roots:
        # 如果没找到带 namespace 的，也可以试着找不带的 FKRootGround_M
        found_roots = cmds.ls("FKRootGround_M", recursive=True, long=False)
        
    if found_roots:
        default_text = found_roots[0] # 取找到的第一个
        print(f"Auto-detected root: {default_text}")
    else:
        # 如果也没找到 FKRootGround_M，检查是否有默认的 rootMotion
        if cmds.objExists(DEFAULT_ROOT_NAME):
             default_text = DEFAULT_ROOT_NAME
    
    ui_elements["root_field"] = cmds.textFieldButtonGrp(
        label="Root:", 
        text=default_text,
        buttonLabel="<<<",
        buttonCommand=on_assign_root_click,
        columnWidth3=[70, 120, 80],
        adjustableColumn=2
    )
    cmds.setParent("..") # End frameLayout

    # --- 2. 轴向与方向选择 ---
    cmds.frameLayout(label="Configuration", collapsable=False)
    ui_elements["axis_collection"] = cmds.radioCollection()
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[80, 80, 80])
    cmds.radioButton("x_rb", label="X")
    cmds.radioButton("y_rb", label="Y")
    cmds.radioButton("z_rb", label="Z", select=True)
    cmds.setParent("..")

    ui_elements["dir_collection"] = cmds.radioCollection()
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[120, 120])
    cmds.radioButton("plus_rb", label="+ (Positive)", select=True)
    cmds.radioButton("minus_rb", label="- (Negative)")
    cmds.setParent("..")
    cmds.setParent(main_layout)

    # --- 3. 数值输入框 ---
    ui_elements["maxSpeed_field"] = cmds.floatFieldGrp(label="Max Speed", numberOfFields=1, value1=500.0, columnWidth2=[80, 100])
    ui_elements["accel_field"] = cmds.floatFieldGrp(label="Accel", numberOfFields=1, value1=800.0, columnWidth2=[80, 100])
    ui_elements["decel_field"] = cmds.floatFieldGrp(label="Decel", numberOfFields=1, value1=800.0, columnWidth2=[80, 100])

    cmds.separator(h=10, style="in")

    # --- 4. 预设按钮区域 ---
    cmds.text(label="Run Presets:", align='left')
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[65, 65, 65, 65])
    cmds.button(label="Run_F", command=functools.partial(set_speed_values, UESpeed.run_f, UESpeed.run_accel, UESpeed.run_decel))
    cmds.button(label="Run_L/R", command=functools.partial(set_speed_values, UESpeed.run_lp, UESpeed.run_accel, UESpeed.run_decel))
    cmds.button(label="Run_Side", command=functools.partial(set_speed_values, UESpeed.run_ln, UESpeed.run_accel, UESpeed.run_decel))
    cmds.button(label="Run_B", command=functools.partial(set_speed_values, UESpeed.run_b, UESpeed.run_accel, UESpeed.run_decel))
    cmds.setParent(main_layout)

    cmds.text(label="Walk Presets:", align='left')
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[65, 65, 65, 65])
    cmds.button(label="Walk_F", command=functools.partial(set_speed_values, UESpeed.walk_f, UESpeed.walk_accel, UESpeed.walk_decel))
    cmds.button(label="Walk_L/R", command=functools.partial(set_speed_values, UESpeed.walk_lp, UESpeed.walk_accel, UESpeed.walk_decel))
    cmds.button(label="Walk_Side", command=functools.partial(set_speed_values, UESpeed.walk_ln, UESpeed.walk_accel, UESpeed.walk_decel))
    cmds.button(label="Walk_B", command=functools.partial(set_speed_values, UESpeed.walk_b, UESpeed.walk_accel, UESpeed.walk_decel))
    cmds.setParent(main_layout)

    cmds.text(label="Sprint Preset:", align='left')
    cmds.button(label="Sprint", command=functools.partial(set_speed_values, UESpeed.sprint, UESpeed.sprint_accel, UESpeed.sprint_decel))

    # --- 5. 动作执行按钮 ---
    cmds.separator(h=20, style="double")
    cmds.button(label="GENERATE LOOP", command=on_loop_click, height=40, backgroundColor=[0.2, 0.4, 0.3])
    cmds.button(label="GENERATE ACCEL", command=on_accel_click, height=30)
    cmds.button(label="GENERATE DECEL", command=on_decel_click, height=30)

    cmds.showWindow(window_name)


# -----------------------------------------------------------------
# 4. 运行脚本
# -----------------------------------------------------------------
if __name__ == "__main__":
    create_simple_ui()