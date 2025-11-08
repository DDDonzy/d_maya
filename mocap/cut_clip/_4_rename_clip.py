import maya.cmds as cmds

if not cmds.ls(sl=1):
    cmds.error("Please Select Clip !")
if cmds.objectType(cmds.ls(sl=1)[-1]) != "timeEditorClip":
    cmds.error("Please Select Clip !")
# --- 1. Pop up a text input dialog ---
result = cmds.promptDialog(
    title="Enter Clip Name",
    message="Please enter the new clip name:",
    button=["OK", "Cancel"],
    defaultButton="OK",
    cancelButton="Cancel",
    dismissString="Cancel",
)

# --- 2. Check if the user pressed 'OK' ---
if result == "OK":
    # Get the text input by the user and set it as the 'name' variable
    name = cmds.promptDialog(query=True, text=True)

    # --- 3. This is your original code block ---
    # (Note: 'clipid' in your code might be 'clipId', keeping it as is)

    try:
        clip = cmds.ls(sl=1)[-1]
        clipNode = clip.split(".")[0]
        clipId = cmds.getAttr(f"{clip}.clipid")  # Using 'clipid' from your code
        cmds.select(clipNode)
        clips = cmds.ls(type="timeEditorClip")
        for x in clips:
            if cmds.getAttr(f"{x}.clip[0].clipid") == clipId:  # Using 'clip[0].clipid' from your code
                continue
            cmds.delete(x)

        cmds.setAttr(f"{clip}.clipStart", 1)
        cmds.setAttr(f"{clip}.clipName", name, type="string")
        cmds.playbackOptions(min=1, max=cmds.getAttr(f"{clip}.clipDuration") + 1)
        cmds.playbackOptions(ast=1, aet=cmds.getAttr(f"{clip}.clipDuration") + 1)

        print(f"Script execution finished. Name set to: {name}")

    except Exception as e:
        cmds.warning(f"Error executing your original code: {e}")
        cmds.warning("Tip: Please check if 'clipid' spelling is correct (it's often 'clipId' in Maya) and if the node attributes are correct.")

else:
    print("Operation cancelled by user.")
