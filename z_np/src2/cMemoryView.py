import ctypes
import array


class CMemoryManager:
    _CTYPES_MAP = {
        "d": ctypes.c_double,
        "f": ctypes.c_float,
        "i": ctypes.c_int32,
        "I": ctypes.c_uint32,
        "b": ctypes.c_int8,
        "B": ctypes.c_uint8,
    }

    def __init__(self):
        self._cache = None
        self.view = None
        self.ptr_addr = 0
        self.format_char = ""
        self.shape = ()

    @staticmethod
    def allocate(format_char: str, shape: tuple):
        """
        主动向系统申请 C 连续内存，返回管理器实例。
        用法: mem = CMemoryManager.allocate("f", (100, 4))
        """
        instance = CMemoryManager()

        if format_char not in CMemoryManager._CTYPES_MAP:
            raise ValueError(f"Unsupported format character: {format_char}")

        total_elements = 1
        for dim in shape:
            total_elements *= dim

        if total_elements <= 0:
            return instance

        # 1. 申请物理内存并存入 cache 防 GC
        ctype_base = CMemoryManager._CTYPES_MAP[format_char]
        instance._cache = (ctype_base * total_elements)()

        # 2. 记录基础信息
        instance.ptr_addr = ctypes.addressof(instance._cache)
        instance.format_char = format_char
        instance.shape = shape

        # 3. 生成零拷贝视图
        instance.view = memoryview(instance._cache).cast("B").cast(format_char, shape=shape)

        return instance

    @staticmethod
    def from_list(data_list: list, format_char: str = "f", shape: tuple = None):
        """
        将 Python 列表转化为 C 连续内存，返回管理器实例。
        用法: mem = CMemoryManager.from_list([1.0, 2.0], "f", (2, 1))
        """
        instance = CMemoryManager()
        if not data_list:
            return instance

        # 存入实例变量，强行续命防 GC！
        instance._cache = array.array(format_char, data_list)
        mv = memoryview(instance._cache)

        instance.format_char = format_char
        instance.shape = shape if shape else (len(data_list),)
        instance.ptr_addr = instance._cache.buffer_info()[0]

        # 💥 优化: 直接使用原生 .cast 链式重塑，抛弃旧函数依赖
        if shape is not None:
            instance.view = mv.cast("B").cast(format_char, shape=shape)
        else:
            instance.view = mv

        return instance

    @staticmethod
    def from_ptr(ptr_addr: int, format_char: str, shape: tuple):
        """
        从外部 C/C++ 裸指针直接映射内存视图。
        它不拥有内存的生命周期（_cache 为 None），只提供安全读写的 Python 视图。
        用法: mem = CMemoryManager.from_ptr(raw_addr, "f", (100, 3))
        """
        instance = CMemoryManager()

        if ptr_addr == 0 or not shape:
            return instance

        if format_char not in CMemoryManager._CTYPES_MAP:
            raise ValueError(f"Unsupported format character: {format_char}")

        total_elements = 1
        for dim in shape:
            total_elements *= dim

        if total_elements <= 0:
            return instance

        # 建立 ctypes 数组映射
        ctype_base = CMemoryManager._CTYPES_MAP[format_char]
        ArrayType = ctype_base * total_elements
        ctypes_array = ArrayType.from_address(ptr_addr)

        # 记录基础信息
        instance.ptr_addr = ptr_addr
        instance.format_char = format_char
        instance.shape = shape

        # 💥 生成零拷贝视图
        instance.view = memoryview(ctypes_array).cast("B").cast(format_char, shape=shape)

        return instance

    def reshape(self, new_shape: tuple):
        """
        重塑当前持有的视图，并返回一个新的 CMemoryManager 实例。
        原对象的数据和状态不会受到任何影响（绝对安全）。
        自动适配机制：如果新形状需要的元素少于当前容量，自动截断尾部无效数据。
        """
        if self.view is None:
            raise RuntimeError("当前管理器没有持有任何视图！")

        # 1. 计算目标形状到底需要多少个元素
        target_elements = 1
        for dim in new_shape:
            target_elements *= dim

        # 2. 将当前视图强行展平为 1D 视图，方便计算和切片
        flat_view = self.view.cast("B").cast(self.format_char)
        current_elements = len(flat_view)

        # 3. 拦截越界：你要的积木比我总共拥有的还多，那只能报错了
        if target_elements > current_elements:
            raise ValueError(f"重塑失败: 目标形状需要 {target_elements} 个元素，但当前内存仅有 {current_elements} 个。")

        # 4. 🌟 创建全新的管理器实例
        new_manager = CMemoryManager()
        new_manager.format_char = self.format_char
        new_manager.shape = new_shape
        new_manager.ptr_addr = self.ptr_addr
        
        # 💥 核心：将底层的 _cache 引用传递给新对象，确保原生内存不会被提早 GC 回收
        new_manager._cache = self._cache 

        # 5. 在新对象上生成零拷贝的重塑视图
        new_manager.view = flat_view[:target_elements].cast("B").cast(self.format_char, shape=new_shape)

        return new_manager