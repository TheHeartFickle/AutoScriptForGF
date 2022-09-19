from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QThread, pyqtSignal
from sys import argv, exit
from os import getcwd, system
from json import load, dump
from time import time, localtime
from sys import path

path.append('modules')

from Ui_mainwindow import Ui_Form

DEBUG = 0

QCoreApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
cfg = './resource/Profile.json'
with open(cfg, 'r', encoding='utf-8') as file:  # 从cfg.json配置文件读取配置
    file_dict = load(file)


def get_time():
    asc = localtime(time())
    return "{}-{}  {}:{}:{}".format(
        str(asc.tm_mon).zfill(2),
        str(asc.tm_mday).zfill(2),
        str(asc.tm_hour).zfill(2),
        str(asc.tm_min).zfill(2),
        str(asc.tm_sec).zfill(2),
    )


def ch_utf_tran(input_, Flag=True):
    if Flag:
        return str(input_.encode('unicode_escape'))[2:-1]
    else:
        return input_.encode('utf-8').replace(b'\\\\', b'\\').decode('unicode_escape')


class MySignal(object):
    def __init__(self, Type=None, Message=None):
        self.type = Type
        self.message = Message

    def valuation(self, Type=None, Message=None):
        if Type is not None:
            self.type = Type
        if Message is not None:
            self.message = Message


class MyThread(QThread):  # 建立一个任务线程类
    signal = pyqtSignal(str)  # 设置触发信号传递的参数数据类型,这里是字符串
    signal_back = pyqtSignal(MySignal)

    def __init__(self):
        super(MyThread, self).__init__()
        self.message = MySignal()
        self.signal_back.connect(self.get_message)

    def get_message(self, Input):
        self.message = Input

    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        print(self.message.type, self.message.message)
        if self.message.type == 'save_json':
            with open(cfg, 'w', encoding='utf-8') as file:
                dump(file_dict, file)


