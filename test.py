import shutil
from pathlib import Path

def sync_mocap_files():
    # 1. 定义路径
    path_a = Path(r"N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260329\FBX")
    path_b = Path(r"N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260329\MVN")
    path_c = Path(r"N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260329")

    # 确保目标文件夹 C 存在
    path_c.mkdir(parents=True, exist_ok=True)

    print(f"正在扫描文件夹 B: {path_b}...")

    # 2. 遍历 B 文件夹
    count = 0
    for file_b in path_b.iterdir():
        # 检查是否为文件且没有后缀
        if file_b.is_file() and file_b.suffix == "":
            file_name = file_b.name
            target_fbx = path_a / f"{file_name}.FBX"

            # 3. 在 A 路径下寻找对应的 .FBX
            if target_fbx.exists():
                dest_path = path_c / target_fbx.name
                
                try:
                    shutil.copy2(target_fbx, dest_path)
                    print(f"[成功] 已复制: {target_fbx.name}")
                    count += 1
                except Exception as e:
                    print(f"[错误] 复制失败 {target_fbx.name}: {e}")
            else:
                print(f"[缺失] A 文件夹中找不到: {target_fbx.name}")

    print(f"\n任务完成！共复制了 {count} 个文件到 {path_c}")

if __name__ == "__main__":
    sync_mocap_files()