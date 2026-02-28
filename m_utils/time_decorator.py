import time
from contextlib import contextmanager

# ==========================================
# ⏱️ 版本一：函数装饰器 (用于测算整个函数的耗时)
# ==========================================
def time_decorator(func):
    """
    函数级性能剖析器 (毫秒级，控制台完美对齐版)
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time_ms = (end_time - start_time) * 1000
        
        # 💥 格式化魔法：
        # prefix:<60  -> 前缀字符串强制左对齐，占据 60 个字符的宽度，不够的用空格补齐
        # >8.3f       -> 浮点数强制右对齐，占据 8 个字符宽度，保留 3 位小数
        prefix = f"[Func: {func.__name__}]"
        print(f"{prefix:=<60} executed in {execution_time_ms:>8.2f} ms.")
        
        return result
    return wrapper

# ==========================================
# ⏱️ 版本二：with 上下文管理器 (用于测算局部代码块的耗时)
# ==========================================
@contextmanager
def time_block(block_name="CodeBlock"):
    """
    代码块级性能剖析器 (毫秒级，控制台完美对齐版)
    """
    start_time = time.perf_counter()
    try:
        yield 
    finally:
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000
        
        # 💥 格式化魔法与上面保持绝对一致
        prefix = f"[Block: {block_name}]"
        print(f"{prefix:-<60} executed in {execution_time_ms:>8.2f} ms.")