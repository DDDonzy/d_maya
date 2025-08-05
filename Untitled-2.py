data = {
    "eyeLine_Sec": [
        "Controller_L_eyerush_tips",
        "Controller_L_eyerush_root",
        "Controller_L_eyerush_mid",
        "Controller_R_eyerush_mid",
        "Controller_R_eyerush_root",
        "Controller_R_eyerush_tips",
    ],
    "lip_Sec": [
        "Controller_L_mouth_s_up1",
        "Controller_L_mouth_c_up1",
        "Controller_L_mouth_c_down1",
        "Controller_L_mouth_side_down1",
        "Controller_L_mouth_s_down1",
        "Controller_mouth_up1",
        "Controller_L_mouth_side_up1",
        "Controller_mouth_down1",
        "Controller_R_mouth_c_up1",
        "Controller_R_mouth_c_down1",
        "Controller_R_mouth_s_down1",
        "Controller_R_mouth_side_down1",
        "Controller_R_mouth_s_up1",
        "Controller_R_mouth_side_up1",
    ],
    "tongue_Sec": [
        "Controller_tongue_root",
        "Controller_tongue1",
        "Controller_tongue2",
        "Controller_tongue3",
    ],
    "teeth_Sec": [
        "Controller_L_teeth_up",
        "Controller_R_teeth_up_center",
        "Controller_teeth_root",
        "Controller_teeth_up",
        "Controller_R_teeth_up",
        "Controller_L_teeth_up_center",
        "Controller_R_teeth_down",
        "Controller_L_teeth_down",
        "Controller_L_teeth_up_front",
        "Controller_teeth_down",
        "Controller_teeth_down_center",
        "Controller_R_teeth_up_front",
        "Controller_L_teeth_down_front",
        "Controller_R_teeth_down_front",
    ],
    "nose_Sec": [
        "Controller_nose_under",
        "Controller_nose_root",
    ],
    "jaw_Sec": [
        "Controller_L_jawline2",
        "Controller_jaw_top",
        "Controller_L_jawline1",
        "Controller_R_jawline1",
        "Controller_R_jawline2",
    ],
    "cheek_Sec": [
        "Controller_R_cheek",
        "Controller_R_jaw",
        "Controller_L_jaw",
        "Controller_L_chobo",
        "Controller_R_chobo",
        "Controller_L_cheek",
        "Controller_R_cheek_inside",
        "Controller_L_cheek_inside",
        "Controller_L_cheek_outline",
        "Controller_R_cheek_outline",
    ],
    "brow_Sec": [
        "Controller_R_eyeblow_inner",
        "Controller_R_eyeblow3",
        "Controller_L_eyeblow13",
        "Controller_R_eyeblow_root",
        "Controller_R_eyeblow_c",
        "Controller_R_eyeblow1",
        "Controller_L_eyeblow14",
        "Controller_R_eyeblow2",
        "Controller_R_eyeblow0",
        "Controller_R_eyeblow4",
        "Controller_R_eyeblow7",
        "Controller_R_eyeblow8",
        "Controller_R_eyeblow12",
        "Controller_R_eyeblow6",
        "Controller_R_eyeblow10",
        "Controller_R_eyeblow5",
        "Controller_R_eyeblow9",
        "Controller_R_eyeblow11",
        "Controller_R_eyeblow13",
        "Controller_R_eyeblow14",
        "Controller_L_eyeblow2",
        "Controller_eyeblow_center",
        "Controller_L_eyeblow_root",
        "Controller_L_eyeblow_c",
        "Controller_L_eyeblow_inner",
        "Controller_L_eyeblow3",
        "Controller_L_eyeblow5",
        "Controller_L_eyeblow4",
        "Controller_L_eyeblow7",
        "Controller_L_eyeblow9",
        "Controller_L_eyeblow11",
        "Controller_L_eyeblow12",
        "Controller_L_eyeblow10",
        "Controller_L_eyeblow8",
        "Controller_L_eyeblow6",
        "Controller_L_eyeblow0",
        "Controller_L_eyeblow1",
    ],
    "eye_Sec": [
        "Controller_L_eyelid_up3",
        "Controller_L_eyelid_up2",
        "Controller_L_eyelid_up1",
        "Controller_L_eyelid_up4",
        "Controller_L_eyelid_side1",
        "Controller_L_iris",
        "Controller_L_eyelid_side2",
        "Controller_L_eyelid_down3",
        "Controller_L_eyelid_down2",
        "Controller_L_eyelid_down1",
        "Controller_eye_L",
        "Controller_R_eyelid_up1",
        "Controller_L_eye_highlight1",
        "Controller_L_pupil",
        "Controller_L_eye_highlight2",
        "Controller_R_eyelid_up3",
        "Controller_R_eyelid_up2",
        "Controller_R_eyelid_up4",
        "Controller_R_eyelid_down3",
        "Controller_R_eyelid_down2",
        "Controller_R_eyelid_down1",
        "Controller_R_eyelid_side1",
        "Controller_R_eyelid_side2",
        "Controller_R_eye_highlight1",
        "Controller_eye_R",
        "Controller_R_pupil",
        "Controller_R_iris",
        "Controller_R_eye_highlight2",
    ],
    "other_Sec": ["Controller_Head_J"],
}


