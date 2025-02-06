import yaml
from dataclasses import dataclass

from gameFace.choseFile import choseFile
from UTILS.ui.showMessage import showMessage

from maya import cmds


@dataclass
class DriverData(yaml.YAMLObject):
    yaml_tag = 'DriverData'
    name: str
    driverAttr: str
    min: int = 0
    max: int = 1


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
