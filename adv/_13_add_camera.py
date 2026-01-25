from maya import cmds

cam_path = r"N:\SourceAssets\Camera\RIG_Camera.ma"
cmds.file(cam_path, reference=True, namespace="CAM", force=1)

cmds.parentConstraint("root", "CAM:CAMERA", mo=1)
