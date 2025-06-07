# z_bs/_tools/reloader.py
import sys
import importlib
from loguru import logger
import maya.cmds as cmds

# (maya_sink 函数和 logger 的配置部分保持不变)
def maya_sink(message):
    record = message.record
    level_name = record["level"].name
    formatted_message = message.strip()
    if level_name == "ERROR" or level_name == "CRITICAL":
        cmds.error(formatted_message)
    elif level_name == "WARNING":
        cmds.warning(formatted_message)
    else:
        print(formatted_message)

logger.remove()
logger.add(
    maya_sink,
    level="INFO",
    format="{level: <8} | {name}:{function}:{line} - {message}",
    colorize=False 
)
# (以上部分无需改动)


def reload_project(project_prefix: str):
    """
    使用loguru和自定义的maya_sink查找并重载模块，同时会跳过.qrc文件。
    """
    if not isinstance(project_prefix, str) or not project_prefix:
        logger.error("必须为 project_prefix 提供一个有效的字符串。")
        return

    logger.info(f"--- 开始重载所有 '{project_prefix}' 相关模块 ---")

    # ----- 核心改动在这里 -----
    # 在筛选条件中，增加一项：排除以 '.qrc' 结尾的模块
    modules_to_reload = [
        name for name in sys.modules
        if name.startswith(project_prefix) and not name.endswith('.qrc')
    ]
    # --------------------------

    # (可选) 明确地告诉用户我们跳过了哪些文件，提升用户体验
    qrc_modules_skipped = [
        name for name in sys.modules
        if name.startswith(project_prefix) and name.endswith('.qrc')
    ]
    for name in qrc_modules_skipped:
        logger.info(f"已跳过重载资源文件: {name}")


    if not modules_to_reload:
        logger.warning(f"未找到任何以 '{project_prefix}' 开头的可重载模块。")
        return

    # (函数的其余部分代码保持不变)
    modules_to_reload.sort(key=lambda name: name.count('.'), reverse=True)
    reloaded_count = 0
    failed_count = 0
    for module_name in modules_to_reload:
        try:
            module_obj = sys.modules[module_name]
            importlib.reload(module_obj)
            logger.success(f"成功重载: {module_name}")
            reloaded_count += 1
        except Exception:
            logger.exception(f"重载模块失败: {module_name}")
            failed_count += 1
    logger.info("--- 重载完成 ---")
    logger.info(f"总结: 成功 {reloaded_count} 个, 失败 {failed_count} 个。")
reload_project("z_bs")