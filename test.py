import os
import shutil

# 定义路径
mvn_dir = r'N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260419\MVN'
base_dir = r'N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260419\FBX\base'
target_dir = r'N:\SourceAssets\Characters\Hero\Mocap\Xsens\20260419\FBX'

def sync_fbx_files():
    # 1. 获取 MVN 目录下没有后缀的文件名
    print("正在扫描 MVN 目录...")
    missing_ext_files = []
    for f in os.listdir(mvn_dir):
        # 拼接完整路径以判断是否为文件
        full_path = os.path.join(mvn_dir, f)
        if os.path.isfile(full_path) and '.' not in f:
            missing_ext_files.append(f)
    
    if not missing_ext_files:
        print("未在 MVN 目录中找到无后缀的文件。")
        return

    print(f"找到 {len(missing_ext_files)} 个无后缀文件。开始匹配并复制...")

    # 2. 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 3. 寻找对应的 FBX 并复制
    copied_count = 0
    for file_name in missing_ext_files:
        # 构建 base 目录下的源文件路径 (文件名 + .fbx)
        source_fbx = os.path.join(base_dir, file_name + '.fbx')
        # 构建目标路径
        destination_fbx = os.path.join(target_dir, file_name + '.fbx')

        if os.path.exists(source_fbx):
            try:
                shutil.copy2(source_fbx, destination_fbx)
                print(f"已成功复制: {file_name}.fbx")
                copied_count += 1
            except Exception as e:
                print(f"复制 {file_name}.fbx 时出错: {e}")
        else:
            print(f"跳过: 在 base 目录中未找到 {file_name}.fbx")

    print(f"\n任务完成！共计复制 {copied_count} 个文件到 {target_dir}")

if __name__ == "__main__":
    sync_fbx_files()