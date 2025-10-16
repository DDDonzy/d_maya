from pathlib import Path

from maya import cmds, mel


from mocap.mayapy import init_maya
from mocap.suppress_maya_logs import suppress_maya_logs
from mocap.reference import list_all_references, repath_reference
import mocap.gameExportInfo as exportInfo

PRESET = r"E:\d_maya\mocap\FBX_Export\FBX_Preset\Animation.mel"
EXPORT_SETS = "UE_Animation_Sets"


#
#
#
# get animation preset
#
#
#

try:
    preset_anim = Path(__file__).parent / r"FBX_Preset" / r"Animation.mel"
except Exception:
    preset_anim = Path(PRESET)
if not preset_anim.exists():
    raise RuntimeError(f"Preset file not found: {preset_anim}")


#
#
#
# debug function
#
#
#
def info(title: str, total_length: int = 200) -> None:
    formatted_title = f"{f' {title} ':=^{total_length}}"
    print(formatted_title)


def debug(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ DEBUG ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


def error(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ ERROR ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


#
#  run maya.exe
#
init_maya()


#
#
#
# project file path
#
#
#
task_file = list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\xx").glob("*.ma"))
fbx_output_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap\xx")
rig_file = r"N:\SourceAssets\Characters\Hero\Rigs\RIG_Hero.ma"
rig_namespace = "RIG"
rig_reference_node = "RIGRN"

for maya_file in task_file:
    debug(f"Open File: {maya_file}")
    with suppress_maya_logs():
        cmds.file(maya_file, open=1, force=1)
    debug("set fbx preset")

    # get export data
    debug("get export data")
    export_info = {
        "exportPath": "N:/SourceAssets/Characters/Hero/Animations/FBX",
        "exportName": "",
        "clip": {
            maya_file.stem: (cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
        },
    }
    exportInfo.create_exportData(export_info)
    cmds.file(save=1, force=1)
    export_set = cmds.ls(f"*:{EXPORT_SETS}")
    if not export_set:
        raise RuntimeError(f"Export set not found: {export_set}")
    export_set = export_set[0]

    try:
        mel.eval(f'source "{preset_anim.as_posix()}";')
    except Exception:
        raise

    # export clip fbx
    for clip_name, (time_start, time_end) in export_info["clip"].items():
        print(f"Exporting: {clip_name}  |  ({time_start} - {time_end})")
        debug(f"set bake time,{time_start} - {time_end}")
        mel.eval(f"FBXExportBakeComplexStart -v {int(time_start)};")
        mel.eval(f"FBXExportBakeComplexEnd -v {int(time_end)};")

        # set export path
        export_path = fbx_output_dir / f"{export_info['exportName']}{clip_name}.fbx"
        export_path.parent.mkdir(parents=True, exist_ok=True)

        cmds.select(export_set, replace=True)
        mel.eval(f'FBXExport -f "{export_path.as_posix()}" -s;')
        print(f"Exported: {export_path.as_posix()}")

    #
