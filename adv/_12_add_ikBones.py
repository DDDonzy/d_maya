from maya import cmds
from m_utils.create.createBase import AssetCallback
from m_utils.compounds.matrixConstraint import matrixConstraint

cmds.createNode("joint", name="ik_foot_root", parent="root")
cmds.createNode("joint", name="ik_foot_l", parent="ik_foot_root")
cmds.createNode("joint", name="ik_foot_r", parent="ik_foot_root")
cmds.createNode("joint", name="ik_hand_root", parent="root")
cmds.createNode("joint", name="ik_hand_gun", parent="ik_hand_root")
cmds.createNode("joint", name="ik_hand_l", parent="ik_hand_gun")
cmds.createNode("joint", name="ik_hand_r", parent="ik_hand_gun")

with AssetCallback(name="RIG_ASSET", force=False):
    matrixConstraint("hand_r", "ik_hand_r", mo=0)
    matrixConstraint("hand_l", "ik_hand_l", mo=0)
    matrixConstraint("foot_r", "ik_foot_r", mo=0)
    matrixConstraint("foot_l", "ik_foot_l", mo=0)
    matrixConstraint("root", "ik_foot_root", mo=0)
    matrixConstraint("root", "ik_hand_root", mo=0)
    matrixConstraint("hand_r", "ik_hand_gun", mo=0)
