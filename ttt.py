from maya import cmds, mel
from UTILS.getHistory import get_history, get_shape
import UTILS.transform as t


cmds.delete("M_Brow_base")

# 删除下眉毛 历史
brow = "brow_L_base"
cmds.select(brow)
cmds.DeleteHistory()
for x in cmds.listRelatives(brow, s=1):
    if cmds.getAttr(x+".intermediateObject"):
        cmds.delete(x)

# 删除下睫毛 历史
eyeLash = "upLash_L2_base"
cmds.select(eyeLash)
cmds.DeleteHistory()
for x in cmds.listRelatives(eyeLash, s=1):
    if cmds.getAttr(x+".intermediateObject"):
        cmds.delete(x)


# 合并前后肩甲绳子
PauldronStrap = ["shengzi_Front_UVpin", "Shengzi_Back_UvPin"]
shape = get_shape(PauldronStrap[0])[0]
uvPin = cmds.listConnections(shape, type="uvPin")[0]
target_list = cmds.listConnections(f"{uvPin}.outputMatrix", s=0, d=1)

shape = get_shape(PauldronStrap[1])[0]
uvPin = cmds.listConnections(shape, type="uvPin")[0]
target_list += cmds.listConnections(f"{uvPin}.outputMatrix", s=0, d=1)
# 删除旧的肩甲绳子uvPin
cmds.delete(PauldronStrap)
# 创建新的 uvPin
t.uvPin(target_list, name="PauldronStrap", size=0.3)



# 腰带飘带 uvPin 重命名
cmds.rename("M_Belt_02_UVpin", "BeltStrap_uvPinMesh")
cmds.rename("uvPin", "BeltStrap_UvPin")

# 腰带 uvPin 重命名
cmds.rename("Belt_uvPin", "Belt_uvPinMesh")
cmds.rename("uvPin2", "Belt_uvPin")
# 裙子 uvPin 重命名
cmds.rename("skirt_uvPin", "Skirt_uvPinMesh")
cmds.rename("uvPin1", "Skirt_uvPin")
# 肩甲 uvPin 重命名
cmds.rename("Jianjia_Uvpin", "Pauldron_uvPinMesh")
cmds.rename("uvPin4", "Pauldron_uvPin")
# 手套 uvPin 重命名
cmds.rename("ShouTao_UvPiN", "Glove_uvPinMesh")
cmds.rename("uvPin18", "Glove_uvPin")
# 袖子 uvPin 重命名
cmds.rename("uvPin21", "Sleeve_uvPinMesh")
cmds.rename("uvPin22", "Sleeve_uvPin")

# 颈肌 uvPin 重命名
cmds.rename("Sternocleidomastoid_muscle_uvPin", "Sternocleidomastoid_muscle_uvPinMesh")
cmds.rename("uvPin26", "Sternocleidomastoid_muscle_uvPin")
cmds.setAttr("Sternocleidomastoid_muscle_uvPinMeshShapeOrig.intermediateObject", 1)

# 删除 颈uvPin wrap
cmds.delete("proximityWrap7")
# 删除 颈 uv 缩放约束
cmds.delete("Sternocleidomastoid_muscle_uvPin_scaleConstraint1")


# 删除 铠甲 uvPin
BodyArmor = "uvPin23"
shape = get_shape("uvPin23")[0]
uvPin = cmds.listConnections(shape, type="uvPin")[0]
target_list = cmds.listConnections(f"{uvPin}.outputMatrix", s=0, d=1)
# 删除 铠甲 uvPin
cmds.delete(BodyArmor)
# 创建新的 uvPin
t.uvPin(target_list, name="BodyArmor", size=0.3)

# 删除垃圾模型
cmds.delete(["OLD_YIFU_PROXYA", "headBreatWrap", "eyeLashWrap"])
cmds.delete("Finger_Grp", "End_Skin", "Xiukou_Proxy_Skin", "Xiukou_End_Skin", "KaiJia_Sec_Proxy", "Belt_Proxy")

# 复制变形到 铠甲uvPin
cmds.select("PRE_bodyPrp2", "BodyArmor_uvPinMesh")
autoCopyDeform()

# 传递睫毛变形
mel.eval("""file -import -type "FBX"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "lid_proxy" -options "fbx"  -pr  -importFrameRate true  -importTimeRange "override" "D:/lid_proxy.fbx";""")
cmds.select("M_Head_base", "lid_proxy")
autoCopyDeform()
cmds.select("lid_proxy", eyeLash)
autoCopyDeform()
# TODO
copyWeightsOneToN("PRE_body", "Yun_Temp_upLash_R")
cmds.delete("lid_proxy")


def createProxWrap(*args, **kwargs):
    influence = list(args)[:-1]
    surface = list(args)[-1]

    name = kwargs.get("name", "")
    wrapData = cmds.deformer(surface, type='proximityWrap', name=name)
    wrapNode = wrapData[0]

    for i, inf in enumerate(influence):
        if not get_orig(inf):
            cmds.deformableShape(inf, cog=1)
        inf_orig = get_orig(inf)[0]
        inf_shape = get_shape(inf)[0]
        cmds.connectAttr(inf_shape + ".worldMesh[0]", wrapNode + f".drivers[{i}].driverGeometry")
        cmds.connectAttr(inf_orig+".outMesh", wrapNode + f".drivers[{i}].driverBindGeometry")

    return wrapNode


