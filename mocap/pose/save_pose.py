# Author:   Donzy.xu
# CreateTime:   2022/6/30 - 14:06
# FileName:  savePose.py


import json
from maya import cmds
from UTILS.transform import get_trs, set_trs



import ctypes
from ctypes import wintypes

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)

CF_UNICODETEXT = 13  # Windows剪贴板使用Unicode文本格式
GMEM_MOVEABLE = 0x0002  # 定义内存为可移动的
GMEM_ZEROINIT = 0x0040  # 定义内存内容初始化为0

kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
kernel32.GlobalAlloc.restype = wintypes.HGLOBAL

kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalLock.restype = wintypes.LPVOID

kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalUnlock.restype = wintypes.BOOL

kernel32.GlobalSize.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalSize.restype = ctypes.c_size_t

user32.OpenClipboard.argtypes = [wintypes.HWND]
user32.OpenClipboard.restype = wintypes.BOOL

user32.CloseClipboard.argtypes = []
user32.CloseClipboard.restype = wintypes.BOOL

user32.EmptyClipboard.argtypes = []
user32.EmptyClipboard.restype = wintypes.BOOL

user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
user32.SetClipboardData.restype = wintypes.HANDLE

user32.IsClipboardFormatAvailable.argtypes = [wintypes.UINT]
user32.IsClipboardFormatAvailable.restype = wintypes.BOOL

user32.GetClipboardData.argtypes = [wintypes.UINT]
user32.GetClipboardData.restype = wintypes.HANDLE


def get_clipboard_text() -> str:
    """
    使用 Windows API 获取剪贴板中的文本内容。
    """
    text = ""
    if not user32.OpenClipboard(None):
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        if user32.IsClipboardFormatAvailable(CF_UNICODETEXT):
            h_clipboard_data = user32.GetClipboardData(CF_UNICODETEXT)
            if h_clipboard_data:
                p_clipboard_data = kernel32.GlobalLock(h_clipboard_data)
                if p_clipboard_data:
                    try:
                        size = kernel32.GlobalSize(h_clipboard_data)
                        text = ctypes.wstring_at(p_clipboard_data, size // 2 - 1)
                    finally:
                        kernel32.GlobalUnlock(h_clipboard_data)
    finally:
        user32.CloseClipboard()

    return text

def set_clipboard_text(text: str) -> bool:
    """
    使用 Windows API 将文本内容设置到剪贴板中。
    
    Args:
        text (str): 要设置到剪贴板的文本内容
        
    Returns:
        bool: 操作成功返回True，失败返回False
    """
    try:
        if not user32.OpenClipboard(None):
            raise ctypes.WinError(ctypes.get_last_error())
        
        # 清空剪贴板
        if not user32.EmptyClipboard():
            raise ctypes.WinError(ctypes.get_last_error())
        
        # 计算需要的内存大小 (包括null终止符)
        text_bytes = text.encode('utf-16le')
        size = len(text_bytes) + 2  # +2 for null terminator
        
        # 分配全局内存
        h_global = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, size)
        if not h_global:
            raise ctypes.WinError(ctypes.get_last_error())
        
        # 锁定内存并复制数据
        p_global = kernel32.GlobalLock(h_global)
        if not p_global:
            kernel32.GlobalFree(h_global)
            raise ctypes.WinError(ctypes.get_last_error())
        
        try:
            # 复制文本数据到全局内存
            ctypes.memmove(p_global, text_bytes, len(text_bytes))
        finally:
            kernel32.GlobalUnlock(h_global)
        
        # 设置剪贴板数据
        if not user32.SetClipboardData(CF_UNICODETEXT, h_global):
            kernel32.GlobalFree(h_global)
            raise ctypes.WinError(ctypes.get_last_error())
        
        return True
        
    except Exception as e:
        print(f"设置剪贴板失败: {e}")
        return False
    finally:
        user32.CloseClipboard()

def copy_pose_to_clipboard():
    """
    将当前选中物体的Pose数据复制到剪贴板
    """
    selection_list = cmds.ls(sl=1)
    if not selection_list:
        cmds.warning("请先选择要复制Pose的物体")
        return
    
    pose_dataDict = {}
    for obj in selection_list:
        obj_TRS = get_trs(obj)
        pose_dataDict.update({obj: obj_TRS})
    
    # 转换为JSON字符串
    pose_json = json.dumps(pose_dataDict, sort_keys=True, indent=4, separators=(",", ": "))
    
    # 复制到剪贴板
    if set_clipboard_text(pose_json):
        cmds.inViewMessage(amg=f"Pose数据已复制到剪贴板\n{len(selection_list)} 个物体", pos="midCenterBot", fade=True)
        print(f"成功复制 {len(selection_list)} 个物体的Pose数据到剪贴板")
    else:
        cmds.warning("复制Pose数据到剪贴板失败")

def paste_pose_from_clipboard():
    """
    从剪贴板粘贴Pose数据并应用到物体
    """
    try:
        # 从剪贴板获取数据
        clipboard_text = get_clipboard_text()
        if not clipboard_text.strip():
            cmds.warning("剪贴板中没有数据")
            return
        
        # 解析JSON数据
        pose_dataDict = json.loads(clipboard_text)
        
        applied_count = 0
        for obj in pose_dataDict:
            if cmds.objExists(obj):
                try:
                    set_trs(obj, pose_dataDict[obj])
                    applied_count += 1
                except Exception as e:
                    print(f"应用Pose到 {obj} 失败: {e}")
        
        if applied_count > 0:
            cmds.inViewMessage(amg=f"从剪贴板应用Pose数据\n成功: {applied_count} 个物体", pos="midCenterBot", fade=True)
            print(f"成功从剪贴板应用Pose数据到 {applied_count} 个物体")
        else:
            cmds.warning("没有找到匹配的物体来应用Pose数据")
            
    except json.JSONDecodeError:
        cmds.warning("剪贴板中的数据格式不正确")
    except Exception as e:
        cmds.warning(f"从剪贴板粘贴Pose数据失败: {e}")
        
