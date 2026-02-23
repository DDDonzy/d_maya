import ctypes
import maya.OpenMaya as om1



def _get_bind_matrices_view(self, dataBlock, active_bones_count):
    """
    零拷贝获取 Bind Pre Matrix 的连续内存视图。
    直接映射 Maya 底层 C++ 内存，返回给 Cython 核心使用。
    """
    if active_bones_count <= 0:
        return None

    bind_data_obj = dataBlock.inputValue(self.aBindPreMatrix).data()
    if bind_data_obj is None or bind_data_obj.isNull():
        return None

    fn_bind_array = om1.MFnMatrixArrayData(bind_data_obj)
    bind_m_array = fn_bind_array.array()
    
    # 安全拦截：确保 Maya 里的矩阵数量足够本次解算
    if bind_m_array.length() < active_bones_count:
        return None

    # 1. 获取 C++ 原生连续内存首地址
    addr_base = int(bind_m_array[0].this)

    # 2. 定义 C 语言的一维 Double 数组类型 (每个 MMatrix 占 16 个 double)
    ArrayType = ctypes.c_double * (active_bones_count * 16)

    # 3. 瞬间映射内存并返回视图！(绝对的 0.0000 毫秒开销)
    bind_view = ArrayType.from_address(addr_base)

    return bind_view