import os

FACE_ROOT = "FACE_SYSTEM"
FIT_ROOT = "FaceFit"
CONTROL_ROOT = "Controls_GRP"
SKIN_JOINT_ROOT = "SkinJoint_GRP"
UN_SKIN_JOINT_ROOT = "UnSkinJoint_GRP"
LOCAL_JOINT_ROOT = "LocalJoint_GRP"
BRIDGE = "FaceBridge"

SKIN_JOINT_LABEL = "SK"
END_LABEL = "End"

LOC_LABEL = "LOC"

CTL_LABEL = "CTL"
SDK_LABEL = "SDK"
GRP_LABEL = "GRP"

PART_LABEL = "Part"
CLASS_LABEL = "Class"
SEC_LABEL = "Sec"


CONTROL_HIERARCHY_LIST = [GRP_LABEL, SDK_LABEL, CTL_LABEL]

UN_SKIN_LABEL = [CLASS_LABEL, PART_LABEL, END_LABEL]

SUFFIX_LIST = CONTROL_HIERARCHY_LIST + [LOC_LABEL, END_LABEL, SKIN_JOINT_LABEL]

MIRROR_BUILD = True

PART_JOINT = {"L_BrowPart1": "L_BrowSec1",
              "L_BrowPart2": "L_BrowSec3",
              "L_BrowPart3": "L_BrowSec5",

              "R_BrowPart1": "R_BrowSec1",
              "R_BrowPart2": "R_BrowSec3",
              "R_BrowPart3": "R_BrowSec5",

              "L_LidInnerPart": "L_LidInnerSec",
              "L_LidOuterPart": "L_LidOuterSec",
              "L_LidUpperPart": "L_LidUpperSec2",
              "L_LidLowerPart": "L_LidLowerSec2",

              "R_LidInnerPart": "R_LidInnerSec",
              "R_LidOuterPart": "R_LidOuterSec",
              "R_LidUpperPart": "R_LidUpperSec2",
              "R_LidLowerPart": "R_LidLowerSec2",

              "L_LipCornerPart": "L_LipCornerSec",
              "M_LipUpperPart": "M_LipUpperSec",
              "M_LipLowerPart": "M_LipLowerSec",
              "R_LipCornerPart": "R_LipCornerSec"}

PROJECT_DIR = os.path.dirname(__file__)

DEFAULT_FIT_DIR = f"{PROJECT_DIR}\\fit"
DEFAULT_FIT_FILE = f"{DEFAULT_FIT_DIR}\\fit.yaml"

DEFAULT_SHAPES_DIR = f"{PROJECT_DIR}\\shapes"
DEFAULT_SHAPES_FILE = f"{DEFAULT_SHAPES_DIR}\\defaultShapes.yaml"

DEFAULT_WEIGHT_DIR = f"{PROJECT_DIR}\\tempWeights"
PART_WEIGHT_FILE = f"{DEFAULT_WEIGHT_DIR}\\Part_uvPin.yaml"
SEC_WEIGHT_FILE = f"{DEFAULT_WEIGHT_DIR}\\Sec_uvPin.yaml"
JAW_WEIGHT_FILE = f"{DEFAULT_WEIGHT_DIR}\\Jaw_uvPin.yaml"

DEFAULT_SDK_DIR = f"{PROJECT_DIR}\\sdk"
DEFAULT_SDK_FILE = f"{DEFAULT_SDK_DIR}\\defaultSDK.yaml"


CONTROLS_PANEL_ROOT = "EM_FaceSystem"
CONTROLS_PANEL_DIR = f"{PROJECT_DIR}\\controlPanel"
CONTROLS_PANEL_FILE = f"{CONTROLS_PANEL_DIR}\\controlPanel.editMA"
