from maya import cmds
from UTILS.dag.selectHierarchy import selectHierarchy_cmd
from UTILS.dag.iterHierarchy import IterHierarchy
from UTILS.rename import rename
from UTILS.control.add_group_new import addGroupNew
from Rainbow.rainbow_UI import create_curve
from UTILS.transform import get_trs, set_trs
from UTILS.control.cvShape import import_cvData

# TODO
eyeFile = r"Z:\face\eye.ma"  # 眼睛控制逻辑的maya文件
cvShapeFile = r"Z:\face\cv.yaml"  # 控制器形态文件
head = "Head_J"
anim_head = "Head_J"
# TODO












controller_head = cmds.duplicate(head, name="Controller_" + head)[0]

cmds.select(controller_head)
selectHierarchy_cmd()
cmds.select(controller_head, d=1)
rename("Controller_@")


add_group_list = []
for x, dag in IterHierarchy(controller_head, False):
    addGroupNew(
        obj=x,
        add_string="GRP,SDK,CTL",
        replaceString="",
    )

controls = cmds.ls("Controller*CTL")
cmds.select(controls)
create_curve(1, "C00_sphere")


cmds.file(eyeFile, i=1, type="mayaAscii", ignoreVersion=1, ra=1, mergeNamespacesOnClash=0, rpr="L")
cmds.file(eyeFile, i=1, type="mayaAscii", ignoreVersion=1, ra=1, mergeNamespacesOnClash=0, rpr="R")

p_con = cmds.parentConstraint("Controller_L_eye_root_CTL", "L_EyeController", mo=1)[0]
s_con = cmds.scaleConstraint("Controller_L_eye_root_CTL", "L_EyeController")[0]
cmds.setAttr(f"{p_con}.target[0].targetOffsetTranslate", *(0, 0, -5))
cmds.setAttr(f"{p_con}.target[0].targetOffsetRotate", *(90, 90, 0))
cmds.delete(p_con, s_con)


p_con = cmds.parentConstraint("Controller_R_eye_root_CTL", "R_EyeController", mo=1)[0]
s_con = cmds.scaleConstraint("Controller_R_eye_root_CTL", "R_EyeController")[0]
cmds.setAttr(f"{p_con}.target[0].targetOffsetTranslate", *(0, 0, 5))
cmds.setAttr(f"{p_con}.target[0].targetOffsetRotate", *(90, 90, 0))
cmds.setAttr(f"{s_con}.offsetX", -1)
cmds.delete(p_con, s_con)

cmds.parent("L_EyeController", f"Controller_{head}_GRP")
cmds.parent("R_EyeController", f"Controller_{head}_GRP")

import_cvData(cvShapeFile)


# do con
def sdk(dr, dn):
    cmds.setDrivenKeyframe(f"{dn}.tx", cd=dr)
    cmds.setDrivenKeyframe(f"{dn}.ty", cd=dr)
    cmds.setDrivenKeyframe(f"{dn}.tz", cd=dr)
    cmds.setDrivenKeyframe(f"{dn}.rx", cd=dr)
    cmds.setDrivenKeyframe(f"{dn}.ry", cd=dr)
    cmds.setDrivenKeyframe(f"{dn}.rz", cd=dr)
    cmds.setDrivenKeyframe(f"{dn}.sx", cd=dr)
    cmds.setDrivenKeyframe(f"{dn}.sy", cd=dr)
    cmds.setDrivenKeyframe(f"{dn}.sz", cd=dr)

