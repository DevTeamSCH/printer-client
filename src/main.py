import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QListWidgetItem

import api_wrapper
from active_printers import ActivePrinters
from design.main_ui import Ui_MainWindow
from design.myprinterslistitem_ui import Ui_MyPrintersListItem
from design.printerlistitem_ui import Ui_PrinterListItem
from options import OptionsDialog, options_instance


class PrinterMainWindow(QMainWindow):
    refresh_thread = None
    start = True

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.refresh()

    def open_options_window(self):
        options_dialog = OptionsDialog()
        options_dialog.exec_()

    def refresh(self):
        self.ui.available_printer_list.clear()
        self.ui.my_printers_list.clear()
        api_wrapper.refresh(self.refresh_done)

    def refresh_done(self, result):
        self.available_printers_loaded(result['active-printers'])
        self.my_printers_loaded(result['my-printers'])

    def available_printers_loaded(self, printers):
        for printer in printers:
            item = QListWidgetItem(self.ui.available_printer_list)
            self.ui.available_printer_list.addItem(item)
            item_widget = PrinterListItemWidget(printer)
            item.setSizeHint(item_widget.sizeHint())
            self.ui.available_printer_list.setItemWidget(item, item_widget)

    def my_printers_loaded(self, printers):
        for printer in printers:
            item = QListWidgetItem(self.ui.my_printers_list)
            self.ui.my_printers_list.addItem(item)
            item_widget = MyPrintersListItemWidget(printer)
            item.setSizeHint(item_widget.sizeHint())
            self.ui.my_printers_list.setItemWidget(item, item_widget)

        if self.start:
            self.start = False
            if options_instance.inactivatePrinters:
                active_printers = ActivePrinters()
                active_printers.load_from_file()
                for printer in active_printers.activePrinters:
                    # TODO: Itt ossze kene rakni egy id -> status dictionary-t, pl { '1': true, '2': true}
                    pass

                # TODO: es meghivni vele az api_wrapper.update_status_multiple fuggvenyt

    def offline_mode_changed(self):
        if self.ui.offline_mode_checkbox.isChecked():
            # TODO: Le kell menteni az aktiv nyomtatokat, es az osszeset deaktivalni
            pass
        else:
            # TODO: A lementett aktiv nyomtatokat vissza kell allitani
            pass


class PrinterListItemWidget(QWidget):
    def __init__(self, printer):
        super().__init__()
        self.ui = Ui_PrinterListItem()
        self.ui.setupUi(self)
        self.ui.name_label.setText(printer['name'])
        self.ui.owner_label.setText(printer['owner'])
        self.ui.room_label.setText(printer['room'])
        self.ui.type_label.setText(printer['type'])
        self.ui.comment_label.setText(printer['comment'])


class MyPrintersListItemWidget(QWidget):
    printer = None
    update_printer_thread = None

    def __init__(self, printer):
        super().__init__()
        self.ui = Ui_MyPrintersListItem()
        self.ui.setupUi(self)
        self.printer = printer
        self.ui.name_label.setText(printer['name'])
        self.ui.active_check_box.setChecked(printer['status'])
        self.ui.active_check_box.clicked.connect(self.checkbox_clicked)

    def checkbox_clicked(self):
        self.printer['status'] = self.ui.active_check_box.isChecked()
        api_wrapper.update_status(self.printer['id'], self.printer['status'])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = PrinterMainWindow()
    widget.show()

    app.exec()
