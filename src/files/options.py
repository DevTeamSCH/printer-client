import json


class Options:

    def __init__(self):
        self.language = "English"
        self.apiKey = ""
        self.serverURL = ""
        self.inactivatePrinters = True
        self.startWithSystem = False

    def load_from_file(self):
        try:
            with open('options.json') as json_data:
                d = json.load(json_data)
                self.language = d['language']
                self.apiKey = d['apiKey']
                self.serverURL = d['serverURL']
                self.inactivatePrinters = d['inactivatePrinters']
                self.startWithSystem = d['startWithSystem']
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open('options.json', 'w') as json_data:
            json.dump(self.__dict__, json_data)
        pass


options_instance = Options()
options_instance.load_from_file()