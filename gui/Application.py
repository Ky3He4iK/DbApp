import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui

from db_tools.DAO import *
from gui.TableWidget import TableWidget


class AppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.db = DAO()

        self.layout_ = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.resize(800, 600)
        self.tabs = [(TableWidget(self.db, table), table) for table in table_info_data.keys()]
        for tab in self.tabs:
            self.tab_widget.addTab(*tab)
        self.tabs[0][0].activated()
        self.tab_widget.currentChanged.connect(self.tab_changed)

        self.layout_.addWidget(self.tab_widget)

        self.setLayout(self.layout_)

    @QtCore.Slot()
    def tab_changed(self, tab_id: int):
        self.tabs[tab_id][0].activated()


def application():
    app = QtWidgets.QApplication()

    widget = AppWindow()
    # widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
