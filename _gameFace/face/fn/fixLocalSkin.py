from face.fn.localSkin import skinClusterToLocal
from face.fn.getHistory import get_history
from face.fn import transform as t
from face.fn.showMessage import showMessage
import yaml
from maya import cmds


FACE_ROOT = "FACE_SYSTEM"
CONTROLS_ROOT = "Controls_GRP"


def fixLocalSkin():

    uvPinList = yaml.load(cmds.getAttr(FACE_ROOT+".notes"))["uvPin"]

    for uvPinMesh in uvPinList:
        sk = get_history(uvPinMesh, "skinCluster")
        if sk:
            skinClusterToLocal(sk[0])
            t.matrixConstraint(CONTROLS_ROOT, uvPinMesh)

    showMessage("Fix Local Skin Done!")
