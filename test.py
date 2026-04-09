import time
import ctypes
import array


# 测试数据量：300万个 float (float32 为 4 字节，总计约 11.44 MB)
COUNT = 3_000_000

def benchmark_memory_copy():
    print(f"开始测试 {COUNT} 个 float32 的内存拷贝性能...\n")



    # --- 4. ctypes.memmove (最接近你 Maya 插件底层的逻辑) ---
    # 直接操作内存地址，跳过所有 Python 对象包装
    # 创建两个连续内存块
    BufferType = ctypes.c_float * COUNT
    src_buffer = BufferType()
    dst_buffer = BufferType()
    
    start = time.perf_counter()
    # 核心：直接从源地址拷贝 N 字节到目标地址
    ctypes.memmove(
        ctypes.addressof(dst_buffer), 
        ctypes.addressof(src_buffer), 
        COUNT * ctypes.sizeof(ctypes.c_float)
    )
    end = time.perf_counter()
    print(f"4. ctypes.memmove (地址偏移): {(end - start) * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark_memory_copy()