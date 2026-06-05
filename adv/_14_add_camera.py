from maya import cmds
import m_utils.compounds.matrixConstraint as matrixConstraint
from m_utils.create.createBase import AssetCallback


cam_path = r"N:\SourceAssets\Camera\RIG_Camera.ma"
cmds.file(cam_path, i=True, namespace=":", force=True)
with AssetCallback(name="RIG_ASSET", force=False):
    matrixConstraint("root", "CAMERA", mo=1)
