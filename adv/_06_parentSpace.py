from m_utils.compounds import parentSpaceConstraint
from m_utils.create.createBase import AssetCallback

with AssetCallback(name="RIG_ASSET", force=False):
    pcs = parentSpaceConstraint(
        "Chest_M",
        "Wrist_L",
        "Wrist_R",
        "FKRootGround_M",
        "Main",
        "RootX_M",
        "FKOffsetWeapon_R",
        translate=True,
        rotate=True,
        scale=True,
        shear=True,
        niceName=["Chest", "Wrist_L", "Wrist_R", "Root", "Main", "Pelvis"],
        proxyAttrObject=["FKWeapon_R", "FKWeaponGimbal_R"],
    )
