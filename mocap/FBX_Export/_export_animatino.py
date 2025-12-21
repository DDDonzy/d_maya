from pathlib import Path

from maya import cmds, mel

import mocap.gameExportInfo as exportInfo


EXPORT_SETS = "Export_Animation_Sets"

try:
    preset_anim = Path(__file__).parent / r"FBX_Preset" / r"Animation.mel"
except Exception:
    preset_anim = Path(r"E:\d_maya\mocap\FBX_Export") / r"FBX_Preset" / r"Animation.mel"
if not preset_anim.exists():
    raise RuntimeError(f"Preset file not found: {preset_anim}")
try:
    mel.eval(f'source "{preset_anim.as_posix()}";')
except Exception:
    raise


# get export data
export_info = exportInfo.get_exportData()
export_set = cmds.ls(f"*:{EXPORT_SETS}")
if not export_set:
    raise RuntimeError(f"Export set not found: {export_set}")
export_set = export_set[0]

for clip_name, (time_start, time_end) in export_info["clip"].items():
    print(f"Exporting: {clip_name}  |  ({time_start} - {time_end})")

    mel.eval(f"FBXExportBakeComplexStart -v {int(time_start)};")
    mel.eval(f"FBXExportBakeComplexEnd -v {int(time_end)};")

    # set export path
    export_path = Path(export_info["exportPath"]) / f"{export_info['exportName']}{clip_name}.fbx"
    export_path.parent.mkdir(parents=True, exist_ok=True)
    # select export set
    cmds.select(export_set, replace=True)
    mel.eval(f'FBXExport -f "{export_path.as_posix()}" -s;')
    print(f"Exported: {export_path.as_posix()}")
