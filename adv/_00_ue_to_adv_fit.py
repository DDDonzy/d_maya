import m_utils.compounds.matrixConstraint as matrixConstraint
from m_utils.create.createBase import AssetCallback
from maya import cmds

fit_constraint_data = {
    "RootGround": {"driver": "root", "driven": "RootGround", "offsetMatrix": [1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1]},
    "Root": {"driver": "pelvis", "driven": "Root", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Spine1": {"driver": "spine_01", "driven": "Spine1", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Spine2": {"driver": "spine_02", "driven": "Spine2", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Spine3": {"driver": "spine_03", "driven": "Spine3", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Chest": {"driver": "spine_04", "driven": "Chest", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "ChestEnd": {"driver": "spine_05", "driven": "ChestEnd", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Scapula": {"driver": "clavicle_r", "driven": "Scapula", "offsetMatrix": [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Shoulder": {"driver": "upperarm_r", "driven": "Shoulder", "offsetMatrix": [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Elbow": {"driver": "lowerarm_r", "driven": "Elbow", "offsetMatrix": [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Wrist": {"driver": "hand_r", "driven": "Wrist", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "Cup": {"driver": "ring_metacarpal_r", "driven": "Cup", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 2, 0, 0, 1]},
    "ThumbFinger1": {"driver": "thumb_01_r", "driven": "ThumbFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "ThumbFinger2": {"driver": "thumb_02_r", "driven": "ThumbFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "ThumbFinger3": {"driver": "thumb_03_r", "driven": "ThumbFinger3", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "IndexFingerRoot": {"driver": "index_metacarpal_r", "driven": "IndexFingerRoot", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "IndexFinger1": {"driver": "index_01_r", "driven": "IndexFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "IndexFinger2": {"driver": "index_02_r", "driven": "IndexFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "IndexFinger3": {"driver": "index_03_r", "driven": "IndexFinger3", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "MiddleFingerRoot": {"driver": "middle_metacarpal_r", "driven": "MiddleFingerRoot", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "MiddleFinger1": {"driver": "middle_01_r", "driven": "MiddleFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "MiddleFinger2": {"driver": "middle_02_r", "driven": "MiddleFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "MiddleFinger3": {"driver": "middle_03_r", "driven": "MiddleFinger3", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "RingFingerRoot": {"driver": "ring_metacarpal_r", "driven": "RingFingerRoot", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "RingFinger1": {"driver": "ring_01_r", "driven": "RingFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "RingFinger2": {"driver": "ring_02_r", "driven": "RingFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "RingFinger3": {"driver": "ring_03_half_r", "driven": "RingFinger3", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "PinkyFingerRoot": {"driver": "pinky_metacarpal_r", "driven": "PinkyFingerRoot", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "PinkyFinger1": {"driver": "pinky_01_r", "driven": "PinkyFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "PinkyFinger2": {"driver": "pinky_02_r", "driven": "PinkyFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "PinkyFinger3": {"driver": "pinky_03_r", "driven": "PinkyFinger3", "offsetMatrix": [-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]},
    "Neck": {"driver": "neck_01", "driven": "Neck", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Neck1": {"driver": "neck_02", "driven": "Neck1", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Head": {"driver": "head", "driven": "Head", "offsetMatrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1]},
    "Hip": {"driver": "thigh_r", "driven": "Hip", "offsetMatrix": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "Knee": {"driver": "calf_r", "driven": "Knee", "offsetMatrix": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "Ankle": {"driver": "foot_r", "driven": "Ankle", "offsetMatrix": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "Toes": {"driver": "ball_r", "driven": "Toes", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootThumbFinger1": {"driver": "bigtoe_01_r", "driven": "FootThumbFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootThumbFinger2": {"driver": "bigtoe_02_r", "driven": "FootThumbFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootIndexFinger1": {"driver": "indextoe_01_r", "driven": "FootIndexFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootIndexFinger2": {"driver": "indextoe_02_r", "driven": "FootIndexFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootMiddleFinger1": {"driver": "middletoe_01_r", "driven": "FootMiddleFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootMiddleFinger2": {"driver": "middletoe_02_r", "driven": "FootMiddleFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootRingFinger1": {"driver": "ringtoe_01_r", "driven": "FootRingFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootRingFinger2": {"driver": "ringtoe_02_r", "driven": "FootRingFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootPinkyFinger1": {"driver": "littletoe_01_r", "driven": "FootPinkyFinger1", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
    "FootPinkyFinger2": {"driver": "littletoe_02_r", "driven": "FootPinkyFinger2", "offsetMatrix": [-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]},
}


with AssetCallback(name="ue_to_adv_fit_constraints"):
    for x in fit_constraint_data:
        con = matrixConstraint(fit_constraint_data[x]["driver"], fit_constraint_data[x]["driven"])
        cmds.setAttr(con.inputOffsetMatrix, fit_constraint_data[x]["offsetMatrix"], type="matrix")
