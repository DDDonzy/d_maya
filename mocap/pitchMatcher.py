from maya import cmds


object_attr = ".tx"
speed_attr = ".speed"

original_motion = cmds.keyframe(object_attr, query=True, valueChange=True) or []  # Get original motion values
original_keyframe = cmds.keyframe(object_attr, query=True, timeChange=True) or []  # Get original keyframe times
rates = [cmds.getAttr(speed_attr, t=x) for x in original_keyframe]  # Get speed rates at each keyframe time


new_motion = [original_motion[0]]  # output motion values
current_pos = new_motion[0]
for t in range(1, len(original_motion)):
    original_delta = original_motion[t] - original_motion[t - 1]  # Original delta movement
    rate = rates[t]  # Speed rate at this keyframe
    new_step = original_delta * rate  # Adjusted delta movement
    current_pos += new_step  # New position
    new_motion.append(current_pos)  # Append to output motion values
    cmds.keyframe(object_attr, e=1, t=(original_keyframe[t], original_keyframe[t]), vc=current_pos)  # Set new keyframe value



