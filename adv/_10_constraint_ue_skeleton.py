import re
import json
from pathlib import Path

import m_utils.compounds.matrixConstraint as matrixConstraint
from m_utils.create.createBase import AssetCallback
from m_utils.dag.iterHierarchy import IterHierarchy

from maya import cmds

# 使用 Path 获取当前脚本所在目录，并拼接 JSON 文件路径
file_list = cmds.fileDialog2(dialogStyle=2, caption="Constraint Data", fileFilter="Constraint Data (*.json)", fileMode=1)
config_path = Path(file_list[0])


with config_path.open("r", encoding="utf-8") as f:
    constraint_data = json.load(f)

with AssetCallback(name="RIG_ASSET", force=False):
    for k, v in constraint_data.items():
        con = matrixConstraint(v["driver"], k, mo=1)
        cmds.setAttr(con.inputOffsetMatrix, v["offsetMatrix"], type="matrix")
cmds.parent("Root_M", "RootGround_M")

# ################
# 额外的骨骼


def advanced_name_process(node_name):
    # 1. 把原本的下划线替换为空格
    cleaned = node_name.replace("_", " ")

    # 2. 在大写字母前注入空格（处理驼峰命名 UpperArm -> Upper Arm）
    cleaned = re.sub(r"(?<!^)(?=[A-Z])", " ", cleaned)

    # 4. 在数字前后注入空格 \d+ 匹配连续的数字
    cleaned = re.sub(r"(\d+)", r" \1 ", cleaned)

    # 5. 切分成单词列表
    words = cleaned.split()

    # 6. 过滤掉不需要的标记（删除 m 和 dup）
    discard_words = {"m", "dup"}
    filtered_words = [w for w in words if w.lower() not in discard_words]

    # 7. 【核心修改】创建分类收集器
    base_words = []  # 存放普通名字单词（如 sword, arm）
    digit_words = []  # 存放格式化后的数字（如 01, 02）
    side_word = None  # 存放方位词（l 或 r）

    for w in filtered_words:
        w_lower = w.lower()

        if w_lower in {"l", "r"}:
            side_word = w_lower  # 捕获 l 或 r
        elif w.isdigit():
            digit_words.append(w.zfill(2))  # 数字化并强制补齐为2位数
        else:
            base_words.append(w)  # 纯文本名字

    # 8. 【核心修改】严格按照你的规则重新拼装列表：
    # 基础名字 + 数字 + 方位(L/R)
    # 这样能完美保证：数字一定在 L/R 的前一个位置；如果没有 L/R，数字自然就在最后。
    final_words = base_words + digit_words
    if side_word:
        final_words.append(side_word)

    # 9. 用下划线重新拼接并转为全小写
    return "_".join(final_words).lower()


def duplicate_and_rename_chain(root_joint):
    """
    一键复制整条骨骼链并正确命名（支持任意复杂分支层级）
    """
    new_root = cmds.duplicate(root_joint, rr=True, name=f"dup_{root_joint}")[0]

    all_joints = cmds.listRelatives(new_root, ad=True, f=True, type="joint") or []
    all_joints.append(cmds.ls(new_root, l=True)[0])  # 把新根骨骼也加进去

    all_joints.sort(key=len, reverse=True)

    final_joints = []
    for jnt_path in all_joints:
        # 提取当前节点的短名
        short_name = jnt_path.split("|")[-1]

        # 计算清洗后的新名字
        target_name = advanced_name_process(short_name)

        # 执行重命名
        actual_name = cmds.rename(jnt_path, target_name)
        final_joints.append(actual_name)

    print(f"成功复制并重命名了 {len(final_joints)} 根骨骼！")
    return final_joints


extend = cmds.listRelatives("DeformationSystem", c=1)
extend.remove("RootGround_M")
for x in extend:
    dup_obj = duplicate_and_rename_chain(x)
    cmds.parent(dup_obj[-1], w=1)
    _source_iter = IterHierarchy(x)
    for obj, _ in IterHierarchy(dup_obj[-1]):
        with AssetCallback(name="RIG_ASSET", force=False):
            source_obj, _ = _source_iter.__next__()
            matrixConstraint(source_obj, obj)
