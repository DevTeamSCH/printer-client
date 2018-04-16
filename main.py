import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from main_ui import Ui_MainWindow


class PrinterMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def openOptionsWindow(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = PrinterMainWindow()
    widget.show()

    app.exec()

