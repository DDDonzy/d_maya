import m_utils.compounds.matrixConstraint as matrixConstraint
from m_utils.create.createBase import AssetCallback
from maya import cmds

weapon_bone = "root_weapon"
attach_bones = ["root", "hand_r", "hand_l", "spine_05"]


for x in attach_bones:
    weapon_attach = cmds.createNode("joint", name=f"weapon_{x}", parent=x)
    with AssetCallback(name="RIG_ASSET", force=False):
        con = matrixConstraint(weapon_bone, weapon_attach, mo=0)