def auto_sdk(
    attr_controller="Controller_mouth_root_CTL",
    timeRange=[1, 60],
    controller_list=[],
    default_pose_time=-1,
):
    cmds.currentTime(default_pose_time)
    con = []
    for x in controller_list:
        source = x.replace("Controller_", "").replace("_SDK", "")
        if cmds.objExists(source):
            con.extend(cmds.parentConstraint(source, x, mo=1))
    pose = {}
    for i, x in enumerate(list(range(timeRange[0], timeRange[1] + 1))):
        cmds.currentTime(x)
        i_time_pose = {}
        for obj in controller_list:
            if cmds.objExists(obj):
                trs = get_trs(obj)
                i_time_pose[obj] = trs
        pose[i] = i_time_pose

    cmds.currentTime(default_pose_time)
    cmds.delete(con)

    cmds.addAttr(attr_controller, ln="____________", at="enum", en="_______", k=1)
    for k, v in pose.items():
        if not cmds.objExists(f"{attr_controller}.pose{k}"):
            cmds.addAttr(attr_controller, ln=f"pose{k}", at="double", min=0, max=1, dv=0, k=1)
        dr_attr = f"{attr_controller}.pose{k}"

        for obj, trs in v.items():
            sdk(dr_attr, obj)

        cmds.setAttr(dr_attr, 1)

        for obj, trs in v.items():
            set_trs(obj, trs)
            sdk(dr_attr, obj)

        cmds.setAttr(dr_attr, 0)
        cmds.refresh()




