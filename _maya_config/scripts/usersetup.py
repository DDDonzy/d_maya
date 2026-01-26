import maya.utils
import d_hotkeys
import userprefs


maya.utils.executeDeferred(d_hotkeys.setup_hotkey)
maya.utils.executeDeferred(userprefs.setup_userprefs)
