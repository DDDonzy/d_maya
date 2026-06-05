
import os
import sys
from pathlib import Path
import json

from maya import cmds,mel
from maya.api import OpenMaya as om

import log
import mocap.gameExportInfo as exportInfo
import mocap.FBX_Export.fbx_preset as fbx_preset
from mocap.suppress_maya_logs import suppress_maya_logs
from mocap.mayapy import init_maya

init_maya()



def append_pipeline_log(file_path, status, maya_file, message):
    """
    持续追加 JSONL 日志，通过对整列实施固定宽度，彻底解决 success/error 长度不同导致的错位。
    单行绝对锁定 300 字符。
    """
    # 1. 规范化路径与输入文本
    win_file_path = os.path.normpath(file_path)
    directory = os.path.dirname(win_file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    clean_status = str(status).lower().strip()
    clean_maya_file = os.path.normpath(str(maya_file))
    clean_msg = str(message).replace('\n', ' ').replace('\r', '').strip()
    
    # 2. 生成标准的键值对字符串（去掉大括号）
    kv_status = json.dumps({"status": clean_status}, ensure_ascii=False)[1:-1] # 'status": "error"' 或 'status": "success"'
    kv_file   = json.dumps({"file": clean_maya_file}, ensure_ascii=False)[1:-1] # 'file": "..."'
    kv_log    = json.dumps({"log": clean_msg}, ensure_ascii=False)[1:-1]       # 'log": "..."'
    
    # 3. 核心：整列强行固定宽度
    # 【第一列：状态列】拼上开头的逗号，强行固定占用 25 个字符
    col_status = f"{kv_status}, ".ljust(25)
    
    # 【第二列：文件列】拼上开头的逗号，强行固定占用 110 个字符
    col_file = f"{kv_file}, ".ljust(200)
    
    # 4. 精确计算留给最后一列（日志列）的剩余空间
    # 总长 500 - 开头大括号 '{ ' (2) - 状态列 (25) - 文件列 (200) - 结尾大括号 ' }\n' (3) = 270 字符
    allowed_log_space = 500 - 2 - 25 - 200 - 3
    
    # 截断或用空格补齐日志列
    col_log = kv_log.ljust(allowed_log_space)[:allowed_log_space]
    
    # 5. 拼装成最终整行（这里没有任何额外增加长度的字符了）
    json_line = f"{{ {col_status}{col_file}{col_log} }}\n"
    
    # 6. 追加写入文件
    with open(win_file_path, 'a', encoding='utf-8') as f:
        f.write(json_line)




task_file = list(Path(r"N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260419\Anim\xxx").glob("*.ma"))
# fbx_output_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260000\Anim\FBX")


for maya_file in task_file:
    try:
        # open file
        log.info(f"Open File: {maya_file}")
        with suppress_maya_logs():
            cmds.file(maya_file, open=1, force=1)
        log.debug("Opened File")

        # # root
        # namespace = ""
        # root = "FKRootGround_M"
        # EXPORT_SETS = cmds.ls("Export_ANI_Body",r=1)[0]

        # offset_matrix = [1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1]
        # offset_matrix = om.MMatrix(offset_matrix)

        # anim_data = []
        # obj = cmds.ls(root,r=1)[0]
        # keyframes = cmds.keyframe(obj, query=True, timeChange=True)
        # for k in keyframes:
        #     matrix = om.MMatrix(cmds.getAttr(f"{obj}.matrix",t=k))
        #     anim_data.append(matrix * offset_matrix)
            
        # cmds.cutKey(obj,clear=True)
        # for i,k in enumerate(keyframes):
        #     cmds.setKeyframe(obj, attribute="translateX", time=k, value=anim_data[i][12])
        #     cmds.setKeyframe(obj, attribute="translateY", time=k, value=anim_data[i][13])
        #     cmds.setKeyframe(obj, attribute="translateZ", time=k, value=anim_data[i][14])
        # log.success("Root animation baked to translate")


        # weapon
        ctrls = ['Fingers_R', 'FKMiddleFinger1_R', 'FKMiddleFinger2_R', 'FKMiddleFinger3_R', 'FKIndexFingerRoot_R', 'FKIndexFinger1_R', 'FKIndexFinger2_R', 'FKThumbFinger1_R', 'FKIndexFinger3_R', 'FKThumbFinger2_R', 'FKThumbFinger3_R', 'FKCup_R', 'FKRingFingerRoot_R', 'FKRingFinger1_R', 'FKRingFinger2_R', 'FKPinkyFingerRoot_R', 'FKRingFinger3_R', 'FKPinkyFinger1_R', 'FKPinkyFinger2_R', 'FKPinkyFinger3_R', 'FKMiddleFingerRoot_R', 'FKSword0_M', 'FKRootWeapon_M']
        for x in ctrls:
            x = cmds.ls(x,r=1)[0]
            cmds.cutKey(x,clear=True)

        weapon = "FKRootWeapon_M"
        weapon = cmds.ls(weapon,r=1)[0]
        cmds.setAttr(f"{weapon}.parentSpace",3)

        if r"C:\Users\Donzy\Documents\maya\studiolibrary-2.21.3\src" not in sys.path:
            sys.path.insert(0, r"C:\Users\Donzy\Documents\maya\studiolibrary-2.21.3\src")
        import mutils  # type: ignore  # noqa: E402

        mutils.loadPose(r"N:\SourceAssets\Characters\Hero\Animations\Pose\hand\hand_wepaon.pose\pose.json", namespaces=":", key=True)
        log.success("Weapon pose applied")




        # # export
        # log.debug("get export data")
        # if min(keyframes) != cmds.playbackOptions(q=1, min=1) or max(keyframes) != cmds.playbackOptions(q=1, max=1):
        #     raise ValueError("Keyframe range does not match playback range.")

        # export_info = {
        #     "exportPath": fbx_output_dir,
        #     "exportName": "",
        #     "clip": {
        #         maya_file.stem: (cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
        #     },
        # }
        # log.trace(f"export info: {export_info}")
        # exportInfo.create_exportData(export_info)
        # log.debug("export data created")

        # export_set = EXPORT_SETS

        # fbx_preset.set_preset()  # set preset

        # # export clip fbx
        # for clip_name, (time_start, time_end) in export_info["clip"].items():
        #     log.debug(f"Exporting: {clip_name}  |  ({time_start} - {time_end})")
        #     log.trace(f"set bake time,{time_start} - {time_end}")
        #     mel.eval(f"FBXExportBakeComplexStart -v {int(time_start)};")
        #     mel.eval(f"FBXExportBakeComplexEnd -v {int(time_end)};")

        #     # set export path
        #     export_path = fbx_output_dir / f"{export_info['exportName']}{clip_name}.fbx"
        #     export_path.parent.mkdir(parents=True, exist_ok=True)

        #     cmds.select(export_set, replace=True)
        #     with suppress_maya_logs():
        #         mel.eval(f'FBXExport -f "{export_path.as_posix()}" -s;')
        #     log.success(f"Exported: {export_path.as_posix()}")
        # log.success(f"Completed File: {maya_file}")

        # save file
        cmds.file(save=1)
        log.success(f"File saved: {maya_file}")
        append_pipeline_log(r"C:\Users\Donzy\Desktop\log_success.json", "success", maya_file, "")
    except Exception as e:
        log.error(f"Error processing file: {maya_file}  |  {e!s}")
        append_pipeline_log(r"C:\Users\Donzy\Desktop\log_error.json", "error", maya_file, str(e))
