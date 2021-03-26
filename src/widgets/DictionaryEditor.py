"""
class ListItem(QWidget):
    removed = pyqtSignal(object)
    changed_key = pyqtSignal(object)
    changed_value = pyqtSignal(object)

    def __init__(self, autocomplete_key = []):
        super().__init__()


        self.autocomplete_key = QCompleter(autocomplete_key)
        self.autocomplete_key.setCaseSensitivity(Qt.CaseInsensitive)
        self.initUI()

    def initUI(self):
        hLayout = QHBoxLayout()

        self.enable = QCheckBox()
        self.enable.setChecked(True)

        self.name = QLineEdit() 
        self.name.setCompleter( self.autocomplete_key )
        self.name.textEdited.connect( self._fireChangedKey )

        self.value = QLineEdit() 
        self.value.textEdited.connect( self._fireChangedValue )

        self.remove = QPushButton("Delete")
        self.remove.clicked.connect( self._fireRemoved )

        hLayout.addWidget(self.enable)
        hLayout.addWidget(self.name)
        hLayout.addWidget(self.value)
        hLayout.addWidget(self.remove)
        hLayout.setAlignment(Qt.AlignTop)

        self.setLayout(hLayout)

    def _fireRemoved(self):
        self.removed.emit(self)

    def _fireChangedKey(self):
        self.changed_key.emit(self)

    def _fireChangedValue(self):
        self.changed_value.emit(self)

    def getKey(self):
        return self.name.text()

    def getValue(self):
        return self.value.text()

    def isEnabled(self):
        return self.enable.isChecked()

class List(QWidget):
    def __init__(self):
        super().__init__()
        self.items = []
        self.initUI()

        self.addItem()

    def initUI(self):
        hLayout = QVBoxLayout()
        hLayout.setContentsMargins(0,0,0,0)
        hLayout.setSpacing(0)
        hLayout.setAlignment(Qt.AlignTop)
        self.setLayout(hLayout)

    @pyqtSlot(object)
    def removeItem(self, item):
        self.layout().removeWidget(item)
        self.items.remove(item)

    @pyqtSlot(object)
    def _handleChanged(self, item):
        if self.items[-1] == item and item.getKey() != "":
            self.addItem()

    def addItem(self):
        item = ListItem()
        item.removed.connect(self.removeItem)

        item.changed_key.connect(self._handleChanged)
        item.changed_value.connect(self._handleChanged)

        self.items.append( item )
        self.layout().addWidget(item)

    def getValues(self):
        response = {}
        for i in self.items:
            enabled = i.isEnabled()
            key = i.getKey()
            value = i.getValue()

            if enabled and key != "":
                response[key] = value

        return response
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt 
class DictionaryEditor(QTableWidget):
    def __init__(self):
        super().__init__(0,3)
        self.initUI()

        self.addItem(None, None)

    def initUI(self):
        self.horizontalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.verticalHeader().hide()

        self.cellChanged.connect( self._handleCellChanged )

    def _handleCellChanged(self, row,col):
        item = self.itemAt(row, col)
        total_rows = self.rowCount()
        if col == 0 and row == total_rows - 1 and item.text() != "" :
            self.addItem(None, None)

    def removeItem(self):
        button = self.sender()
        parent = button.parent()
        row = self.indexAt( parent.pos() ).row()

        total_rows = self.rowCount()
        if total_rows < 2:
            return

        self.removeRow(row)

    def addItem(self,key,value):
        # We need to stop listening while we insert to prevent calling it while adding item
        self.cellChanged.disconnect( self._handleCellChanged )

        total_rows = self.rowCount()
        self.insertRow( total_rows )

        checkbox = QTableWidgetItem(key)
        checkbox.setCheckState(Qt.Checked)

        self.setItem(total_rows,0, checkbox )
        self.setItem(total_rows,1, QTableWidgetItem(value) )

        # I dont know why, but without adding a wrapper widget, i cannot get the current row
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0,0,0,0)
        button_widget.setLayout(button_layout)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect( self.removeItem )
        button_layout.addWidget(delete_button)

        self.setCellWidget(total_rows,2, button_widget )

        self.cellChanged.connect( self._handleCellChanged )

    def getValues(self):
        response = {}
        for i in range(0, self.rowCount()):
            key = self.item(i, 0)
            enabled = key.checkState() 
            key = key.text()

            value = self.item(i, 1).text()

            if enabled and key != "":
                response[key] = value

        return response

