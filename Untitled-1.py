  # 之前

ALL_IN_RANGE    = r"all_in_range"
FAR_OPACITY     = r"far_opacity"
GEOMETRY_FILTER = r"geometry_filter"
POST_FRAMES     = r"post_frames"

CMD_FLAGS = {
    ALL_IN_RANGE: r"allInRange",
    FAR_OPACITY : r"farOpacity",
}


DEFAULT_SETTINGS = {
    ALL_IN_RANGE   : GhostingPreferenceAllInRange().value_default,
    FAR_OPACITY    : GhostingPreferenceFarOpacity().value_default,
    GEOMETRY_FILTER: GhostingPreferenceGeometryFilter().value_default,
    POST_FRAMES    : GhostingPreferencePostFrames().value_default,
}


  # 格式化后
ALL_IN_RANGE    = r"all_in_range"
FAR_OPACITY     = r"far_opacity"
GEOMETRY_FILTER = r"geometry_filter"
POST_FRAMES     = r"post_frames"

CMD_FLAGS = {ALL_IN_RANGE: r"allInRange", FAR_OPACITY: r"farOpacity"}


DEFAULT_SETTINGS = {ALL_IN_RANGE: GhostingPreferenceAllInRange().value_default, FAR_OPACITY: GhostingPreferenceFarOpacity().value_default, GEOMETRY_FILTER: GhostingPreferenceGeometryFilter().value_default, POST_FRAMES: GhostingPreferencePostFrames().value_default}