######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
######### sdk
# TODO
mouth = [
    "Controller_Head_J_SDK",
    "Controller_L_cheek_SDK",
    "Controller_L_cheek_inside_SDK",
    "Controller_L_cheek_outline_SDK",
    "Controller_L_chobo_SDK",
    "Controller_L_eye_highlight1_SDK",
    "Controller_L_eye_highlight2_SDK",
    "Controller_L_eye_root_SDK",
    "Controller_L_eyeblow0_SDK",
    "Controller_L_eyeblow1_SDK",
    "Controller_L_eyeblow2_SDK",
    "Controller_L_eyeblow3_SDK",
    "Controller_L_eyeblow4_SDK",
    "Controller_L_eyeblow5_SDK",
    "Controller_L_eyeblow6_SDK",
    "Controller_L_eyeblow7_SDK",
    "Controller_L_eyeblow8_SDK",
    "Controller_L_eyeblow9_SDK",
    "Controller_L_eyeblow10_SDK",
    "Controller_L_eyeblow11_SDK",
    "Controller_L_eyeblow12_SDK",
    "Controller_L_eyeblow13_SDK",
    "Controller_L_eyeblow14_SDK",
    "Controller_L_eyeblow_c_SDK",
    "Controller_L_eyeblow_inner_SDK",
    "Controller_L_eyeblow_root_SDK",
    "Controller_L_eyelash_up2_SDK",
    "Controller_L_eyelash_up3_SDK",
    "Controller_L_eyelash_up4_SDK",
    "Controller_L_eyelid_down1_SDK",
    "Controller_L_eyelid_down2_SDK",
    "Controller_L_eyelid_down3_SDK",
    "Controller_L_eyelid_side1_SDK",
    "Controller_L_eyelid_side2_SDK",
    "Controller_L_eyelid_up1_SDK",
    "Controller_L_eyelid_up2_SDK",
    "Controller_L_eyelid_up3_SDK",
    "Controller_L_eyelid_up4_SDK",
    "Controller_L_eyerush_mid_SDK",
    "Controller_L_eyerush_root_SDK",
    "Controller_L_eyerush_tips_SDK",
    "Controller_L_iris_SDK",
    "Controller_L_jaw_SDK",
    "Controller_L_jawline1_SDK",
    "Controller_L_jawline2_SDK",
    "Controller_L_mouth_c_down1_SDK",
    "Controller_L_mouth_c_up1_SDK",
    "Controller_L_mouth_inner_c_down2_SDK",
    "Controller_L_mouth_inner_c_up2_SDK",
    "Controller_L_mouth_inner_s_down2_SDK",
    "Controller_L_mouth_inner_s_up2_SDK",
    "Controller_L_mouth_inner_side_down2_SDK",
    "Controller_L_mouth_inner_side_up2_SDK",
    "Controller_L_mouth_outer_c_up2_SDK",
    "Controller_L_mouth_s_down1_SDK",
    "Controller_L_mouth_s_up1_SDK",
    "Controller_L_mouth_side_down1_SDK",
    "Controller_L_mouth_side_up1_SDK",
    "Controller_L_mouth_side_wrinkle_SDK",
    "Controller_L_pupil_SDK",
    "Controller_L_teeth_down_SDK",
    "Controller_L_teeth_down_front_SDK",
    "Controller_L_teeth_up_SDK",
    "Controller_L_teeth_up_center_SDK",
    "Controller_L_teeth_up_front_SDK",
    "Controller_R_cheek_SDK",
    "Controller_R_cheek_inside_SDK",
    "Controller_R_cheek_outline_SDK",
    "Controller_R_chobo_SDK",
    "Controller_R_eye_highlight1_SDK",
    "Controller_R_eye_highlight2_SDK",
    "Controller_R_eye_root_SDK",
    "Controller_R_eyeblow0_SDK",
    "Controller_R_eyeblow1_SDK",
    "Controller_R_eyeblow2_SDK",
    "Controller_R_eyeblow3_SDK",
    "Controller_R_eyeblow4_SDK",
    "Controller_R_eyeblow5_SDK",
    "Controller_R_eyeblow6_SDK",
    "Controller_R_eyeblow7_SDK",
    "Controller_R_eyeblow8_SDK",
    "Controller_R_eyeblow9_SDK",
    "Controller_R_eyeblow10_SDK",
    "Controller_R_eyeblow11_SDK",
    "Controller_R_eyeblow12_SDK",
    "Controller_R_eyeblow13_SDK",
    "Controller_R_eyeblow14_SDK",
    "Controller_R_eyeblow_c_SDK",
    "Controller_R_eyeblow_inner_SDK",
    "Controller_R_eyeblow_root_SDK",
    "Controller_R_eyelash_up2_SDK",
    "Controller_R_eyelash_up3_SDK",
    "Controller_R_eyelash_up4_SDK",
    "Controller_R_eyelid_down1_SDK",
    "Controller_R_eyelid_down2_SDK",
    "Controller_R_eyelid_down3_SDK",
    "Controller_R_eyelid_side1_SDK",
    "Controller_R_eyelid_side2_SDK",
    "Controller_R_eyelid_up1_SDK",
    "Controller_R_eyelid_up2_SDK",
    "Controller_R_eyelid_up3_SDK",
    "Controller_R_eyelid_up4_SDK",
    "Controller_R_eyerush_mid_SDK",
    "Controller_R_eyerush_root_SDK",
    "Controller_R_eyerush_tips_SDK",
    "Controller_R_iris_SDK",
    "Controller_R_jaw_SDK",
    "Controller_R_jawline1_SDK",
    "Controller_R_jawline2_SDK",
    "Controller_R_mouth_c_down1_SDK",
    "Controller_R_mouth_c_up1_SDK",
    "Controller_R_mouth_inner_c_down2_SDK",
    "Controller_R_mouth_inner_c_up2_SDK",
    "Controller_R_mouth_inner_s_down2_SDK",
    "Controller_R_mouth_inner_s_up2_SDK",
    "Controller_R_mouth_inner_side_down2_SDK",
    "Controller_R_mouth_inner_side_up2_SDK",
    "Controller_R_mouth_outer_c_up2_SDK",
    "Controller_R_mouth_s_down1_SDK",
    "Controller_R_mouth_s_up1_SDK",
    "Controller_R_mouth_side_down1_SDK",
    "Controller_R_mouth_side_up1_SDK",
    "Controller_R_mouth_side_wrinkle_SDK",
    "Controller_R_pupil_SDK",
    "Controller_R_teeth_down_SDK",
    "Controller_R_teeth_down_front_SDK",
    "Controller_R_teeth_up_SDK",
    "Controller_R_teeth_up_center_SDK",
    "Controller_R_teeth_up_front_SDK",
    "Controller_bo_facewear01_SDK",
    "Controller_bo_l_ears01_SDK",
    "Controller_bo_l_ears02_SDK",
    "Controller_bo_l_ears03_SDK",
    "Controller_bo_l_ears04_SDK",
    "Controller_bo_mouthwear01_SDK",
    "Controller_bo_r_ears01_SDK",
    "Controller_bo_r_ears02_SDK",
    "Controller_bo_r_ears03_SDK",
    "Controller_bo_r_ears04_SDK",
    "Controller_eye_L_SDK",
    "Controller_eye_R_SDK",
    "Controller_eyeblow_center_SDK",
    "Controller_jaw_root_SDK",
    "Controller_jaw_top_SDK",
    "Controller_mouth_down1_SDK",
    "Controller_mouth_down2_SDK",
    "Controller_mouth_inner_down2_SDK",
    "Controller_mouth_inner_up2_SDK",
    "Controller_mouth_outer_up2_SDK",
    "Controller_mouth_root_SDK",
    "Controller_mouth_up1_SDK",
    "Controller_nose_root_SDK",
    "Controller_nose_under_SDK",
    "Controller_teeth_down_SDK",
    "Controller_teeth_down_center_SDK",
    "Controller_teeth_root_SDK",
    "Controller_teeth_up_SDK",
    "Controller_tongue1_SDK",
    "Controller_tongue2_SDK",
    "Controller_tongue3_SDK",
    "Controller_tongue_root_SDK",
]
L_Brow = [
    "Controller_L_eyeblow_root_SDK",
    "Controller_L_eyeblow_c_SDK",
    "Controller_L_eyeblow_inner_SDK",
    "Controller_L_eyeblow0_SDK",
    "Controller_L_eyeblow1_SDK",
    "Controller_L_eyeblow2_SDK",
    "Controller_L_eyeblow3_SDK",
    "Controller_L_eyeblow4_SDK",
    "Controller_L_eyeblow5_SDK",
    "Controller_L_eyeblow6_SDK",
    "Controller_L_eyeblow7_SDK",
    "Controller_L_eyeblow8_SDK",
    "Controller_L_eyeblow9_SDK",
    "Controller_L_eyeblow10_SDK",
    "Controller_L_eyeblow11_SDK",
    "Controller_L_eyeblow12_SDK",
    "Controller_L_eyeblow13_SDK",
    "Controller_L_eyeblow14_SDK",
    "Controller_eyeblow_center_SDK",
]
R_Brow = [
    "Controller_R_eyeblow_root_SDK",
    "Controller_R_eyeblow_c_SDK",
    "Controller_R_eyeblow_inner_SDK",
    "Controller_R_eyeblow0_SDK",
    "Controller_R_eyeblow1_SDK",
    "Controller_R_eyeblow2_SDK",
    "Controller_R_eyeblow3_SDK",
    "Controller_R_eyeblow4_SDK",
    "Controller_R_eyeblow5_SDK",
    "Controller_R_eyeblow6_SDK",
    "Controller_R_eyeblow7_SDK",
    "Controller_R_eyeblow8_SDK",
    "Controller_R_eyeblow9_SDK",
    "Controller_R_eyeblow10_SDK",
    "Controller_R_eyeblow11_SDK",
    "Controller_R_eyeblow12_SDK",
    "Controller_R_eyeblow13_SDK",
    "Controller_R_eyeblow14_SDK",
    "Controller_eyeblow_center_SDK",
]
Nose = ["Controller_nose_root_SDK", "Controller_nose_under_SDK"]
L_Cheek = ["Controller_L_cheek_SDK", "Controller_L_cheek_inside_SDK", "Controller_L_cheek_outline_SDK", "Controller_L_chobo_SDK", "Controller_L_jaw_SDK"]
R_Cheek = ["Controller_R_jaw_SDK", "Controller_R_cheek_outline_SDK", "Controller_R_chobo_SDK", "Controller_R_cheek_inside_SDK", "Controller_R_cheek_SDK"]
L_Eye = [
    "Controller_L_eye_root_SDK",
    "Controller_L_eyerush_root_SDK",
    "Controller_L_eyerush_mid_SDK",
    "Controller_L_eyerush_tips_SDK",
    "Controller_L_eyelid_up1_SDK",
    "Controller_L_eyelid_up2_SDK",
    "Controller_L_eyelash_up2_SDK",
    "Controller_L_eyelid_up3_SDK",
    "Controller_L_eyelash_up3_SDK",
    "Controller_L_eyelash_up4_SDK",
    "Controller_L_eyelid_up4_SDK",
    "Controller_L_eyelid_side2_SDK",
    "Controller_L_eyelid_down3_SDK",
    "Controller_L_eyelid_down2_SDK",
    "Controller_L_eyelid_down1_SDK",
    "Controller_L_eyelid_side1_SDK",
    "Controller_eye_L_SDK",
    "Controller_L_iris_SDK",
    "Controller_L_pupil_SDK",
    "Controller_L_eye_highlight1_SDK",
    "Controller_L_eye_highlight2_SDK",
]
R_Eye = [
    "Controller_R_eye_root_SDK",
    "Controller_R_eyerush_root_SDK",
    "Controller_R_eyerush_mid_SDK",
    "Controller_R_eyerush_tips_SDK",
    "Controller_R_eyelid_up1_SDK",
    "Controller_R_eyelid_up2_SDK",
    "Controller_R_eyelash_up2_SDK",
    "Controller_R_eyelid_up3_SDK",
    "Controller_R_eyelash_up3_SDK",
    "Controller_R_eyelash_up4_SDK",
    "Controller_R_eyelid_up4_SDK",
    "Controller_R_eyelid_side2_SDK",
    "Controller_R_eyelid_down3_SDK",
    "Controller_R_eyelid_down2_SDK",
    "Controller_R_eyelid_down1_SDK",
    "Controller_R_eyelid_side1_SDK",
    "Controller_eye_R_SDK",
    "Controller_R_iris_SDK",
    "Controller_R_pupil_SDK",
    "Controller_R_eye_highlight1_SDK",
    "Controller_R_eye_highlight2_SDK",
]




