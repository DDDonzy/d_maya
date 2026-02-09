import os

def batch_rename_files(folder_path, search_str, replace_str):
    """
    批量重命名文件夹内的文件。
    
    :param folder_path: 文件夹路径
    :param search_str: 需要被替换的字符串
    :param replace_str: 替换后的新字符串
    """
    # 检查路径是否存在
    if not os.path.exists(folder_path):
        print(f"错误：路径 '{folder_path}' 不存在。")
        return

    count = 0
    # 遍历文件夹
    for filename in os.listdir(folder_path):
        # 检查文件名中是否包含目标字符串
        if search_str in filename:
            # 构建旧文件的完整路径
            old_file_path = os.path.join(folder_path, filename)
            
            # 跳过文件夹，只处理文件
            if os.path.isdir(old_file_path):
                continue
                
            # 生成新文件名
            new_filename = filename.replace(search_str, replace_str)
            new_file_path = os.path.join(folder_path, new_filename)

            # 执行重命名
            try:
                os.rename(old_file_path, new_file_path)
                print(f"成功: '{filename}' -> '{new_filename}'")
                count += 1
            except Exception as e:
                print(f"重命名 '{filename}' 失败: {e}")

    print(f"\n任务完成！共重命名了 {count} 个文件。")

# --- 使用示例 ---
folder = r"N:\SourceAssets\Characters\Hero\Mocap\Xsens\FBX"
batch_rename_files(folder, "Run_F_0", "Run_F_Rfoot_0")