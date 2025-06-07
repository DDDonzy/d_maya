from maya import cmds, mel


def get_lastSelection():
    return mel.eval("getShapeEditorTreeviewSelection 20")


def get_selectionBlendShape():
    return mel.eval("getShapeEditorTreeviewSelection 11")


def get_selectionTarget():
    return mel.eval("getShapeEditorTreeviewSelection 14")


def get_selectionInbetween():
    return mel.eval("getShapeEditorTreeviewSelection 16")
