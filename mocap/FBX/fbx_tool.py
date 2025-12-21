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


def get_fbx(directory_path_str: str):
    """
    获取指定目录下的所有FBX文件
    """
    directory_path = Path(directory_path_str)

    if not directory_path.is_dir():
        raise ValueError(f"Can not find directory: '{directory_path}")

    fbx_files = list(directory_path.glob("*.fbx"))
    if not fbx_files:
        raise ValueError(f"Can not find '*.fbx' files in '{directory_path}'")

    return fbx_files

def remove_fbx_containers(scene):
    """
    移除场景中的所有 FbxContainer 对象
    """
    container_class_id = manager.FindClass("FbxContainer") or []
    container_criteria = FBX.FbxCriteria.ObjectType(container_class_id)
    container_count = scene.GetSrcObjectCount(container_criteria)
    delete_list = []
    for i in range(container_count):
        obj = scene.GetSrcObject(container_criteria, i)
        delete_list.append(obj)
    for obj in delete_list:
        obj.Destroy()

if __name__ == "__main__":
    """
    测试脚本
    功能：
    1. 批量导入指定文件夹下的FBX文件
    2. 遍历场景节点，打印节点名称及其类型
    3. 重命名节点（如果在映射表中找到对应名称）
    4. 导出处理后的FBX文件到指定输出文件夹
    """
    # 读取名称映射表
    name_json_path = Path(__file__).parent / "motive_remap_ue.json"
    with open(name_json_path, "r") as f:
        name_dict = json.load(f)

    reverse_dict = {v: k for k, v in name_dict.items()}  # 反转字典以便查找

    input_folder = r"N:\SourceAssets\Characters\Hero\Mocap\Bake"  # 输入文件夹
    output_folder = r"N:\SourceAssets\Characters\Hero\Mocap\Bake"  # 输出文件夹

    output_folder = Path(output_folder)  # 转换为 Path 对象
    output_folder.mkdir(parents=True, exist_ok=True)  # 直接创建，如果存在就跳过

    for fbx in get_fbx(input_folder):
        file_name = fbx.stem  # 获取文件名（不含扩展名）
        export_file = Path(output_folder) / f"{file_name}.fbx"  # 输出文件路径

        with new_scene(fbx) as scene:  # 创建新场景
            fbx_importer(manager, scene, str(fbx), -1, manager.GetIOSettings())  # 导入FBX
            # rename
            for node in iter_scene_nodes(scene.GetRootNode()):  # 遍历所有节点
                node_name = node.GetName()  # 获取节点名称
                node_name = node_name.replace("hero_", "")  # 去掉前缀
                if node_name in reverse_dict:  # 如果在映射表中找到对应名称
                    new_node_name = reverse_dict[node_name]  # 获取新名称
                    node.SetName(new_node_name)  # 重命名节点
                    print(f"RENAME: {node_name} -> {new_node_name}")
                remove_fbx_containers(scene)  # 移除 FbxContainer 对象
            fbx_exporter(manager, scene, str(export_file), -1, manager.GetIOSettings())  # 导出FBX
        # break  # 只处理一个文件，测试用, 删除这行以处理所有文件
