import sys
from pathlib import Path

from maya import cmds

this_python_file_path = Path(__file__)
project_path = this_python_file_path.parent.parent
module = this_python_file_path.parent / "modules" / "d_maya.mod"

sys.path.append(str(project_path))

import log  # noqa: E402


def install_module():
    app_dir = cmds.internalVar(userAppDir=True)
    target_module = Path(app_dir) / "modules" / "d_maya.mod"
    if module.exists():
        lines = module.read_text(encoding="utf-8").splitlines()
        if lines:
            first_line_parts = lines[0].split()
            if len(first_line_parts) >= 3:
                new_first_line = f"{first_line_parts[0]} {first_line_parts[1]} {first_line_parts[2]} {project_path.as_posix()}"
                lines[0] = new_first_line
                target_module.parent.mkdir(parents=True, exist_ok=True)
                target_module.write_text("\n".join(lines), encoding="utf-8")
                log.success(f'Modules path: "{target_module}"')
                log.success("Installation complete.")
            else:
                log.error(f"'{module}' file's first line does not have enough parts.")
    else:
        log.error("Installation failed, original .mod file not found.")


def install_hotkeys():
    import _maya_config.hotkeys.d_hotkeys

    _maya_config.hotkeys.d_hotkeys.install_hotkey()
    log.success("Hotkeys installation complete.")


def install_package():
    from _maya_config.pythonPackage.installPackage import install_package

    install_package()


def onMayaDroppedPythonFile(*args, **kwargs):
    install_package()
    install_module()
    install_hotkeys()
