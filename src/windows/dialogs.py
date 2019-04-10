from PyQt5.QtWidgets import QDialog

from design.options_ui import Ui_OptionsDialog
from files.options import options_instance


class OptionsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(self)
        self.ui.languageBox.setCurrentText(options_instance.language)
        self.ui.apiKeyEdit.setText(options_instance.apiKey)
        self.ui.serverURLEdit.setText(options_instance.serverURL)
        self.ui.inactivatePrintersBox.setChecked(options_instance.inactivatePrinters)
        self.ui.startBox.setChecked(options_instance.startWithSystem)

    def accept(self):
        options_instance.language = self.ui.languageBox.currentText()
        options_instance.apiKey = self.ui.apiKeyEdit.text()
        options_instance.serverURL = self.ui.serverURLEdit.text()
        options_instance.inactivatePrinters = self.ui.inactivatePrintersBox.isChecked()
        options_instance.startWithSystem = self.ui.startBox.isChecked()
        options_instance.save_to_file()
        super().accept()
