from pathlib import Path
import ctypes
from ctypes import wintypes
from maya import cmds


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


def convert_dir(path: str) -> Path:
    """
    将路径转换为 Maya 可识别的格式。
    """
    source_dir = Path(path)
    name = source_dir.stem
    print(source_dir)
    target_dir = source_dir.parent.parent / r"data" / name
    print(target_dir)
    fbx_files = list(target_dir.glob("*.fbx"))
    print(fbx_files)
    for fbx_file in fbx_files:
        if "skeleton" in str(fbx_file):
            return Path(fbx_file)


def openFbxWithFileDialog():
    """
    使用标准文件对话框来获取FBX文件路径并导入。
    """
    cmds.file(new=True, force=True)
    cmds.currentUnit(time="ntscf")

    file_filter = "FBX (*.fbx)"

    clipboard_path = get_clipboard_text()
    clipboard_path = clipboard_path[1:-1]
    fbx_path = convert_dir(clipboard_path)
    result = cmds.fileDialog2(
        fileFilter=file_filter,
        dialogStyle=2,
        fileMode=1,
        caption="Select FBX Clip to Import",
        startingDirectory=fbx_path,
    )

    if result:
        fbx_path = result[0]
        print(f"File selected: {fbx_path}")

        try:
            cmds.file(fbx_path,type="FBX", ignoreVersion=True, namespace="MOCAP", r=1)
            print("FBX file imported successfully.")
        except Exception as e:
            cmds.warning(f"Failed to import FBX file: {e}")
    else:
        print("File selection was cancelled.")


openFbxWithFileDialog()
