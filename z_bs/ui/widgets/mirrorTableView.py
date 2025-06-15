from PySide2 import QtCore, QtWidgets, QtGui


class MirrorTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mirrorData = [("L", "R"),
                           ("Left", "Right"),
                           ("LF", "RT")]
        self.tableViewModel: QtGui.QStandardItemModel = None
        self.radioButtonList = []
        self._active_row = -1  # Used to store the index of the currently selected radiobutton row

        self.setup()

    def setup(self):
        self.tableViewModel = QtGui.QStandardItemModel()
        self.setModel(self.tableViewModel)

        self.verticalHeader().hide()

        self.tableViewModel.itemChanged.connect(self._tableView_changed)

        self.selectionModel().currentChanged.connect(self._selection_changed)

        self.set_mirror_data(self.mirrorData)
        # Ensure at least one item is selected by default after initial data setup
        self._ensure_default_selection()

    def _ensure_default_selection(self):
        """Ensures at least one radiobutton is selected, defaulting to the first row if none are."""
        if self._active_row == -1 and self.tableViewModel.rowCount() > 1:  # Check if there's at least one data row + empty row
            # If the model is not empty and no row is active, select the first data row
            if len(self.radioButtonList) > 0 and self.radioButtonList[0] is not None:
                self.radioButtonList[0].setChecked(True)
                self._active_row = 0

    def _selection_changed(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        """Updates radiobutton selection when table selection changes."""
        # If the selected column is the radiobutton column, auto-select the corresponding radiobutton
        if current.column() == 0:
            row = current.row()
            if 0 <= row < len(self.radioButtonList):
                radio_button = self.radioButtonList[row]
                if radio_button:
                    radio_button.setChecked(True)
                    # _active_row is already updated by _radio_button_toggled
        else:
            # If a different column is clicked, deselect all radiobuttons
            for radio_button in self.radioButtonList:
                radio_button.setChecked(False)
            self._active_row = -1

    def _create_tableViewItem(self, text=""):
        """Creates a centered QStandardItem."""
        item = QtGui.QStandardItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item

    def _tableView_changed(self, item):
        """
        Handles table data changes, including:
        1. Cleaning empty rows.
        2. Adding a new row when input occurs in the last row.
        3. Maintaining radiobutton state and ensuring default selection.
        """
        if self.blockSignals(True):
            try:
                current_data = self.get_mirror_data(include_empty_last_row=True)

                cleaned_data = []
                last_row_is_empty = True

                for i, (text1, text2) in enumerate(current_data):
                    if text1.strip() or text2.strip():
                        cleaned_data.append((text1, text2))
                        last_row_is_empty = False
                    elif i == len(current_data) - 1:
                        last_row_is_empty = True

                # If the last row was not empty, add a new empty row for input
                if not last_row_is_empty:
                    cleaned_data.append(("", ""))

                # Store the current active row before data refresh
                previous_active_row = self._active_row
                self.set_mirror_data(cleaned_data, previous_active_row=previous_active_row)

            finally:
                self.blockSignals(False)

            # After data is refreshed, ensure default selection
            self._ensure_default_selection()

    def get_mirror_data(self, include_empty_last_row=False):
        """
        Retrieves valid mirror data.
        - By default, it ignores all empty rows (including the last empty input row).
        - If include_empty_last_row is True, it will include the last potentially empty input row.
        """
        mirror_data = []
        row_count = self.tableViewModel.rowCount()

        limit_row = row_count - 1 if not include_empty_last_row else row_count

        for row in range(limit_row):
            item1 = self.tableViewModel.item(row, 1)
            item2 = self.tableViewModel.item(row, 2)

            text1 = item1.text() if item1 else ""
            text2 = item2.text() if item2 else ""

            if include_empty_last_row or text1.strip() or text2.strip():
                mirror_data.append((text1, text2))

        return mirror_data

    def set_mirror_data(self, data, previous_active_row=-1):
        """
        Sets the mirror data, ensuring correct header, empty row, and radiobutton states.
        Args:
            data (list): List of mirror data to set, e.g., [("L", "R"), ...].
            previous_active_row (int): The previously active radiobutton row index, used to restore selection.
        """
        # Clear old QRadioButton widgets
        for radio_button in self.radioButtonList:
            if radio_button.parentWidget():
                radio_button.parentWidget().deleteLater()
        self.radioButtonList.clear()
        self._active_row = -1  # Reset active row as widgets are being deleted

        self.tableViewModel.clear()

        self.tableViewModel.setHorizontalHeaderLabels(['', 'Pattern', 'Opposite'])
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.resizeSection(0, 30)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        for idx, row_data in enumerate(data):
            if len(row_data) == 2:
                row_items = [self._create_tableViewItem(""),
                             self._create_tableViewItem(row_data[0]),
                             self._create_tableViewItem(row_data[1])]
                self.tableViewModel.appendRow(row_items)

                radio_button_widget = self._create_radio_button_widget(idx)
                self.setIndexWidget(self.tableViewModel.index(idx, 0), radio_button_widget)

                # Try to restore the previous selection
                if idx == previous_active_row:
                    self.radioButtonList[idx].setChecked(True)
                    self._active_row = idx  # Update active row after successful restoration

        # Add an empty row for input if data is empty or the last row is not empty
        if not data or (data and (data[-1][0].strip() or data[-1][1].strip())):
            self.tableViewModel.appendRow([self._create_tableViewItem(), self._create_tableViewItem()])

    def _create_radio_button_widget(self, row):
        """
        Creates a QRadioButton widget and places it in a centered container.
        """
        radio_button = QtWidgets.QRadioButton(self)
        radio_button.row = row
        radio_button.toggled.connect(lambda checked: self._radio_button_toggled(checked, row))

        container_widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(container_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch()
        layout.addWidget(radio_button)
        layout.addStretch()
        container_widget.setLayout(layout)
        self.radioButtonList.append(radio_button)
        return container_widget

    def _radio_button_toggled(self, checked: bool, row: int):
        """Called when a radiobutton is checked or unchecked."""
        if checked:
            self._active_row = row
            # Ensure only one radiobutton is selected
            for i, rb in enumerate(self.radioButtonList):
                if i != row:
                    rb.setChecked(False)
        elif self._active_row == row:
            # If the currently active radiobutton is unchecked, clear the active row
            # This allows external code to force deselect all, if desired
            self._active_row = -1
            # Re-ensure default selection if all become unchecked
            QtCore.QTimer.singleShot(0, self._ensure_default_selection)

    def get_active_mirror_data(self):
        """
        Retrieves the second and third column data for the currently active (radiobutton selected) row.
        Returns None if no radiobutton is selected.
        """
        if self._active_row != -1 and 0 <= self._active_row < self.tableViewModel.rowCount() - 1:  # Exclude the empty input row
            item1 = self.tableViewModel.item(self._active_row, 1)
            item2 = self.tableViewModel.item(self._active_row, 2)

            text1 = item1.text() if item1 else ""
            text2 = item2.text() if item2 else ""

            if text1 and text2:
                return text1, text2
        return None
