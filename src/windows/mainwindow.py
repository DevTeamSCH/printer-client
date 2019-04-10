from PyQt5.QtWidgets import QListWidgetItem, QMainWindow

from files.active_printers import ActivePrinters
from design.main_ui import Ui_MainWindow
from files.options import options_instance
from printer_api import api_wrapper
from widgets.printerlist import MyPrintersListItemWidget, PrinterListItemWidget
from windows.dialogs import OptionsDialog


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

