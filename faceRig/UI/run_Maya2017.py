# !/usr/bin/python
# -*- coding: utf-8 -*-
from imp import reload
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from maya import OpenMayaUI as omui, cmds
from shiboken2 import wrapInstance
mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


from pymel.core import *
from ..rigging.fit import *
from ..rigging.rigTool import *
from ..rigging.spherePath import *
from ..rigging import rig


import UI.mainProgress as mainProgress
class Ui_RigTools(object):
    def __init__(self):
        if cmds.dockControl('Facial_RigTool', q=True, ex=True):
            cmds.deleteUI('Facial_RigTool')
        mayaWindow = cmds.window(title='Facial_RigTool')
        mayaLayout = cmds.paneLayout(configuration='single')
        cmds.dockControl("Facial_RigTool", l='Facial Rig Tool', w=450, area = 'left', content=mayaWindow, allowedArea=['left', 'right'])
        self.ui = QWidget()
        self.setupUi(self.ui)
        self.ui.setParent(mayaMainWindow)
        self.ui.setWindowFlags(Qt.Window)
        cmds.control('RigTools', e=True, p=mayaLayout)

        self.Face_Button.clicked.connect(self.face_load)
        self.EyeBall_Button.clicked.connect(self.eyeBall_load)
        self.UpperTeeth_Button.clicked.connect(self.upperTeeth_load)
        self.LowerTeeth_Button.clicked.connect(self.lowerTeeth_load)
        self.Tongue_Button.clicked.connect(self.tongue_load)
        self.Other_Button.clicked.connect(self.other_load)

        self.ImportSkeleton_Button.clicked.connect(self.importFit)
        self.TeethSecond_Button.clicked.connect(self.importTeethSecond)
        self.CtrlsVisibility_Button.clicked.connect(self.positionCtrlsVisibility)
        self.LatticeVisibility_Button.clicked.connect(self.latticeVisibility)
        self.LocalVisibility_Button.clicked.connect(self.localRotateAxes)
        self.MouthPathVisibility_Button.clicked.connect(self.addMouthPath)
        self.Mirror_Button.clicked.connect(self.mirror)
        self.MirrorDuplicate_Button.clicked.connect(self.mirrorDuplicate)
        self.Rigging_Button.clicked.connect(self.rig)

        self.ImportMatrix_Button.clicked.connect(self.importMatrix)
        self.ExportMatrix_Button.clicked.connect(self.exportMatrix)
        self.AddMatrix_Button.clicked.connect(self.addMatrix)
        self.DeleteMatrix_Button.clicked.connect(self.deleteMatrix)
        self.MirrorMatrix_Button.clicked.connect(self.mirrorMatrix)
        self.MirrorMatrixWeight_Button.clicked.connect(self.mirrorMatrixWeight)
        self.FindParent_Button.clicked.connect(self.getParentOBJ)
        self.FindChildren_Button.clicked.connect(self.getChildrenOBJ)
        self.setWeight_Button.clicked.connect(self.findWeightObj)

        self.IsolateSkin_Button
        self.IsolateLattice_Button
        self.IsolateSecond_Button
        self.IsolateOutput_Button
        if objExists('M_Head_Position'):
            self.info = PyNode('M_Head_Position')
            try:
                self.Face_LineEdit.setText(self.info.faceGeo.get())
                self.EyeBall_LineEdit.setText(self.info.eyeBallGeo.get())
                self.UpperTeeth_LineEdit.setText(self.info.teethUpperGeo.get())
                self.LowerTeeth_LineEdit.setText(self.info.teethLowerGeo.get())
                self.Tongue_LineEdit.setText(self.info.tongueGeo.get())
                self.Other_LineEdit.setText(self.info.allOtherGeo.get())
            except:
                pass
    def setupUi(self, RigTools):
        RigTools.setObjectName("RigTools")
        RigTools.setWindowModality(Qt.NonModal)
        RigTools.setEnabled(True)
        RigTools.resize(500, 750)
        #RigTools.setMinimumSize(QSize(500, 750))
        self.verticalLayout = QVBoxLayout(RigTools)
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.Load_Layout = QVBoxLayout()
        self.Load_Layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.Load_Layout.setObjectName("Load_Layout")
        self.Face_Layout = QHBoxLayout()
        self.Face_Layout.setObjectName("Face_Layout")
        self.Face_Label = QLabel(RigTools)
        self.Face_Label.setMinimumSize(QSize(110, 0))
        self.Face_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Face_Label.setObjectName("Face_Label")
        self.Face_Layout.addWidget(self.Face_Label)
        self.Face_LineEdit = QLineEdit(RigTools)
        self.Face_LineEdit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Face_LineEdit.setObjectName("Face_LineEdit")
        self.Face_Layout.addWidget(self.Face_LineEdit)
        self.Face_Button = QPushButton(RigTools)
        self.Face_Button.setMinimumSize(QSize(80, 0))
        self.Face_Button.setObjectName("Face_Button")
        self.Face_Layout.addWidget(self.Face_Button)
        self.Load_Layout.addLayout(self.Face_Layout)
        self.EyeBall_Layout = QHBoxLayout()
        self.EyeBall_Layout.setObjectName("EyeBall_Layout")
        self.EyeBall_Label = QLabel(RigTools)
        self.EyeBall_Label.setMinimumSize(QSize(110, 0))
        self.EyeBall_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.EyeBall_Label.setObjectName("EyeBall_Label")
        self.EyeBall_Layout.addWidget(self.EyeBall_Label)
        self.EyeBall_LineEdit = QLineEdit(RigTools)
        self.EyeBall_LineEdit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.EyeBall_LineEdit.setObjectName("EyeBall_LineEdit")
        self.EyeBall_Layout.addWidget(self.EyeBall_LineEdit)
        self.EyeBall_Button = QPushButton(RigTools)
        self.EyeBall_Button.setMinimumSize(QSize(80, 0))
        self.EyeBall_Button.setObjectName("EyeBall_Button")
        self.EyeBall_Layout.addWidget(self.EyeBall_Button)
        self.Load_Layout.addLayout(self.EyeBall_Layout)
        self.UpperTeeth_Layout = QHBoxLayout()
        self.UpperTeeth_Layout.setObjectName("UpperTeeth_Layout")
        self.UpperTeeth_Label = QLabel(RigTools)
        self.UpperTeeth_Label.setMinimumSize(QSize(110, 0))
        self.UpperTeeth_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.UpperTeeth_Label.setObjectName("UpperTeeth_Label")
        self.UpperTeeth_Layout.addWidget(self.UpperTeeth_Label)
        self.UpperTeeth_LineEdit = QLineEdit(RigTools)
        self.UpperTeeth_LineEdit.setObjectName("UpperTeeth_LineEdit")
        self.UpperTeeth_Layout.addWidget(self.UpperTeeth_LineEdit)
        self.UpperTeeth_Button = QPushButton(RigTools)
        self.UpperTeeth_Button.setMinimumSize(QSize(80, 0))
        self.UpperTeeth_Button.setObjectName("UpperTeeth_Button")
        self.UpperTeeth_Layout.addWidget(self.UpperTeeth_Button)
        self.Load_Layout.addLayout(self.UpperTeeth_Layout)
        self.LowerTeeth_Layout = QHBoxLayout()
        self.LowerTeeth_Layout.setObjectName("LowerTeeth_Layout")
        self.LowerTeeth_Label = QLabel(RigTools)
        self.LowerTeeth_Label.setMinimumSize(QSize(110, 0))
        self.LowerTeeth_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.LowerTeeth_Label.setObjectName("LowerTeeth_Label")
        self.LowerTeeth_Layout.addWidget(self.LowerTeeth_Label)
        self.LowerTeeth_LineEdit = QLineEdit(RigTools)
        self.LowerTeeth_LineEdit.setObjectName("LowerTeeth_LineEdit")
        self.LowerTeeth_Layout.addWidget(self.LowerTeeth_LineEdit)
        self.LowerTeeth_Button = QPushButton(RigTools)
        self.LowerTeeth_Button.setMinimumSize(QSize(80, 0))
        self.LowerTeeth_Button.setObjectName("LowerTeeth_Button")
        self.LowerTeeth_Layout.addWidget(self.LowerTeeth_Button)
        self.Load_Layout.addLayout(self.LowerTeeth_Layout)
        self.Tongue_Layout = QHBoxLayout()
        self.Tongue_Layout.setObjectName("Tongue_Layout")
        self.Tongue_Label = QLabel(RigTools)
        self.Tongue_Label.setMinimumSize(QSize(110, 0))
        self.Tongue_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Tongue_Label.setObjectName("Tongue_Label")
        self.Tongue_Layout.addWidget(self.Tongue_Label)
        self.Tongue_LineEdit = QLineEdit(RigTools)
        self.Tongue_LineEdit.setObjectName("Tongue_LineEdit")
        self.Tongue_Layout.addWidget(self.Tongue_LineEdit)
        self.Tongue_Button = QPushButton(RigTools)
        self.Tongue_Button.setMinimumSize(QSize(80, 0))
        self.Tongue_Button.setObjectName("Tongue_Button")
        self.Tongue_Layout.addWidget(self.Tongue_Button)
        self.Load_Layout.addLayout(self.Tongue_Layout)
        self.Other_Layout = QHBoxLayout()
        self.Other_Layout.setObjectName("Other_Layout")
        self.Other_Label = QLabel(RigTools)
        self.Other_Label.setMinimumSize(QSize(110, 0))
        self.Other_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Other_Label.setObjectName("Other_Label")
        self.Other_Layout.addWidget(self.Other_Label)
        self.Other_LineEdit = QLineEdit(RigTools)
        self.Other_LineEdit.setObjectName("Other_LineEdit")
        self.Other_Layout.addWidget(self.Other_LineEdit)
        self.Other_Button = QPushButton(RigTools)
        self.Other_Button.setMinimumSize(QSize(80, 0))
        self.Other_Button.setObjectName("Other_Button")
        self.Other_Layout.addWidget(self.Other_Button)
        self.Load_Layout.addLayout(self.Other_Layout)
        self.verticalLayout.addLayout(self.Load_Layout)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.Import_Layout = QVBoxLayout()
        self.Import_Layout.setObjectName("Import_Layout")
        self.ImportSkeleton_Button = QPushButton(RigTools)
        self.ImportSkeleton_Button.setObjectName("ImportSkeleton_Button")
        self.Import_Layout.addWidget(self.ImportSkeleton_Button)
        self.TeethSecond_Button = QPushButton(RigTools)
        self.TeethSecond_Button.setObjectName("TeethSecond_Button")
        self.Import_Layout.addWidget(self.TeethSecond_Button)
        self.Visibility_Layout = QHBoxLayout()
        self.Visibility_Layout.setObjectName("Visibility_Layout")
        self.CtrlsVisibility_Button = QPushButton(RigTools)
        self.CtrlsVisibility_Button.setObjectName("CtrlsVisibility_Button")
        self.Visibility_Layout.addWidget(self.CtrlsVisibility_Button)
        self.LatticeVisibility_Button = QPushButton(RigTools)
        self.LatticeVisibility_Button.setObjectName("LatticeVisibility_Button")
        self.Visibility_Layout.addWidget(self.LatticeVisibility_Button)
        self.LocalVisibility_Button = QPushButton(RigTools)
        self.LocalVisibility_Button.setObjectName("LocalVisibility_Button")
        self.Visibility_Layout.addWidget(self.LocalVisibility_Button)
        self.MouthPathVisibility_Button = QPushButton(RigTools)
        self.MouthPathVisibility_Button.setObjectName("MouthPathVisibility_Button")
        self.Visibility_Layout.addWidget(self.MouthPathVisibility_Button)
        self.Import_Layout.addLayout(self.Visibility_Layout)
        self.Mirror_Layout = QHBoxLayout()
        self.Mirror_Layout.setObjectName("Mirror_Layout")
        self.Mirror_Button = QPushButton(RigTools)
        self.Mirror_Button.setObjectName("Mirror_Button")
        self.Mirror_Layout.addWidget(self.Mirror_Button)
        self.MirrorDuplicate_Button = QPushButton(RigTools)
        self.MirrorDuplicate_Button.setObjectName("MirrorDuplicate_Button")
        self.Mirror_Layout.addWidget(self.MirrorDuplicate_Button)
        self.Import_Layout.addLayout(self.Mirror_Layout)
        self.Rigging_Layout = QVBoxLayout()
        self.Rigging_Layout.setObjectName("Rigging_Layout")
        self.Rigging_Button = QPushButton(RigTools)
        self.Rigging_Button.setMinimumSize(QSize(0, 40))
        self.Rigging_Button.setObjectName("Rigging_Button")
        self.Rigging_Layout.addWidget(self.Rigging_Button)
        self.Import_Layout.addLayout(self.Rigging_Layout)
        self.verticalLayout.addLayout(self.Import_Layout)
        spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.Rig_Layout = QVBoxLayout()
        self.Rig_Layout.setObjectName("Rig_Layout")
        self.ImportMatrix_Layout = QHBoxLayout()
        self.ImportMatrix_Layout.setObjectName("ImportMatrix_Layout")
        self.ImportMatrix_Button = QPushButton(RigTools)
        self.ImportMatrix_Button.setObjectName("ImportMatrix_Button")
        self.ImportMatrix_Layout.addWidget(self.ImportMatrix_Button)
        self.ExportMatrix_Button = QPushButton(RigTools)
        self.ExportMatrix_Button.setObjectName("ExportMatrix_Button")
        self.ImportMatrix_Layout.addWidget(self.ExportMatrix_Button)
        self.Rig_Layout.addLayout(self.ImportMatrix_Layout)
        self.Add_Layout = QHBoxLayout()
        self.Add_Layout.setObjectName("Add_Layout")
        self.AddMatrix_Button = QPushButton(RigTools)
        self.AddMatrix_Button.setObjectName("AddMatrix_Button")
        self.Add_Layout.addWidget(self.AddMatrix_Button)
        self.DeleteMatrix_Button = QPushButton(RigTools)
        self.DeleteMatrix_Button.setObjectName("DeleteMatrix_Button")
        self.Add_Layout.addWidget(self.DeleteMatrix_Button)
        self.Rig_Layout.addLayout(self.Add_Layout)
        self.MirrorMatrix_Layout = QHBoxLayout()
        self.MirrorMatrix_Layout.setObjectName("MirrorMatrix_Layout")
        self.MirrorMatrix_Button = QPushButton(RigTools)
        self.MirrorMatrix_Button.setObjectName("MirrorMatrix_Button")
        self.MirrorMatrix_Layout.addWidget(self.MirrorMatrix_Button)
        self.MirrorMatrixWeight_Button = QPushButton(RigTools)
        self.MirrorMatrixWeight_Button.setObjectName("MirrorMatrixWeight_Button")
        self.MirrorMatrix_Layout.addWidget(self.MirrorMatrixWeight_Button)
        self.Rig_Layout.addLayout(self.MirrorMatrix_Layout)
        self.Find_Layout = QHBoxLayout()
        self.Find_Layout.setObjectName("Find_Layout")
        self.FindParent_Button = QPushButton(RigTools)
        self.FindParent_Button.setObjectName("FindParent_Button")
        self.Find_Layout.addWidget(self.FindParent_Button)
        self.FindChildren_Button = QPushButton(RigTools)
        self.FindChildren_Button.setObjectName("FindChildren_Button")
        self.Find_Layout.addWidget(self.FindChildren_Button)
        self.Rig_Layout.addLayout(self.Find_Layout)
        self.setWeight_Button = QPushButton(RigTools)
        self.setWeight_Button.setMinimumSize(QSize(0, 40))
        self.setWeight_Button.setObjectName("setWeight_Button")
        self.Rig_Layout.addWidget(self.setWeight_Button)
        self.verticalLayout.addLayout(self.Rig_Layout)
        spacerItem3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.Isolate_Layout = QVBoxLayout()
        self.Isolate_Layout.setObjectName("Isolate_Layout")
        self.IsolateSkin_Button = QPushButton(RigTools)
        self.IsolateSkin_Button.setObjectName("IsolateSkin_Button")
        self.Isolate_Layout.addWidget(self.IsolateSkin_Button)
        self.IsolateSecond_Button = QPushButton(RigTools)
        self.IsolateSecond_Button.setObjectName("IsolateSecond_Button")
        self.Isolate_Layout.addWidget(self.IsolateSecond_Button)
        self.IsolateLattice_Button = QPushButton(RigTools)
        self.IsolateLattice_Button.setObjectName("IsolateLattice_Button")
        self.Isolate_Layout.addWidget(self.IsolateLattice_Button)
        self.IsolateOutput_Button = QPushButton(RigTools)
        self.IsolateOutput_Button.setObjectName("IsolateOutput_Button")
        self.Isolate_Layout.addWidget(self.IsolateOutput_Button)
        self.verticalLayout.addLayout(self.Isolate_Layout)
        spacerItem4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)

        self.retranslateUi(RigTools)
        QMetaObject.connectSlotsByName(RigTools)

    def retranslateUi(self, RigTools):
        RigTools.setWindowTitle(QApplication.translate("RigTools", "Facial Rig Tools", None))
        self.Face_Label.setText(QApplication.translate("RigTools", "Face Geometry", None))
        self.Face_Button.setText(QApplication.translate("RigTools", "Load", None))
        self.EyeBall_Label.setText(QApplication.translate("RigTools", "EyeBall Geometry", None))
        self.EyeBall_Button.setText(QApplication.translate("RigTools", "Load", None))
        self.UpperTeeth_Label.setText(QApplication.translate("RigTools", "UpperTeeth Geometry", None))
        self.UpperTeeth_Button.setText(QApplication.translate("RigTools", "Load", None))
        self.LowerTeeth_Label.setText(QApplication.translate("RigTools", "LowerTeeth Geometry", None))
        self.LowerTeeth_Button.setText(QApplication.translate("RigTools", "Load", None))
        self.Tongue_Label.setText(QApplication.translate("RigTools", "Tongue Geometry", None))
        self.Tongue_Button.setText(QApplication.translate("RigTools", "Load", None))
        self.Other_Label.setText(QApplication.translate("RigTools", "All/Other Geometry", None))
        self.Other_Button.setText(QApplication.translate("RigTools", "Load", None))
        self.ImportSkeleton_Button.setText(QApplication.translate("RigTools", "Import Skeleton", None))
        self.TeethSecond_Button.setText(QApplication.translate("RigTools", "Teeth Second OFF", None))
        self.CtrlsVisibility_Button.setText(QApplication.translate("RigTools", "Ctrls Visibility", None))
        self.LatticeVisibility_Button.setText(QApplication.translate("RigTools", "Lattice Visibility", None))
        self.LocalVisibility_Button.setText(QApplication.translate("RigTools", "Local Axis", None))
        self.MouthPathVisibility_Button.setText(QApplication.translate("RigTools", "MouthPath OFF", None))
        self.Mirror_Button.setText(QApplication.translate("RigTools", "Mirror", None))
        self.MirrorDuplicate_Button.setText(QApplication.translate("RigTools", "Mirror Duplicate", None))
        self.Rigging_Button.setText(QApplication.translate("RigTools", "Rigging", None))
        self.ImportMatrix_Button.setText(QApplication.translate("RigTools", "Import Matrix", None))
        self.ExportMatrix_Button.setText(QApplication.translate("RigTools", "Export Matrix", None))
        self.AddMatrix_Button.setText(QApplication.translate("RigTools", "Add Matrix", None))
        self.DeleteMatrix_Button.setText(QApplication.translate("RigTools", "Delete Matrix", None))
        self.MirrorMatrix_Button.setText(QApplication.translate("RigTools", "Mirror Matrix", None))
        self.MirrorMatrixWeight_Button.setText(QApplication.translate("RigTools", "Mirror Matrix Weight", None))
        self.FindParent_Button.setText(QApplication.translate("RigTools", "Find Parent", None))
        self.FindChildren_Button.setText(QApplication.translate("RigTools", "Find Children", None))
        self.setWeight_Button.setText(QApplication.translate("RigTools", "Set Weight", None))
        self.IsolateSkin_Button.setText(QApplication.translate("RigTools", "Isolate Skin Mesh", None))
        self.IsolateSecond_Button.setText(QApplication.translate("RigTools", "Isolate Lattice Mesh", None))
        self.IsolateLattice_Button.setText(QApplication.translate("RigTools", "Isolate Second Mesh", None))
        self.IsolateOutput_Button.setText(QApplication.translate("RigTools", "Isolate Output Mesh", None))
    def closeExistingWindow(self):
        for qt in QApplication.topLevelWidgets():
            try:
                if qt.windowTitle() == u'Facial Rig Tools':
                    qt.close()
            except:pass
    def importFit(self):
        createFaceFitSkeleton()
    def positionCtrlsVisibility(self):
        positionCtrlsVisibility()
    def latticeVisibility(self):
        latticeVisibility()
    def addMouthPath(self):
        addMouthPath()
        if self.MouthPathVisibility_Button.text() == 'MouthPath ON':
            self.MouthPathVisibility_Button.setText('MouthPath OFF')
        else:self.MouthPathVisibility_Button.setText('MouthPath ON')
    def localRotateAxes(self):
        localRotateAxes()
    def mirror(self):
        mirrorTransform(duplicateMode=0)
    def mirrorDuplicate(self):
        mirrorTransform(duplicateMode=1)
    def rig(self):
        faceGeo = []
        EyeBallGeo = []
        upperTeethGeo = []
        lowerTeethGeo = []
        tongueGeo = []
        otherGeo = []
        if self.Face_LineEdit.text() != '' :faceGeo = eval(self.Face_LineEdit.text())
        if self.EyeBall_LineEdit.text() != '' :EyeBallGeo = eval(self.EyeBall_LineEdit.text())
        if self.UpperTeeth_LineEdit.text() != '' :upperTeethGeo = eval(self.UpperTeeth_LineEdit.text())
        if self.LowerTeeth_LineEdit.text() != '' :lowerTeethGeo = eval(self.LowerTeeth_LineEdit.text())
        if self.Tongue_LineEdit.text() != '' :tongueGeo = eval(self.Tongue_LineEdit.text())
        if self.Other_LineEdit.text() != '' :otherGeo = eval(self.Other_LineEdit.text())
        rig.rig(faceGeo = faceGeo , EyeBallGeo = EyeBallGeo , upperTeethGeo = upperTeethGeo , lowerTeethGeo = lowerTeethGeo , tongueGeo = tongueGeo , otherGeo = otherGeo)
    def importMatrix(self):
        matrix.importMtx()
    def exportMatrix(self):
        matrix.exportMtx()
    def getParentOBJ(self):
        matrix.findParent(selected()[0],selectMode = 1)
    def getChildrenOBJ(self):
        matrix.findChildren(selected()[0],selectMode = 1)
    def addMatrix(self):
        addMtx_UI = addMatrix_UI(self.ui)
    def deleteMatrix(self):
        matrix.deleteMatrix2()
    def findWeightObj(self):
        matrix.findWeightObj(selected()[0],selectMode=1)
    def face_load(self):
        loadString = str([x.name() for x in selected()])
        self.Face_LineEdit.setText(loadString)
        try:self.info.faceGeo.set(loadString)
        except:pass
    def eyeBall_load(self):
        loadString = str([x.name() for x in selected()])
        self.EyeBall_LineEdit.setText(loadString)
        try:self.info.eyeBallGeo.set(loadString)
        except:pass
    def upperTeeth_load(self):
        loadString = str([x.name() for x in selected()])
        self.UpperTeeth_LineEdit.setText(loadString)
        try:self.info.teethUpperGeo.set(loadString)
        except:pass
    def lowerTeeth_load(self):
        loadString = str([x.name() for x in selected()])
        self.LowerTeeth_LineEdit.setText(loadString)
        try:self.info.teethLowerGeo.set(loadString)
        except:pass
    def tongue_load(self):
        loadString = str([x.name() for x in selected()])
        self.Tongue_LineEdit.setText(loadString)
        try:self.info.tongueGeo.set(loadString)
        except:pass
    def other_load(self):
        loadString = str([x.name() for x in selected()])
        self.Other_LineEdit.setText(loadString)
        try:self.info.allOtherGeo.set(loadString)
        except:pass
    def importTeethSecond(self):
        addTeethSecond()
        if self.TeethSecond_Button.text() == 'Teeth Second ON':
            self.TeethSecond_Button.setText('Teeth Second OFF')
        else:self.TeethSecond_Button.setText('Teeth Second ON')
    def mirrorMatrix(self):
        matrix.mirrorMtx()
    def mirrorMatrixWeight(self):
        matrix.mirrorWeight()
