import os

FACE_ROOT = "FACE_SYSTEM"
FIT_ROOT = "FaceFit"
CONTROL_ROOT = "Controls_GRP"
JOINT_ROOT = "SkinJoint_GRP"

LOC_LABEL = "LOC"
CTL_LABEL = "CTL"
SDK_LABEL = "SDK"
GRP_LABEL = "GRP"
END_LABEL = "End"

JOINT_LABEL = "SK"

CONTROL_LABEL_LIST = ["controls", "ctrl", "ctl"]

UN_SKIN_LABEL = ["class", "part", "end"]

MIRROR_BUILD = True

PART_JOINT = {"L_BrowPart1": "L_Brow1",
              "L_BrowPart2": "L_Brow3",
              "L_BrowPart3": "L_Brow5",

              "R_BrowPart1": "R_Brow1",
              "R_BrowPart2": "R_Brow3",
              "R_BrowPart3": "R_Brow5",

              "L_LidInnerPart": "L_LidInner",
              "L_LidOuterPart": "L_LidOuter",
              "L_LidUpperPart": "L_LidUpper2",
              "L_LidLowerPart": "L_LidLower2",

              "R_LidInnerPart": "R_LidInner",
              "R_LidOuterPart": "R_LidOuter",
              "R_LidUpperPart": "R_LidUpper2",
              "R_LidLowerPart": "R_LidLower2",

              "L_LipCornerPart": "L_LipCorner",
              "M_LipUpperPart": "M_LipUpper",
              "M_LipLowerPart": "M_LipLower",
              "R_LipCornerPart": "R_LipCorner"}


FACE_SHAPES_FILE = f"{os.path.dirname(__file__)}\\shapes\\faceShapes.yaml"
