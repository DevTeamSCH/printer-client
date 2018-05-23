import json
from PyQt5.QtWidgets import QDialog

from design.options_ui import Ui_OptionsDialog


class Options:

    def __init__(self):
        self.language = "English"
        self.apiKey = ""
        self.startWithSystem = False

    def load_from_file(self):
        try:
            with open('options.json', 'r') as json_data:
                d = json.load(json_data)
                self.language = d['language']
                self.apiKey = d['apiKey']
                self.startWithSystem = d['startWithSystem']
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open('options.json', 'w') as json_data:
            json.dump(self.__dict__, json_data)
        pass


options_instance = Options()
options_instance.load_from_file()


class OptionsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(self)
        self.ui.languageBox.setCurrentText(options_instance.language)
        self.ui.apiKeyEdit.setText(options_instance.apiKey)
        self.ui.startBox.setChecked(options_instance.startWithSystem)

    def accept(self):
        options_instance.language = self.ui.languageBox.currentText()
        options_instance.apiKey = self.ui.apiKeyEdit.text()
        options_instance.startWithSystem = self.ui.startBox.isChecked()
        options_instance.save_to_file()
        super().accept()
