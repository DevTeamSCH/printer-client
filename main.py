import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QListWidgetItem, QMessageBox

from design.main_ui import Ui_MainWindow
from design.printerlistitem_ui import Ui_PrinterListItem
from options import OptionsDialog
from printer_api import ApiThread, get_available_printers, get_my_printers


class PrinterMainWindow(QMainWindow):
    available_printers_thread = None
    my_printers_thread = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.refresh()

    def open_options_window(self):
        options_dialog = OptionsDialog()
        options_dialog.exec_()

    def refresh(self):
        self.load_available_printers()
        self.load_my_printers()

    def load_available_printers(self):
        self.available_printers_thread = ApiThread(get_available_printers)
        self.available_printers_thread.have_result.connect(self.available_printers_loaded)
        self.available_printers_thread.error.connect(self.error_handler)
        self.available_printers_thread.start()

    def load_my_printers(self):
        self.my_printers_thread = ApiThread(get_my_printers)
        self.my_printers_thread.have_result.connect(self.my_printers_loaded)
        self.my_printers_thread.error.connect(self.error_handler)
        self.my_printers_thread.start()

    def available_printers_loaded(self, printers):
        for printer in printers:
            item = QListWidgetItem(self.ui.available_printer_list)
            self.ui.available_printer_list.addItem(item)
            item_widget = PrinterListItemWidget()
            item_widget.load_data(printer)
            item.setSizeHint(item_widget.sizeHint())
            self.ui.available_printer_list.setItemWidget(item, item_widget)

    def my_printers_loaded(self, printers):
        for printer in printers:
            item = QListWidgetItem(self.ui.my_printers_list)
            self.ui.my_printers_list.addItem(item)
            item_widget = PrinterListItemWidget()
            item_widget.load_data(printer)
            item.setSizeHint(item_widget.sizeHint())
            self.ui.my_printers_list.setItemWidget(item, item_widget)

    def error_handler(self, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Critical)
        message_box.setWindowTitle("Error")
        message_box.setText(message)
        message_box.exec_()


class PrinterListItemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PrinterListItem()
        self.ui.setupUi(self)

    def load_data(self, printer):
        self.ui.printername.setText(printer['name'])
        self.ui.printerdescription.setText(printer['comment'])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = PrinterMainWindow()
    widget.show()

    app.exec()
