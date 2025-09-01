import fbx as FBX

import json
from pathlib import Path
from contextlib import contextmanager


manager = FBX.FbxManager.Create()  # 创建管理器


@contextmanager
def new_scene(scene):
    """场景处理器，确保处理后清理"""
    scene = FBX.FbxScene.Create(manager, "")
    print("INFO: New scene created.")
    try:
        yield scene
    except Exception as e:
        print(f"ERROR in scene operation: {e}")
        raise
    finally:
        scene.Destroy()
        print("INFO: Scene destroyed.")


def fbx_importer(manager, scene, *args):
    """导入器上下文管理器"""
    importer = FBX.FbxImporter.Create(manager, "")

    # 检查初始化是否成功
    if not importer.Initialize(*args):
        error_string = importer.GetStatus().GetErrorString()
        importer.Destroy()
        raise RuntimeError(f"FBX导入器初始化失败: {error_string}")

    print("INFO: 开始导入 FBX 文件...")

    # 检查导入是否成功
    if not importer.Import(scene):
        error_string = importer.GetStatus().GetErrorString()
        importer.Destroy()
        raise RuntimeError(f"FBX导入失败: {error_string}")

    print("INFO: FBX 文件导入成功")
    importer.Destroy()


def fbx_exporter(manager, scene, *args):
    """导出器上下文管理器"""
    exporter = FBX.FbxExporter.Create(manager, "")

    # 检查初始化是否成功
    if not exporter.Initialize(*args):
        error_string = exporter.GetStatus().GetErrorString()
        exporter.Destroy()
        raise RuntimeError(f"FBX导出器初始化失败: {error_string}")

    print(f"INFO: 开始导出 FBX 文件到: {args[0]}")

    # 检查导出是否成功
    if not exporter.Export(scene):
        error_string = exporter.GetStatus().GetErrorString()
        exporter.Destroy()
        raise RuntimeError(f"FBX导出失败: {error_string}")

    print(f"INFO: FBX 文件导出成功: {args[0]}")
    exporter.Destroy()


def iter_scene_nodes(node):
    """
    一个生成器函数，用于递归地遍历并 yield 场景中的所有节点。
    它采用“先序遍历”（Pre-order traversal），即先返回父节点，再遍历其子节点。
    """
    yield node

    for i in range(node.GetChildCount()):
        child_node = node.GetChild(i)
        yield from iter_scene_nodes(child_node)


def get_fbx(directory_path_str: str):
    directory_path = Path(directory_path_str)

    if not directory_path.is_dir():
        raise ValueError(f"Can not find directory: '{directory_path}")

    fbx_files = list(directory_path.glob("*.fbx"))
    if not fbx_files:
        raise ValueError(f"Can not find '*.fbx' files in '{directory_path}'")

    return fbx_files


def get_type_from_maya_fbx(node) -> str:
    """
    根据Maya到FBX的映射规则，判断节点的原始类型。
    """
    node_attribute = node.GetNodeAttribute()
    if not node_attribute:
        # Maya中的空组 (empty group) 会被导出为没有属性的节点
        # 或者带有 FbxNull 属性的节点
        return "Group"

    attribute_type = node_attribute.GetAttributeType()

    # --- 核心判断逻辑 ---
    if attribute_type == FBX.FbxNodeAttribute.EType.eSkeleton:
        return "Joint"
    
    elif attribute_type == FBX.FbxNodeAttribute.EType.eMarker:
        return "Locator"
    # --- 核心判断逻辑结束 ---
        
    elif attribute_type == FBX.FbxNodeAttribute.EType.eMesh:
        return "Mesh"
        
    elif attribute_type == FBX.FbxNodeAttribute.EType.eCamera:
        return "Camera"
        
    elif attribute_type == FBX.FbxNodeAttribute.EType.eLight:
        return "Light"

    elif attribute_type == FBX.FbxNodeAttribute.EType.eNull:
        return "Group / Null"

    else:
        return "Other Type"



if __name__ == "__main__":
    name_json_path = r"E:\d_maya\motive_skeleton_name.json"
    with open(name_json_path, "r") as f:
        name_dict = json.load(f)

    reverse_dict = {v: k for k, v in name_dict.items()}

    input_folder = r"N:\SourceAssets\Characters\Hero\Mocap\20250830\mocap_source"
    output_folder = r"N:\SourceAssets\Characters\Hero\Mocap\20250830\mocap_source"
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)  # 直接创建，如果存在就跳过

    for fbx in get_fbx(input_folder):
        file_name = fbx.stem
        export_file = Path(output_folder) / f"{file_name}.fbx"

        with new_scene(fbx) as scene:
            fbx_importer(manager, scene, str(fbx), -1, manager.GetIOSettings())
            # rename
            for node in iter_scene_nodes(scene.GetRootNode()):
                node_name = node.GetName()
                node_name = node_name.replace("hero_", "")  # remove prefix
                if node_name in reverse_dict:
                    new_node_name = reverse_dict[node_name]
                    node.SetName(new_node_name)
                    print(f"RENAME: {node_name} -> {new_node_name}")
            fbx_exporter(manager, scene, str(export_file), -1, manager.GetIOSettings())
        break


