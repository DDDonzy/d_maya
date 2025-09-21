import maya.standalone
from maya import cmds

from pathlib import Path


def info(title: str, total_length: int = 200) -> None:
    formatted_title = f"{f' {title} ':=^{total_length}}"
    print(formatted_title)


def debug(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ DEBUG ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


def error(label: str, total_length: int = 20, fill_char: str = " ") -> None:
    formatted_line = f"{f'[ ERROR ]: {label} ':{fill_char}<{total_length}}"
    print(formatted_line)


def list_all_references():
    reference_nodes = cmds.ls(type="reference")
    references_info = []
    for ref_node in reference_nodes:
        try:
            file_path = cmds.referenceQuery(ref_node, filename=True)
            is_loaded = cmds.referenceQuery(ref_node, isLoaded=True)
            references_info.append({"node": ref_node, "path": file_path, "loaded": is_loaded})
        except Exception:
            continue

    return references_info


def get_reference_by_path(path):
    reference_data = list_all_references()
    reference = []
    for ref in reference_data:
        if Path(ref["path"]) == Path(path):
            reference.append(ref["node"])
    return reference


def get_path_by_reference(reference_node):
    reference_data = list_all_references()
    for ref in reference_data:
        if ref["node"] == reference_node:
            return ref["path"]
    return None


def repath_reference(reference_node, new_path):
    if not cmds.objExists(reference_node):
        raise
    reference_data = list_all_references()
    for ref in reference_data:
        if ref["node"] != reference_node:
            continue

        old_path = ref["path"]
        try:
            cmds.file(new_path, loadReference=reference_node)
            debug(f"Repath Success: {old_path} -> {new_path}")
            return True
        except Exception as e:
            error(f"Repath Failed: {old_path} -> {new_path} | Error: {e}")
            return False


if __name__ == "__main__":
    task_file = list(Path(r"N:\SourceAssets\Characters\Hero\Mocap").glob("*.ma"))
    output_dir = Path(r"N:\SourceAssets\Characters\Hero\Mocap")

    rig_file = r"N:\SourceAssets\Characters\Hero\Rigs\RIG_TestCharacter.ma"
    rig_ref_node = "RIGRN"

    maya.standalone.initialize(name="python")
    info("Maya Standalone Initialized")

    success_list = []
    for maya_file in task_file:
        file_name = maya_file.name

        info(f"Process : {maya_file}")
        try:
            # Open File
            debug(f"Open File: {file_name}")
            try:
                cmds.file(maya_file, open=1, force=1, loadNoReferences=True)
            except RuntimeError:
                pass
            debug(f"File Opened: {file_name}")

            repath_reference(rig_ref_node, rig_file)

            debug(f"Repath Reference: {rig_ref_node} -> {rig_file}")

            cmds.file(rename=str(output_dir / file_name))
            cmds.file(save=True, force=True, type="mayaAscii")

        except Exception:
            continue