class MainForm(QWidget, Ui_Form):
    def __init__(self):
        global file_dict
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(
            "AutoScriptForGF - ({})".format(file_dict['connect_address'])
        )
        self.setWindowIcon(QIcon("resource\kar98k.ico"))
        self.setFixedSize(1005, 700)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.Page.setCurrentWidget(self.page_1)
        self.running_text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )  # 初始化完成
        if DEBUG == 1:
            self.Page.setCurrentWidget(self.page_debug)

        self.lineEdit.setText(str(file_dict['time']))
        self.text_adb.setText(file_dict['adb_path'])
        self.text_address.setText(file_dict['connect_address'])
        self.skip = file_dict['skip_strengthen']
        self.comboBox.setCurrentIndex(file_dict['done_index'])
        self.comboBox_5.setCurrentIndex(file_dict['produce_doll'])
        self.comboBox_4.setCurrentIndex(file_dict['produce_equipment'])
        self.kinetic_list_0 = file_dict['kinetic_profile_0']
        self.kinetic_list_1 = file_dict['kinetic_profile_1']
        for ele in self.kinetic_list_0:
            self.textBrowser.append(ch_utf_tran(ele, False))
        self.remain = 12
        for ele in self.kinetic_list_1:
            self.remain -= ele
        self.lineEdit_2.setText(str(self.remain))
        self.check_init()
        if self.skip == "True":
            self.checkBox_11.setChecked(True)

        self.Button_1.clicked.connect(lambda: self.change_page(1))  # 页面切换
        self.Button_2.clicked.connect(lambda: self.change_page(2))
        self.Button_3.clicked.connect(lambda: self.change_page(3))

        self.Button_select_adb.clicked.connect(self.select_adb)
        self.text_address.editingFinished.connect(
            lambda a='connect_address': self.edit_final(a)
        )
        self.lineEdit.editingFinished.connect(lambda a='time': self.edit_final(a))
        self.comboBox.currentIndexChanged.connect(
            lambda a, b='done': self.edit_final(a, b)
        )
        self.comboBox_5.currentIndexChanged.connect(
            lambda a, b='produce_doll': self.edit_final(a, b)
        )
        self.comboBox_4.currentIndexChanged.connect(
            lambda a, b='produce_equipment': self.edit_final(a, b)
        )
        self.comboBox_2.currentIndexChanged.connect(
            lambda a, b='kinetic_index': self.edit_final(a, b)
        )
        self.pushButton_8.clicked.connect(lambda a, b=1: self.kinetic_profile(a, b))
        self.pushButton_9.clicked.connect(lambda a, b=0: self.kinetic_profile(a, b))
        self.pushButton_6.clicked.connect(self.start)
        self.pushButton_7.clicked.connect(self.stop)

        self.signal = MySignal()
        self.thread = MyThread()
        self.thread.signal.connect(self.callback)

    def start(self):
        self.begin("start", None)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(True)

    def stop(self):
        self.begin("stop", None)
        self.pushButton_6.setEnabled(True)

    def begin(self, Type, Message):
        self.signal.valuation(Type, Message)
        self.thread.signal_back.emit(self.signal)
        self.thread.start()

    def callback(self, Text):
        print(Text)

    def get(self, message, may="nope"):
        print(message, may)

    def edit_final(self, key, may="nope"):
        print(key, may)
        if may == "nope":
            if key == 'connect_address':
                value = self.text_address.text()
                try:
                    for ele in value:
                        if 48 <= ord(ele) <= 57 or ele == ':' or ele == '.':
                            pass
                    file_dict[key] = value
                    self.setWindowTitle(
                        "AutoScriptForGF - ({})".format(file_dict['connect_address'])
                    )
                except:
                    self.text_address.setText(file_dict['connect_address'])

            elif key == 'time':
                try:
                    file_dict[key] = int(self.lineEdit.text())
                except:
                    self.lineEdit.setText(str(file_dict['time']))
            else:
                print("error")
                return 0
        else:
            if may == "done":  # 脚本运行完成
                file_dict['done_index'] = key
            elif may == "produce_doll":
                file_dict['produce_doll'] = key
            elif may == "produce_equipment":
                file_dict['produce_equipment'] = key
            elif may == "kinetic_index":
                if self.comboBox_2.currentIndex() == 5:
                    self.comboBox_3.hide()
                else:
                    self.comboBox_3.show()
            else:
                print("error")
                return 0
        self.begin("save_json", None)

    def change_page(self, button):
        self.Button_1.setStyleSheet(
            "color:rgb(0, 0, 0);\n"
            "border: 2px solid silver;\n"
            "border-radius: 0px;\n"
            "border-style: hidden hidden solid hidden;\n"
        )
        self.Button_2.setStyleSheet(
            "color:rgb(0, 0, 0);\n"
            "border: 2px solid silver;\n"
            "border-radius: 0px;\n"
            "border-style: hidden hidden solid hidden;\n"
        )
        self.Button_3.setStyleSheet(
            "color:rgb(0, 0, 0);\n"
            "border: 2px solid silver;\n"
            "border-radius: 0px;\n"
            "border-style: hidden hidden solid hidden;\n"
        )
        if button == 1:
            self.Page.setCurrentWidget(self.page_1)
            self.Button_1.setStyleSheet(
                "color:rgb(50, 108, 243);\n"
                "border: 4px solid rgb(50, 108, 243);\n"
                "border-radius: 0px;\n"
                "border-style: hidden hidden solid hidden;\n"
            )
        elif button == 2:
            self.Page.setCurrentWidget(self.page_2)
            self.Button_2.setStyleSheet(
                "color:rgb(50, 108, 243);\n"
                "border: 4px solid rgb(50, 108, 243);\n"
                "border-radius: 0px;\n"
                "border-style: hidden hidden solid hidden;\n"
            )
        elif button == 3:
            self.Page.setCurrentWidget(self.page_3)
            self.Button_3.setStyleSheet(
                "color:rgb(50, 108, 243);\n"
                "border: 4px solid rgb(50, 108, 243);\n"
                "border-radius: 0px;\n"
                "border-style: hidden hidden solid hidden;\n"
            )

    def select_adb(self):
        global file_dict
        file_style = "可执行文件(*.exe);;All Files(*)"
        _translate = QtCore.QCoreApplication.translate
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(
            self, "选取文件", getcwd(), file_style
        )
        self.text_adb.setText(fileName)
        file_dict['adb_path'] = fileName
        self.begin("save_json", None)
        return 0

    def add_message(self, string):
        self.running_text.append(
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; '
            'text-indent:0px;"><span style=" font-size:11pt; color:#808080;">{}</span></p>'.format(
                string
            )
        )

    def change_check(self):
        global file_dict
        value = ''
        value += str(int(self.checkBox.isChecked()))
        value += str(int(self.checkBox_2.isChecked()))
        value += str(int(self.checkBox_3.isChecked()))
        value += str(int(self.checkBox_4.isChecked()))
        value += str(int(self.checkBox_5.isChecked()))
        value += str(int(self.checkBox_6.isChecked()))
        value += str(int(self.checkBox_7.isChecked()))
        value += str(int(self.checkBox_8.isChecked()))
        value += str(int(self.checkBox_9.isChecked()))
        value += str(int(self.checkBox_10.isChecked()))
        file_dict['check_list'] = value
        self.begin("save_json", None)

    def check_init(self):
        check = [file_dict['check_list']]
        judge = {"1": True, "0": False}
        for i in range(10):
            check.append(judge[check[0][i]])
        check.pop(0)
        self.checkBox.setChecked(check[0])
        self.checkBox_2.setChecked(check[1])
        self.checkBox_3.setChecked(check[2])
        self.checkBox_4.setChecked(check[3])
        self.checkBox_5.setChecked(check[4])
        self.checkBox_6.setChecked(check[5])
        self.checkBox_7.setChecked(check[6])
        self.checkBox_8.setChecked(check[7])
        self.checkBox_9.setChecked(check[8])
        self.checkBox_10.setChecked(check[9])

        self.checkBox.clicked.connect(self.change_check)
        self.checkBox_2.clicked.connect(self.change_check)
        self.checkBox_3.clicked.connect(self.change_check)
        self.checkBox_4.clicked.connect(self.change_check)
        self.checkBox_5.clicked.connect(self.change_check)
        self.checkBox_6.clicked.connect(self.change_check)
        self.checkBox_7.clicked.connect(self.change_check)
        self.checkBox_8.clicked.connect(self.change_check)
        self.checkBox_9.clicked.connect(self.change_check)
        self.checkBox_10.clicked.connect(self.change_check)
        self.checkBox_11.clicked.connect(self.skip_or_not)

    def skip_or_not(self, Flag):
        file_dict['skip_strengthen'] = str(Flag)
        self.begin("save_json", None)

    def kinetic_profile(self, nope="nope", operation=1):
        kinetic_dict = {
            "0": "强化演习",
            "1": "资料采样",
            "2": "经验特训",
            "3": "经验特训-特种",
            "4": "云图回廊",
            "5": "防御演习",
        }
        level_dict = {"0": "high", "1": "mid", "2": "low"}
        if operation == 1:
            expend = 3 - self.comboBox_3.currentIndex()
            if self.remain >= expend:
                self.remain -= expend
                self.kinetic_list_1.append(expend)
                self.lineEdit_2.setText(str(self.remain))
                kinetic = kinetic_dict[str(self.comboBox_2.currentIndex())]
                level = level_dict[str(self.comboBox_3.currentIndex())]
                if kinetic == "防御演习":
                    message = '防御演习'
                else:
                    message = '{}-{}'.format(level, kinetic)
                self.kinetic_list_0.append(ch_utf_tran(message, True))
                self.textBrowser.append(message)
            else:
                print("error")
        else:
            self.textBrowser.clear()
            self.kinetic_list_0.pop()
            for ele in self.kinetic_list_0:
                message = ch_utf_tran(ele, False)
                self.textBrowser.append(message)
            self.remain += self.kinetic_list_1.pop()
            self.lineEdit_2.setText(str(self.remain))
        print(self.kinetic_list_0)
        print(self.kinetic_list_1)
        self.begin("save_json", None)


def start():
    app = QtWidgets.QApplication(argv)
    Form = MainForm()
    Form.show()
    exit(app.exec_())


if __name__ == '__main__':
    start()
