import os

# Build
MIRROR_BUILD = True

# Maya Dag
FIT_ROOT = "FaceFit"
FACE_ROOT = "FACE_SYSTEM"
CONTROL_ROOT = "Controls_GRP"
SKIN_JOINT_ROOT = "SkinJoint_GRP"
UN_SKIN_JOINT_ROOT = "UnSkinJoint_GRP"
LOCAL_JOINT_ROOT = "LocalJoint_GRP"
CONTROLS_PANEL_ROOT = "EM_FaceSystem"
BRIDGE = "FaceBridge"

# Label
SKIN_JOINT_LABEL = "SK"
END_LABEL = "End"
LOC_LABEL = "LOC"
CTL_LABEL = "CTL"
SDK_LABEL = "SDK"
GRP_LABEL = "GRP"
PART_LABEL = "Part"
CLASS_LABEL = "Class"
SEC_LABEL = "Sec"
UN_SKIN_LABEL = [CLASS_LABEL,
                 PART_LABEL,
                 END_LABEL]
CONTROL_HIERARCHY_LIST = [GRP_LABEL,
                          SDK_LABEL,
                          CTL_LABEL]
ALL_LABEL = [SKIN_JOINT_LABEL,
             END_LABEL,
             LOC_LABEL,
             CTL_LABEL,
             SDK_LABEL,
             GRP_LABEL,
             PART_LABEL,
             CLASS_LABEL,
             SEC_LABEL]


# File Path
PROJECT_DIR = os.path.dirname(__file__)

DEFAULT_FIT_DIR = os.path.join(PROJECT_DIR, "fit")
DEFAULT_FIT_FILE = os.path.join(DEFAULT_FIT_DIR, "fit.yaml")

DEFAULT_SHAPES_DIR = os.path.join(PROJECT_DIR, "shapes")
DEFAULT_SHAPES_FILE = os.path.join(DEFAULT_SHAPES_DIR, "defaultShapes.yaml")

DEFAULT_WEIGHT_DIR = os.path.join(PROJECT_DIR, "tempWeights")
PART_WEIGHT_FILE = os.path.join(DEFAULT_WEIGHT_DIR, "Part_uvPin.yaml")
SEC_WEIGHT_FILE = os.path.join(DEFAULT_WEIGHT_DIR, "Sec_uvPin.yaml")
JAW_WEIGHT_FILE = os.path.join(DEFAULT_WEIGHT_DIR, "Jaw_uvPin.yaml")

DEFAULT_SDK_DIR = os.path.join(PROJECT_DIR, "sdk")
DEFAULT_SDK_FILE = os.path.join(DEFAULT_SDK_DIR, "defaultSDK.yaml")

CONTROLS_PANEL_DIR = os.path.join(PROJECT_DIR, "controlPanel")
CONTROLS_PANEL_FILE = os.path.join(CONTROLS_PANEL_DIR, "controlPanel.editMA")

POSE_DIR = os.path.join(PROJECT_DIR, "pose")
