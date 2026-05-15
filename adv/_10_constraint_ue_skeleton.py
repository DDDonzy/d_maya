import json
from pathlib import Path
import m_utils.compounds.matrixConstraint as matrixConstraint
from m_utils.create.createBase import AssetCallback
from maya import cmds

# 使用 Path 获取当前脚本所在目录，并拼接 JSON 文件路径
config_path = Path(r"E:\d_maya\adv\__adv_constraint_ue.json")

with config_path.open("r", encoding="utf-8") as f:
    constraint_data = json.load(f)

with AssetCallback(name="RIG_ASSET", force=False):
    for k, v in constraint_data.items():
        con = matrixConstraint(v["driver"], k, mo=1)
        cmds.setAttr(con.inputOffsetMatrix, v["offsetMatrix"], type="matrix")
