import maya.cmds as cmds
import maya.api.OpenMaya as om
from maya import OpenMayaUI as omui
from . import d_skin_cmd as command
try:
    from shiboken2 import wrapInstance
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from shiboken import wrapInstance
    from PySide.QtCore import *
    from PySide.QtGui import *
    

class BaseCallBack(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class UndoCallback(BaseCallBack):
    def __call__(self, *args):
        cmds.undoInfo(openChunk=1)
        try:
            return self.func(*self.args, **self.kwargs)
        finally:
            cmds.undoInfo(closeChunk=1)


class D_skinTool_ui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName("D_SkinTool_ui")
        self.setMinimumSize(QSize(300, 750))
        self.setMaximumSize(QSize(9999, 9999))
        self.resize(300, 800)
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.win_layout = QVBoxLayout()
        self.win_layout.setObjectName("win_layout")
        spacerItem = QSpacerItem(40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.win_layout.addItem(spacerItem)
        self.mesh_layout = QHBoxLayout()
        self.mesh_layout.setObjectName("mesh_layout")
        self.mesh_label = QLabel(self)
        self.mesh_label.setMinimumSize(QSize(70, 30))
        self.mesh_label.setMaximumSize(QSize(80, 40))
        self.mesh_label.setObjectName("mesh_label")
        self.mesh_layout.addWidget(self.mesh_label)
        self.mesh_line = QLineEdit(self, text='No Mesh')
        self.mesh_line.setEnabled(0)
        self.mesh_line.setMinimumSize(QSize(0, 20))
        self.mesh_line.setObjectName("mesh_line")
        self.mesh_layout.addWidget(self.mesh_line)
        self.load_btn = QPushButton(self)
        self.load_btn.setMinimumSize(QSize(54, 0))
        self.load_btn.setMaximumSize(QSize(40, 25))
        self.load_btn.setStyleSheet("background-color: rgb(55, 98, 112)")
        self.load_btn.setObjectName("load_btn")
        self.mesh_layout.addWidget(self.load_btn)
        self.win_layout.addLayout(self.mesh_layout)

        self.skinClusterNode_layout = QHBoxLayout()
        self.skinClusterNode_layout.setObjectName("mesh_layout")

        self.skinCluster_label = QLabel(self)
        self.skinCluster_label.setMinimumSize(QSize(70, 30))
        self.skinCluster_label.setMaximumSize(QSize(60, 40))
        self.skinCluster_label.setObjectName("mesh_label")
        self.skinClusterNode_layout.addWidget(self.skinCluster_label)

        self.skinClusterNode_line = QLineEdit(self)
        self.skinClusterNode_line.setMinimumSize(QSize(0, 20))
        self.skinClusterNode_line.setObjectName("skinClusterNode_line")
        self.skinClusterNode_line.setEnabled(0)
        self.skinClusterNode_layout.addWidget(self.skinClusterNode_line)
        self.win_layout.addLayout(self.skinClusterNode_layout)
        spacerItem1 = QSpacerItem(40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.win_layout.addItem(spacerItem1)
        self.add_layout = QHBoxLayout()
        self.add_layout.setObjectName("add_layout")
        self.addSkinGraph_btn = QPushButton(self)
        self.addSkinGraph_btn.setMinimumSize(QSize(0, 30))
        self.addSkinGraph_btn.setAutoFillBackground(False)
        self.addSkinGraph_btn.setStyleSheet("background-color: rgb(55, 98, 112)")
        self.addSkinGraph_btn.setObjectName("addSkinGraph_btn")
        self.add_layout.addWidget(self.addSkinGraph_btn)
        self.delSkinGraph_btn = QPushButton(self)
        self.delSkinGraph_btn.setMinimumSize(QSize(54, 30))
        self.delSkinGraph_btn.setMaximumSize(QSize(40, 40))
        self.delSkinGraph_btn.setStyleSheet("background-color: rgb(55, 98, 112)")
        self.delSkinGraph_btn.setObjectName("delSkinGraph_btn")
        self.add_layout.addWidget(self.delSkinGraph_btn)
        self.win_layout.addLayout(self.add_layout)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.addMask_btn = QPushButton(self)
        self.addMask_btn.setMaximumSize(QSize(60, 20))
        self.addMask_btn.setStyleSheet("background-color: rgb(55, 98, 112)")
        self.addMask_btn.setObjectName("addMask_btn")
        self.horizontalLayout.addWidget(self.addMask_btn)
        self.deleteMask_btn = QPushButton(self)
        self.deleteMask_btn.setMaximumSize(QSize(60, 20))
        self.deleteMask_btn.setStyleSheet("background-color: rgb(55, 98, 112)")
        self.deleteMask_btn.setObjectName("deleteMask_btn")
        self.horizontalLayout.addWidget(self.deleteMask_btn)
        self.win_layout.addLayout(self.horizontalLayout)
        # self.Mask List_line = QLineEdit(self,text='None',enabled=0)
        # self.win_layout.addWidget(self.Mask List_line)
        self.treeWidget = new_TreeWidget()
        self.treeWidget.setMinimumSize(QSize(200, 300))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setHeaderHidden(0)
        self.treeWidget.setHeaderLabels(['Mask List'])
        self.treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        # self.treeWidget.headerItem().setBackgroundColor(0,QColor(120, 120, 60))
        # self.treeWidget.headerItem().setTextColor(0,QColor(0, 200, 0))
        self.treeWidget.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.win_layout.addWidget(self.treeWidget)
        self.checkBox_layout = QHBoxLayout()
        self.checkBox_layout.setObjectName("checkBox_layout")
        self.isolated_checkBox = QCheckBox(self)
        self.isolated_checkBox.setObjectName("isolated_checkBox")
        self.autoRefresh_checkBox = QCheckBox(self)
        self.autoRefresh_checkBox.setObjectName("autoRefresh_checkBox")
        self.checkBox_layout.addWidget(self.autoRefresh_checkBox)
        self.checkBox_layout.addWidget(self.isolated_checkBox)
        self.win_layout.addLayout(self.checkBox_layout)
        self.filter_layout = QHBoxLayout()
        self.filter_layout.setObjectName("filter_layout")
        self.filter_label = QLabel(self)
        self.filter_label.setMinimumSize(QSize(0, 25))
        self.filter_label.setObjectName("filter_label")
        self.filter_layout.addWidget(self.filter_label)
        self.filter_line = QLineEdit(self)
        self.filter_line.setMinimumSize(QSize(0, 25))
        self.filter_line.setObjectName("filter_line")
        self.filter_layout.addWidget(self.filter_line)
        self.win_layout.addLayout(self.filter_layout)
        self.refresh_btn = QPushButton(self)
        self.refresh_btn.setMinimumSize(QSize(0, 25))
        self.refresh_btn.setStyleSheet("background-color: rgb(55, 98, 112)")
        self.refresh_btn.setObjectName("refresh_btn")
        self.win_layout.addWidget(self.refresh_btn)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.win_layout.addItem(spacerItem3)
        self.sendLayout = QVBoxLayout()
        self.win_layout.addLayout(self.sendLayout)
        self.preview_btn = QPushButton('Refresh Preview')
        self.preview_btn.setMinimumSize(QSize(0, 30))
        self.preview_btn.setStyleSheet("background-color: rgb(55, 98, 112)")
        self.sendLayout.addWidget(self.preview_btn)
        self.combine_btn = QPushButton(self)
        self.combine_btn.setMinimumSize(QSize(0, 50))
        self.combine_btn.setStyleSheet("background-color: rgb(55, 98, 112)")
        self.combine_btn.setObjectName("Combine_btn")
        self.win_layout.addWidget(self.combine_btn)
        self.By_Label = QLabel(self)
        self.By_Label.setMinimumSize(QSize(0, 20))
        self.By_Label.setMaximumSize(QSize(16777215, 40))
        self.By_Label.setTextFormat(Qt.AutoText)
        self.By_Label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.By_Label.setObjectName("By_Label")
        self.win_layout.addWidget(self.By_Label)
        self.progressBar = QProgressBar(self)
        self.progressBar.setEnabled(True)
        self.progressBar.setMaximumSize(QSize(16777215, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.win_layout.addWidget(self.progressBar)
        self.horizontalLayout_2.addLayout(self.win_layout)

        self.setWindowTitle("SkinTool  Donzy v1.0")
        self.mesh_label.setText("Mesh  :")
        self.load_btn.setText("Load")
        self.addSkinGraph_btn.setText("Create SkinGraph")
        self.delSkinGraph_btn.setText("Delete")
        self.refresh_btn.setText("Refresh List")
        self.addMask_btn.setText("Add Mask")
        self.deleteMask_btn.setText("Del Mask")
        self.autoRefresh_checkBox.setText("Auto Refresh")
        self.isolated_checkBox.setText("Isolated")
        self.filter_label.setText("Filter:")
        self.combine_btn.setText("Combine")
        self.By_Label.setText("By:Donzy")
        self.skinCluster_label.setText("SkinCluster  :")
        self.skinClusterNode_line.setText('No SkinCluster')
        self.progressBar.hide()
        self.By_Label.show()
        self.connect_btn()

    def openUI(self):
        def toMaya2017():
            # 2017
            # toMaya
            mayaMainWindowPtr = omui.MQtUtil.mainWindow()
            mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
            self.setParent(mayaMainWindow)
            self.setWindowFlags(Qt.Window)
            if cmds.workspaceControl('maya_SkinTool', q=1, ex=1):
                cmds.deleteUI('maya_SkinTool')
            dock = cmds.workspaceControl('maya_SkinTool', retain=True, label='SkinTool V1.0')
            dockLayout = cmds.paneLayout(configuration='single', p=dock)
            cmds.control('D_SkinTool_ui', e=True, p=dockLayout)

        def toMaya2016():
            mayaMainWindowPtr = omui.MQtUtil.mainWindow()
            mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
            self.setParent(mayaMainWindow)
            self.setWindowFlags(Qt.Window)
            if cmds.dockControl('maya_SkinTool', q=1, ex=1):
                cmds.deleteUI('maya_SkinTool')
            if cmds.window('maya_SkinTool_win', q=1, ex=1):
                cmds.deleteUI('maya_SkinTool_win')
            mayaWindow = cmds.window('maya_SkinTool', title='SkinTool V1.0')
            mayaWindow_layout = cmds.paneLayout(configuration='single', p=mayaWindow)
            dock = cmds.dockControl('maya_SkinTool', label='SkinTool V1.0', area='left', content=mayaWindow,
                                    allowedArea=['left', 'right'])
            cmds.control('D_SkinTool_ui', e=True, p=mayaWindow_layout)

        if int((cmds.about(v=1))) >= 2017:
            toMaya2017()
        else:
            toMaya2016()

    def connect_btn(self):
        self.load_btn.clicked.connect(UndoCallback(self.loadMesh))
        self.addMask_btn.clicked.connect(UndoCallback(self.addMask))
        self.deleteMask_btn.clicked.connect(UndoCallback(self.deleteMask))
        self.addSkinGraph_btn.clicked.connect(UndoCallback(self.createGraph))
        self.refresh_btn.clicked.connect(UndoCallback(self.refreshTreeView))
        self.filter_line.textChanged.connect(self.filterTreeWidget)
        self.preview_btn.clicked.connect(UndoCallback(self.sendToBlendShape))
        self.combine_btn.clicked.connect(UndoCallback(self.combinecommand))

    def loadMesh(self):
        mesh = command.loadMesh_cmd()
        skinNode = command.loadSkinNode_cmd()
        self.mesh_line.setText(mesh)
        self.skinClusterNode_line.setText(skinNode)
        self.treeWidget.setHeaderLabels([mesh.replace('_Mask_mesh', '')])
        self.refreshTreeView()

    def refreshTreeView(self):
        oldDict = self.treeWidget.getTreeWidgetDict()
        expandedDict = {}
        for x in oldDict:
            expandedDict.update({x.text(0): x.isExpanded()})
        self.treeWidget.clear()
        Dict = self.getMessageFromScene_cmd()
        self.addTreeViewChildren(Dict)
        newDict = self.treeWidget.getTreeWidgetDict()
        for x in newDict:
            if x.text(0) in expandedDict:
                x.setExpanded(expandedDict[x.text(0)])
        self.filterTreeWidget()

    def addTreeViewChildren(self, Dict):
        for x in sorted(Dict.keys()):
            c_children = sorted(Dict[x])
            maskItems = QTreeWidgetItem(self.treeWidget)
            maskItems.setSizeHint(0, QSize(100, 25))
            maskItems.setText(0, x)
            for i in c_children:
                secItems = QTreeWidgetItem(maskItems)
                secItems.setSizeHint(0, QSize(100, 18))
                secItems.setText(0, i)

    def getMessageFromScene_cmd(self):
        try:
            prefix = self.mesh_line.text().replace('_Mask_mesh', '')
            messageInfo = command.getMessageFromScene(prefix)
            maskList = messageInfo['meshList']
            treeDict = {}
            for x in maskList:
                treeDict.update({x: messageInfo[x]})
            return treeDict
        except:
            return {}

    def addMask(self):
        self.addMask_ui = name_ui('Name')
        self.addMask_ui.enter_btn.clicked.connect(UndoCallback(self.addMask_enter))
        self.addMask_ui.enter_btn.clicked.connect(self.addMask_ui.close)
        self.addMask_ui.show()

    def addMask_enter(self):
        prefix = self.mesh_line.text().replace('_Mask_mesh', '')
        na = self.addMask_ui.line.text()
        sk = command.addMask(prefix=prefix, name=na)[-1]
        self.skinClusterNode_line.setText(sk)
        self.refreshTreeView()

    def deleteMask(self):
        selectedItems = self.treeWidget.selectedItems()
        for x in selectedItems:
            na = x.text(0)
            prefix = self.mesh_line.text().replace('_Mask_mesh', '')
            na = na.replace(prefix + '_', '')
            na = na.replace('_mesh', '')
            sk = command.deleteMask(prefix=prefix, name=na)
        self.skinClusterNode_line.setText(sk)
        self.refreshTreeView()

    def deleteMask_enter(self):
        prefix = self.mesh_line.text().replace('_Mask_mesh', '')
        na = self.addMask_ui.line.text()
        sk = command.deleteMask(prefix=prefix, name=na)
        self.skinClusterNode_line.setText(sk)
        self.refreshTreeView()

    def createGraph(self):
        meshName = self.mesh_line.text()
        skinClusterName = self.skinClusterNode_line.text()
        if cmds.objExists(meshName) == False:
            om.MPxCommand().displayError('Please load mesh')
            return
        if cmds.objExists(skinClusterName) == True:
            self.create_ui = createGraph_ui()
            self.create_ui.TrueButton.clicked.connect(UndoCallback(self.createGraph_False))
            self.create_ui.TrueButton.clicked.connect(self.create_ui.close)
            self.create_ui.FalseButton.clicked.connect(UndoCallback(self.createGraph_True))
            self.create_ui.FalseButton.clicked.connect(self.create_ui.close)
            self.create_ui.show()
        else:
            self.createGraph_False()
        self.refreshTreeView()

    def createGraph_False(self):
        meshName = self.mesh_line.text()
        skinClusterName = self.skinClusterNode_line.text()
        re = command.createWeightGraph(mesh=meshName, prefix=meshName, convert=False)
        self.mesh_line.setText(command.loadMesh_cmd(re))
        self.skinClusterNode_line.setText(command.loadSkinNode_cmd(re))
        self.refreshTreeView()

    def createGraph_True(self):
        meshName = self.mesh_line.text()
        skinClusterName = self.skinClusterNode_line.text()
        re = command.createWeightGraph(mesh=meshName, prefix=meshName, convert=True)
        self.mesh_line.setText(command.loadMesh_cmd(re))
        self.skinClusterNode_line.setText(command.loadSkinNode_cmd(re))
        self.refreshTreeView()

    def addInfluence(self):
        mesh = self.treeWidget.selected()[-1]
        selectedInfluence = cmds.ls(sl=1)
        command.addInfluence(mesh, selectedInfluence)
        self.refreshTreeView()

    def removeInfluence(self):
        treeDict = self.treeWidget.getTreeWidgetDict_text()
        selected = self.treeWidget.selected()
        mesh = self.treeWidget.selectedItems()[-1].parent().text(0)
        treeSecList = []
        for x in treeDict.values():
            treeSecList = treeSecList + x
        influenceList = []
        for x in selected:
            if x in treeSecList:
                influenceList.append(x)
        command.removeInfluence(mesh, influenceList)
        self.refreshTreeView()

    def addSelectedAsMask(self):
        prefix = self.mesh_line.text().replace('_Mask_mesh', '')
        for x in cmds.ls(sl=1):
            maskJoint = command.addMask(prefix, x, x)[0]
            cmds.parentConstraint(x, maskJoint)
        self.refreshTreeView()

    def filterTreeWidget(self):
        text = self.filter_line.text().upper()
        treeDict = self.treeWidget.getTreeWidgetDict()
        if text != '':
            for x in treeDict:
                treeParentText = x.text(0).upper()
                x.setHidden(1)
                if text in treeParentText:
                    x.setHidden(0)
                for i in treeDict[x]:
                    treeChildText = i.text(0).upper()
                    i.setHidden(1)
                    if text in treeChildText:
                        i.setHidden(0)

    def sendToBlendShape(self):
        prefix = self.mesh_line.text().replace('_Mask_mesh', '')
        messageInfo = command.getMessageFromScene(prefix=prefix)
        maskMesh = messageInfo['maskMesh']
        outMesh = messageInfo['outMesh']
        meshList = messageInfo['meshList']
        blendShapeNode = command.getHistoryNode(outMesh, 'blendShape')
        command.sendToDeform(blendShapeNode, maskMesh, meshList)

    def sendToSkinCluster(self):
        prefix = self.mesh_line.text().replace('_Mask_mesh', '')
        messageInfo = command.getMessageFromScene(prefix=prefix)
        maskMesh = messageInfo['maskMesh']
        outMesh = messageInfo['outMesh']
        blendShapeNode = command.getHistoryNode(outMesh, 'blendShape')
        meshList = self.treeWidget.selected()
        command.sendToSkinCluster(blendShapeNode, maskMesh, meshList)

    def combinecommand(self):
        prefix = self.mesh_line.text().replace('_Mask_mesh', '')
        command.combinedWeights(prefix)


class name_ui(QWidget):
    def __init__(self, title):
        QWidget.__init__(self)
        self.title = title
        self.setWindowTitle(title)
        self.setFixedWidth(250)
        self.setFixedHeight(100)
        self.setWindowFlags(Qt.Window)
        self.setWindowModality(Qt.ApplicationModal)
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)
        self.v_layout.addWidget
        self.line = QLineEdit()
        self.line.setMinimumSize(QSize(0, 27))
        self.line.setMaximumSize(QSize(999, 27))
        self.line.setPlaceholderText('name')
        self.v_layout.addWidget(self.line)
        self.enter_btn = QPushButton('Enter')
        self.enter_btn.setMinimumSize(QSize(80, 25))
        self.enter_btn.setMaximumSize(QSize(80, 25))
        self.v_layout.addWidget(self.enter_btn, 0, Qt.AlignRight)
        for x in QApplication.topLevelWidgets():
            if x.windowTitle() == 'SkinTool V1.0':
                ui_position = x.pos()
                ui_size = x.size()
        self.move(ui_position + QPoint((ui_size / 2).width() - 125, (ui_size / 2).height() - 150))


class createGraph_ui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setFixedWidth(350)
        self.setFixedHeight(100)
        self.setWindowTitle('Convert win')
        self.setWindowFlags(Qt.Window)
        self.setWindowModality(Qt.ApplicationModal)
        self.createSkinGraph_ui_layout = QVBoxLayout()
        self.setLayout(self.createSkinGraph_ui_layout)
        self.createSkinGraph_ui_layout2 = QHBoxLayout()
        self.createSkinGraph_ui_layout3 = QHBoxLayout()
        self.createSkinGraph_ui_layout.addLayout(self.createSkinGraph_ui_layout2)
        self.createSkinGraph_ui_layout.addLayout(self.createSkinGraph_ui_layout3)
        self.createLabel = QLabel('This mesh already has skinCluster node')
        self.createSkinGraph_ui_layout2.addWidget(self.createLabel, 0, Qt.AlignCenter)
        self.TrueButton = QPushButton('Create New')
        self.FalseButton = QPushButton('Convert')
        self.createSkinGraph_ui_layout3.addWidget(self.TrueButton)
        self.createSkinGraph_ui_layout3.addWidget(self.FalseButton)
        self.move(QDesktopWidget().screenGeometry().width() / 2, QDesktopWidget().screenGeometry().height() / 2)


class new_TreeWidget(QTreeWidget):
    def __init__(self):
        super(new_TreeWidget, self).__init__()

    def mousePressEvent(self, event):
        super(new_TreeWidget, self).mousePressEvent(event)
        if event.buttons() == Qt.RightButton:
            self.maskItemsMenu()

    def isMask(self, item):
        dictInfo = self.getTreeWidgetDict_text()
        maskList = dictInfo.keys()
        if item in maskList:
            return True
        else:
            return False

    def isSecond(self, item):
        dictInfo = self.getTreeWidgetDict_text()
        secList = []
        for x in dictInfo.values():
            secList = secList + x
        if item in secList:
            return True
        else:
            return False

    def maskItemsMenu(self, enabled=True):
        popMenu = QMenu()
        self.addMask = popMenu.addAction('Add Mask')
        self.addMaskSelected = popMenu.addAction('Add Selected As Mask')
        self.deleteMask = popMenu.addAction('Delete Mask')
        popMenu.addSeparator()
        self.addInfluence = popMenu.addAction('Add Influence')
        self.removeInfluence = popMenu.addAction('Remove Influence')
        popMenu.addSeparator()
        self.updateBlendShapeWeight = popMenu.addAction('Update BlendShape Weight')
        self.updateSkinClusterWeight = popMenu.addAction('Update SkinCluster Weight')
        popMenu.addSeparator()
        self.reSkin = popMenu.addAction('Re Skin')
        self.addMask.triggered.connect(UndoCallback(self.addMask_cmd))
        self.addMaskSelected.triggered.connect(UndoCallback(self.addMaskSelected_cmd))
        self.deleteMask.triggered.connect(UndoCallback(self.deleteMask_cmd))
        self.addInfluence.triggered.connect(UndoCallback(self.addInfluence_cmd))
        self.removeInfluence.triggered.connect(self.removeInfluence_cmd)
        self.reSkin.triggered.connect(UndoCallback(self.reSkin_cmd))
        self.updateBlendShapeWeight.triggered.connect(UndoCallback(self.sendToBlendShape))
        self.updateSkinClusterWeight.triggered.connect(UndoCallback(self.sendToSkinCluster))
        try:
            if self.isMask(self.selected()[-1]):
                self.removeInfluence.setEnabled(0)
            if self.isSecond(self.selected()[-1]):
                self.deleteMask.setEnabled(0)
                self.updateBlendShapeWeight.setEnabled(0)
                self.updateSkinClusterWeight.setEnabled(0)
                self.reskin.setEnabled(0)
        except:
            self.deleteMask.setEnabled(0)
            self.addInfluence.setEnabled(0)
            self.removeInfluence.setEnabled(0)
            self.reSkin.setEnabled(0)
            self.updateBlendShapeWeight.setEnabled(0)
            self.updateSkinClusterWeight.setEnabled(0)
        popMenu.exec_(QCursor.pos())

    def selected(self):
        sel = [x.text(0) for x in self.selectedItems()]
        return sel

    def getTreeWidgetDict_text(self):
        treeWidget_dict = {}
        num = 0
        while self.topLevelItem(num):
            maskItem = self.topLevelItem(num)
            c_num = 0
            secJointList = []
            while maskItem.child(c_num):
                c_Item = maskItem.child(c_num).text(0)
                secJointList.append(c_Item)
                c_num = c_num + 1
            treeWidget_dict.update({maskItem.text(0): secJointList})
            num = num + 1
        return treeWidget_dict

    def getTreeWidgetDict(self):
        treeWidget_dict = {}
        num = 0
        while self.topLevelItem(num):
            maskItem = self.topLevelItem(num)
            c_num = 0
            secJointList = []
            while maskItem.child(c_num):
                c_Item = maskItem.child(c_num)
                secJointList.append(c_Item)
                c_num = c_num + 1
            treeWidget_dict.update({maskItem: secJointList})
            num = num + 1
        return treeWidget_dict

    def addMask_cmd(self):
        self.parent().addMask()

    def addMaskSelected_cmd(self):
        self.parent().addSelectedAsMask()

    def deleteMask_cmd(self):
        self.parent().deleteMask()

    def reSkin_cmd(self):
        sel = self.selectedItems()
        reSkinMesh = []
        for x in sel:
            if self.isMask(x.text(0)):
                reSkinMesh.append(x.text(0))
            if self.isSecond(x.text(0)):
                x.parent().text(0)
        reSkinMesh = list(set(reSkinMesh))
        for x in reSkinMesh:
            command.reSkin(x)

    def addInfluence_cmd(self):
        self.parent().addInfluence()

    def removeInfluence_cmd(self):
        self.parent().removeInfluence()

    def sendToSkinCluster(self):
        self.parent().sendToSkinCluster()

    def sendToBlendShape(self):
        prefix = self.parent().mesh_line.text().replace('_Mask_mesh', '')
        messageInfo = command.getMessageFromScene(prefix=prefix)
        maskMesh = messageInfo['maskMesh']
        outMesh = messageInfo['outMesh']
        meshList = self.selected()
        blendShapeNode = command.getHistoryNode(outMesh, 'blendShape')
        command.sendToDeform(blendShapeNode, maskMesh, meshList)
# a = D_skinTool_ui()
# a.openUI()
