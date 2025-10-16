"""
初始化 无 UI Maya 独立环境，并加载必要的插件。
"""

from maya import cmds
import maya.standalone

plugin_list = [
    "fbxmaya",
]


def init_maya():
    """
    初始化 Maya 独立环境，并加载必要的插件。
    """
    print("------------------------------")
    print("启动maya环境...")
    maya.standalone.initialize(name="python")
    # 加载 FBX 插件
    for plugin in plugin_list:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            print(f"Loading plugin: {plugin}...")
            try:
                cmds.loadPlugin(plugin)
                print(f"{plugin} loaded successfully.")
            except Exception as e:
                print(f"!!! FAILED to load plugin {plugin}. Error: {e}")
                # 如果插件加载失败，后续操作很可能会失败，可以选择退出
    print("启动maya环境完成")
    print("------------------------------")


if __name__ == "__main__":
    init_maya()