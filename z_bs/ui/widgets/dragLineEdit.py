import sys
from PySide2.QtGui import QPainter, QColor, QPaintEvent, QPainterPath, QMouseEvent, QFocusEvent, QKeyEvent
from PySide2.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout, QPushButton, QColorDialog, QLabel
from PySide2.QtCore import Qt, Property, Slot, Signal, QEvent


class DragLineEdit(QLineEdit):
    """拖拽式LineEdit"""
    valueChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 默认配置
        self._value_type = float  # 值类型，默认为float
        self._min_val = 0  # 最小值
        self._max_val = 20  # 最大值
        self._radius = 3  # 圆角半径
        self._border_width = 1  # 边框宽度
        self._background_color = QColor(45, 45, 45)  # 背景颜色
        self._fill_color = QColor(85, 85, 85)  # 填充颜色

        # 拖拽状态
        self._is_dragging = False  # 是否正在拖拽
        self._has_dragged = False  # 是否已经拖拽过
        self._drag_start_pos = None  # 拖拽开始位置
        self._drag_start_value = 0.0  # 拖拽开始时的值
        self._normalized_value = 0.0  # 归一化值（0-1之间）
        self._public_value = 0.0  # 公共值，外部访问的值

        self._init_ui()

    def _init_ui(self):
        """初始化UI设置"""
        self.setReadOnly(True)  # 设置为只读模式
        self.setCursor(Qt.PointingHandCursor)  # 设置鼠标指针为手型
        self._update_stylesheet()  # 更新样式表
        # self.setValue(0.0)  # 初始化值为0.0

    @property
    def _is_ranged(self):
        """检查是否有有效范围"""
        return (self._max_val is not None)\
            and (self._min_val is not None)\
            and (self._max_val > self._min_val)
    # 配置API

    @Slot(float, float)
    def set_range(self, min_val: float, max_val: float):
        self._min_val, self._max_val = min_val, max_val
        self.setValue(self.getValue())
        self.update()

    @Slot(type)
    def set_value_type(self, value_type: type):
        if value_type in (int, float):
            self._value_type = value_type
            self._update_text()

    @Slot(QColor)
    def set_background_color(self, color: QColor):
        self._background_color = color
        self.update()

    @Slot(QColor)
    def set_fill_color(self, color: QColor):
        self._fill_color = color
        self.update()

    @Slot(int)
    def set_border_radius(self, radius: int):
        self._radius = max(0, radius)
        self._update_stylesheet()
        self.update()

    @Slot(int)
    def set_border_width(self, width: int):
        self._border_width = max(0, width)
        self._update_stylesheet()
        self.update()

    # 值处理
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

        if self._public_value != new_value:
            self._public_value = new_value
            if self._is_ranged:
                val_range = self._max_val - self._min_val
                self._normalized_value = (new_value - self._min_val) / val_range if val_range > 0 else 0

            self._update_text()
            self.update()
            self.valueChanged.emit(self._public_value)

    value = Property(float, getValue, setValue)

    def _update_text(self):
        """更新显示文本"""
        if self._value_type == int:
            self.setText(str(int(self._public_value)))
        else:
            self.setText(f'{round(self._public_value, 3):g}')

    def _update_stylesheet(self):
        """更新样式表"""
        self.setStyleSheet(f"""
            QLineEdit {{ 
                background-color: transparent; 
                color: white; 
                border: {self._border_width}px solid rgb({self._background_color.red()},{self._background_color.green()},{self._background_color.blue()},{self._background_color.alpha()}); 
                border-radius: {self._radius}px; 
                
            }}
        """)

    # 绘制
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 创建圆角裁剪路径
        clip_path = QPainterPath()
        clip_path.addRoundedRect(self.rect(), self._radius, self._radius)
        painter.setClipPath(clip_path)

        # 绘制背景
        painter.fillRect(self.rect(), self._background_color)

        # 绘制进度条
        if self._is_ranged and self.isReadOnly():
            fill_width = int(self.width() * self._normalized_value)
            fill_rect = self.rect()
            fill_rect.setWidth(fill_width)
            painter.fillRect(fill_rect, self._fill_color)

        super().paintEvent(event)

    # 事件处理
    def keyPressEvent(self, event: QKeyEvent):
        # 处理回车键和Enter键
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not self.isReadOnly():
            self.clearFocus()
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        # 处理鼠标左键按下事件
        if event.button() == Qt.LeftButton and self.isReadOnly():
            self._is_dragging = True
            self._has_dragged = False
            self._drag_start_pos = event.pos()
            self._drag_start_value = self._public_value
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        # 处理鼠标移动事件
        if self._is_dragging:
            self._has_dragged = True
            dx = event.pos().x() - self._drag_start_pos.x()

            if self._is_ranged:
                val_range = self._max_val - self._min_val
                delta_value = (dx / self.width()) * val_range
                new_value = self._drag_start_value + delta_value
            else:
                if self._drag_start_value == 0:
                    new_value = (dx / self.width())
                else:
                    drag_percentage = dx / self.width()
                    new_value = self._drag_start_value * (1.0 + drag_percentage)

            self.setValue(new_value)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._is_dragging and event.button() == Qt.LeftButton:
            if not self._has_dragged:
                self.setReadOnly(False)
                self.setCursor(Qt.IBeamCursor)
                self.selectAll()
                self.update()
            self._is_dragging = False
            self._has_dragged = False
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        try:
            val_from_text = self._value_type(self.text())
            self.setValue(val_from_text)
        except ValueError:
            self._update_text()

        self.setReadOnly(True)
        self.setCursor(Qt.PointingHandCursor)
        self.update()
        super().focusOutEvent(event)

    def eventFilter(self, watched_obj, event: QEvent) -> bool:
        if (event.type() == QEvent.MouseButtonPress and
            not self.isReadOnly() and
                QApplication.widgetAt(event.globalPos()) != self):
            self.clearFocus()
        return super().eventFilter(watched_obj, event)

if __name__ == "__main__":

    edit = DragLineEdit()
    edit.set_value_type(int)
    edit.set_range(0,10)
    edit.show()
