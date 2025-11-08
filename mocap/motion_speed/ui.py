import maya.cmds as cmds
import functools  # <-- 我们需要这个来实现简洁的按钮命令

# -----------------------------------------------------------------
# 1. 定义你的主脚本逻辑 (与之前相同)
# -----------------------------------------------------------------


def run_script_with_ui_values(attr, is_positive, max_speed, accel, decel):
    print(attr, is_positive, max_speed, accel, decel)
    if not cmds.objExists("rootMotion"):
        cmds.spaceLocator(name="rootMotion")

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

    ui_elements["decel_field"] = cmds.floatFieldGrp(label="Decel", numberOfFields=1, value1=2000.0, columnWidth2=[80, 100])

    cmds.setParent(main_layout)

    cmds.separator(h=10, style="in")

    # 布局参数: 4列, 间距为5, 每列宽度60
    btn_width = 60
    btn_spacing = 5

    # --- Row 1: Run ---
    cmds.rowLayout(numberOfColumns=4)
    cmds.button(label="Run_F", w=60, command=functools.partial(set_speed_values, 500, 1000, 2000))
    cmds.button(label="Run_LRP", w=60, command=functools.partial(set_speed_values, 450, 1000, 2000))
    cmds.button(label="Run_LRN", w=60, command=functools.partial(set_speed_values, 400, 1000, 2000))
    cmds.button(label="Run_B", w=60, command=functools.partial(set_speed_values, 400, 1000, 2000))
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
    cmds.button(label="Sprint", command=functools.partial(set_speed_values, 700, 1000, 2000), width=full_width)
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
