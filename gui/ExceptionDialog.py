from PySide2 import QtWidgets


class ExceptionDialog(QtWidgets.QDialog):
    def __init__(self, exception: Exception):
        super().__init__()

        self.setWindowTitle("ERROR!")

        QBtn = QtWidgets.QDialogButtonBox.Ok

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Incorrect action. " + str(exception))
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
