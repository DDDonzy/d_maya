import numpy as np
import math
from collections import deque

class UE_MotionController:
    """
    一个模仿Unreal Engine角色移动概念的运动控制器。
    它管理一个移动指令队列，并能够平滑地过渡指令，同时允许为每个
    移动指定不同的目标速度。
    """
    def __init__(self, max_acceleration, braking_deceleration, max_walk_speed, min_analog_walk_speed=20.0, initial_position=None):
        """
        初始化运动控制器。

        Args:
            max_acceleration (float): 物体加速的速率 (对应UE的Max Acceleration)。
            braking_deceleration (float): 物体停止时的减速率 (对应UE的Braking Deceleration Walking)。
            max_walk_speed (float): 物体能达到的全局最大速度 (对应UE的Max Walk Speed)。
            min_analog_walk_speed (float, optional): 允许的最低行走速度 (对应UE的Min Analog Walk Speed)。
            initial_position (list or np.ndarray, optional): 初始位置 [x, y, z]。
        """
        self.max_acceleration = max_acceleration
        self.braking_deceleration = braking_deceleration
        self.max_walk_speed = max_walk_speed
        self.min_analog_walk_speed = min_analog_walk_speed

        self.position = np.array(initial_position, dtype=float) if initial_position else np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.state = 'idle'
        
        self.command_queue = deque()
        self.motion_plan = None

    def __repr__(self):
        pos_str = f"[{self.position[0]:.2f}, {self.position[1]:.2f}, {self.position[2]:.2f}]"
        vel_mag = np.linalg.norm(self.velocity)
        plan_speed = f"target_v={self.motion_plan['peak_velocity']:.2f}" if self.motion_plan else ""
        return (f"<UE_MotionController state='{self.state}' queue={len(self.command_queue)} "
                f"pos={pos_str} vel={vel_mag:.2f} {plan_speed}>")

    def add_move(self, distance, direction, target_speed=None):
        """
        向队列中添加一个新的移动任务，并可指定本次移动的目标速度。

        Args:
            distance (float): 移动距离 (m)。
            direction (list or np.ndarray): 移动方向向量 [x, y, z]。
            target_speed (float, optional): 本次移动的目标巡航速度。
                                           如果未提供，则默认为 max_walk_speed。
                                           该值会被限制在 [min_analog_walk_speed, max_walk_speed] 之间。
        """
        direction_vec = np.array(direction, dtype=float)
        norm = np.linalg.norm(direction_vec)
        if norm == 0: return

        # 确定并限制本次移动的目标速度
        peak_velocity = target_speed if target_speed is not None else self.max_walk_speed
        peak_velocity = np.clip(peak_velocity, self.min_analog_walk_speed, self.max_walk_speed)

        self.command_queue.append({
            "distance": distance,
            "direction": direction_vec / norm,
            "peak_velocity": peak_velocity
        })
        print(f"指令已添加: 移动 {distance:.2f}m, 目标速度 {peak_velocity:.2f} m/s。队列中现有 {len(self.command_queue)} 个指令。")

    def _plan_next_move(self):
        if not self.command_queue: return

        current_cmd = self.command_queue.popleft()
        distance = current_cmd["distance"]
        direction = current_cmd["direction"]
        peak_velocity = current_cmd["peak_velocity"]
        
        next_cmd_exists = len(self.command_queue) > 0
        
        t_accel = peak_velocity / self.max_acceleration
        dist_accel = 0.5 * self.max_acceleration * t_accel**2
        
        transition_type = 'decelerate'
        t_transition = peak_velocity / self.braking_deceleration
        dist_transition_along_axis = 0.5 * self.braking_deceleration * t_transition**2
        next_direction = None

        if next_cmd_exists:
            next_cmd = self.command_queue[0]
            next_peak_velocity = next_cmd["peak_velocity"]
            next_direction = next_cmd["direction"]

            transition_type = 'blend'
            t_decel_for_blend = peak_velocity / self.braking_deceleration
            t_accel_for_blend = next_peak_velocity / self.max_acceleration
            t_transition = max(t_decel_for_blend, t_accel_for_blend)
            dist_transition_along_axis = peak_velocity * t_decel_for_blend - 0.5 * self.braking_deceleration * t_decel_for_blend**2

        dist_cruise = distance - dist_accel - dist_transition_along_axis
        if dist_cruise < 0: dist_cruise = 0
        t_cruise = dist_cruise / peak_velocity if peak_velocity > 0 else 0

        self.motion_plan = {
            "direction": direction,
            "peak_velocity": peak_velocity,
            "t_accel": t_accel,
            "t_cruise": t_cruise,
            "t_transition": t_transition,
            "transition_type": transition_type,
            "next_direction": next_direction,
            "total_time": t_accel + t_cruise + t_transition,
            "time_elapsed": 0.0
        }
        self.state = 'accelerating'

    def update(self, dt):
        if self.state == 'idle' and self.command_queue:
            self._plan_next_move()
        if self.state == 'idle': return

        plan = self.motion_plan
        plan['time_elapsed'] += dt
        t_elapsed = plan['time_elapsed']
        
        t_accel_end = plan['t_accel']
        t_cruise_end = t_accel_end + plan['t_cruise']
        
        if t_elapsed <= t_accel_end:
            self.state = 'accelerating'
            vel_mag = self.max_acceleration * t_elapsed
            self.velocity = plan['direction'] * min(vel_mag, plan['peak_velocity'])
        
        elif t_elapsed <= t_cruise_end:
            self.state = 'cruising'
            self.velocity = plan['direction'] * plan['peak_velocity']

        else:
            self.state = plan['transition_type']
            time_in_transition = t_elapsed - t_cruise_end
            
            if self.state == 'blend':
                vel_mag_current = max(0, plan['peak_velocity'] - self.braking_deceleration * time_in_transition)
                next_peak_vel = self.command_queue[0]['peak_velocity'] if self.command_queue else self.max_walk_speed
                vel_mag_next = min(next_peak_vel, self.max_acceleration * time_in_transition)
                self.velocity = (plan['direction'] * vel_mag_current) + (plan['next_direction'] * vel_mag_next)
            
            elif self.state == 'decelerate':
                vel_mag = max(0, plan['peak_velocity'] - self.braking_deceleration * time_in_transition)
                self.velocity = plan['direction'] * vel_mag

        self.position += self.velocity * dt

        if t_elapsed >= plan['total_time']:
            self.state = 'idle'
            print(f"计划段结束。当前速度 {np.linalg.norm(self.velocity):.2f} m/s。")
            if not self.command_queue:
                self.velocity = np.array([0.0, 0.0, 0.0]) # 确保最终停止
                print("所有指令已完成。")
                
                
                
# 1. 用UE风格的参数创建控制器实例
#   - 加速很快
#   - 刹车也很快
#   - 最高能跑 30 m/s
character = UE_MotionController(
    max_acceleration=25.0, 
    braking_deceleration=30.0, 
    max_walk_speed=30.0,
    min_analog_walk_speed=5.0
)
print("角色控制器已创建:", character)
print("-" * 50)

# 2. 连续添加三个移动指令，具有不同的目标速度
#   - 指令1: 冲刺 (使用默认最大速度)
character.add_move(distance=100, direction=[1, 0, 0])
#   - 指令2: 慢走 (指定一个较低的速度)
character.add_move(distance=100, direction=[0, 1, 0])
#   - 指令3: 再次冲刺
character.add_move(distance=100, direction=[-1, 0, 0])
print("-" * 50)


from maya import cmds
# 3. 运行模拟循环
dt = 0.2
total_sim_time = 0
print("开始模拟...")
while character.state != 'idle' or character.command_queue:
    character.update(dt)
    total_sim_time += dt
    cmds.spaceLocator(name="motion_locator", position=character.position.tolist())
    print(f"Time: {total_sim_time:5.2f}s, {character}")