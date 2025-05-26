from PySide2 import QtWidgets, QtCore, QtGui


class BsHeader:
    nameIdx = 0
    valueIdx = 1
    visIdx = 2
    name = "Name"
    value = "Value"
    vis = "Vis"
    headerList = [name, value, vis]


class SliderWithEdit(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SliderWithEdit, self).__init__(parent)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setChecked(True)
        self.textEdit = QtWidgets.QLineEdit(self)
        self.textEdit.setFixedWidth(80)
        validator = QtGui.QDoubleValidator(0.0, 1.0, 3, self.textEdit)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.textEdit.setValidator(validator)
        self.textEdit.setText("0.000")
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setRange(0, 1000)
        self.slider.setValue(0)
        self.rowLayout = QtWidgets.QHBoxLayout(self)
        self.rowLayout.addWidget(self.textEdit)
        self.rowLayout.addWidget(self.slider)
        self.rowLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.slider.valueChanged.connect(self.on_slider_changed)
        self.textEdit.editingFinished.connect(self.on_edit_finished)
        self.checkBox.stateChanged.connect(self.on_checkBox_changed)
        self.checkBox.setStyleSheet("""
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
                border-radius: 8px;
                border: 2px solid #000000;
                background: white;
            }
            QCheckBox::indicator:checked {
                background: #ffffff;
                border: 2px solid #000000;
            }
            QCheckBox::indicator:unchecked {
                background: #000000;
                border: 2px solid #323232;
            }
        """)
        self.slider.setStyleSheet("""            
            QSlider::groove:horizontal {
                height: 6px;
                background: #000000;
            }
            QSlider::sub-page:horizontal {
                background: #000000;
            }
            QSlider::add-page:horizontal {
                background: #5f5f5f;
            }
            QSlider::handle:horizontal {
                width: 10px;
                margin: -6px 0;
                background: #bababa;
                border-radius: 5px;
            }
            QSlider::groove:horizontal:disabled,
            QSlider::sub-page:horizontal:disabled,
            QSlider::add-page:horizontal:disabled {
                background: #404040;
            }
            QSlider::handle:horizontal:disabled {
                background: #404040;
            }
        """)

    def on_slider_changed(self, value):
        float_val = value / 1000.0
        self.textEdit.setText("{:.3f}".format(float_val))

    def on_edit_finished(self):
        try:
            val = float(self.textEdit.text())
            val = max(0.0, min(1.0, val))
            self.slider.setValue(int(val * 1000))
        except ValueError:
            pass

    def on_checkBox_changed(self, state):
        enabled = state == QtCore.Qt.Checked
        self.slider.setEnabled(enabled)
        self.textEdit.setEnabled(enabled)



class BsManagerWidget(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.bsList = []
        # 连接项目修改信号
        self.itemChanged.connect(self._handle_item_changed)

    def init_ui(self):
        self.setHeaderLabels(BsHeader.headerList)
        self.header().swapSections(0, 2)
        self.header().swapSections(1, 2)
        header = self.header()
        header.resizeSection(BsHeader.visIdx, 40)
        header.setSectionResizeMode(BsHeader.visIdx, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(BsHeader.nameIdx, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(BsHeader.valueIdx, QtWidgets.QHeaderView.Stretch)
        header.setSectionsMovable(False)

    def _handle_item_changed(self, item, column):
        """处理项目名称修改事件"""
        if column == BsHeader.nameIdx:
            instance = item.data(BsHeader.nameIdx, QtCore.Qt.UserRole)
            if instance:
                new_name = item.text(BsHeader.nameIdx)
                instance.on_name_edited(new_name)



class ItemHierarchy:
    """层级项基类，管理树形结构关系"""
    def __init__(self, name="item", parent=None, tree=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.tree = tree
        
        # 创建对应的Qt项
        self.item = QtWidgets.QTreeWidgetItem([name, "", ""])
        # 存储自身引用到Qt项
        self.item.setData(BsHeader.nameIdx, QtCore.Qt.UserRole, self)
        
        # 自动添加项到树结构
        if isinstance(parent, ItemHierarchy):
            parent.add_child(self)
        elif tree is not None and parent is None:
            tree.addTopLevelItem(self.item)
            
        # 初始化界面组件
        self.bsWidget = SliderWithEdit()
        self.tree.setItemWidget(self.item, BsHeader.valueIdx, self.bsWidget)
        self.tree.setItemWidget(self.item, BsHeader.visIdx, self.bsWidget.checkBox)
        self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)

    def on_name_edited(self, new_name):
        """名称修改时的处理（可被子类重写）"""
        print(f"Name changed to: {new_name}")
        self.name = new_name

        
    def add_child(self, child):
        self.children.append(child)
        self.item.addChild(child.item)
        child.parent = self
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, parent={self.parent.name if self.parent else None})"
    
    def __str__(self):
        return self.name


class Item_BlendShape(ItemHierarchy):
    def __init__(self, name="BlendShapeRoot", tree=None):
        super().__init__(name=name, tree=tree)

class Item_Target(ItemHierarchy):
    def __init__(self, parent, name="bsTarget"):
        if not isinstance(parent, Item_BlendShape):
            raise ValueError("Target item must be a child of BlendShape item.")
        self.tree = parent.tree
        super().__init__(name=name, parent=parent,tree=self.tree)

class Item_Inbetween(ItemHierarchy):
    def __init__(self, parent, name="bsItem"):
        if not isinstance(parent, Item_Target):
            raise ValueError("Target item must be a child of BlendShape item.")
        self.tree = parent.parent.tree
        super().__init__(name=name, parent=parent,tree=self.tree)
        self.tree.removeItemWidget(self.item,BsHeader.visIdx)
        self.bsWidget.slider.setStyleSheet("""            
            QSlider::groove:horizontal {
                height: 6px;
                background: #5f5f5f;
            }
            QSlider::handle:horizontal {
                width: 4px;
                margin: -6px 0;
                background: #a05f36;
                border-radius: 5px;
            }""")






manager = BsManagerWidget()

manager.show()


# 创建混合形状根节点（自动添加到tree）
blendshape_root = Item_BlendShape("BlendShapeRoot", tree=manager)

# 创建目标节点
target1 = Item_Target(blendshape_root, "bsTarget1")
target2 = Item_Target(blendshape_root, "bsTarget2")

# 创建中间节点
item1 = Item_Inbetween(target1, "bsItemA")
item2 = Item_Inbetween(target1, "bsItemB")