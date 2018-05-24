import json

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from options import options_instance

TYPE_CHOICES = {
    "BW": "Black and white",
    "CL": "Color"
}


def get_base_url():
    if options_instance.serverURL is None or options_instance.serverURL is "":
        raise Exception("No server URL provided")

    return options_instance.serverURL


def get_headers():
    if options_instance.apiKey is None or options_instance.apiKey is '':
        raise Exception('No api key provided')

    return {
        'Authorization': 'Token ' + options_instance.apiKey,
        'Content-Type': 'application/json'
    }


def get_available_printers():
    result = requests.get(get_base_url() + 'active-printers', headers=get_headers()).json()
    if type(result) is dict:
        raise Exception(result['detail'])

    printers = []
    for user in result:
        for printer in user['active_printers']:
            printer['owner'] = user['name']
            printer['room'] = user['room']
            printer['type'] = TYPE_CHOICES[printer['type']]
            printers.append(printer)

    return printers


def get_my_printers():
    result = requests.get(get_base_url() + 'my-printers', headers=get_headers()).json()
    if type(result) is dict:
        raise Exception(result['detail'])

    return result


def get_printers():
    return {
        'active-printers': get_available_printers(),
        'my-printers': get_my_printers()
    }


def update_printer_status(printer_id, status):
    content = json.dumps({'status': status})
    response = requests.patch(get_base_url() + 'my-printers/' + str(printer_id) + '/', content, headers=get_headers())
    if response.status_code is 404:
        raise Exception('Printer not found, please refresh')

    return response.json()


class ApiThread(QThread):
    have_result = pyqtSignal(object)
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
