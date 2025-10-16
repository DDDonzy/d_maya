from pathlib import Path
from maya import cmds

from mocap.suppress_maya_logs import suppress_maya_logs


def list_all_references():
    """
    遍历当前 Maya 场景，列出所有的引用信息。

    Returns:
        list[dict]: 一个包含字典的列表，每个字典代表一个引用，
                    包含 'node' (节点名), 'path' (文件路径), 和 'loaded' (是否加载)
                    三个键。
                    例如:
                    [
                        {'node': 'RIGRN', 'path': 'C:/path/to/rig.ma', 'loaded': True},
                        ...
                    ]
    """
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
    """
    根据给定的文件路径，查找场景中对应的引用节点。

    Args:
        path (str): 要查找的引用文件路径。

    Returns:
        list[str]: 一个包含所有匹配该路径的引用节点名称的列表。
                   如果找不到，则返回空列表。
    """
    reference_data = list_all_references()
    reference = []
    for ref in reference_data:
        if Path(ref["path"]) == Path(path):
            reference.append(ref["node"])
    return reference


def get_path_by_reference(reference_node):
    """
    根据给定的引用节点名称，查找其对应的文件路径。

    Args:
        reference_node (str): 要查询的引用节点的名称。

    Returns:
        str | None: 如果找到，返回对应的文件路径字符串；否则返回 None。
    """
    reference_data = list_all_references()
    for ref in reference_data:
        if ref["node"] == reference_node:
            return ref["path"]
    return None


def repath_reference(reference_node, new_path):
    """
    修改指定引用节点的文件路径。

    Args:
        reference_node (str): 要修改路径的引用节点的名称。
        new_path (str): 新的文件路径。

    Returns:
        bool: 如果路径修改成功，返回 True；否则返回 False。
    """
    if not cmds.objExists(reference_node):
        raise
    reference_data = list_all_references()
    for ref in reference_data:
        if ref["node"] != reference_node:
            continue

        old_path = ref["path"]
        with suppress_maya_logs():
            cmds.file(new_path, loadReference=reference_node)
        print(f"Repath Reference Success: {old_path} -> {new_path}")
