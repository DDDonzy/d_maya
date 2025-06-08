from PySide2.QtGui import QPainter, QColor, QPaintEvent, QPainterPath, QMouseEvent, QFocusEvent, QKeyEvent
from PySide2.QtWidgets import QApplication, QLineEdit
from PySide2.QtCore import Qt, Property, Slot, Signal, QEvent


class DragLineEdit(QLineEdit):
    """拖拽式LineEdit"""
    valueChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 默认配置
        self._value_type = float
        self._min_val = None
        self._max_val = None
        self._radius = 3
        self._border_width = 1
        self._background_color = QColor(45, 45, 45)
        self._fill_color = QColor(85, 85, 85)

        # 拖拽状态
        self._is_dragging = False
        self._has_dragged = False
        self._drag_start_pos = None
        self._drag_start_value = 0.0
        self._normalized_value = 0.0
        self._public_value = 0.0

        self._init_ui()

    def _init_ui(self):
        """初始化UI设置"""
        self.setReadOnly(True)
        self.setCursor(Qt.SizeHorCursor) # 已根据您之前的请求修改为水平光标
        self._update_stylesheet()

    @property
    def _is_ranged(self):
        """
        【修改】检查是否有有效范围。
        现在，只要设置了最大值或最小值中任何一个，就认为是有范围的。
        并且，只有在两者都设置的情况下，才检查 max > min。
        """
        if self._min_val is not None and self._max_val is not None:
            return self._max_val > self._min_val
        # 只要有一个限制，就认为是有范围的
        return self._min_val is not None or self._max_val is not None

    # 配置API
    @Slot(float, float)
    def set_range(self, min_val, max_val):
        """
        【修改】允许 min_val 或 max_val 为 None。
        """
        self._min_val = min_val
        self._max_val = max_val
        # 重新设置当前值，以确保它符合新的范围
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

        # --- 【核心修改】 ---
        # 分别独立地检查和应用最小值和最大值限制
        if self._min_val is not None:
            new_value = max(self._min_val, new_value)
        
        if self._max_val is not None:
            new_value = min(self._max_val, new_value)
        # ---------------------

        if self._public_value != new_value:
            self._public_value = new_value
            
            # 归一化值的计算逻辑也需要更新
            if self._min_val is not None and self._max_val is not None:
                val_range = self._max_val - self._min_val
                self._normalized_value = (new_value - self._min_val) / val_range if val_range > 0 else 0
            else:
                # 如果范围不完整，则进度条没有明确意义，可以不显示或显示为0
                self._normalized_value = 0

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
                color: rgb(200, 200, 200);
                border: {self._border_width}px solid rgb({self._background_color.red()},{self._background_color.green()},{self._background_color.blue()},{self._background_color.alpha()}); 
                border-radius: {self._radius}px; 
                padding-left: 10px;
            }}
        """)

    # 绘制
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        clip_path = QPainterPath()
        clip_path.addRoundedRect(self.rect(), self._radius, self._radius)
        painter.setClipPath(clip_path)

        painter.fillRect(self.rect(), self._background_color)

        # 仅在同时具有min和max时才绘制进度条
        if self._min_val is not None and self._max_val is not None and self.isReadOnly():
            fill_width = int(self.width() * self._normalized_value)
            fill_rect = self.rect()
            fill_rect.setWidth(fill_width)
            painter.fillRect(fill_rect, self._fill_color)

        super().paintEvent(event)

    # 事件处理
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not self.isReadOnly():
            self.clearFocus()
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.isReadOnly():
            self._is_dragging = True
            self._has_dragged = False
            self._drag_start_pos = event.pos()
            self._drag_start_value = self._public_value
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging:
            self._has_dragged = True
            dx = event.pos().x() - self._drag_start_pos.x()
            
            # 对于无上限或无下限的拖拽，增量计算需要一个“灵敏度”
            # 这里我们简化处理，假设拖拽整个控件宽度等于改变10个单位（如果类型是int）或1.0（如果类型是float）
            sensitivity = 10.0 if self._value_type == int else 1.0
            
            # 如果有完整的范围，则按比例计算
            if self._min_val is not None and self._max_val is not None:
                val_range = self._max_val - self._min_val
                delta_value = (dx / self.width()) * val_range
                new_value = self._drag_start_value + delta_value
            else:
                # 否则，按灵敏度计算
                delta_value = (dx / self.width()) * sensitivity
                new_value = self._drag_start_value + delta_value

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
        self.setCursor(Qt.SizeHorCursor) # 恢复水平光标
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
