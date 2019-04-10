from PyQt5.QtWidgets import QWidget

from design.myprinterslistitem_ui import Ui_MyPrintersListItem
from design.printerlistitem_ui import Ui_PrinterListItem
from printer_api import api_wrapper


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
