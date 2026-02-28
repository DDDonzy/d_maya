import maya.cmds as cmds
from pathlib import Path
import maya.api.OpenMaya as om


root_dir = Path(r"E:\d_maya\z_np")


def reload_all_plugins():
    cmds.file(new=True, force=True)

    def _reload():
        plugin_paths = list(root_dir.glob("*Plugin.py"))

        if not plugin_paths:
            om.MGlobal.displayWarning(f"在 {root_dir} 下未找到任何 *Plugin.py 文件！")
            return

        # 遍历卸载
        print("=================== UNLOAD ===========================")
        for plugin in plugin_paths:
            if cmds.pluginInfo(plugin.name, q=True, loaded=True):
                try:
                    cmds.unloadPlugin(plugin.name)
                    print(f"SUCCESS UNLOAD: {plugin.name}")
                except Exception:
                    om.MGlobal.displayError("FAILED UNLOAD: {plugin.name}")
        print("==================== LOAD ============================")
        # 遍历加载
        for plugin in plugin_paths:
            try:
                cmds.loadPlugin(str(plugin))
                print(f"SUCCESS LOAD: {plugin.name}")
            except Exception as e:
                om.MGlobal.displayError(f"FAILED LOAD: {plugin.name} - {e}")
        print("====================================================")

    cmds.evalDeferred(_reload)


reload_all_plugins()
