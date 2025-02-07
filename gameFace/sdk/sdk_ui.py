from PySide2 import QtWidgets, QtCore
import maya.cmds as cmds
from UTILS.ui.getMayaMainWindow import getMayaMainWindow
from gameFace.sdk.planeControls import importSDK

# 你提供的列表
my_list = importSDK()

class ListWidgetExample(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(getMayaMainWindow())
        
        self.setWindowTitle("List Widget Example")
        self.setGeometry(100, 100, 300, 600)  # 扩大窗口高度
        
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # 创建 QLineEdit 用于输入过滤关键词
        self.filter_line_edit = QtWidgets.QLineEdit(self)
        self.filter_line_edit.setPlaceholderText("Filter...")
        self.filter_line_edit.textChanged.connect(self.filter_list)  # 连接过滤功能
        
        # 创建 QListWidget
        self.list_widget = QtWidgets.QListWidget()
        
        # 将列表元素添加到 QListWidget
        self.items = []  # 保存添加的列表项，用于过滤时匹配
        for item in my_list:
            list_item = QtWidgets.QListWidgetItem(item.name)
            self.items.append(list_item)
            self.list_widget.addItem(list_item)
        
        # 连接选中事件
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        
        # 创建 Result 按钮
        self.result_button = QtWidgets.QPushButton("Set")
        self.result_button.clicked.connect(self.on_result_clicked)
        # flip current
        self.flipCurrent_button = QtWidgets.QPushButton("Flip Current Pose")
        self.flipCurrent_button.clicked.connect(self.on_result_clicked)
        # flip all
        self.flipAll_button = QtWidgets.QPushButton("Flip All Pose")
        self.flipAll_button.clicked.connect(self.on_result_clicked)
        # flip all
        self.mirror_button = QtWidgets.QPushButton("Mirror self Pose")
        self.mirror_button.clicked.connect(self.on_result_clicked)
        
        # 将过滤框、QListWidget 和按钮添加到布局
        self.layout.addWidget(self.filter_line_edit)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.result_button)
        self.layout.addWidget(self.flipCurrent_button)
        self.layout.addWidget(self.flipAll_button)
        self.layout.addWidget(self.mirror_button)
    
    def on_item_clicked(self, item):
        # 打印选中的元素
        print("Selected item:", item.text())
    
    def on_result_clicked(self):
        # 获取当前选中的项
        selected_item = self.list_widget.currentItem()
        if selected_item:
            print("Result button clicked. Selected item is:", selected_item.text())
        else:
            print("Result button clicked. No item is selected.")
    
    def filter_list(self):
        filter_text = self.filter_line_edit.text().lower()  # 获取用户输入的过滤关键词，并转为小写
        
        for item in self.items:
            item.setHidden(filter_text not in item.text().lower())  # 隐藏不匹配的项

# 显示 UI
def show_ui():
    global dialog
    try:
        dialog.close()
    except:
        pass
    dialog = ListWidgetExample()
    dialog.show()

# 运行 UI
show_ui()
