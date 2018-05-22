import requests
from PyQt5.QtCore import QThread, pyqtSignal

from options import options_instance

BASE_URL = 'http://127.0.0.1:8000/api/v1/'


def get_headers():
    if options_instance.apiKey is None or options_instance.apiKey is '':
        raise ValueError('No api key provided')

    return {'Authorization': 'Token ' + options_instance.apiKey}


def get_available_printers():
    result = requests.get(BASE_URL + 'active-printers', headers=get_headers()).json()
    printers = []
    for user in result:
        printers.extend(user['active_printers'])

    return printers


def get_my_printers():
    return requests.get(BASE_URL + 'my-printers', headers=get_headers()).json()


class ApiThread(QThread):
    have_result = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self):
        try:
            self.have_result.emit(self.func())
        except Exception as e:
            self.error.emit(str(e))
            pass
