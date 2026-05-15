# 添加自定义骨骼，比如武器


from m_utils.rename import rename
import m_utils.compounds.matrixConstraint as matrixConstraint
from m_utils.create.createBase import AssetCallback
from m_utils.dag.iterHierarchy import IterHierarchy

from maya import cmds

adv_weapon = [x for x, _ in IterHierarchy("WeaponGimbal_R")]
weapon = cmds.duplicate(adv_weapon[0], name="dup_weapon", rc=1)

cmds.parent(weapon[0], "hand_r")

cmds.select(weapon)

new_name = rename("weapon", weapon)


with AssetCallback(name="RIG_ASSET", force=False):
    for i, _ in enumerate(new_name):
        matrixConstraint(adv_weapon[i], new_name[i], mo=0)
