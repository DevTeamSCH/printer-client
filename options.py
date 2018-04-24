import json
from PyQt5.QtWidgets import QDialog

from design.options_ui import Ui_OptionsDialog


class Options:

    def __init__(self):
        self.language = "Hungarian"
        self.apiKey = ""
        self.startWithSystem = False

    def LoadFromFile(self):
        try:
            with open('options.json', 'r') as json_data:
                d = json.load(json_data)
                self.language = d['language']
                self.apiKey = d['apiKey']
                self.startWithSystem = d['startWithSystem']
        except FileNotFoundError:
            pass

    def SaveToFile(self):
        with open('options.json', 'w') as json_data:
            d = json.dump(self.__dict__, json_data)
        pass


class OptionsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(self)
        options = Options()
        options.LoadFromFile()
        self.ui.languageBox.setCurrentText(options.language)
        self.ui.apiKeyEdit.setText(options.apiKey)
        self.ui.startBox.setChecked(options.startWithSystem)

    def accept(self):
        options = Options()
        options.language = self.ui.languageBox.currentText()
        options.apiKey = self.ui.apiKeyEdit.text()
        options.startWithSystem = self.ui.startBox.isChecked()
        options.SaveToFile()
        super().accept()