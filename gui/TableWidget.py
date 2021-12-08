from PySide2 import QtCore, QtWidgets

from db_tools.DAO import *
from .ExceptionDialog import ExceptionDialog


class TableWidget(QtWidgets.QWidget):
    def __init__(self, db: DAO, table: str):
        super().__init__()
        self.db = db
        self.table = table
        self.layout_ = QtWidgets.QVBoxLayout()

        self.table_info = table_info_data[table]
        self.data = self.db.get_all(self.table_info)

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(len(self.table_info.primary_keys) + len(self.table_info.other_fields))
        self.table_widget.setHorizontalHeaderLabels(self.table_info.primary_keys + self.table_info.other_fields)
        self.table_widget.horizontalHeader().setVisible(True)
        self.layout_.addWidget(self.table_widget)

        self.button_plus = QtWidgets.QPushButton(None, "Add")
        self.button_plus.setText("Add")
        self.button_plus.clicked.connect(self.plus_clicked)
        self.layout_.addWidget(self.button_plus)
        self.button_minus = QtWidgets.QPushButton(None, "Remove")
        self.button_minus.setText("Remove")
        self.button_minus.clicked.connect(self.minus_clicked)
        self.layout_.addWidget(self.button_minus)

        self.table_widget.cellChanged.connect(self.on_cell_changed)
        self.setLayout(self.layout_)
        self.show()

        # self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def plus_clicked(self):
        # self.data.append()
        new_entry = self.db.get_all(self.table_info)[-1]
        setattr(new_entry, self.table_info.primary_keys[0], getattr(new_entry, self.table_info.primary_keys[0]) + 1)
        self.data.append(self.db.get_all(self.table_info)[-1])
        self.db.insert(new_entry, self.table_info)
        i = self.table_widget.rowCount()
        self.table_widget.setRowCount(i + 1)
        for j, field in enumerate(self.table_info.primary_keys + self.table_info.other_fields):
            self.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(getattr(new_entry, field)))
        print("plus " + self.table)

    @QtCore.Slot()
    def minus_clicked(self):
        print("minus " + self.table)
        rows = list(set(index.row() for index in self.table_widget.selectedIndexes()))
        if len(rows) != 1:
            ExceptionDialog("Must me 1 row selected!").exec_()
            return
        row = rows[0]
        self.db.remove(self.data[row], self.table_info)
        self.table_widget.removeRow(row)
        self.data = self.data[:row] + self.data[row + 1:]

    @QtCore.Slot()
    def on_cell_changed(self, row: int, column: int):
        field = (self.table_info.primary_keys + self.table_info.other_fields)[column]
        try:
            item = self.table_widget.item(row, column)
            if str(self.data[row]) == item.text():
                return
            field_type = (self.table_info.primary_types + self.table_info.other_types)[column]
            if 'Optional' in str(field_type) and 'str' not in str(field_type) and len(item.text()) == 0:
                field_value = None
            # elif 'Optional' in str(field_type):
            #     field_value = field_type(item.text())
            else:
                field_value = item.text()
            setattr(self.data[row], field, field_value)
            self.db.update(self.data[row], self.table_info)
        except Exception as e:
            print(e)
            ExceptionDialog(e).exec_()
            self.table_widget.item(row, column).setText(str(getattr(self.data[row], field)))
            print("error " + self.table)

    def activated(self):
        print("activated " + self.table)
        self.data = self.db.get_all(self.table_info)
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, field in enumerate(self.table_info.primary_keys + self.table_info.other_fields):
                self.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(self.safe_get(row, field)))

    def safe_get(self, obj, field):
        res = getattr(obj, field)
        if res is None:
            return ""
        return str(res)
