import functools
from PyQt5.QtWidgets import QMessageBox
from printer_api import ApiThread, get_printers, update_printer_status

threads = []


def remove_finished_threads():
    global threads
    threads = [t for t in threads if not t.isFinished()]


def refresh(done_signal):
    refresh_thread = ApiThread(get_printers)
    refresh_thread.have_result.connect(functools.partial(success_handler, func=done_signal))
    refresh_thread.error.connect(error_handler)
    refresh_thread.start()
    threads.append(refresh_thread)


def update_status(printer_id, status):
    update_thread = ApiThread(functools.partial(update_printer_status, printer_id, status))
    update_thread.have_result.connect(success_handler)
    update_thread.error.connect(error_handler)
    update_thread.start()
    threads.append(update_thread)


def update_status_multiple(printers):
    update_thread = ApiThread(functools.partial(update_status_multiple, printers))
    update_thread.have_result.connect(success_handler)
    update_thread.error.connect(error_handler)
    update_thread.start()
    threads.append(update_thread)


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
