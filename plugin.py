import maya.api.OpenMaya as om


def maya_useNewAPI():
    pass


class UnitMatrixPin(om.MPxNode):
    TYPE_NAME = "unitMatrixPin"
    TYPE_ID = om.MTypeId(0x87001)

    aInputMesh = om.MObject()
    aOrigMesh = om.MObject()
    aOutputMatrices = om.MObject()

    def __init__(self):
        super(UnitMatrixPin, self).__init__()

    @staticmethod
    def creator():
        return UnitMatrixPin()

    @staticmethod
    def initialize():
        tAttr = om.MFnTypedAttribute()
        mAttr = om.MFnMatrixAttribute()

        # 输入变形后的网格
        UnitMatrixPin.aInputMesh = tAttr.create("inputMesh", "in", om.MFnData.kMesh)
        tAttr.storable = True
        tAttr.writable = True

        # 输入原始参考网格
        UnitMatrixPin.aOrigMesh = tAttr.create("origMesh", "orig", om.MFnData.kMesh)
        tAttr.storable = True
        tAttr.writable = True

        # 输出矩阵数组
        UnitMatrixPin.aOutputMatrices = mAttr.create("outputMatrices", "out")
        mAttr.array = True
        mAttr.usesArrayDataBuilder = True
        mAttr.storable = False
        mAttr.writable = False

        UnitMatrixPin.addAttribute(UnitMatrixPin.aInputMesh)
        UnitMatrixPin.addAttribute(UnitMatrixPin.aOrigMesh)
        UnitMatrixPin.addAttribute(UnitMatrixPin.aOutputMatrices)

        UnitMatrixPin.attributeAffects(UnitMatrixPin.aInputMesh, UnitMatrixPin.aOutputMatrices)
        UnitMatrixPin.attributeAffects(UnitMatrixPin.aOrigMesh, UnitMatrixPin.aOutputMatrices)

    def getSchedulingType(self):
        return om.MPxNode.kParallel

    def compute(self, plug, dataBlock):
        if plug != UnitMatrixPin.aOutputMatrices:
            return

        hInput = dataBlock.inputValue(UnitMatrixPin.aInputMesh)
        hOrig = dataBlock.inputValue(UnitMatrixPin.aOrigMesh)

        mInputMesh = hInput.asMesh()
        mOrigMesh = hOrig.asMesh()

        if mInputMesh.isNull() or mOrigMesh.isNull():
            return

        # 批量获取点数据，减少 API 调用次数
        points = om.MFnMesh(mInputMesh).getPoints(om.MSpace.kWorld)
        orig_points = om.MFnMesh(mOrigMesh).getPoints(om.MSpace.kWorld)

        num_points = len(points)
        unit_count = num_points // 4

        outArrayHandle = dataBlock.outputArrayValue(UnitMatrixPin.aOutputMatrices)
        outBuilder = outArrayHandle.builder()

        for i in range(unit_count):
            idx = i * 4

            # --- 当前网格计算 ---
            p_base = om.MVector(points[idx])
            v_x = om.MVector(points[idx + 1]) - p_base
            v_y = om.MVector(points[idx + 2]) - p_base
            v_z = om.MVector(points[idx + 3]) - p_base

            # --- 原始网格计算 ---
            p_orig_base = om.MVector(orig_points[idx])
            v_orig_x = om.MVector(orig_points[idx + 1]) - p_orig_base
            v_orig_y = om.MVector(orig_points[idx + 2]) - p_orig_base
            v_orig_z = om.MVector(orig_points[idx + 3]) - p_orig_base

            # --- 缩放计算：使用逻辑判断替代 +0.0001 ---
            # 获取原始向量长度
            l_ox = v_orig_x.length()
            l_oy = v_orig_y.length()
            l_oz = v_orig_z.length()

            # 计算缩放比例，如果原始长度为 0，则强制设为 1
            sx = v_x.length() / l_ox if l_ox > 0 else 1.0
            sy = v_y.length() / l_oy if l_oy > 0 else 1.0
            sz = v_z.length() / l_oz if l_oz > 0 else 1.0

            v_x = v_x.normalize() * sx
            v_y = v_y.normalize() * sy
            v_z = v_z.normalize() * sz

            # --- 构建矩阵 ---
            # 直接使用当前 v_x, v_y, v_z 构建包含缩放信息的矩阵
            # 如果原始长度为0，这里构建出来的矩阵将基于 v_x 的实际长度

            new_matrix = om.MMatrix([
                [v_x.x, v_x.y, v_x.z, 0.0],
                [v_y.x, v_y.y, v_y.z, 0.0],
                [v_z.x, v_z.y, v_z.z, 0.0],
                [p_base.x, p_base.y, p_base.z, 1.0],
            ])

            hOut = outBuilder.addElement(i)
            hOut.setMMatrix(new_matrix)

        outArrayHandle.set(outBuilder)
        # 核心性能优化：批量清理脏标记，防止 EM 多次触发计算
        outArrayHandle.setAllClean()
        dataBlock.setClean(plug)


# 注册与卸载函数保持不变
def initializePlugin(mObject):
    mPlugin = om.MFnPlugin(mObject, "YourName", "1.2", "Any")
    try:
        mPlugin.registerNode(UnitMatrixPin.TYPE_NAME, UnitMatrixPin.TYPE_ID, UnitMatrixPin.creator, UnitMatrixPin.initialize)
    except Exception:
        raise RuntimeError("Failed to register node")


def uninitializePlugin(mObject):
    mPlugin = om.MFnPlugin(mObject)
    try:
        mPlugin.deregisterNode(UnitMatrixPin.TYPE_ID)
    except Exception:
        raise RuntimeError("Failed to deregister node")
