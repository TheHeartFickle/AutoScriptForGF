from time import sleep
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QThread, pyqtSignal, QObject
from sys import argv, exit

from Ui_test import Ui_MainWindow


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r', encoding='UTF-8') as file:
            return file.read()


class Object_(QObject):
    stop_analyz_signal = pyqtSignal()
    start_print_result = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super(Object_, self).__init__(parent)
        self.analyz_thread = QThread()
        self.analyze = Object_()
        self.analyze.moveToThread(self.analyz_thread)

        self.analyz_thread.started.connect(self.analyze.analyz_work)
        self.analyz_thread.start()

        self.analyze.stop_analyz_signal.connect(self.stop_analyze)

    def stop_analyze(self):
        self.analyz_thread.quit()

    def run(self):
        test_fun(input='sleep')
        self.start_print_result.emit()
        self.stop_analyz_signal.emit()


def test_fun(**kwargs):
    input = kwargs['input']
    print(input)
    if input == 'sleep':
        for i in range(10):
            print(i)
            sleep(1)


def sleeps():
    for i in range(10):
        print(i)
        sleep(1)


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.Button_start.clicked.connect(lambda: test_fun(input=True))


if __name__ == '__main__':
    # app = QtWidgets.QApplication(argv)
    # Form = MainForm()

    # style_file = 'resource/style.qss'
    # style_sheet = QSSLoader.read_qss_file(style_file)
    # Form.setStyleSheet(style_sheet)

    # Form.show()
    # exit(app.exec_())
    pass
