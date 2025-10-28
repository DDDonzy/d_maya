"""
================================================================================
suppress_maya_log.py
================================================================================

[ 脚本目的 ]
maya 打开文件时，禁止输出警告和错误信息。
这在批处理脚本中非常有用，可以避免日志被大量无关信息淹没。

[ 工作流程 ]
1.  定义一个上下文管理器 `suppress_maya_logs`，用于临时禁止 Maya 的警告信息输出。
2.  在需要禁止日志输出的代码块中，使用 `with suppress_maya_logs():` 语句包裹。
3.  在代码块执行完毕后，日志输出会自动恢复。

[ 如何使用 ]

with suppress_maya_logs():
    cmds.file("path/to/your/file.ma", o=True, f=True)

================================================================================
"""

import contextlib

from maya import cmds


@contextlib.contextmanager
def suppress_maya_logs(suppressError=True, suppressWarning=True, suppressInfo=True):
    """
    一个上下文管理器，用于临时禁止 Maya 的警告信息输出。
    """
    # 记录当前的警告设置状态
    try:
        # 禁止警告输出
        cmds.scriptEditorInfo(e=True, suppressWarnings=suppressWarning, suppressInfo=suppressInfo, suppressErrors=suppressError)
        yield
    finally:
        # 无论成功还是失败，都恢复原始设置
        cmds.scriptEditorInfo(e=True, suppressWarnings=False, suppressInfo=False, suppressErrors=False)


if __name__ == "__main__":
    # 打开文件
    with suppress_maya_logs():
        cmds.file(r"N:\SourceAssets\Characters\Hero\Mocap\xx\M_Blade_Stand_Run_F_Loop.ma", o=1, f=1)

    print("+++++++++++++++++++++++++++++++++++++")
    print("打开文件完成")
