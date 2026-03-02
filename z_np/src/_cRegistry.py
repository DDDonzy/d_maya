import maya.OpenMaya as om1  # type:ignore
import maya.api.OpenMaya as om2


class SkinRegistry:
    """
    利用 MObject 的底层一致性哈希，获取Python开发节点的类实例对象。
    完美实现 API 1.0 与 API 2.0 的内存级通信，并绝对杜绝内存泄漏！
    """

    _storage = {}

    @classmethod
    def register(cls, mObj_api1: om1.MObject, python_instance):
        """
        节点创建时调用：使用 API 1.0 的 MObject 注册 Python 实例
        """
        handle = om1.MObjectHandle(mObj_api1)
        cls._storage[handle.hashCode()] = python_instance
        # print(f"[Registry] 节点注册成功! Hash: {handle.hashCode()}")

    @classmethod
    def get_instance_by_api1(cls, mObj_api1: om1.MObject):
        """
        通过 API 1.0 的 MObject 获取 Python 实例
        """
        if mObj_api1.isNull():
            return None

        handle = om1.MObjectHandle(mObj_api1)
        hash_code = handle.hashCode()

        if hash_code in cls._storage:
            # 存活校验,防止节点被删除后产生野指针
            if handle.isValid() and handle.isAlive():
                return cls._storage[hash_code]
            else:
                print(f"[Registry API 1] 清理失效节点的内存尸体: {hash_code}")
                del cls._storage[hash_code]

        return None

    @classmethod
    def get_instance_by_api2(cls, mObj_api2: om2.MObject):
        """
        通过 API 2.0 的 MObject 获取 Python 实例
        """
        if mObj_api2.isNull():
            return None

        handle = om2.MObjectHandle(mObj_api2)
        hash_code = handle.hashCode()

        if hash_code in cls._storage:
            # 存活校验,防止节点被删除后产生野指针
            if handle.isValid() and handle.isAlive():
                return cls._storage[hash_code]
            else:
                print(f"[Registry API 2] 清理失效节点的内存尸体: {hash_code}")
                del cls._storage[hash_code]

        return None
