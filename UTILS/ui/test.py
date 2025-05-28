import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QTreeView, QPushButton, QVBoxLayout, QWidget
from PySide2.QtGui import QStandardItemModel, QStandardItem

class SimpleTreeView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TreeView Insert Widget")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建界面
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建 TreeView 和模型
        self.tree_view = QTreeView()
        layout.addWidget(self.tree_view)
        
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name", "Age", "Action"])
        
        # 添加数据行
        for i in range(3):
            row = [QStandardItem(f"用户{i+1}"), QStandardItem(f"{20+i}"), QStandardItem("")]
            model.appendRow(row)
        
        self.tree_view.setModel(model)
        
        # 关键代码：在第3列插入按钮 widget
        for row in range(model.rowCount()):
            button = QPushButton(f"按钮{row+1}")
            button.clicked.connect(lambda checked, r=row: print(f"点击了第{r}行的按钮"))
            
            # 使用 setIndexWidget 插入 widget
            index = model.index(row, 2)  # 第3列(索引2)
            self.tree_view.setIndexWidget(index, button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleTreeView()
    window.show()
    sys.exit(app.exec_())