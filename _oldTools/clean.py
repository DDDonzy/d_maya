import os
import re

import time
import sys


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"TIME: [{func.__name__}] executed in {execution_time:.6f} seconds.")
        return result

    return wrapper


@time_decorator
def clean_maya_advanced_inplace(input_file):
    """
    清理 .ma 文件中的 scriptNode 和 expression。
    如果有修改：备份原文件为 .ma_bake，保存修改到原文件名。
    如果没有修改：保持现状。
    """
    if not os.path.exists(input_file):
        print(f"错误: 找不到文件 {input_file}")
        return

    temp_file = input_file + ".tmp"
    bake_file = input_file + "_bake"

    # 匹配 scriptNode 和 expression
    target_pattern = re.compile(r'^createNode\s+"?(script|expression)"?')

    modified = False
    removed_nodes = []

    try:
        with open(input_file, "r", encoding="latin-1") as f_in:
            with open(temp_file, "w", encoding="latin-1") as f_out:
                is_skipping = False

                for line in f_in:
                    # 只有行首非空格的才是顶级命令开始
                    if not line.startswith((" ", "\t")):
                        if target_pattern.match(line):
                            is_skipping = True
                            modified = True
                            removed_nodes.append(line.strip())
                            continue
                        else:
                            is_skipping = False

                    if not is_skipping:
                        f_out.write(line)

        # 处理完成后判断是否发生了修改
        if modified:
            # 1. 如果旧备份存在，先删除旧备份（可选，根据需求决定）
            if os.path.exists(bake_file):
                os.remove(bake_file)

            # 2. 将原始文件重命名为备份文件
            os.rename(input_file, bake_file)
            # 3. 将临时处理后的文件重命名为原文件名
            os.rename(temp_file, input_file)

            print(f"已清理: {os.path.basename(input_file)}")
            print(f"  - 移除节点数: {len(removed_nodes)}")
            for node in removed_nodes:
                print(f"    - {node}")

            print(f"  - 原始文件已备份至: {os.path.basename(bake_file)}")
        else:
            # 如果没改动，删除临时文件，保持原文件不动
            if os.path.exists(temp_file):
                os.remove(temp_file)
            print(f"无需修改: {os.path.basename(input_file)}")

    except Exception as e:
        print(f"处理过程中出错: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    files = sys.argv[1:]

    if not files:
        print("提示: 请将一个或多个 .ma 文件拖拽到 .bat 文件上。")
    else:
        for f in files:
            # 简单判断一下后缀，防止误处理
            if f.lower().endswith(".ma"):
                clean_maya_advanced_inplace(f)
            else:
                print(f"跳过非 .ma 文件: {f}")
