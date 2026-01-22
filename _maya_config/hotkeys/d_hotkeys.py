from maya import cmds


def setup_hotkey():

    name_commands = [
        {
            "name": "toggle_joint_optionNameCommand",
            "annotation": "Toggle Joint Option",
            "command": 'python("import d_hotbox; d_hotbox.UI_Command.toggle_joint_option()")',
        },
        {
            "name": "hotbox_releaseNameCommand",
            "annotation": "Hotbox Release",
            "command": 'python("import d_hotbox; d_hotbox.ui_logic.d_hotbox_release()")',
        },
        {
            "name": "resetAllNameCommand",
            "annotation": "Reset All Attributes",
            "command": 'python("import d_hotbox; d_hotbox.UI_Command.reset_transform_user_defined()")',
        },
        {
            "name": "hotbox_pressNameCommand",
            "annotation": "Hotbox Press",
            "command": 'python("import d_hotbox; d_hotbox.ui_logic.d_hotbox_press()")',
        },
        {
            "name": "CopyVertexWeightsNameCommand",
            "annotation": "CopyVertexWeights",
            "command": "CopyVertexWeights",
        },
        {
            "name": "PasteVertexWeightsNameCommand",
            "annotation": "PasteVertexWeights",
            "command": "PasteVertexWeights",
        },
    ]

    for nc in name_commands:
        cmds.nameCommand(nc["name"], annotation=nc["annotation"], sourceType="mel", command=nc["command"])

    hotkey_set_name = "d_hotKey"
    if not cmds.hotkeySet(hotkey_set_name, exists=True):
        cmds.hotkeySet(hotkey_set_name, source="Maya_Default")

    cmds.hotkeySet(hotkey_set_name, current=True, edit=True)

    # Alt + 3 -> toggle_joint_option
    cmds.hotkey(keyShortcut="3", alt=True, name="toggle_joint_optionNameCommand")

    # Ctrl + ` (Backtick) -> reset_all_attrs
    cmds.hotkey(keyShortcut="`", ctl=True, name="resetAllNameCommand")

    # ` (Backtick) -> Press & Release hotbox
    cmds.hotkey(keyShortcut="`", name="hotbox_pressNameCommand", releaseName="hotbox_releaseNameCommand")

    # Shift + v -> Paste Weights
    cmds.hotkey(keyShortcut="v", sht=True, name="PasteVertexWeightsNameCommand")

    # Shift + c -> Copy Weights
    cmds.hotkey(keyShortcut="c", sht=True, name="CopyVertexWeightsNameCommand")


if __name__ == "__main__":
    setup_hotkey()
