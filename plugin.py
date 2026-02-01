import maya.api.OpenMaya as om


def maya_useNewAPI():
    pass


class UnitMatrixPin(om.MPxNode):
    TYPE_NAME = "unitMatrixPin"
    TYPE_ID = om.MTypeId(0x87001)

    attrInputMesh = om.MObject()
    attrInputScaleMesh = om.MObject()
    attrInputOrigMesh = om.MObject()

    attrOutputMatrices = om.MObject()

    def __init__(self):
        super(UnitMatrixPin, self).__init__()

    @staticmethod
    def creator():
        return UnitMatrixPin()

    @staticmethod
    def initialize():
        fn_typedAttr = om.MFnTypedAttribute()
        fn_matrixAttr = om.MFnMatrixAttribute()

        # 输入变形后的网格
        UnitMatrixPin.attrInputMesh = fn_typedAttr.create("inputMesh", "im", om.MFnData.kMesh)
        fn_typedAttr.storable = True
        fn_typedAttr.writable = True
        # 输入用于计算缩放的参考网格
        UnitMatrixPin.attrInputScaleMesh = fn_typedAttr.create("inputScaleMesh", "ism", om.MFnData.kMesh)
        fn_typedAttr.storable = True
        fn_typedAttr.writable = True

        # 输入原始参考网格
        UnitMatrixPin.attrInputOrigMesh = fn_typedAttr.create("origMesh", "iom", om.MFnData.kMesh)
        fn_typedAttr.storable = True
        fn_typedAttr.writable = True

        # 输出矩阵数组
        UnitMatrixPin.attrOutputMatrices = fn_matrixAttr.create("outputMatrices", "om")
        fn_matrixAttr.array = True
        fn_matrixAttr.usesArrayDataBuilder = True
        fn_matrixAttr.storable = False
        fn_matrixAttr.writable = False

        UnitMatrixPin.addAttribute(UnitMatrixPin.attrInputMesh)
        UnitMatrixPin.addAttribute(UnitMatrixPin.attrInputScaleMesh)
        UnitMatrixPin.addAttribute(UnitMatrixPin.attrInputOrigMesh)
        UnitMatrixPin.addAttribute(UnitMatrixPin.attrOutputMatrices)

        UnitMatrixPin.attributeAffects(UnitMatrixPin.attrInputMesh, UnitMatrixPin.attrOutputMatrices)
        UnitMatrixPin.attributeAffects(UnitMatrixPin.attrInputScaleMesh, UnitMatrixPin.attrOutputMatrices)
        UnitMatrixPin.attributeAffects(UnitMatrixPin.attrInputOrigMesh, UnitMatrixPin.attrOutputMatrices)

    def compute(self, plug, dataBlock):
        if plug != UnitMatrixPin.attrOutputMatrices:
            return

        inputMesh_handle = dataBlock.inputValue(UnitMatrixPin.attrInputMesh)
        inputScaleMesh_handle = dataBlock.inputValue(UnitMatrixPin.attrInputScaleMesh)
        inputOrigMesh_handle = dataBlock.inputValue(UnitMatrixPin.attrInputOrigMesh)

        inputMesh_mObject = inputMesh_handle.asMesh()
        inputScaleMesh_mObject = inputScaleMesh_handle.asMesh()
        inputOrigMesh_mObject = inputOrigMesh_handle.asMesh()

        if inputMesh_mObject.isNull() or inputOrigMesh_mObject.isNull() or inputScaleMesh_mObject.isNull():
            return

        # 批量获取点数据，减少 API 调用次数
        mesh_points = om.MFnMesh(inputMesh_mObject).getPoints(om.MSpace.kWorld)
        scale_points = om.MFnMesh(inputScaleMesh_mObject).getPoints(om.MSpace.kWorld)
        orig_points = om.MFnMesh(inputOrigMesh_mObject).getPoints(om.MSpace.kWorld)

        num_points = len(mesh_points)
        unit_count = num_points // 4

        outArrayHandle = dataBlock.outputArrayValue(UnitMatrixPin.attrOutputMatrices)
        outBuilder = outArrayHandle.builder()

        for i in range(unit_count):
            idx = i * 4

            # --- 当前网格计算 ---
            pos = om.MVector(mesh_points[idx])
            axis_x = (om.MVector(mesh_points[idx + 1]) - pos).normalize()
            axis_y = (om.MVector(mesh_points[idx + 2]) - pos).normalize()
            axis_z = (om.MVector(mesh_points[idx + 3]) - pos).normalize()

            axis_y = (axis_z ^ axis_x).normalize()
            axis_x = (axis_y ^ axis_z).normalize()

            # --- 缩放参考网格计算 ---
            scale_pos = om.MVector(scale_points[idx])
            axis_x_length = (om.MVector(scale_points[idx + 1]) - scale_pos).length()
            axis_y_length = (om.MVector(scale_points[idx + 2]) - scale_pos).length()
            axis_z_length = (om.MVector(scale_points[idx + 3]) - scale_pos).length()

            # --- 原始网格计算 ---
            orig_pos = om.MVector(orig_points[idx])
            orig_axis_x_length = (om.MVector(orig_points[idx + 1]) - orig_pos).length()
            orig_axis_y_length = (om.MVector(orig_points[idx + 2]) - orig_pos).length()
            orig_axis_z_length = (om.MVector(orig_points[idx + 3]) - orig_pos).length()

            # --- 应用缩放 ---
            axis_x *= axis_x_length / orig_axis_x_length if orig_axis_x_length != 0 else 1.0
            axis_y *= axis_y_length / orig_axis_y_length if orig_axis_y_length != 0 else 1.0
            axis_z *= axis_z_length / orig_axis_z_length if orig_axis_z_length != 0 else 1.0

            # --- 构建矩阵 ---
            new_matrix = om.MMatrix([
                [axis_x.x, axis_x.y, axis_x.z, 0.0],
                [axis_y.x, axis_y.y, axis_y.z, 0.0],
                [axis_z.x, axis_z.y, axis_z.z, 0.0],
                [pos.x, pos.y, pos.z, 1.0],
            ])

            hOut = outBuilder.addElement(i)
            hOut.setMMatrix(new_matrix)

        outArrayHandle.set(outBuilder)

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
