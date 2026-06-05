import json
from pathlib import Path
import m_utils.compounds.matrixConstraint as matrixConstraint
from m_utils.create.createBase import AssetCallback
from maya import cmds

# 使用 Path 获取当前脚本所在目录，并拼接 JSON 文件路径

file_list = cmds.fileDialog2(dialogStyle=2, caption="Constraint Data", fileFilter="Constraint Data (*.json)", fileMode=1)
config_path = Path(file_list[0])

with config_path.open("r", encoding="utf-8") as f:
    fit_constraint_data = json.load(f)

with AssetCallback(name="ue_to_adv_fit_constraints") as asset:
    for key, data in fit_constraint_data.items():
        con = matrixConstraint(data["driver"], data["driven"])
        cmds.setAttr(con.inputOffsetMatrix, data["offsetMatrix"], type="matrix")

# 检查是否有问题，如果没问题就删除约束
cmds.refresh(f=1)
cmds.delete(asset)
