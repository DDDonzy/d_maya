from maya import cmds
import maya.mel as mel


ACCELERATION = 800
MAX_SPEED = 500
CURRENT_FRAMERATE = mel.eval("currentTimeUnitToFPS()")


def get_acceleration_time(max_speed = MAX_SPEED, acceleration=ACCELERATION):
    return max_speed / acceleration


def get_acceleration_distance(max_speed = MAX_SPEED, acceleration=ACCELERATION):
    time = get_acceleration_time(max_speed, acceleration)
    return 0.5 * acceleration * time ** 2


def get_distance_from_time(time, max_speed=MAX_SPEED, acceleration=ACCELERATION):
    acceleration_time = get_acceleration_time(max_speed, acceleration)
    acceleration_distance = get_acceleration_distance(max_speed, acceleration)
    
    if time < acceleration_time:
        return 0.5 * acceleration * time ** 2
    else:
        return acceleration_distance + max_speed * (time - acceleration_time)


def get_time_from_distance(distance, max_speed=MAX_SPEED, acceleration=ACCELERATION):
    acceleration_time = get_acceleration_time(max_speed, acceleration)
    acceleration_distance = get_acceleration_distance(max_speed, acceleration)
    
    if distance < acceleration_distance:
        return (2 * distance / acceleration) ** 0.5
    else:
        return acceleration_time + (distance - acceleration_distance) / max_speed


print(f"加速时间：{get_acceleration_time()}")
print(f"加速距离：{get_acceleration_distance()}")

print(f"移动1000个单位的时间：{get_time_from_distance(1000)}")
print(f"移动10s的距离：{get_distance_from_time(10)}")


start_frame = int(cmds.playbackOptions(query=True, minTime=True))
end_frame = int(cmds.playbackOptions(query=True, maxTime=True))

for x in range(start_frame,end_frame+1):
    cmds.currentTime(x)
    time = (x - start_frame) / CURRENT_FRAMERATE
    pos = get_distance_from_time(time)
    cmds.setAttr("locator1.translateX",pos)
    cmds.setKeyframe()