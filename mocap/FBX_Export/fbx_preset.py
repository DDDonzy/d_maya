import log
from pathlib import Path
from maya import mel


PRESET = r"E:\d_maya\mocap\FBX_Export\FBX_Preset\Animation.mel"


def set_preset():
    """
    Load FBX export preset for animation export.
    """
    # get animation preset
    try:
        preset_anim = Path(__file__).parent / r"FBX_Preset" / r"Animation.mel"
    except Exception:
        preset_anim = Path(PRESET)
    if not preset_anim.exists():
        log.exception(f"Preset file not found: {preset_anim}")
        return

    try:
        mel.eval(f'source "{preset_anim.as_posix()}";')
    except Exception as e:
        log.exception(f"Failed to load preset \n {e}")
        return
