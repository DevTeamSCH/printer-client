import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QListWidgetItem

from design.main_ui import Ui_MainWindow
from design.printerlistitem_ui import Ui_PrinterListItem
from printer_api import GetAvailablePrintersThread


class PrinterMainWindow(QMainWindow):
    thread = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def openOptionsWindow(self):
        pass

    def load_available_printers(self):
        self.thread = GetAvailablePrintersThread()
        self.thread.have_result.connect(self.available_printers_loaded)
        self.thread.start()

    def available_printers_loaded(self, printers):
        for printer in printers:
            item = QListWidgetItem(self.ui.available_printer_list)
            self.ui.available_printer_list.addItem(item)
            item_widget = PrinterListItemWidget()
            item_widget.load_data(printer)
            item.setSizeHint(item_widget.sizeHint())
            self.ui.available_printer_list.setItemWidget(item, item_widget)


class PrinterListItemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PrinterListItem()
        self.ui.setupUi(self)

    def load_data(self, printer):
        self.ui.printername.setText(printer['name'])
        self.ui.printerdescription.setText(printer['description'])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = PrinterMainWindow()
    widget.show()

    app.exec()
