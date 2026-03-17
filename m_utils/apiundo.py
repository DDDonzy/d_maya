# -*- coding: utf-8 -*-
"""
======================================================================================
Module: apiundo.py
======================================================================================
为 Maya OpenMaya (OM2) API 提供了通用撤销/重做（Undo/Redo）桥接。
在内存中构建安全的指令队列（Command Buffer），使任意无状态的 Python 闭包函数，
都能安全、有序地接入 Maya 原生的 C++ 历史撤销栈。

Features:
  - 对外仅暴露 `commit` 唯一接口
  - 自带 `execute` 开关，兼容 `立刻执行` 与 `提交但不执行` 双模式。
  - 单文件导入即用，自动完成 Maya Plugin 的静默注册与跨域共享。

Reference:
  - Marcus Ottosson (GitHub: mottosso)开源项目 `apiundo`.

======================================================================================
"""

import sys
import types
from maya import cmds
from maya.api import OpenMaya as om

__all__ = [
    "commit",
]

__version__ = "1.0.0"
COMMAND_NAME = f"OpenMayaUndo_{__version__.replace('.', '_')}"


SHARED_MODULE_NAME = "_OpenMayaUndoShared"
if SHARED_MODULE_NAME not in sys.modules:
    sys.modules[SHARED_MODULE_NAME] = types.ModuleType(SHARED_MODULE_NAME)

buffer_space = sys.modules[SHARED_MODULE_NAME]


if not hasattr(buffer_space, "command_buffer"):
    buffer_space.command_buffer = []


def commit(redo_func, undo_func, execute=True):
    """
    将撤销/重做动作注册进 Maya 的 Undo 栈。

    Args:
        redo_func (callable): 重做动作
        undo_func (callable): 撤销动作
        execute (bool):
            - True (默认): 注册的同时立刻触发一次 redo_func()。适用于 UI 按钮触发的操作。
            - False: 仅做静默注册，不触发 redo_func()。适用于画刷等已经实时修改过内存的交互工具。
    """

    if not hasattr(cmds, COMMAND_NAME):
        _install()

    buffer_space.command_buffer.append({
        "undo": undo_func,
        "redo": redo_func,
        "execute": execute,
    })

    getattr(cmds, COMMAND_NAME)()


class OpenMayaUndoCmd(om.MPxCommand):
    def __init__(self):
        super(OpenMayaUndoCmd, self).__init__()
        self.undo_action = None
        self.redo_action = None

    def doIt(self, args):
        if not buffer_space.command_buffer:
            return

        task = buffer_space.command_buffer.pop(0)
        self.undo_action = task.get("undo")
        self.redo_action = task.get("redo")

        if task.get("execute", True):
            self.redoIt()

    def undoIt(self):
        if self.undo_action:
            self.undo_action()

    def redoIt(self):
        if self.redo_action:
            self.redo_action()

    def isUndoable(self):
        return True

    @classmethod
    def creator(cls):
        return OpenMayaUndoCmd()


def _install():
    plugin_path = __file__.replace(".pyc", ".py")
    cmds.loadPlugin(plugin_path, quiet=True)


def maya_useNewAPI():
    pass


def initializePlugin(plugin):
    om.MFnPlugin(plugin).registerCommand(COMMAND_NAME, OpenMayaUndoCmd.creator)


def uninitializePlugin(plugin):
    om.MFnPlugin(plugin).deregisterCommand(COMMAND_NAME)
