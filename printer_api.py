import requests
from PyQt5.QtCore import QThread, pyqtSignal

BASE_URL = 'http://donald.sch.bme.hu:4465/api/v1/'


def get_available_printers():
    result = requests.get(BASE_URL + 'active-printers').json()
    printers = []
    for user in result:
        printers.extend(user['active_printers'])

    return printers


class GetAvailablePrintersThread(QThread):
    have_result = pyqtSignal(list)

    def run(self):
        self.have_result.emit(get_available_printers())
