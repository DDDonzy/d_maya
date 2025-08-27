logs = [
    "FlipCopy: head_lod0_mesh__Mstretch_MlowerLipDepress_MupperLipRaise_Jopen_L >>> head_lod0_mesh__Mstretch_MlowerLipDepress_MupperLipRaise_Jopen_R",
    "Mirror:   head_lod0_mesh__jaw_right",
    "FlipCopy: head_lod0_mesh__MlowerLipDepress_JopenExtreme_R >>> head_lod0_mesh__MlowerLipDepress_JopenExtreme_L",
    "FlipCopy: head_lod0_mesh__eye_widen_R--- >>> head_lod0_mesh__eye_widen_L",
    "Mirror:   head_lod0_mesh__Mfunnel_MupperLipRaise_UL",
    "Mirror:   head_lod0_mesh__Mfunnel_Mtighten_DR",
    "FlipCopy: head_lod0_mesh__McornerPull_MlowerLipDepress_Jopen_L >>> head_lod0_mesh__McornerPull_MlowerLipDepress_Jopen_R",
    "FlipCopy: head_lod0_mesh__McornerPull_Mstretch_JopenExtreme_R >>> head_lod0_mesh__McornerPull_Mstretch_JopenExtreme_L",
    "FlipCopy: head_lod0_mesh__McornerPull_MlowerLipDepress_MupperLipRaise_Jopen_L >>> head_lod0_mesh__McornerPull_MlowerLipDepress_MupperLipRaise_Jopen_R",
    "Mirror:   head_lod0_mesh__Mfunnel_Mtighten_DL",
]

# 1. 解析数据
parsed_logs = []
max_source_name_length = 0

for line in logs:
    log_type, content = line.split(':', 1)
    content = content.strip()
    
    if ">>>" in content:
        source_name, target_name = content.split('>>>', 1)
        source_name = source_name.strip()
        target_name = target_name.strip()
        parsed_logs.append({
            "type": log_type + ":",
            "source": source_name,
            "target": target_name
        })
        # 2. 计算源名称的最大宽度
        if len(source_name) > max_source_name_length:
            max_source_name_length = len(source_name)
    else:
        # Mirror 类型的处理
        source_name = content
        parsed_logs.append({
            "type": log_type + ":",
            "source": source_name,
            "target": None
        })
        # 同样需要计算宽度
        if len(source_name) > max_source_name_length:
            max_source_name_length = len(source_name)

# 3. 格式化输出
print("--- Formatted Log Output ---")
for log in parsed_logs:
    # 使用 f-string 进行格式化
    # {log['type']:<10} 表示左对齐，宽度为 10
    # {log['source']:{max_source_name_length}} 表示使用计算出的最大宽度进行对齐
    
    log_type_formatted = f"{log['type']:<10}" # 固定类型列的宽度为10，左对齐
    source_formatted = f"{log['source']:<{max_source_name_length}}" # 使用最大宽度对齐源名称，左对齐

    if log['target']:
        # 是 FlipCopy 类型
        print(f"{log_type_formatted} {source_formatted} >>> {log['target']}")
    else:
        # 是 Mirror 类型
        print(f"{log_type_formatted} {source_formatted}")