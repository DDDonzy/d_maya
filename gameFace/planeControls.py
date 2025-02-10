import yaml
from dataclasses import dataclass

from UTILS.other.choseFile import choseFile
from gameFace.data.config import *

from UTILS.ui.showMessage import showMessage
from UTILS.bs.blendShapePsdTool.blendShapePsdTool import *
from UTILS.create.createBase import CreateBase
from UTILS.getHistory import get_history

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


def exportSDK(data, path=None):

    path = choseFile(path, dialogStyle=2, caption="Export SDK", fileFilter="SDK YAML file(*.yaml)", startingDirectory=DEFAULT_SDK_DIR)
    if not path:
        return

    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False, indent=4, width=80)

    showMessage("Export SDK.")


def importSDK(path=None):

    path = choseFile(path, dialogStyle=2, caption="Import weights", fileFilter="SDK YAML file(*.yaml)", fileMode=1, startingDirectory=DEFAULT_SDK_DIR)
    if not path:
        return

    with open(path, "r") as f:
        data = yaml.unsafe_load(f)

    showMessage("Import SDK.")
    return data


class PlaneControls(CreateBase):
    isDagAsset = False
    isBlackBox = False

    def __init__(self, data, mesh, *args, **kwargs):
        self.data = data

        if isinstance(mesh, str):
            mesh = [mesh]
        self.mesh = mesh

        super().__init__(*args, **kwargs)

    def _pre_create(self):
        self.thisAssetName = BRIDGE
        if cmds.objExists(BRIDGE):
            cmds.delete(BRIDGE)

    def create(self):
        bridge_list = []
        for x in self.data:
            cmds.addAttr(self.thisAssetName, ln=x.name, at="double", dv=0, k=1)
            attr_name = f"{self.thisAssetName}.{x.name}"
            bridge_list.append(attr_name)

            if not x.driverAttr:
                continue
            if not cmds.objExists(x.driverAttr):
                continue

            cmds.setDrivenKeyframe(attr_name, cd=x.driverAttr, dv=x.min, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setDrivenKeyframe(attr_name, cd=x.driverAttr, dv=x.max, v=1, inTangentType="linear", outTangentType="linear")

        for _mesh in self.mesh:
            check_bs = get_history(_mesh, "blendShape")
            if check_bs:
                cmds.delete(check_bs)

            bsNode = cmds.blendShape(_mesh, name=f"{_mesh}_bs", foc=1, tc=0)[0]
            for i, x in enumerate(self.data):
                bs_attr = add_bsTarget(bsNode, x.name)

                cmds.setDrivenKeyframe(bs_attr, cd=bridge_list[i], dv=0, v=0, inTangentType="linear", outTangentType="linear")
                cmds.setDrivenKeyframe(bs_attr, cd=bridge_list[i], dv=1, v=1, inTangentType="linear", outTangentType="linear")

    def _post_create(self):
        try:
            cmds.addAttr(BRIDGE, ln="notes", dt="string")
        except:
            pass
        info = self.data
        infoStr = yaml.dump(info, sort_keys=False, indent=4, width=80)
        cmds.setAttr(f"{BRIDGE}.notes", infoStr, type="string")
