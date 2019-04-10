import functools

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from printer_api import api

threads = []


# A simple thread class. Runs the given function on a background thread, emits the have_results signal with the result.
# If an error occurs, the error signal is emitted.
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


def remove_finished_threads():
    global threads
    threads = [t for t in threads if not t.isFinished()]


def success_handler(result, func=None):
    remove_finished_threads()
    if func is not None:
        func(result)


def error_handler(message):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Critical)
    message_box.setWindowTitle("Error")
    message_box.setText(message)
    message_box.exec_()


# Runs the parameterless function func in a separate thread. Displays an error message on error, calls done_func on
# success.
def run_threaded(func, done_func=None):
    thread = ApiThread(func)
    thread.have_result.connect(functools.partial(success_handler, func=done_func))
    thread.error.connect(error_handler)
    thread.start()
    threads.append(thread)


def refresh(done_func):
    run_threaded(api.get_printers, done_func)


def update_status(printer_id, status):
    run_threaded(functools.partial(api.update_printer_status, printer_id, status))


def update_status_multiple(printers):
    run_threaded(functools.partial(api.update_status_multiple, printers))
