from maya import cmds


def setup_userprefs():
    # Rigging.Skin.Bind Skin preferences
    cmds.optionVar(iv=("bindTo", 2))
    cmds.optionVar(iv=("colorizeSkeleton", 0))
    cmds.optionVar(iv=("multipleBindPosesOpt", 0))
    cmds.optionVar(iv=("obeyMaxInfl", 0))
    cmds.optionVar(iv=("maxInfl", 4))
    cmds.optionVar(iv=("removeUnusedInfluences", 0))

    # Rigging.Skin.Add Influence preferences
    cmds.optionVar(iv=("lockWeights", 1))
    cmds.optionVar(iv=("useGeometry", 0))
    cmds.optionVar(iv=("defaultWeight", 0))

    # Set default time unit to 60 FPS
    cmds.currentUnit(time='60fps')

    # Set default time range to 0-120 frames
    cmds.playbackOptions(minTime=0, maxTime=120, animationStartTime=0, animationEndTime=120)
    cmds.currentTime(0)
