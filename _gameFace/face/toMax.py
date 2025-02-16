from face.fn.transform import *
from face.fit import *

toMax = [
    {'L_BrowSec1_SK': 'Brow_L01'},
    {'L_BrowSec2_SK': 'Brow_L02'},
    {'L_BrowSec3_SK': 'Brow_L03'},
    {'L_BrowSec4_SK': 'Brow_L04'},
    {'L_BrowSec5_SK': 'Brow_L05'},
    {'R_BrowSec1_SK': 'Brow_R01'},
    {'R_BrowSec2_SK': 'Brow_R02'},
    {'R_BrowSec3_SK': 'Brow_R03'},
    {'R_BrowSec4_SK': 'Brow_R04'},
    {'R_BrowSec5_SK': 'Brow_R05'},
    {'L_EyeLineSec1_SK': 'Eyelash_L01'},
    {'L_EyeLineSec2_SK': 'Eyelash_L02'},
    {'L_EyeLineSec3_SK': 'Eyelash_L03'},
    {'R_EyeLineSec1_SK': 'Eyelash_R01'},
    {'R_EyeLineSec2_SK': 'Eyelash_R02'},
    {'R_EyeLineSec3_SK': 'Eyelash_R03'},
    {'L_LidInnerSec_SK': 'Eye_L01'},
    {'L_LidUpperSec1_SK': 'Eye_L02'},
    {'L_LidUpperSec2_SK': 'Eye_L03'},
    {'L_LidUpperSec3_SK': 'Eye_L04'},
    {'L_LidUpperSec4_SK': 'Eye_L05'},
    {'L_LidUpperSec5_SK': 'Eye_L06'},
    {'L_LidOuterSec_SK': 'Eye_L07'},
    {'L_LidLowerSec1_SK': 'Eye_L08'},
    {'L_LidLowerSec2_SK': 'Eye_L09'},
    {'L_LidLowerSec3_SK': 'Eye_L010'},
    {'L_LidLowerSec4_SK': 'Eye_L011'},
    {'L_LidLowerSec5_SK': 'Eye_L012'},
    {'L_Eye_SK': 'EyeBall_L'},
    {'R_LidInnerSec_SK': 'Eye_R01'},
    {'R_LidUpperSec1_SK': 'Eye_R02'},
    {'R_LidUpperSec2_SK': 'Eye_R03'},
    {'R_LidUpperSec3_SK': 'Eye_R04'},
    {'R_LidUpperSec4_SK': 'Eye_R05'},
    {'R_LidUpperSec5_SK': 'Eye_R06'},
    {'R_LidOuterSec_SK': 'Eye_R07'},
    {'R_LidLowerSec1_SK': 'Eye_R08'},
    {'R_LidLowerSec2_SK': 'Eye_R09'},
    {'R_LidLowerSec3_SK': 'Eye_R010'},
    {'R_LidLowerSec4_SK': 'Eye_R011'},
    {'R_LidLowerSec5_SK': 'Eye_R012'},
    {'R_Eye_SK': 'EyeBall_R'},
    {'L_CheekUpperSec1_SK': 'Check_L03'},
    {'L_CheekUpperSec2_SK': 'Check_L01'},
    {'L_CheekUpperSec3_SK': 'Check_L04'},
    {'L_CheekSec_SK': 'Check_L02'},
    {'R_CheekUpperSec1_SK': 'Check_R03'},
    {'R_CheekUpperSec2_SK': 'Check_R01'},
    {'R_CheekUpperSec3_SK': 'Check_R04'},
    {'R_CheekSec_SK': 'Check_R02'},
    {'M_TeethUpper_SK': 'Tooth_M_Up'},
    {'M_TeethLower_SK': 'Tooth_M_Down'},
    {'R_LipCornerSec_SK': 'Lip_R'},
    {'R_LipUpperSec2_SK': 'Lip_R_Up01'},
    {'R_LipUpperSec1_SK': 'Lip_R_Up02'},
    {'M_LipUpperSec_SK': 'Lip_M_Up'},
    {'L_LipUpperSec1_SK': 'Lip_L_Up02'},
    {'L_LipUpperSec2_SK': 'Lip_L_Up01'},
    {'L_LipCornerSec_SK': 'Lip_L'},
    {'L_LipLowerSec2_SK': 'Lip_L_Down01'},
    {'L_LipLowerSec1_SK': 'Lip_L_Down02'},
    {'M_LipLowerSec_SK': 'Lip_M_Down'},
    {'R_LipLowerSec1_SK': 'Lip_R_Down02'},
    {'R_LipLowerSec2_SK': 'Lip_R_Down01'},
    {'M_Jaw_SK': 'jaw'},
    {'M_Tongue_SK': 'Tongue_001'},
    {'M_Tongue1_SK': 'Tongue_002'},
    {'M_Tongue2_SK': 'Tongue_003'},
]


class buildMaxJoint(CreateBase):
    thisAssetName = "MaxJoints"

    def create(self):
        self.maxJoints = CreateNode("transform", name="MaxJoints_GRP")
        for x in toMax:
            jnt = JointData(x.values()[0])
            jnt.worldMatrix = om.MMatrix()
            jnt.parent = self.maxJoints
            jnt.create()
            matrixConstraint(x.keys()[0], x.values()[0], mo=False)

    def _post_create(self):
        cmds.parent(self.maxJoints, w=1)


if __name__ == "__main__":
    buildMaxJoint("maxJoints")
