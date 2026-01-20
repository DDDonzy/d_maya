# Author:   Donzy.xu
# CreateTime:   2023/2/6 - 21:06
# FileName:  combineFaceAndBody



##### combine face and body


import maya.cmds as cmds

body_addon = 'Rig'
face_joint_grp = "FacialJoint_GRP"
face_grp = "FacialRig_GRP"
body_head_ctl = "FKHead_M"
face_head_ctl = "M_Head_CTL"
l_body_eye_ctl = "FKEye_L"
r_body_eye_ctl = "FKEye_R"
l_face_eye_sdk = "L_EyeBall_00_CTL_SDK"
r_face_eye_sdk = "R_EyeBall_00_CTL_SDK"


cmds.parentConstraint(body_head_ctl,face_head_ctl,mo=1)
cmds.scaleConstraint(body_head_ctl,face_head_ctl)

l_eye_connect = cmds.createNode("transform",name="L_eyeConnect")
r_eye_connect = cmds.createNode("transform",name="R_eyeConnect")
l_eye_connect_grp = cmds.createNode("transform",name="L_eyeConnect_GRP")
r_eye_connect_grp = cmds.createNode("transform",name="R_eyeConnect_GRP")

cmds.parent(l_eye_connect,l_eye_connect_grp)
cmds.parent(r_eye_connect,r_eye_connect_grp)
cmds.parent(l_eye_connect_grp,body_head_ctl)
cmds.parent(r_eye_connect_grp,body_head_ctl)

cmds.delete(cmds.parentConstraint(l_face_eye_sdk,l_eye_connect_grp))
cmds.delete(cmds.parentConstraint(r_face_eye_sdk,r_eye_connect_grp))

cmds.orientConstraint(l_body_eye_ctl,l_eye_connect,mo=1)
cmds.orientConstraint(r_body_eye_ctl,r_eye_connect,mo=1)

cmds.connectAttr(l_eye_connect+".rotateX",l_face_eye_sdk+".rotateX")
cmds.connectAttr(l_eye_connect+".rotateY",l_face_eye_sdk+".rotateY")
cmds.connectAttr(l_eye_connect+".rotateZ",l_face_eye_sdk+".rotateZ")
cmds.connectAttr(r_eye_connect+".rotateX",r_face_eye_sdk+".rotateX")
cmds.connectAttr(r_eye_connect+".rotateY",r_face_eye_sdk+".rotateY")
cmds.connectAttr(r_eye_connect+".rotateZ",r_face_eye_sdk+".rotateZ")


cmds.parent(face_grp,body_addon)
cmds.setAttr(face_joint_grp+".visibility",0)