#
auto_sdk(
    attr_controller="Controller_mouth_root_CTL",
    timeRange=[0, 60],
    controller_list=mouth,
    default_pose_time=-1,
)


auto_sdk(
    attr_controller="Controller_L_eye_root_CTL",
    timeRange=[61, 119],
    controller_list=L_Eye,
    default_pose_time=-1,
)

auto_sdk(
    attr_controller="Controller_R_eye_root_CTL",
    timeRange=[61, 119],
    controller_list=R_Eye,
    default_pose_time=-1,
)

auto_sdk(
    attr_controller="Controller_L_eyeblow_root_CTL",
    timeRange=[120, 149],
    controller_list=L_Brow,
    default_pose_time=-1,
)

auto_sdk(
    attr_controller="Controller_R_eyeblow_root_CTL",
    timeRange=[120, 149],
    controller_list=R_Brow,
    default_pose_time=-1,
)

auto_sdk(
    attr_controller="Controller_nose_root_CTL",
    timeRange=[171, 173],
    controller_list=Nose,
    default_pose_time=-1,
)

auto_sdk(
    attr_controller="Controller_L_chobo_CTL",
    timeRange=[169, 169],
    controller_list=L_Cheek,
    default_pose_time=-1,
)

auto_sdk(
    attr_controller="Controller_R_chobo_CTL",
    timeRange=[169, 169],
    controller_list=R_Cheek,
    default_pose_time=-1,
)


# eye
auto_sdk(
    attr_controller="L_Eye_CTL",
    timeRange=[101, 108],
    controller_list=L_Eye,
    default_pose_time=-1,
)

auto_sdk(
    attr_controller="R_Eye_CTL",
    timeRange=[101, 108],
    controller_list=R_Eye,
    default_pose_time=-1,
)

# TODO























# TODO

grp = cmds.createNode("transform", name="FACE_Constraint")
for x in cmds.ls("Controller_*_CTL"):
    dn = x.replace("Controller_", "").replace("_CTL", "")
    if cmds.objExists(dn):
        p = cmds.parentConstraint(x, dn)
        s = cmds.scaleConstraint(x, dn)
        cmds.parent(p + s, grp)

cmds.delete(f"Controller_{head}")

def hideShapeInChannelBox(objectList: list):
    if type(objectList) is str:
        objectList = [objectList]
    for obj in objectList:
        cmds.setAttr(f"{obj}.isHistoricallyInteresting",0)



hideShapeInChannelBox(cmds.ls(type="animCurve")+cmds.ls(type="blendWeighted"))