class addMatrix_UI(QWidget):
    def __init__(self , win):
        QWidget.__init__(self)
        self.closeExistingWindow()
        self.setupUi()
        self.setParent(win)
        self.setWindowFlags(Qt.Window) 
        self.show()
    def setupUi(self):
        self.setObjectName("self")
        self.resize(200, 200)
        self.setMinimumSize(QSize(200, 200))
        self.setMaximumSize(QSize(200, 200))
        self.verticalLayout_6 = QVBoxLayout(self)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem)
        self.checkBox = QCheckBox(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setChecked(True)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_6.addWidget(self.checkBox)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem1)
        self.checkBox_2 = QCheckBox(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_6.addWidget(self.checkBox_2)
        spacerItem2 = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem2)
        self.pushButton = QPushButton(self)
        self.pushButton.setMinimumSize(QSize(0, 50))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_6.addWidget(self.pushButton)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        self.pushButton.clicked.connect(self.add)
    def retranslateUi(self):
        self.setWindowTitle(QApplication.translate("self", "AddMatrixSetting", None, -1))
        self.checkBox.setText(QApplication.translate("self", "Matrix", None, -1))
        self.checkBox_2.setText(QApplication.translate("self", "SDK", None, -1))
        self.pushButton.setText(QApplication.translate("self", "Add Matrix", None, -1))
    def closeExistingWindow(self):
        for qt in QApplication.topLevelWidgets():
            try:
                if qt.windowTitle() == u'AddMatrixSetting':
                    qt.close()
            except:pass
    def add(self) :
        parentGRP = []
        if self.checkBox.isChecked() :
            parentGRP.append('CTL_Matrix')
        if self.checkBox_2.isChecked():
            parentGRP.append('CTL_SDK')
        with UndoChunk():
            parentCtl = selected()[0]
            childrenCtl = selected()[1:]
            for x in childrenCtl:
                matrix.addMatrix( parentCtl=parentCtl, childCtl=x, childCtlOffect=x.name()+'_Matrix' , attrPlace='', value=1 , parentGRP = parentGRP)