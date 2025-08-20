from maya import cmds, mel

from pathlib import Path

# file
fbx_path = r"C:\Users\ext.dxu\Downloads\2025.8.9\data\Idle + turn_11\Take_011_skeleton_0.fbx"
root = "skeleton_0_Hips"
cmds.file(new=1, f=1)
cmds.currentUnit(time="ntscf")
cmds.file(fbx_path, i=1, f=1)


# build clip
cmds.select(root)
cmds.TimeEditorCreateClip()

start = 0
end = 0
for clip in cmds.ls("*.clip[*].clipStart"):
    _start = cmds.getAttr(clip)
    print(_start)
    if _start < start:
        start = _start

for clip in cmds.ls("*.clip[*].clipDuration"):
    _end = cmds.getAttr(clip)
    if _end > end:
        end = _end

cmds.playbackOptions(min=start, max=end)


# export
export_list = []
clip_list = cmds.ls(type="timeEditorClip")

for clip in clip_list:
    if cmds.getAttr(f"{clip}.clip[0].clipMuted"):
        print(f"skip muted clip: {clip}")
        continue
    clip_name = cmds.getAttr(f"{clip}.clip[0].clipName")
    start_time = cmds.getAttr(f"{clip}.clip[0].clipStart")
    end_time = cmds.getAttr(f"{clip}.clip[0].clipDuration")
    export_list.append({
        "name": clip_name,
        "start": start_time,
        "end": start_time + end_time,
    })


def build_export_preset():
    node_name = "_ANIM_EXPORTER_"

    current_file = Path(cmds.file(query=True, sceneName=True))
    current_dir = current_file.parent
    file_name = current_file.stem
    fbx_dir = current_dir / "fbx"

    if cmds.objExists(node_name):
        cmds.delete(node_name)

    for x in cmds.ls(type="gameFbxExporter"):
        cmds.setAttr(f"{x}.ils", False)
        cmds.setAttr(f"{x}.ilu", False)
    exporter_node = cmds.createNode("gameFbxExporter", name=node_name)
    cmds.setAttr(f"{exporter_node}.pn", node_name, type="string")
    cmds.setAttr(f"{exporter_node}.ils", True)
    cmds.setAttr(f"{exporter_node}.ilu", True)
    cmds.setAttr(f"{exporter_node}.eti", 2)
    cmds.setAttr(f"{exporter_node}.spt", 2)
    cmds.setAttr(f"{exporter_node}.ic", False)
    cmds.setAttr(f"{exporter_node}.ebm", True)
    cmds.setAttr(f"{exporter_node}.fv", "FBX201800", type="string")
    cmds.setAttr(f"{exporter_node}.exp", fbx_dir, type="string")
    cmds.setAttr(f"{exporter_node}.exf", file_name, type="string")
    return node_name


exporter_node = build_export_preset()
for i, clip in enumerate(export_list):
    cmds.setAttr(f"{exporter_node}.ac[{i}].acn", clip["name"], type="string")
    cmds.setAttr(f"{exporter_node}.ac[{i}].acs", clip["start"])
    cmds.setAttr(f"{exporter_node}.ac[{i}].ace", clip["end"])

if cmds.window("gameExporterWindow", q=1, ex=1):
    cmds.deleteUI("gameExporterWindow")
mel.eval("gameFbxExporter")


# rename clips
def rename_clips():
    selected_clips = cmds.ls(sl=1)
    for x in selected_clips:
        try:
            if cmds.objectType(x, isa="timeEditorClip"):
                clipid = cmds.getAttr(f"{x}.clipid")
                mel.eval(f"teRenameClip {clipid}")
        except Exception as e:
            print(f"Error renaming clip {x}: {e}")


# mute
for x in cmds.ls(sl=1):
    try:
        if cmds.objectType(x, isa="timeEditorClip"):
            cmds.setAttr(f"{x}.clipMuted", not cmds.getAttr(f"{x}.clipMuted"))
    except Exception as e:
        print(f"Error muting clip {x}: {e}")




