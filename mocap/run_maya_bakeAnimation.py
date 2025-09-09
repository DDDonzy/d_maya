from maya import cmds
import maya.standalone


from pathlib import Path

from mocap.mocap_bake_rig import bakeAnimations
from mocap.export_data import get_exportData, create_exportData
from UTILS.scene.removeUnknownPlugin import removeUnknownPlugin


def info(title: str, total_length: int = 200) -> None:
    formatted_title = f"{f' {title} ':=^{total_length}}"
    print(formatted_title)


def debug(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ DEBUG ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


def error(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ ERROR ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


def clean_unknown_data():
    try:
        unknown_nodes = cmds.ls(type="unknown")
        if unknown_nodes:
            cmds.delete(unknown_nodes)

        unknown_plugin_nodes = cmds.ls(type="unknownPlugin")
        if unknown_plugin_nodes:
            cmds.delete(unknown_plugin_nodes)

        unknown_transforms = cmds.ls(type="unknownTransform")
        if unknown_transforms:
            cmds.delete(unknown_transforms)

        refs = cmds.ls(references=True)
        for ref in refs:
            if not cmds.referenceQuery(ref, isLoaded=True):
                try:
                    cmds.file(removeReference=True, referenceNode=ref)
                except Exception:
                    pass

        cmds.dataStructure(removeAll=True)
        print("Clear unknown data complete.")

    except Exception as e:
        print(f"Clear unknown error: {e}")


task_file      = list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\clip_preprocessing").glob("*.ma"))
output_dir     = Path(r"N:\SourceAssets\Characters\Hero\Mocap")
fbx_output_dir = Path(r"N:\SourceAssets\Characters\Hero\Animations\FBX")

rig_file        = r"N:\SourceAssets\Characters\Hero\Rigs\RIG_TestCharacter.ma"
rig_namespace   = "RIG"
mocap_namespace = "MOCAP"
clip_namespace  = "CLIP"

maya.standalone.initialize(name="python")
cmds.optionVar(iv=("fileIgnoreMissingPlugin", 1))
info("Maya Standalone Initialized")
plugin_name = "fbxmaya"
cmds.loadPlugin(plugin_name)
debug(f"Plugin {plugin_name} loaded successfully.")


success_list = []
already_done = [x.name for x in output_dir.glob("*.ma")]
for maya_file in task_file:
    file_name = maya_file.name
    if file_name in already_done:
        info(f"Skip (already done): {maya_file}")
        continue
    info(f"Process : {maya_file}")
    try:
        # Open File
        debug(f"Open File: {file_name}")
        try:
            cmds.file(maya_file, open=1, force=1)
        except RuntimeError:
            pass

        # Get Clip Data
        clip_data = get_exportData()
        if clip_data:
            debug("Get Clip Success")
        else:
            debug("No Clip Data Found, Skip!")
            continue
        # data structure clear
        cmds.dataStructure(removeAll=True)
        removeUnknownPlugin()
        debug("Clear Data Structure Complete And Remove Unknown Plugin")
        cmds.file(rename=maya_file)
        cmds.file(save=True, force=True)
        debug("Cleaned File Saved")

        # Create New File
        cmds.file(file_name, new=1, force=1)
        debug("New File Created")

        cmds.currentUnit(time="ntscf")
        debug("Set Time Unit to ntscf-----60 FPS")

        export_node = create_exportData(clip_data)
        debug("Create Export Node Complete")

        # reference Rig and Mocap
        debug("Reference Clip and Rig")
        cmds.file(rig_file, reference=True, namespace="RIG", force=1)
        debug("Rig Reference Complete")

        cmds.file(maya_file, reference=True, namespace="CLIP", force=1)
        debug("Clip Reference Complete")

        # bake Animation
        clips_attrs = cmds.ls(f"{export_node}.animClips[*]")
        start = cmds.getAttr(f"{clips_attrs[0]}.animClipStart")
        end = cmds.getAttr(f"{clips_attrs[-1]}.animClipEnd")

        cmds.playbackOptions(ast=start)
        cmds.playbackOptions(aet=end)
        debug(f"Set Playback Range: {start} - {end}")
        debug("Baking Animation...")
        bakeAnimations(
            target_namespace=rig_namespace,
            source_namespace=":".join([clip_namespace, mocap_namespace]),
            time=(start, end),
        )
        debug("Baking Animation Complete")

        cmds.setAttr(f"{export_node}.exportPath", str(fbx_output_dir), type="string")
        debug("Set Export Path Complete")
        clean_unknown_data()
        debug("Clean Unknown Data Complete")
        cmds.file(unloadReference=f"{clip_namespace}RN")
        debug("Unload Clip Reference Complete")
        cmds.file(rename=str(output_dir / file_name))
        cmds.file(save=True, force=True, type="mayaAscii")
        debug("Save File Complete")

    except Exception as e:
        error(maya_file)
        error(e)
        raise
    success_list.append(maya_file)
    info(f"Complate: {str(output_dir / file_name)}")

info(f"Total {len(success_list)} files processed successfully.")
for x in success_list:
    info(x)

