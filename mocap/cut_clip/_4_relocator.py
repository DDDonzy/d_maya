import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

from m_utils.create.assetCallback import AssetCallback
from m_utils.compounds import matrixConstraint


def get_selected_clip_id():
    """获取当前选中 Clip 的名称和 ID"""
    selected = cmds.ls(sl=1, o=1)
    clip = None
    for x in selected:
        if cmds.objectType(x) == "timeEditorClip":
            clip = x
            break
    if not clip:
        raise RuntimeError("请先在 Time Editor 中选中一个 Clip。")

    try:
        clip_ids = mel.eval('timeEditor -selectedClips ""')
    except Exception as e:
        raise RuntimeError(f"MEL 命令执行失败: {e}")

    if not clip_ids:
        raise RuntimeError("未检测到选中 Clip ID。")

    return clip, int(clip_ids[0])


def reLocator(pelvis="RIG:spine_04"):

    # 1. 获取 Clip
    clip_node, clip_id = get_selected_clip_id()
    print(f"处理 Clip: {clip_node} (ID: {clip_id})")

    clip_plug = f"{clip_node}.clip[0]"
    try:
        start_time = cmds.getAttr(f"{clip_plug}.clipStart")
        duration = cmds.getAttr(f"{clip_plug}.clipDuration")
    except ValueError:
        raise RuntimeError("无法读取属性。")
    end_time = start_time + duration

    # 清理旧控制器 (如果有)
    rerot_name = f"{clip_node}_Rerotate"
    if cmds.objExists(rerot_name):
        cmds.delete(rerot_name)

    # 2. 【核心】完全保留你的数学逻辑 (不动任何算法)
    # ---------------------------------------------------------
    matrix_a = om.MMatrix(cmds.getAttr(f"{pelvis}.worldMatrix", t=start_time))
    matrix_b = om.MMatrix(cmds.getAttr(f"{pelvis}.worldMatrix", t=end_time))

    vector_a = om.MTransformationMatrix(matrix_a).translation(om.MSpace.kWorld)
    vector_b = om.MTransformationMatrix(matrix_b).translation(om.MSpace.kWorld)

    # 你的逻辑：高度归零
    vector_a.y = 0
    vector_b.y = 0

    # 你的逻辑：构建向量
    y_vec = om.MVector([0, 1, 0])
    x_vec = (vector_b - vector_a).normal()
    if x_vec.length() < 0.001:
        x_vec = om.MVector(1, 0, 0)  # 防止原地不动报错
    z_vec = (x_vec ^ y_vec).normal()
    # 重新正交化 X (确保矩阵合法)
    x_vec = (y_vec ^ z_vec).normal()

    # 你的逻辑：构建旋转矩阵
    rot_matrix_list = [x_vec.x, x_vec.y, x_vec.z, 0, y_vec.x, y_vec.y, y_vec.z, 0, z_vec.x, z_vec.y, z_vec.z, 0, 0, 0, 0, 1]
    rotation_matrix = om.MMatrix(rot_matrix_list)
    # ---------------------------------------------------------

    # 3. 创建 Relocator (MEL)
    cmds.select(clip_node)

    # 查找/创建 Relocator
    # 尝试选中
    mel.eval(f"teSelectRelocator({clip_id})")
    sel = cmds.ls(sl=1)

    relocator_node = None
    if sel and sel[0] != clip_node and "Relocator" in sel[0]:
        relocator_node = sel[0]

    if not relocator_node:
        cmds.select(clip_node)
        try:
            mel.eval(f"teCreateRelocator({clip_id})")
            mel.eval(f"teSelectRelocator({clip_id})")
            sel = cmds.ls(sl=1)
            if sel and "Relocator" in sel[0]:
                relocator_node = sel[0]
        except Exception as e:
            print(f"MEL Warning: {e}")

    if not relocator_node:
        raise RuntimeError("无法获取 Relocator 节点。")

    # 5. 应用你的矩阵逻辑
    # 平移回原点
    trans_matrix = om.MTransformationMatrix()
    trans_matrix.setTranslation(vector_a * -1, om.MSpace.kWorld)

    # 组合：平移 * 旋转逆矩阵 (将角色修正回 X 轴)
    final_matrix = trans_matrix.asMatrix() * rotation_matrix.inverse()

    cmds.xform(relocator_node, m=list(final_matrix), ws=True)

    # 6. 创建 Rerotate 控制器 (在原点)
    rerot_node = cmds.spaceLocator(n=rerot_name)[0]
    cmds.xform(rerot_node, t=(0, 0, 0), ro=(0, 0, 0), ws=True)

    cmds.parentConstraint(rerot_node, relocator_node, mo=True)

    # 8. 选中 Rerotate
    cmds.select(rerot_node)
    print("=======================================================")
    print(f"请旋转 {rerot_node} 来控制方向。")
    print("=======================================================")


def bake_reLocator():
    clip, clip_id = get_selected_clip_id()
    clip_plug = f"{clip}.clip[0]"
    start = cmds.getAttr(f"{clip_plug}.clipStart")
    end = start + cmds.getAttr(f"{clip_plug}.clipDuration")

    mel.eval("teSelectDrivenObjects(-1)")
    driven_object = cmds.ls(sl=1)
    main = cmds.ls("Main", r=1)[0]
    driven_object.remove(main)
    data = {}
    matrixConstraint_list = []
    with AssetCallback() as ast:
        for x in driven_object:
            temp = cmds.createNode("transform", name=f"{x}_temp")
            data[temp] = x
            matrixCon = matrixConstraint(x, temp, mo=0)
            matrixConstraint_list.append(matrixCon.thisAssetName)

        cmds.bakeResults(
            list(data.keys()),
            at=["t", "r"],
            t=(start, end),
            sb=1,
            simulation=1,
        )

        cmds.delete(matrixConstraint_list)
        cmds.timeEditorClip(e=1, clipId=clip_id, removeClip=1)
        cmds.setAttr(f"{main}.t", 0, 0, 0)
        cmds.setAttr(f"{main}.r", 0, 0, 0)

        for k, v in data.items():
            matrixCon = matrixConstraint(k, v, mo=0)

    cmds.bakeResults(
        list(data.values()),
        at=["t", "r"],
        t=(start, end),
        sb=1,
        simulation=1,
    )

    cmds.delete(ast)
    cmds.delete(cmds.ls("*Relocator"))
    cmds.delete(cmds.ls("*Rerotate"))

    cmds.select(main)
    cmds.TimeEditorCreateClip()


if __name__ == "__main__":
    reLocator()

    # bake_reLocator()