import enum
from os import remove
from maya import cmds
from UTILS.dag.selectHierarchy import selectHierarchy_cmd
from UTILS.dag.iterHierarchy import IterHierarchy
from UTILS.rename import rename
from add_group_new import addGroupNew
from Rainbow.rainbow_UI import create_curve
from UTILS.transform import get_trs, set_trs

head = "Head_J"
controller_head = cmds.duplicate(head, name="Controller_" + head)[0]

cmds.select(controller_head)
selectHierarchy_cmd()
cmds.select(controller_head, d=1)
rename("Controller_@")


all_data = []

for k, v in data.items():
    all_data.extend(v)

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


######### sdk
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


# mouth
def auto_sdk(
    attr_controller="Controller_mouth_root_CTL",
    timeRange=[1, 60],
    controller_list=mouth,
    default_pose_time=0,
):
    cmds.currentTime(default_pose_time)
    con = []
    for x in controller_list:
        source = x.replace("Controller_", "").replace("_SDK", "")
        con.extend(cmds.parentConstraint(source, x, mo=1))

    pose = {}
    for i, x in enumerate(list(range(timeRange[0], timeRange[1] + 1))):
        cmds.currentTime(x)
        i_time_pose = {}
        for obj in controller_list:
            trs = get_trs(obj)
            i_time_pose[obj] = trs
        pose[i] = i_time_pose

    cmds.currentTime(default_pose_time)
    cmds.delete(con)

    cmds.addAttr(attr_controller, ln="____________", at="enum", en="_______", k=1)
    for k, v in pose.items():
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


auto_sdk(
    attr_controller="Controller_mouth_root_CTL",
    timeRange=[1, 60],
    controller_list=mouth,
    default_pose_time=0,
)


auto_sdk(
    attr_controller="Controller_L_eye_root_CTL",
    timeRange=[61, 119],
    controller_list=L_Eye,
    default_pose_time=0,
)

auto_sdk(
    attr_controller="Controller_R_eye_root_CTL",
    timeRange=[61, 119],
    controller_list=R_Eye,
    default_pose_time=0,
)

auto_sdk(
    attr_controller="Controller_L_eyeblow_root_CTL",
    timeRange=[120, 161],
    controller_list=L_Brow,
    default_pose_time=0,
)

auto_sdk(
    attr_controller="Controller_R_eyeblow_root_CTL",
    timeRange=[129, 161],
    controller_list=R_Brow,
    default_pose_time=0,
)

auto_sdk(
    attr_controller="Controller_nose_root_CTL",
    timeRange=[171, 173],
    controller_list=Nose,
    default_pose_time=0,
)

auto_sdk(
    attr_controller="Controller_L_chobo_CTL",
    timeRange=[169, 169],
    controller_list=L_Cheek,
    default_pose_time=0,
)

auto_sdk(
    attr_controller="Controller_R_chobo_CTL",
    timeRange=[169, 169],
    controller_list=R_Cheek,
    default_pose_time=0,
)




grp = cmds.createNode("transform", name="FACE_Constraint")
for x in cmds.ls("Controller_*_CTL"):
    dn = x.replace("Controller_", "").replace("_CTL", "")
    if cmds.objExists(dn):
        p = cmds.parentConstraint(x, dn)
        s = cmds.scaleConstraint(x, dn)
        cmds.parent(p + s, grp)