# 输出铠甲控制绳子
createProxWrap("Yun_Temp_bodyPrp4", "Yun_Temp_bodyPrp2", "PauldronStrap_uvPinMesh", name="PauldronStrap_uvPinWrap")
# 表情包裹胡子
createProxWrap("M_Head_base", "hair02_base", name="Beard_wrap")
# 身体包裹胸锁乳突肌
createProxWrap("PRE_body", "Sternocleidomastoid_muscle_uvPinMesh", name="Sternocleidomastoid_muscle_uvPinWrap")
# 眉毛包裹
node = createProxWrap("M_Head_base", brow, name="Brow_uvPinWrap")
cmds.setAttr(node+".wrapMode", 0)
cmds.setAttr(node+".smoothInfluences",5)
cmds.setAttr(node+".smoothNormals",5)
# TODO
copyWeightsOneToN("PRE_body", "Yun_Temp_hair02")




# uvPin 和 中间模型转局部
localSkin = ['BeltStrap_uvPinMesh', 'Belt_uvPinMesh', 'BodyArmor_uvPinMesh', 'Glove_uvPinMesh', 'PauldronStrap_uvPinMesh', 'Pauldron_uvPinMesh', 'Skirt_uvPinMesh', 'Sleeve_uvPinMesh', 'Sternocleidomastoid_muscle_uvPinMesh', 'PRE_body', 'KaiJia_OutPut', 'shengzi_OutPut'] 
for x in localSkin:
    shape = get_shape(x)[0]
    sk = get_history(shape, "skinCluster")
    for a in "xyz":
        for i in "trs":
            cmds.setAttr(f"{x}.{i}{a}", l=0)
    t.matrixConstraint("Root_ctrl", x, mo=1)

    if sk:
        sk = sk[0]
    else:
        print(f"{x} has no skinCluster")
        continue
    if not cmds.listConnections(sk+".bindPreMatrix"):
        s = skinClusterToLocal(sk)
        cmds.setAttr(x+".relativeSpaceEnable", 1)
    else:
        cmds.connectAttr("Root_ctrl.worldMatrix[0]", sk+".geomMatrix")
        print("bind pass")




# 模型组内模型 转局部
geo = ['TEMP_eye_L22', 'TEMP_body16', 'TEMP_shoe_L', 'TEMP_upLash_R', 'TEMP_cloth2', 'TEMP_cloth8', 'TEMP_headPrp', 'TEMP_eye_R16', 'TEMP_hair', 'TEMP_upLash_L', 'TEMP_hair02', 'TEMP_cloth4', 'TEMP_cloth7', 'TEMP_lowTeeth', 'TEMP_cloth5', 'TEMP_cloth10', 'TEMP_bodyPrp8', 'TEMP_cloth6', 'TEMP_body', 'TEMP_cloth9', 'TEMP_lowTeeth8', 'TEMP_eye_L24', 'TEMP_cloth1', 'TEMP_eye_R', 'TEMP_eye_L23', 'TEMP_cloth3', 'TEMP_eye_R15', 'TEMP_brow_L', 'TEMP_bodyPrp9', 'TEMP_tongue', 'TEMP_cloth', 'TEMP_shoe_R', 'TEMP_upTeeth8', 'TEMP_body15', 'TEMP_upTeeth', 'TEMP_eye_L'] 

for x in geo:
    sk = get_history(x, "skinCluster")

    if sk:
        sk = sk[0]
    else:
        print(f"{x} has no skinCluster")
        continue
    if not cmds.listConnections(sk+".bindPreMatrix"):
        s = skinClusterToLocal(sk)
        cmds.setAttr(x+".relativeSpaceEnable", 1)
    else:
        cmds.connectAttr("Root_ctrl.worldMatrix[0]", sk+".geomMatrix")
        print("bind pass")
# 控制模型组
t.matrixConstraint("Root_ctrl", "Yun_Temp_CHR_xc_ss_Geometry", mo=1)


# 隐藏模型
for x in ['BeltStrap_uvPinMesh', 'Belt_uvPinMesh', 'BodyArmor_uvPinMesh', 'Glove_uvPinMesh', 'M_Head_base', 'PauldronStrap_uvPinMesh', 'Pauldron_uvPinMesh', 'Skirt_uvPinMesh', 'Sleeve_uvPinMesh', 'Sternocleidomastoid_muscle_uvPinMesh']:
    cmds.setAttr(x+".visibility", 0)

cmds.parent("RigAssets", "RigAsset")
cmds.parent("RigAsset", "Addon")


for x in cmds.ls(type="skinCluster"):
    s = cmds.listConnections(x+".dqsScale", p=1, d=0, s=1) or []
    if s:
        s = s[0]
        cmds.disconnectAttr(s, x+".dqsScale")
    if cmds.getAttr(x+".skinningMethod") != 0:
        cmds.setAttr(x+".dqsSupportNonRigid", 1)


t.matrixConstraint("Root_ctrl", "model_group", mo=1)




# uvPinMesh = []
# for x in cmds.ls(type="uvPin"):
#     uvPinMesh.extend(cmds.listConnections(x, s=1, d=0))
# cmds.sets(uvPinMesh)