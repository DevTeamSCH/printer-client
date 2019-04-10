import sys

from PyQt5.QtWidgets import QApplication

from windows.mainwindow import PrinterMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = PrinterMainWindow()
    widget.show()

    app.exec()
