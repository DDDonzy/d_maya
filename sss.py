from maya import cmds, mel
from UTILS.getHistory import get_history, get_shape
import UTILS.transform as t


brow = "brow_L_base"
eyeLash = "upLash_L2_base"

shenzi_front = "shengzi_Front_UVpin"
shenzi_back = "Shengzi_Back_UvPin"

belt = "Yun_Belt_uvpin"
beltUVPin = "uvPin32"


cmds.select(brow)
cmds.DeleteHistory(brow)
for x in cmds.listRelatives(brow, s=1):
    if cmds.getAttr(x+".intermediateObject"):
        cmds.delete(x)

cmds.select(eyeLash)
cmds.DeleteHistory(eyeLash)
for x in cmds.listRelatives(eyeLash, s=1):
    if cmds.getAttr(x+".intermediateObject"):
        cmds.delete(x)


# TODO need copy deform
PauldronStrap = [shenzi_front, shenzi_back]
shape = get_shape(PauldronStrap[0])[0]
uvPin = cmds.listConnections(shape, type="uvPin")[0]
target_list = cmds.listConnections(f"{uvPin}.outputMatrix", s=0, d=1)

shape = get_shape(PauldronStrap[1])[0]
uvPin = cmds.listConnections(shape, type="uvPin")[0]
target_list += cmds.listConnections(f"{uvPin}.outputMatrix", s=0, d=1)


cmds.delete(PauldronStrap)
t.uvPin(target_list, name="PauldronStrap", size=0.3)
# TODO need copy deform


# cmds.rename("M_Belt_02_UVpin", "BeltStrap_uvPinMesh")
# cmds.rename("uvPin", "BeltStrap_UvPin")

cmds.rename(belt, "Belt_uvPinMesh")
cmds.rename(beltUVPin, "Belt_uvPin")

cmds.rename("skirt_uvPin", "Skirt_uvPinMesh")
cmds.rename("uvPin1", "Skirt_uvPin")

cmds.rename("Jianjia_Uvpin", "Pauldron_uvPinMesh")
cmds.rename("uvPin4", "Pauldron_uvPin")

cmds.rename("ShouTao_UvPiN", "Glove_uvPinMesh")
cmds.rename("uvPin18", "Glove_uvPin")

cmds.rename("uvPin21", "Sleeve_uvPinMesh")
cmds.rename("uvPin22", "Sleeve_uvPin")

# cmds.rename("uvPin_mesh", "GloveStrap_uvPinMesh")
# cmds.rename("uvPin27", "GloveStrap_uvPin")

cmds.rename("Sternocleidomastoid_muscle_uvPin", "Sternocleidomastoid_muscle_uvPinMesh")
cmds.rename("uvPin26", "Sternocleidomastoid_muscle_uvPin")
cmds.setAttr("Sternocleidomastoid_muscle_uvPinMeshShapeOrig.intermediateObject", 1)


pre = cmds.createNode("transform", n="PRE_RIG")
cmds.parent("body_sk_bs", pre)
cmds.rename("body_sk_bs", "PRE_body")
cmds.parent(['KaiJia_Lower_OutMesh_01', 'KaiJia_Lower_OutMesh_02', 'KaiJia_Lower_OutMesh_03'], pre)
cmds.parent(pre, "Addon")
cmds.delete("wrapSourceBreath")

cmds.delete("M_DownEyelash_proxy")
cmds.delete("proximityWrap18")
cmds.delete("proximityWrap7")
cmds.delete("Sternocleidomastoid_muscle_uvPin_scaleConstraint1")

cmds.delete("Yun_TEMP_body")
cmds.rename("TEMP_body_skinAndBs", "Yun_TEMP_body")
cmds.parent("Yun_TEMP_body", "Yun_TEMP_body_Grp")
cmds.reorder("Yun_TEMP_body", f=1)


# TODO need copy deform
BodyArmor = "uvPin23"
shape = get_shape("uvPin23")[0]
uvPin = cmds.listConnections(shape, type="uvPin")[0]
target_list = cmds.listConnections(f"{uvPin}.outputMatrix", s=0, d=1)
cmds.delete(BodyArmor)
BodyArmor = "KaiJia_Lower_uvpin"
shape = get_shape("KaiJia_Lower_uvpin")[0]
uvPin = cmds.listConnections(shape, type="uvPin")[0]
target_list += cmds.listConnections(f"{uvPin}.outputMatrix", s=0, d=1)
cmds.delete(BodyArmor)
t.uvPin(target_list, name="BodyArmor", size=0.3)

# TODO need copy deform


