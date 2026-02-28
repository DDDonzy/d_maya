import maya.cmds as cmds
import z_np.tool._reload as reload
import z_np.tool._reloadPlugin as reloadPlugin


cmds.file(new=1, force=1)
cmds.setToolTo("selectSuperContext")

if cmds.contextInfo("cBrush", exists=True):
    cmds.deleteUI("cBrush", toolContext=True)

reload.reload_modules_in_path(r"E:\d_maya\z_np\src")
reloadPlugin.reload_all_plugins()


def _test():

    cmds.file(r"C:/Users/Donzy/Desktop/ng_test.ma", o=1, f=1)

    cmds.select("pCube1")
    # 如果上下文还没创建，就创建一个
    if not cmds.contextInfo("cBrush", exists=True):
        cmds.cBrushCtx("cBrush")

    # 把当前鼠标工具切换成我们的笔刷！

    cmds.setToolTo("cBrush")


cmds.evalDeferred(_test)
