import fbx
import sys


def find_fbx_containers_final(file_path):
    # 1. 初始化 Manager
    manager = fbx.FbxManager.Create()
    ios = fbx.FbxIOSettings.Create(manager, fbx.IOSROOT)
    manager.SetIOSettings(ios)

    # 2. 导入场景
    scene = fbx.FbxScene.Create(manager, "MyScene")
    importer = fbx.FbxImporter.Create(manager, "")

    if not importer.Initialize(file_path, -1, manager.GetIOSettings()):
        print(f"Error: {importer.GetStatus().GetErrorString()}")
        return
    importer.Import(scene)
    importer.Destroy()

    container_class_id = manager.FindClass("FbxContainer") or []
    container_criteria = fbx.FbxCriteria.ObjectType(container_class_id)
    container_count = scene.GetSrcObjectCount(container_criteria)
    delete_list = []
    for i in range(container_count):
        obj = scene.GetSrcObject(container_criteria, i)
        delete_list.append(obj)
    for obj in delete_list:
        obj.Destroy()
    exporter = fbx.FbxExporter.Create(manager, "")

    # 初始化导出器 (如果文件已存在，这里会覆盖)
    # 这里的 -1 表示使用默认的文件格式（通常是二进制）
    if not exporter.Initialize("N:\SourceAssets\Characters\Hero\Mocap\Bake\FBX\M_Blade_Stand_Run_F_Loop2.fbx", -1, manager.GetIOSettings()):
        print(f"Export Error: {exporter.GetStatus().GetErrorString()}")
        return

    exporter.Export(scene)
    exporter.Destroy()
    print("Export completed successfully.")


find_fbx_containers_final("N:\SourceAssets\Characters\Hero\Mocap\Bake\FBX\M_Blade_Stand_Run_F_Loop.fbx")
