import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QTreeView, QWidget, 
                              QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                              QAbstractItemView, QStyleFactory, QHeaderView)
from PySide2.QtCore import Qt, QAbstractItemModel, QModelIndex, QSize
from PySide2.QtGui import QStandardItemModel, QStandardItem
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance


class WidgetTreeModel(QStandardItemModel):
    def __init__(self, root_widget, parent=None):
        super().__init__(parent)
        self.root_widget = root_widget
        self.setHorizontalHeaderLabels(['controlType', 'objectName', 'hex(id)', 'vis'])
        self.populate_tree()

    def populate_tree(self, parent_item=None, parent_widget=None):
        if parent_item is None:
            # Add root widget as the first item
            root_type_item = QStandardItem(self.root_widget.__class__.__name__)
            root_name_item = QStandardItem(self.root_widget.objectName() if self.root_widget.objectName() else "unnamed")
            root_id_item = QStandardItem(hex(id(self.root_widget)))
            
            root_vis_item = QStandardItem()
            root_vis_item.setCheckable(True)
            root_vis_item.setCheckState(Qt.Checked if self.root_widget.isVisible() else Qt.Unchecked)
            root_vis_item.setEditable(False)
            
            for item in [root_type_item, root_name_item, root_id_item, root_vis_item]:
                item.setData(self.root_widget, Qt.UserRole + 1)
            
            self.appendRow([root_type_item, root_name_item, root_id_item, root_vis_item])
            parent_item = root_type_item
            parent_widget = self.root_widget

        for child in parent_widget.children():
            if isinstance(child, QWidget):
                # Create items for each column
                type_item = QStandardItem(child.__class__.__name__)
                name_item = QStandardItem(child.objectName() if child.objectName() else "unnamed")
                id_item = QStandardItem(hex(id(child)))
                
                # Create a checkable item for visibility
                vis_item = QStandardItem()
                vis_item.setCheckable(True)
                vis_item.setCheckState(Qt.Checked if child.isVisible() else Qt.Unchecked)
                vis_item.setEditable(False)
                
                # Store widget reference in each item
                for item in [type_item, name_item, id_item, vis_item]:
                    item.setData(child, Qt.UserRole + 1)
                
                # Add items to the parent row
                parent_item.appendRow([type_item, name_item, id_item, vis_item])
                
                # Recursively populate children
                self.populate_tree(type_item, child)


class WidgetDebugTool(QMainWindow):
    def __init__(self, target_widget):
        super().__init__()
        self.target_widget = target_widget
        self.current_selected_widget = None
        self.previous_style = ""  # To store previous style of selected widget
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Maya Widget Debug Tool')
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Tree view
        self.tree_view = QTreeView()
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Set model
        self.model = WidgetTreeModel(self.target_widget)
        self.tree_view.setModel(self.model)
        
        # Resize columns to contents
        self.tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree_view.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tree_view.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tree_view.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        self.reset_btn = QPushButton("Reset Style")
        self.reset_btn.clicked.connect(self.reset_style)
        
        control_layout.addStretch()
        control_layout.addWidget(self.reset_btn)
        
        # Add widgets to main layout
        layout.addWidget(self.tree_view)
        layout.addWidget(control_panel)
        
        # Connect signals
        self.tree_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.model.itemChanged.connect(self.on_item_changed)
        
        # Expand items up to depth 5
        self.expand_to_depth(5)
    
    def expand_to_depth(self, depth, parent_index=QModelIndex(), current_depth=0):
        """Recursively expand tree items up to specified depth"""
        if current_depth > depth:
            return
            
        # Expand current item
        self.tree_view.expand(parent_index)
        
        # Recursively expand children
        for row in range(self.model.rowCount(parent_index)):
            child_index = self.model.index(row, 0, parent_index)
            self.expand_to_depth(depth, child_index, current_depth + 1)
    
    def on_selection_changed(self, selected, deselected):
        # Reset previous selection's style first
        if self.current_selected_widget:
            self.current_selected_widget.setStyleSheet(self.previous_style)
        
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]  # Get the first column index
            item = self.model.itemFromIndex(index)
            widget = item.data(Qt.UserRole + 1)
            self.current_selected_widget = widget
            
            # Store current style before applying highlight
            self.previous_style = widget.styleSheet()
            
            # Apply highlight style
            widget.setStyleSheet(
                "border: 1px solid red;"
            )
    
    def on_item_changed(self, item):
        # Only handle visibility changes (column 3)
        if item.column() == 3:
            widget = item.data(Qt.UserRole + 1)
            if widget:
                widget.setVisible(item.checkState() == Qt.Checked)
    
    def reset_style(self):
        if self.current_selected_widget:
            self.current_selected_widget.setStyleSheet("")
            self.previous_style = ""


def getMayaMainWindow():
    """Get Maya's main window as QWidget"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


def getMayaControl(name):
    """Find Maya control by name and return as QWidget"""
    maya_control = omui.MQtUtil.findControl(name)
    if maya_control:
        return wrapInstance(int(maya_control), QWidget)
    return None



# Example usage
if __name__ == "__main__":
    from maya import cmds
    # Create and show debug tool
    cmds.ShapeEditor()
    cmds.refresh(f=1)
    bsPanelName =cmds.getPanel(type="shapePanel")[0]
    debug_tool = WidgetDebugTool(getMayaControl(bsPanelName))
    debug_tool.show()
    
