from PySide2 import QtWidgets, QtCore

import z_bs.core.bsFunctions as fnBs
import z_bs.core.transferBlendShape as bsTransfer
from z_bs.core.wrap import createWrap, createProximityWrap

import z_bs.ui.logic.treeViewFunction as treeFn
from z_bs.utils.showMessage import showMessage
from z_bs.ui.logic.treeViewSelection import get_lasterSelectedTargetData, get_selectionBlendShape, get_selectionTarget, get_selectionTargetData, get_selectionInbetween
from z_bs.utils.getHistory import get_history, get_shape

from maya import mel, cmds

import time
from functools import partial, wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from z_bs.ui.uiMain import ShapeToolsWidget


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"Function: '{func.__name__}' Runtimes: {duration:.6f} sec")

        return result

    return wrapper


class ActionHandler:
    """按钮动作处理器类"""

    def __init__(self, ui):
        self.ui: ShapeToolsWidget = ui
        self.transferPreviewObject = None
        self.copyDeltaDataTemp = None
        self.treeViewIsExpand = True

    def load_blendshape(self):
        """加载 BlendShape 节点"""
        blendShapeNames = []

        sel = cmds.ls(sl=1)
        for obj in sel:
            blendShapeNames.extend(get_history(obj, type="blendShape"))

        treeviewSelectedBSD = mel.eval("getShapeEditorTreeviewSelection 1")
        blendShapeNames.extend(treeviewSelectedBSD)

        if not treeviewSelectedBSD:
            lastSelectionData = get_lasterSelectedTargetData()
            if lastSelectionData.node:
                blendShapeNames.append(lastSelectionData.node)

        blendShapeNames = list(dict.fromkeys(blendShapeNames))  # 保持顺序去重
        if not blendShapeNames:
            self.ui.filterComboBox.clear()
            showMessage("No blendShape node found in the selected in scene or shapeEdit.")
            return
        self.ui.filterComboBox.clear()
        allStr = "&".join(blendShapeNames)
        if allStr not in blendShapeNames:
            self.ui.filterComboBox.addItem(allStr)
        self.ui.filterComboBox.addItems(blendShapeNames)
        self.ui.filterComboBox.setCurrentIndex(0)
        self.treeView_expand_all()

    def load_target(self):
        """加载目标"""
        # TODO  考虑添加 bsTargetGroup 支持
        # TODO  自动加载有 数值 的target，不太好使，必须选择 bs节点才行。考虑优化一下，
        baseText = self.ui.filterLineEdit.text()
        text = "&"
        targetList = mel.eval("getShapeEditorTreeviewSelection 14")
        targetNamelist = []
        if not targetList:
            targetNamelist = self.get_no_zero_weight_targets()
            if not targetNamelist:
                self.ui.filterLineEdit.setText("")
                return

        for target in targetList:
            if "." in target:
                split = target.split(".")
                targetName = cmds.aliasAttr(f"{split[0]}.w[{split[-1]}]", q=1)
                targetNamelist.append(targetName)

        text = text.join(targetNamelist)
        if baseText == text:
            text = ""
        self.ui.filterLineEdit.setText(text)

    def get_no_zero_weight_targets(self):
        """
        获取所有非零权重的目标
        Get all targets with non-zero weight from the selected blendShape node.
        """
        target = get_lasterSelectedTargetData()

        if target.node is None:
            return []
        if not cmds.objExists(target.node):
            return []

        targetNames = []
        tolerance = 1e-3
        for name in cmds.listAttr(f"{target.node}.w", multi=True):
            w = cmds.getAttr(f"{target.node}.{name}")
            if abs(w) > tolerance:
                targetNames.append(name)
        return targetNames

    def add_sculpt(self):
        """
        添加雕刻到选择的 BlendShape 节点
        Add a sculpt to the selected blendShape node.
        """
        target = get_lasterSelectedTargetData()
        if target.targetIdx < 0:
            showMessage("No target selected in shape editor.")
            return

        sel = cmds.ls(sl=1)
        if not cmds.ls(sl=1):
            showMessage("No mesh selected.")
            return
        sculptGeo = sel[0]
        shapes = get_shape(sculptGeo)
        if not shapes:
            showMessage("Selected object is not a mesh.")
            return
        shape = shapes[0]
        if not cmds.objectType(shape, isa="mesh"):
            showMessage("Selected object is not a mesh.")

        fnBs.add_sculptGeo(sculptGeo=shape, targetData=target, addInbetween=self.ui.addInbetweenCheckBox.isChecked())

        if not self.ui.deleteSculptCheckBox.isChecked():
            cmds.delete(sculptGeo)
        showMessage("Add sculpt target successfully.")

    def auto_set_weight(self):
        """
        自动设置选择目标的权重
        Auto set the weight of the selected target.
        """
        target = get_lasterSelectedTargetData()

        if target.targetIdx < 0:
            weightAttr = f"{target.node}.envelope"
            weightsValue = [0, 1]
        else:
            weightAttr = f"{target.node}.w[{target.targetIdx}]"
            iti_list = cmds.getAttr(f"{target.node}.it[0].itg[{target.targetIdx}].iti", mi=1)
            weightsValue = [0] + [fnBs.convertInbetweenIndexToValue(x) for x in iti_list]

        w = round(cmds.getAttr(weightAttr), 3)
        for x in weightsValue:
            if x <= w:
                if x == weightsValue[-1]:
                    cmds.setAttr(weightAttr, weightsValue[0])
                    break
                continue
            else:
                cmds.setAttr(weightAttr, x)
                break

    def update_object_label(self):
        """更新对象标签"""
        meshText = "None"
        bsText = "None"
        target = get_lasterSelectedTargetData()

        if target.baseMesh:
            if cmds.objExists(target.baseMesh):
                meshText = cmds.listRelatives(target.baseMesh, parent=1)[0]
        if target.node:
            if cmds.objExists(target.node):
                bsText = target.node

        self.ui.meshLabel.setText(meshText)
        self.ui.bsLabel.setText(bsText)

    def filter_changed(self):
        """过滤器变化处理"""
        nodeText = self.ui.filterComboBox.currentText().strip()
        if nodeText == "None":
            nodeText = ""
        targetText = self.ui.filterLineEdit.text().strip()
        treeFn.treeView_filter(self.ui.treeView, targetText, treeFn.SelectedItemType(3))
        treeFn.treeView_filter(self.ui.treeView, nodeText, treeFn.SelectedItemType(2))
        treeFn.treeView_filter(self.ui.treeView, nodeText, treeFn.SelectedItemType(1))
        # 过滤后清除选择项，避免选择项不在过滤后的列表中，导致误操作
        self.ui.treeView.selectionModel().clearSelection()

    def go_to_pose(self):
        """跳转到姿势"""
        print("Go to pose clicked.")

    def select_base_mesh(self):
        """选择基础网格"""
        mesh = self.ui.meshLabel.text()
        if mesh == "None":
            return
        else:
            if cmds.objExists(mesh):
                cmds.select(mesh)
            else:
                showMessage(f"{mesh} does not exist in the scene.")

    def select_bs_node(self):
        """选择 BlendShape 节点"""
        bsName = self.ui.bsLabel.text()
        if bsName == "None":
            return
        else:
            if cmds.objExists(bsName):
                cmds.select(bsName)
            else:
                showMessage(f"{bsName} does not exist in the scene.")

    def tree_view_expand_or_collapse(self):
        """树视图展开/折叠"""
        if self.treeViewIsExpand:
            self.treeView_collapse_all()
        else:
            self.treeView_expand_all()

    def treeView_collapse_all(self):
        model = self.ui.treeView.model()
        for index in treeFn.TreeViewIterator(self.ui.treeView):
            item = model.itemFromIndex(index)
            if not item:
                continue
            item_data = item.data()
            if not item_data:
                continue
            if treeFn.SelectedItemType(item_data) == treeFn.SelectedItemType.blendShape_group:
                continue
            self.ui.treeView.collapse(item.index())
        self.treeViewIsExpand = False

    def treeView_expand_all(self):
        model = self.ui.treeView.model()
        for index in treeFn.TreeViewIterator(self.ui.treeView):
            item = model.itemFromIndex(index)
            if not item:
                continue
            item_data = item.data()
            if not item_data:
                continue
            # 默认不展开 inbetween
            if treeFn.SelectedItemType(item_data) == treeFn.SelectedItemType.blendShape_target:
                self.ui.treeView.collapse(item.index())
                continue
            self.ui.treeView.expand(item.index())
        self.treeViewIsExpand = True

    def wrap_attrs_pag_vis(self):
        """
        切换 proximityWrap 的页面可见性
        """
        self.ui.proximityWrapPag.setVisible(self.ui.proximityWrapRadioButton.isChecked())
        self.ui.wrapPag.setVisible(self.ui.wrapRadioButton.isChecked())

    def copy_QPushButton(self, src_btn):
        """
        创建新的 QPushButton 并复制 src_btn 的常用属性
        Create a new QPushButton and copy common properties from src_btn.
        """
        new_btn = QtWidgets.QPushButton()
        new_btn.setText(src_btn.text())
        new_btn.setIcon(src_btn.icon())
        new_btn.setIconSize(src_btn.iconSize())
        new_btn.setEnabled(src_btn.isEnabled())
        new_btn.setCheckable(src_btn.isCheckable())
        new_btn.setChecked(src_btn.isChecked())
        new_btn.setFlat(src_btn.isFlat())
        new_btn.setFont(src_btn.font())
        new_btn.setStyleSheet(src_btn.styleSheet())
        new_btn.setMinimumSize(src_btn.minimumSize())
        new_btn.setMaximumSize(src_btn.maximumSize())
        new_btn.setSizePolicy(src_btn.sizePolicy())
        return new_btn

    def add_dynamic_button(self):
        """添加动态按钮"""
        if not hasattr(self.ui, "dynamicButtonCount"):
            self.ui.dynamicButtonCount = 0
        if not hasattr(self.ui, "dynamicButtonsDict"):
            self.ui.dynamicButtonsDict = {}

        self.ui.dynamicButtonCount += 1
        btn = self.copy_QPushButton(self.ui.setsButtonTemplate)
        btn.installEventFilter(self.ui)
        btn.sel_sets = self.get_treeviewSelectedList()
        self.ui.setsButtonWidget.layout().addWidget(btn)

        def onButtonClicked():
            self.select_treeViewItems(btn.sel_sets)

        self.ui.dynamicButtonsDict[btn] = onButtonClicked
        btn.clicked.connect(self.ui.dynamicButtonsDict[btn])

    def delete_dynamic_button(self, button_to_delete):
        """从UI和字典中删除一个动态按钮。"""
        if button_to_delete in self.ui.dynamicButtonsDict:
            self.ui.setsButtonWidget.layout().removeWidget(button_to_delete)
            button_to_delete.deleteLater()
            del self.ui.dynamicButtonsDict[button_to_delete]

    def copy_delta_cmd(self):
        target = get_lasterSelectedTargetData()
        if cmds.objExists(target.attr):
            self.copyDeltaDataTemp = fnBs.copy_delta(target)
            showMessage(f"Copy {target.attr}")
        else:
            showMessage("Please select a blendShape target")

    def pasted_delta_cmd(self):
        if self.copyDeltaDataTemp:
            targets = get_selectionTargetData()
            for target in targets:
                if cmds.objExists(target.attr):
                    fnBs.pasted_delta(target, self.copyDeltaDataTemp)
                    showMessage(f"Pasted {target.attr}")
            else:
                showMessage("Please select a blendShape target")

    def transfer_load(self):
        mesh = ""
        bs = ["New BlendShape"]

        def _set():
            self.ui.transferComboBox.clear()
            self.ui.transferComboBox.addItems(bs)
            self.ui.transferMeshLineEdit.setText(mesh)

        sel = cmds.ls(sl=1)
        if not sel:
            _set()
            showMessage("No mesh selected.")
            raise RuntimeError("No mesh selected.")

        mesh = sel[0]
        shapes = get_shape(mesh)
        if not shapes:
            _set()
            showMessage("Selected object is not a mesh.")
            raise RuntimeError("Selected object is not a mesh.")

        if not cmds.objectType(shapes[0], isa="mesh"):
            showMessage("Selected object is not a mesh.")
            raise RuntimeError("Selected object is not a mesh.")

        bs.extend(get_history(mesh, "blendShape"))
        _set()

    def setBlendShapeManagerFilter(self, filter_str: str):
        for manager in cmds.ls(type="shapeEditorManager"):
            cmds.setAttr(f"{manager}.filterString", filter_str, type="string")

    def getTransferData(self):
        targetMesh = self.ui.transferMeshLineEdit.text()
        if not targetMesh:
            showMessage("Please input target mesh name")
            raise RuntimeError("Please input target mesh name")
        newBlendShape = None
        if self.ui.transferComboBox.currentIndex() != 0:
            newBlendShape = self.ui.transferComboBox.currentText()
        if not cmds.objExists(targetMesh):
            showMessage(f"Can not find {targetMesh}")
            raise RuntimeError(f"Can not find {targetMesh}")
        target = get_selectionTarget()
        bs = get_selectionBlendShape()
        if not bs and not target:
            showMessage("Please select blendShape or targets in shapeEdit")
            raise RuntimeError("Please select blendShape or targets in shapeEdit")
        if bs and target:
            showMessage("Please select blendShape or targets in shapeEdit, not both")
            raise RuntimeError("Please select blendShape or targets in shapeEdit, not both")
        if len(bs) > 1:
            showMessage("Please select only one blendShape node in shapeEdit")
            raise RuntimeError("Please select only one blendShape node in shapeEdit")

        if target:
            bs = target[0].split(".")[0]
            idx_list = []
            for i in target:
                i_bs, idx = i.split(".")
                idx_list.append(int(idx))
                if i_bs != bs:
                    showMessage("Please select targets from the same blendShape node")
                    raise RuntimeError("Please select targets from the same blendShape node")
            targetList = fnBs.get_targetDataList(bs)
            transferList = []
            for i in targetList:
                if i.targetIdx in idx_list:
                    transferList.append(i)

            return {"blendShape": bs, "targetList": transferList, "targetMesh": targetMesh, "destinationBlendShape": newBlendShape}

        if bs:
            bs = bs[0]
            transferList = fnBs.get_targetDataList(bs)
            return {"blendShape": bs, "targetList": transferList, "targetMesh": targetMesh, "destinationBlendShape": newBlendShape}

    @timeit
    def transfer(self):
        data = self.getTransferData()
        wrap = self.makeWrapFunctions()
        bsTransfer.transferBlendShape(sourceBlendShape=data["blendShape"], targetDataList=data["targetList"], destinationMesh=data["targetMesh"], destinationBlendShape=data["destinationBlendShape"], wrapFunction=wrap)

    def preview(self):
        if self.transferPreviewObject:
            try:
                cmds.delete(self.transferPreviewObject)
                self.transferPreviewObject = None
                return
            except:
                pass

        data = self.getTransferData()
        wrap = self.makeWrapFunctions()
        self.transferPreviewObject = bsTransfer.transferBlendShape(sourceBlendShape=data["blendShape"], targetDataList=data["targetList"], destinationMesh=data["targetMesh"], destinationBlendShape=data["destinationBlendShape"], wrapFunction=wrap, preview=True)

    def makeWrapFunctions(self):
        if self.ui.wrapRadioButton.isChecked():
            mode = self.ui.wrapModeComboBox.currentIndex()
            exclusiveBind = int(self.ui.wrapExclusiveBindLineEdit.text())
            autoWeight = int(self.ui.warpAutoWeightThresholdLineEdit.text())
            weightThreshold = float(self.ui.wrapWeightThresholdLineEdit.text())
            maxDistance = float(self.ui.wrapMaxDistanceLineEdit.text())

            return partial(createWrap, falloffMode=mode, exclusiveBind=exclusiveBind, autoWeightThreshold=autoWeight, weightThreshold=weightThreshold, maxDistance=maxDistance)

        if self.ui.proximityWrapRadioButton.isChecked():
            mode = self.ui.proximityModeComboBox.currentIndex()
            smoothInfluences = int(self.ui.smoothInfluencesLineEdit.text())
            smoothNormal = int(self.ui.smoothNormalLineEdit.text())
            falloffScale = float(self.ui.falloffScaleLineEdit.text())
            dropoffScale = float(self.ui.dropoffScaleLineEdit.text())

            return partial(createProximityWrap, wrapMode=mode, smoothInfluences=smoothInfluences, smoothNormals=smoothNormal, falloffScale=falloffScale, dropoffRateScale=dropoffScale)

    def get_treeviewSelectedList(self):
        """
        获取treeview当前所有选择的item（简化版）

        Returns:
            list: 包含选中项索引的列表
        """
        selected_items = []
        selection_model = self.ui.treeView.selectionModel()

        if not selection_model:
            return selected_items

        selected_indexes = selection_model.selectedIndexes()

        for index in selected_indexes:
            if index.isValid():
                selected_items.append(index)

        return selected_items

    def select_treeViewItems(self, index_list):
        """
        根据索引列表选中treeview项目

        Args:
            index_list (list): 要选中的索引列表
        """
        selection_model = self.ui.treeView.selectionModel()

        if not selection_model:
            return

        # 清除当前选择
        selection_model.clearSelection()

        # 选择指定的项目
        for index in index_list:
            if index.isValid():
                selection_model.select(index, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)

    @timeit
    def mirror_bsTarget(self):
        """
        镜像 BlendShape 目标
        Mirror the selected BlendShape target.
        """
        targetList = get_selectionTargetData()

        axis = ["x", "y", "z"][self.ui.mirrorAxisComboBox.currentIndex()]
        direction = self.ui.mirrorDirectionComboBox.currentIndex()

        targetDict = {}
        for x in targetList:
            targetDict.update({x.targetName: x})
        targetList = list(targetDict.values())

        for target in targetList:
            fnBs.mirror_bsTarget(
                target,
                axis=axis,
                mirrorDirection=direction,
            )
            print(f"Mirror: {target.targetName} successfully.")

    @timeit
    def flip_bsTarget(self, autoMirror=False):
        """
        翻转 BlendShape 目标
        Flip the selected BlendShape target.
        """
        targetList = get_selectionTargetData()

        targetDict = {}
        for x in targetList:
            targetDict.update({x.targetName: x})
        targetList = list(targetDict.values())

        axis = ["x", "y", "z"][self.ui.mirrorAxisComboBox.currentIndex()]
        direction = self.ui.mirrorDirectionComboBox.currentIndex()
        matchStr = self.ui.mirrorTableView.get_active_mirror_data()
        fnBs.autoFlipCopy(
            targetList[0].node,
            targetList,
            matchStr,
            axis,
            direction,
            autoMirror,
        )

    def resetDelta(self):
        """
        重置 BlendShape 目标的 Delta
        Reset the Delta of the selected BlendShape target.
        """

        target = get_selectionTarget()  # ['M_Head_base_blendShape.1']
        inbetween = get_selectionInbetween()  # ['M_Head_base_blendShape.1.5611']

        output_inbetween = []
        if not inbetween and not target:
            raise RuntimeError("Please select targets or inbetween in shapeEdit.")
        for t in target:
            node, targetIdx = t.split(".")
            output_inbetween.extend(fnBs.get_targetInbetween(node, int(targetIdx)))

        for i in inbetween:
            node, targetIdx, inbetweenIdx = i.split(".")
            output_inbetween.append(fnBs.TargetData(node, int(targetIdx), int(inbetweenIdx)))

        for i in output_inbetween:
            fnBs.resetInbetweenDelta(i, False)
            print(f"Reset {i.attr}")
