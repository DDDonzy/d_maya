from maya import cmds


def setup_userprefs():
    # File
    cmds.optionVar(iv=("fileExecuteSN", 0))  # open file do not execute script

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

    # Animations
    cmds.optionVar(sv=("workingUnitTime", "ntscf"))
    cmds.optionVar(sv=("workingUnitTimeDefault", "ntscf"))

    cmds.optionVar(fv=("playbackMin", 0))
    cmds.optionVar(fv=("playbackMinDefault", 0))
    cmds.optionVar(fv=("playbackMinRange", 0))
    cmds.optionVar(fv=("playbackMinRangeDefault", 0))

    cmds.optionVar(fv=("playbackMax", 100))
    cmds.optionVar(fv=("playbackMaxDefault", 100))
    cmds.optionVar(fv=("playbackMaxRange", 100))
    cmds.optionVar(fv=("playbackMaxRangeDefault", 100))
