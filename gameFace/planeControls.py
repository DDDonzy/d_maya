import yaml
from dataclasses import dataclass

from UTILS.other.choseFile import choseFile
from gameFace.data.config import *

from UTILS.ui.showMessage import showMessage
from UTILS.bs.blendShapePsdTool.blendShapePsdTool import *
from UTILS.create.createBase import CreateBase

from maya import cmds


@dataclass
class DriverData(yaml.YAMLObject):
    yaml_tag = 'DriverData'
    name: str
    driverAttr: str = None
    min: int = 0
    max: int = 1

    def __str__(self):
        return self.name


a = DriverData("L_BrowUp", "Brrow_ctrl3.tx", 0, 1)
b = DriverData("L_BrowDw", "Brrow_ctrl3.tx", 0, -1)


def exportSDK(data, path=None):

    path = choseFile(path, dialogStyle=2, caption="Export SDK", fileFilter="SDK YAML file(*.yaml)")
    if not path:
        return

    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False, indent=4, width=80)

    showMessage("Export SDK.")


def importSDK(path=None):

    path = choseFile(path, dialogStyle=2, caption="Import weights", fileFilter="SDK YAML file(*.yaml)", fileMode=1)
    if not path:
        return

    with open(path, "r") as f:
        data = yaml.unsafe_load(f)

    showMessage("Import SDK.")
    return data


class PlaneControls(CreateBase):
    isDagAsset = False

    def __init__(self, data, mesh, *args, **kwargs):
        self.data = data

        if isinstance(mesh, str):
            mesh = [mesh]
        self.mesh = mesh

        super().__init__(*args, **kwargs)

    def create(self):
        bridge_list = []
        for x in self.data:
            cmds.addAttr(self.thisAssetName, ln=x.name, at="double", dv=0, k=1)
            attr_name = f"{self.thisAssetName}.{x.name}"
            bridge_list.append(attr_name)
            if x.driverAttr is None:
                continue
            cmds.setDrivenKeyframe(attr_name, cd=x.driverAttr, dv=x.min, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setDrivenKeyframe(attr_name, cd=x.driverAttr, dv=x.max, v=1, inTangentType="linear", outTangentType="linear")
        for _mesh in self.mesh:
            bsNode = cmds.blendShape(_mesh, name=f"{_mesh}_bs")[0]
            for i, x in enumerate(self.data):
                bs_attr = add_bsTarget(bsNode, x.name)
                if x.driverAttr is None:
                    continue
                cmds.setDrivenKeyframe(bs_attr, cd=bridge_list[i], dv=0, v=0, inTangentType="linear", outTangentType="linear")
                cmds.setDrivenKeyframe(bs_attr, cd=bridge_list[i], dv=1, v=1, inTangentType="linear", outTangentType="linear")
