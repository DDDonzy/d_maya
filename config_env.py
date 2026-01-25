import re
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
s)
    final_content = []

    if not has_header:
    has_header = any(line.startswith("+") for line in existing_line
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
