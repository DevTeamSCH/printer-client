import json


class ActivePrinters:
    def __init__(self):
        self.activePrinters = []

    def load_from_file(self):
        try:
            with open('active_printers.json', 'r') as json_data:
                d = json.load(json_data)
                self.activePrinters = d['activePrinters']
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open('active_printers.json', 'w') as json_data:
            json.dump(self.__dict__, json_data)
        pass
