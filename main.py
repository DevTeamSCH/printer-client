import functools
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QListWidgetItem, QMessageBox

from design.main_ui import Ui_MainWindow
from design.myprinterslistitem_ui import Ui_MyPrintersListItem
from design.printerlistitem_ui import Ui_PrinterListItem
from options import OptionsDialog
from printer_api import ApiThread, get_available_printers, get_my_printers, update_printer_status


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
        self.ui.available_printer_list.clear()
        self.available_printers_thread = ApiThread(get_available_printers)
        self.available_printers_thread.have_result.connect(self.available_printers_loaded)
        self.available_printers_thread.error.connect(error_handler)
        self.available_printers_thread.start()

    def load_my_printers(self):
        self.ui.my_printers_list.clear()
        self.my_printers_thread = ApiThread(get_my_printers)
        self.my_printers_thread.have_result.connect(self.my_printers_loaded)
        self.my_printers_thread.error.connect(error_handler)
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
            item_widget = MyPrintersListItemWidget()
            item_widget.load_data(printer)
            item.setSizeHint(item_widget.sizeHint())
            self.ui.my_printers_list.setItemWidget(item, item_widget)


class PrinterListItemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PrinterListItem()
        self.ui.setupUi(self)

    def load_data(self, printer):
        self.ui.name_label.setText(printer['name'])
        self.ui.owner_label.setText(printer['owner'])
        self.ui.room_label.setText(printer['room'])
        self.ui.type_label.setText(printer['type'])
        self.ui.comment_label.setText(printer['comment'])


class MyPrintersListItemWidget(QWidget):
    printer = None
    update_printer_thread = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_MyPrintersListItem()
        self.ui.setupUi(self)

    def load_data(self, printer):
        self.printer = printer
        self.ui.name_label.setText(printer['name'])
        self.ui.active_check_box.setChecked(printer['status'])
        self.ui.active_check_box.clicked.connect(self.checkbox_clicked)

    def checkbox_clicked(self):
        self.printer['status'] = self.ui.active_check_box.isChecked()
        self.update_printer_thread = ApiThread(functools.partial(update_printer_status, self.printer['id'], self.printer['status']))
        self.update_printer_thread.error.connect(error_handler)
        self.update_printer_thread.start()
        pass


def error_handler(message):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Critical)
    message_box.setWindowTitle("Error")
    message_box.setText(message)
    message_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = PrinterMainWindow()
    widget.show()

    app.exec()
