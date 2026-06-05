from m_utils.compounds import parentSpaceConstraint
from m_utils.create.createBase import AssetCallback
from maya import cmds

with AssetCallback(name="RIG_ASSET", force=False):
    pcs = parentSpaceConstraint(
        "Spine5_M",
        "Wrist_L",
        "Wrist_R",
        "FKRootGround_M",
        "FKOffsetRootWeapon_M",
        translate=True,
        rotate=True,
        scale=True,
        shear=True,
        niceName=["Chest", "Wrist_L", "Wrist_R", "Root"],
        proxyAttrObject=["FKRootWeapon_M"],  # 顺带映射到 ue的root骨骼上，方便引起中武器挂点切换
    )

cmds.addAttr("root",ln="weapon_space",pxy="FKRootWeapon_M.parentSpace",en=1,k=1)