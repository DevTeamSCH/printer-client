from PyQt5.QtCore import QThread, pyqtSignal


def get_available_printers():
    return [{'name': 'Test printer 1', 'description': 'This is the first test printer'},
            {'name': 'Test printer 2', 'description': 'This is the second test printer'}]


class GetAvailablePrintersThread(QThread):
    have_result = pyqtSignal(list)

    def run(self):
        self.have_result.emit(get_available_printers())
