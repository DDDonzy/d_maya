from UTILS.transform import uvPin
from maya.api import OpenMaya as om
import yaml
from maya import cmds
from UTILS import apiundo
from gameFace.createControls import ControlData

obj = "pCube1_uvPinMesh"
ba = "blendShape1"
targetIndex = 0


def setPose(obj, bs, targetIndex, pose_position=None):
    if not pose_position:
        uvPin_data = yaml.unsafe_load(cmds.getAttr(f"{obj}.notes"))
        driven_list = [ControlData(x["driven"]) for x in uvPin_data]
        control_list = [x.ctl for x in driven_list]
        
        data_fnMesh, data = uvPin.create_planeByObjectList(targetList=control_list, buildInMaya=False)
        pose_position = data_fnMesh.getPoints(om.MSpace.kObject)

    obj_fnMesh = om.MFnMesh(om.MSelectionList().add(obj).getDagPath(0))
    base_pos = obj_fnMesh.getPoints(om.MSpace.kObject)

    def _doit():
        cmds.sculptTarget(bs, e=1, target=targetIndex)
        obj_fnMesh.setPoints(pose_position, om.MSpace.kObject)
        cmds.sculptTarget(bs, e=1, target=-1)

    def _undo():
        cmds.sculptTarget(bs, e=1, target=targetIndex)
        obj_fnMesh.setPoints(base_pos, om.MSpace.kObject)
        cmds.sculptTarget(bs, e=1, target=-1)

    _doit()
    apiundo.commit(undo=_undo,
                   redo=_doit)


setPose(obj, ba, targetIndex)