cmds.delete(["OLD_YIFU_PROXYA"])
cmds.delete("Finger_Grp", "End_Skin", "Xiukou_Proxy_Skin", "Xiukou_End_Skin", "Yun_KaiJia_Sec_Skin_proxy", 'KaiJia_Sec_Skin', 'KaiJia_OutPut', 'shengzi_OutPut',"Yun_Proxy_Belt","Yun_Proxy_GD_GRP")


cmds.select("KaiJia_Lower_OutMesh_01", "BodyArmor_uvPinMesh")
autoCopyDeform()

mel.eval("""file -import -type "FBX"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "lid_proxy" -options "fbx"  -pr  -importFrameRate true  -importTimeRange "override" "D:/lid_proxy.fbx";""")
cmds.select("M_Head_base", "lid_proxy")
autoCopyDeform()
cmds.select("lid_proxy", "upLash_L2_base")
autoCopyDeform()

copyWeightsOneToN("PRE_body", "Yun_TEMP_upLash_L2")


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


createProxWrap("Yun_TEMP_cloth3", "Yun_TEMP_cloth2", "PauldronStrap_uvPinMesh", name="PauldronStrap_uvPinWrap")
createProxWrap("M_Head_base", "hair02_base", name="Beard_wrap")
createProxWrap("PRE_body", "Sternocleidomastoid_muscle_uvPinMesh", name="Sternocleidomastoid_muscle_uvPinWrap")
node = createProxWrap("M_Head_base", "brow_L_base", name="Brow_uvPinWrap")
cmds.setAttr(node+".wrapMode", 0)
cmds.setAttr(node+".smoothInfluences", 5)
cmds.setAttr(node+".smoothNormals", 5)
copyWeightsOneToN("PRE_body", "Yun_TEMP_brow_L")
copyWeightsOneToN("PRE_body", "Yun_TEMP_hair02")



localSkin = ['Belt_uvPinMesh', 'BodyArmor_uvPinMesh', 'Glove_uvPinMesh', 'PauldronStrap_uvPinMesh', 'Pauldron_uvPinMesh', 'Skirt_uvPinMesh', 'Sleeve_uvPinMesh', 'Sternocleidomastoid_muscle_uvPinMesh'] +['PRE_body', 'KaiJia_Lower_OutMesh_01', 'KaiJia_Lower_OutMesh_02', 'KaiJia_Lower_OutMesh_03']

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
cmds.delete("lid_proxy")




geo = ['TEMP_eye_R', 'TEMP_cloth9', 'TEMP_shoe_L', 'TEMP_cloth1', 'TEMP_tongue', 'TEMP_eye_L24', 'TEMP_eye_L', 'TEMP_cloth3', 'TEMP_body16', 'TEMP_hair02', 'TEMP_bodyPrp4', 'TEMP_cloth4', 'TEMP_eye_R16', 'TEMP_eye_L23', 'TEMP_cloth5', 'TEMP_upLash_L2', 'TEMP_cloth8', 'TEMP_upLash_L', 'TEMP_cloth', 'TEMP_cloth7', 'TEMP_body15', 'TEMP_bodyPrp3', 'TEMP_lowTeeth8', 'TEMP_cloth6', 'TEMP_hair', 'TEMP_headPrp', 'TEMP_headPrp1', 'TEMP_eye_L22', 'TEMP_upTeeth', 'TEMP_headPrp2', 'TEMP_bodyPrp1', 'TEMP_cloth2', 'TEMP_brow_L', 'TEMP_bodyPrp2', 'TEMP_shoe_R', 'TEMP_cloth10', 'TEMP_body', 'TEMP_lowTeeth', 'TEMP_eye_R15', 'TEMP_upTeeth8'] 

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

t.matrixConstraint("Root_ctrl", "Yun_TEMP_CHR_xc_gdss_Geometry", mo=1)


for x in ['Belt_uvPinMesh', 'BodyArmor_uvPinMesh', 'Glove_uvPinMesh', 'PauldronStrap_uvPinMesh', 'Pauldron_uvPinMesh', 'Skirt_uvPinMesh', 'Sleeve_uvPinMesh', 'Sternocleidomastoid_muscle_uvPinMesh'] :
    cmds.setAttr(x+".visibility", 0)

cmds.parent("RigAsset", "Addon")


for x in cmds.ls(type="skinCluster"):
    s = cmds.listConnections(x+".dqsScale", p=1, d=0, s=1) or []
    if s:
        s = s[0]
        cmds.disconnectAttr(s, x+".dqsScale")
    if cmds.getAttr(x+".skinningMethod") != 0:
        cmds.setAttr(x+".dqsSupportNonRigid", 1)

cmds.createNode("transform", n="model_group")
t.matrixConstraint("Root_ctrl", "model_group", mo=1)


uvPinMesh = []
for x in cmds.ls(type="uvPin"):
    uvPinMesh.extend(cmds.listConnections(x, s=1, d=0))
cmds.sets(uvPinMesh)
