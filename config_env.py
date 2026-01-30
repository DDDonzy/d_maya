"""
================================================================================
描述:
    此脚本用于自动化配置和同步 Maya 开发项目的运行环境。
    它作为单一事实来源（Single Source of Truth），统一管理项目的 PYTHONPATH，
    并将其分发到 VSCode、Maya 模块配置文件以及环境变量中。

主要功能:
    1. **项目根目录定位 (Project Root Resolution)**:
       - 通过向上递归查找 `.env` 文件来确定项目的根目录。
    
    2. **VSCode 开发环境配置 (VSCode Settings Sync)**:
       - 自动更新 `.vscode/settings.json`。
       - 同步 `python.analysis.extraPaths` 和 `python.autoComplete.extraPaths`。
       - 确保开发时的代码补全、智能感知（IntelliSense）与实际运行环境一致。

    3. **Maya 模块文件生成 (Maya Module Generation)**:
       - 生成或更新 `_maya_config/modules/d_maya.mod`。
       - 配置 Maya 的模块定义及 PYTHONPATH 环境变量。
       - 支持增量更新，保留非 PYTHONPATH 的自定义配置。

    4. **环境文件同步 (.env Synchronization)**:
       - 确保根目录下的 `.env` 文件包含最新的 PYTHONPATH 定义。

使用方法:
    直接运行此脚本即可应用配置：
    $ python config_env.py
================================================================================
"""
import json
from pathlib import Path

MODULE_NAME = "D_MAYA"
VERSION = "1.0"
PYTHONPATH = [
    "./",
    "./_oldTools",
    "./_maya_config/scripts",
    "./_maya_config/hotkeys",
]


def get_project_root() -> Path:
    """
    向上查找包含 .env 文件的目录作为根目录。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists():
            return parent


def update_vscode_settings(root: Path, paths: list):
    """将解析出的路径同步到 .vscode/settings.json"""

    settings_file = root / ".vscode" / "settings.json"

    vscode_env_paths = []
    pylance_paths = []

    for p in paths:
        clean_p = p.replace("\\", "/").lstrip("./").lstrip("/")
        if not clean_p or clean_p == ".":
            vscode_env_paths.append("${workspaceFolder}")
            pylance_paths.append("./")
        else:
            vscode_env_paths.append(f"${{workspaceFolder}}/{clean_p}")
            pylance_paths.append(f"./{clean_p}")

    settings = {}
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text(encoding="utf-8"))
        except Exception:
            settings = {}

    def get_combined_list(key, new_list):
        old_list = settings.get(key, [])
        if not isinstance(old_list, list):
            old_list = []
        return list(dict.fromkeys(old_list + new_list))

    settings["python.analysis.extraPaths"] = get_combined_list("python.analysis.extraPaths", pylance_paths)

    settings["python.autoComplete.extraPaths"] = get_combined_list("python.autoComplete.extraPaths", pylance_paths)

    settings["python.terminal.useEnvFile"] = True

    settings_file.parent.mkdir(exist_ok=True)
    settings_file.write_text(json.dumps(settings, indent=4, ensure_ascii=False), encoding="utf-8")
    print("Updated VSCode settings at:", settings_file)


def update_maya_modules(root: Path, paths: list):
    """
    增量更新 Maya .mod 文件，保留原有配置且不重复添加路径
    """
    module_file = root / "_maya_config" / "modules" / f"{MODULE_NAME.lower()}.mod"

    module_file.parent.mkdir(parents=True, exist_ok=True)

    existing_lines = []
    old_paths = []

    if module_file.exists():
        content = module_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if "PYTHONPATH" in line:
                continue
            elif line:
                existing_lines.append(line)

    new_clean_paths = []
    for p in paths:
        clean_p = p.replace("\\", "/").lstrip("./").lstrip("/")
        new_clean_paths.append(f"./{clean_p}" if clean_p and clean_p != "." else "./")

    combined_paths = list(dict.fromkeys(old_paths + new_clean_paths))

    has_header = any(line.startswith("+") for line in existing_lines)
    final_content = []

    if not has_header:
        final_content.append(f"+ {MODULE_NAME} {VERSION} ./")

    final_content.extend(existing_lines)

    for p in combined_paths:
        final_content.append(f"PYTHONPATH +:= {p}")

    module_file.write_text("\n".join(final_content), encoding="utf-8")
    print("Updated Maya module file at:", module_file)


def sync_env_file():
    """
    确保根目录下存在 .env 文件
    """
    root = get_project_root()
    env_path = root / ".env"

    env_content = f"PYTHONPATH={';'.join(PYTHONPATH)}"
    env_path.write_text(env_content, encoding="utf-8")

    update_vscode_settings(root, PYTHONPATH)
    update_maya_modules(root, PYTHONPATH)


if __name__ == "__main__":
    sync_env_file()
