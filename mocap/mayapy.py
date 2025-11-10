"""
初始化 无 UI Maya 独立环境，并加载必要的插件。
"""

import log

import maya.standalone
from maya import cmds


PLUGIN_LIST = [
    "fbxmaya",
]


def init_maya():
    """
    初始化 Maya 独立环境，并加载必要的插件。
    """

    log.info("Initializing Maya standalone environment...")
    maya.standalone.initialize(name="python")
    # 加载 FBX 插件
    for plugin in PLUGIN_LIST:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            log.debug(f"Loading plugin: '{plugin}'...")
            try:
                cmds.loadPlugin(plugin)
                log.debug(f"Load plugin: '{plugin}' successfully")
            except Exception as e:
                log.warning(e)
    log.info("Maya environment initialized successfully.")


if __name__ == "__main__":
    init_maya()
    import time
    s = time.time()
    log.info(f"Done in {time.time()-s}")