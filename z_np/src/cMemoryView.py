import ctypes
import array

# 预定义类型映射表：让用户只需传入简写的格式符
_CTYPES_MAP = {
    "d": ctypes.c_double,
    "f": ctypes.c_float,
    "i": ctypes.c_int32,
    "I": ctypes.c_uint32,
    "b": ctypes.c_int8,
    "B": ctypes.c_uint8,
}


def get_view_from_ptr(ptr_addr: int, format_char: str, shape: tuple):
    """
    根据内存物理地址、数据类型和形状，生成零拷贝的多维 memoryview。

    参数:
        ptr_addr (int): 底层 C/C++ 内存的首地址。
        format_char (str): 目标数据类型，例如 'd' (double), 'f' (float)。
        shape (tuple): 目标视图的形状，例如 (num_bones, 16) 或 (num_verts, 3)。

    返回:
        memoryview: 安全、纯净且带有正确 shape 的零拷贝视图。
    """
    if ptr_addr == 0 or not shape:
        return None

    if format_char not in _CTYPES_MAP:
        raise ValueError(f"Unsupported format character: {format_char}")
    ctype_base = _CTYPES_MAP[format_char]

    total_elements = 1
    for dim in shape:
        total_elements *= dim

    if total_elements <= 0:
        return None

    ArrayType = ctype_base * total_elements
    ctypes_array = ArrayType.from_address(ptr_addr)

    return memoryview(ctypes_array).cast("B").cast(format_char, shape=shape)


def get_view_from_list(data_list: list, format_char: str = "f", shape: tuple = None):
    """
    将普通的 Python 列表瞬间转化为 C 连续的 memoryview。

    参数:
        data_list (list): 包含浮点数或整数的 Python 列表。
        format_char (str): 目标类型，默认 'f' (float)。
        shape (tuple): 可选的重塑维度。
    """
    if not data_list:
        return None

    c_array = array.array(format_char, data_list)

    mv = memoryview(c_array)

    if shape is not None:
        return reshape_view(mv, shape)

    return mv


def reshape_view(mv: memoryview, shape: tuple):
    """
    零拷贝重塑 memoryview 的形状。

    参数:
        mv (memoryview): 原始的内存视图。
        shape (tuple): 目标形状，例如 (num_verts, num_bones)。

    返回:
        memoryview: 具有新形状的零拷贝视图。
    """
    if not isinstance(mv, memoryview):
        raise TypeError("❌ 传入的对象不是 memoryview！")

    if not shape:
        return mv

    fmt = mv.format

    return mv.cast("B").cast(fmt, shape=shape)
