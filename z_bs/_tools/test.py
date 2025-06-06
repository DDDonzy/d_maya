import sys
from PySide2.QtGui import QPainter, QColor, QPaintEvent, QPainterPath, QMouseEvent, QFocusEvent, QKeyEvent
from PySide2.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout, QPushButton, QColorDialog,QLabel
from PySide2.QtCore import Qt, Property, Slot, Signal, QEvent

class ProgressLineEdit(QLineEdit):
    """
    一个通过成员函数高度配置的进度输入框。
    先创建，后通过 set...() 方法进行详细配置。
    """
    valueChanged = Signal(float)
    
    def __init__(self, parent=None):
        super(ProgressLineEdit, self).__init__(parent)

        # --- 1. 所有属性都在内部初始化为默认值 ---
        self._value_type = float
        self._min_val = 0.0
        self._max_val = 100.0
        self._is_ranged = True
        
        self._radius = 15
        self._border_width = 2
        self._background_color = QColor(45, 45, 45)
        self._fill_color = QColor(42, 130, 218)
        
        self._is_dragging = False
        self._has_dragged = False
        self._drag_start_pos = None
        self._drag_start_public_value = 0.0
        self._value_on_press = 0.0
        self._normalized_value = 0.0
        self._public_value = 0.0
        
        # --- 2. 基础设置 ---
        self.setReadOnly(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignCenter)
        self.update_stylesheet()
        self.setValue(self._public_value)

        if QApplication.instance():
            QApplication.instance().installEventFilter(self)

    # ===================================================================
    # 公开的配置 API (成员函数)
    # ===================================================================
    @Slot(float, float)
    def set_range(self, min_value: float, max_value: float):
        """设置控件的数值范围。"""
        self._min_val = min_value
        self._max_val = max_value
        self._is_ranged = (self._min_val is not None and 
                           self._max_val is not None and 
                           self._max_val > self._min_val)
        # 范围改变后，重新验证当前值
        self.setValue(self.getValue())
        self.update()

    @Slot(type)
    def set_value_type(self, value_type: type):
        """设置数值类型 (int 或 float)。"""
        if value_type in (int, float):
            self._value_type = value_type
            # 类型改变后，重新格式化文本
            self.update_text_from_value()

    @Slot(QColor)
    def set_background_color(self, color: QColor):
        """设置背景颜色。"""
        self._background_color = color
        self.update()

    @Slot(QColor)
    def set_fill_color(self, color: QColor):
        """设置填充条颜色。"""
        self._fill_color = color
        self.update()
        
    @Slot(int)
    def set_border_radius(self, radius: int):
        """设置边框圆角。"""
        self._radius = max(0, radius)
        self.update_stylesheet() # 圆角需要更新样式表
        self.update()

    @Slot(int)
    def set_border_width(self, width: int):
        """设置边框宽度。"""
        self._border_width = max(0, width)
        self.update_stylesheet()
        self.update()

    # ===================================================================
    # 值处理与文本更新 (逻辑不变)
    # ===================================================================
    def getValue(self) -> float:
        return self._public_value

    @Slot(float)
    def setValue(self, val: float):
        try:
            new_value = self._value_type(val)
        except (ValueError, TypeError):
            return
        if self._is_ranged:
            new_value = max(self._min_val, min(self._max_val, new_value))
        
        if self._public_value != new_value or self.text() != str(new_value):
            self._public_value = new_value
            if self._is_ranged:
                val_range = self._max_val - self._min_val
                self._normalized_value = (new_value - self._min_val) / val_range if val_range > 0 else 0
            
            self.update_text_from_value()
            self.update()
            self.valueChanged.emit(self._public_value)

    value = Property(float, getValue, setValue)

    def update_text_from_value(self):
        if self._value_type == int:
             self.setText(str(int(self._public_value)))
        else:
            rounded_value = round(self._public_value, 3)
            self.setText(f'{rounded_value:g}')

    def update_stylesheet(self):
        self.setStyleSheet(f"""QLineEdit {{ 
                                   background-color: transparent; 
                                   color: white; 
                                   border: {self._border_width}px solid rgb(85, 85, 85); 
                                   border-radius: {self._radius}px; 
                               }}""")
    
    # ===================================================================
    # 核心绘制与事件处理 (逻辑不变)
    # ===================================================================
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        clip_path = QPainterPath()
        clip_path.addRoundedRect(self.rect(), self._radius, self._radius)
        painter.setClipPath(clip_path)
        painter.fillRect(self.rect(), self._background_color)
        if self._is_ranged and self.isReadOnly():
            fill_width = self.width() * self._normalized_value
            fill_rect = self.rect()
            fill_rect.setWidth(int(fill_width))
            painter.fillRect(fill_rect, self._fill_color)
        super(ProgressLineEdit, self).paintEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not self.isReadOnly():
            self.clearFocus()
            return
        super(ProgressLineEdit, self).keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.isReadOnly():
            self._value_on_press = self._public_value
            self._is_dragging = True
            self._has_dragged = False 
            self._drag_start_pos = event.pos()
            self._drag_start_public_value = self._public_value
            event.accept()
            return
        super(ProgressLineEdit, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging:
            self._has_dragged = True
            dx = event.pos().x() - self._drag_start_pos.x()
            if self._is_ranged:
                val_range = self._max_val - self._min_val
                delta_value = (dx / self.width()) * val_range
                new_value = self._drag_start_public_value + delta_value
            else:
                if self._drag_start_public_value == 0:
                    new_value = (dx / self.width()) * 100.0
                else:
                    drag_percentage = dx / self.width()
                    sensitivity = 1.0
                    new_value = self._drag_start_public_value * (1.0 + drag_percentage * sensitivity)
            self.setValue(new_value)
            event.accept()
            return
        super(ProgressLineEdit, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._is_dragging and event.button() == Qt.LeftButton and not self._has_dragged:
            self.setReadOnly(False)
            self.setCursor(Qt.IBeamCursor)
            self.selectAll()
            self.update()
            self._is_dragging = False
            self._has_dragged = False
            event.accept()
            return
        self._is_dragging = False
        self._has_dragged = False
        super(ProgressLineEdit, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        super(ProgressLineEdit, self).mouseDoubleClickEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        try:
            val_from_text = self._value_type(self.text())
            self.setValue(val_from_text)
        except ValueError:
            self.update_text_from_value()
        self.setReadOnly(True)
        self.setCursor(Qt.PointingHandCursor)
        self.update()
        super(ProgressLineEdit, self).focusOutEvent(event)
        
    def eventFilter(self, watched_obj, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            if not self.isReadOnly():
                widget_under_mouse = QApplication.widgetAt(event.globalPos())
                if widget_under_mouse != self:
                    self.clearFocus()
        return super(ProgressLineEdit, self).eventFilter(watched_obj, event)

# --- 用于演示和测试的主窗口 ---
class TestWidget(QWidget):
    def __init__(self):
        super(TestWidget, self).__init__()
        self.setWindowTitle("成员函数配置 ProgressLineEdit")
        self.setStyleSheet("QWidget { background-color: rgb(60, 60, 60); color: white; }")
        self.setGeometry(100, 100, 400, 200)

        # 1. 创建一个默认的实例
        self.info_label = QLabel("通过下方的按钮来配置这个控件：")
        self.edit = ProgressLineEdit(self)
        
        # 2. 使用成员函数进行配置
        self.edit.set_range(0, 255)
        self.edit.set_value_type(int)
        self.edit.set_border_radius(5)
        self.edit.set_border_width(2)
        self.edit.setValue(128)

        # 3. 创建一个按钮来动态改变颜色
        self.color_button = QPushButton("动态改变填充颜色")
        self.color_button.clicked.connect(self.change_color)

        layout = QVBoxLayout(self)
        layout.addWidget(self.info_label)
        layout.addWidget(self.edit)
        layout.addWidget(self.color_button)
        layout.addStretch()

    def change_color(self):
        """弹出一个颜色选择对话框，并用选中的颜色更新控件"""
        color = QColorDialog.getColor(self.edit._fill_color, self, "选择颜色")
        if color.isValid():
            self.edit.set_fill_color(color)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TestWidget()
    widget.show()
    sys.exit(app.exec_())