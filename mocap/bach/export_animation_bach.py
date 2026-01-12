from pathlib import Path

import log
from mocap.mayapy import init_maya
from mocap.suppress_maya_logs import suppress_maya_logs
import mocap.gameExportInfo as exportInfo
import mocap.FBX_Export.fbx_preset as fbx_preset

from maya import cmds, mel


EXPORT_SETS = "Export_Animation_Sets"


#  run maya.exe
init_maya()


# project file path
task_file = list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\Bake").glob("*.ma"))
fbx_output_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap\Bake")
rig_file = r"N:\SourceAssets\Characters\Hero\Rigs\RIG_Hero.ma"
rig_namespace = "RIG"
rig_reference_node = "RIGRN"

for maya_file in task_file:
    log.info(f"Open File: {maya_file}")
    with suppress_maya_logs():
        cmds.file(maya_file, open=1, force=1)
    log.debug("Opened File")

    # get export data
    log.debug("get export data")
    export_info = {
        "exportPath": "N:/SourceAssets/Characters/Hero/Animations/FBX",
        "exportName": "",
        "clip": {
            maya_file.stem: (cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
        },
    }
    log.trace(f"export info: {export_info}")
    exportInfo.create_exportData(export_info)
    log.debug("export data created")
    export_set = cmds.ls(f"*:{EXPORT_SETS}")
    if not export_set:
        log.exception(f"Export set not found: {EXPORT_SETS}")
        continue
    export_set = export_set[0]

    fbx_preset.set_preset()  # set preset

    # export clip fbx
    for clip_name, (time_start, time_end) in export_info["clip"].items():
        log.debug(f"Exporting: {clip_name}  |  ({time_start} - {time_end})")
        log.trace(f"set bake time,{time_start} - {time_end}")
        mel.eval(f"FBXExportBakeComplexStart -v {int(time_start)};")
        mel.eval(f"FBXExportBakeComplexEnd -v {int(time_end)};")

        # set export path
        export_path = fbx_output_dir / f"{export_info['exportName']}{clip_name}.fbx"
        export_path.parent.mkdir(parents=True, exist_ok=True)

        cmds.select(export_set, replace=True)
        with suppress_maya_logs():
            mel.eval(f'FBXExport -f "{export_path.as_posix()}" -s;')
        log.success(f"Exported: {export_path.as_posix()}")
    log.success(f"Completed File: {maya_file}")
