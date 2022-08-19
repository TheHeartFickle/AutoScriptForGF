# from mainwindow import Ui_Form
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import QThread, pyqtSignal
# import sys
# import time
# class MySignal(object):
#     def __init__(self, Type=None, Message=None):
#         self.type = Type
#         self.message = Message
#
#     def valuation(self, Type=None, Message=None):
#         if Type is not None:
#             self.type = Type
#         if Message is not None:
#             self.message = Message
#
#
# class MyWin(QWidget, Ui_Form):
#     """docstring for Mywine"""
#
#     def __init__(self):
#         super(MyWin, self).__init__()
#         self.setupUi(self)
#         self.lineEdit_3.setText("233")
#
#         self.My_signal = MySignal("try", self.lineEdit_3.text())
#         self.My_thread = MyThread()  # 实例化自己建立的任务线程类
#
#         self.My_thread.signal.connect(self.callback)  # 设置任务线程发射信号触发的函数
#
#         self.My_thread.signal_back.emit(self.My_signal)
#
#         self.pushButton_8.clicked.connect(self.refresh)
#         self.pushButton_8.clicked.connect(self.begin)
#
#     def refresh(self):
#         self.My_signal.message = self.lineEdit_3.text()
#         self.My_thread.signal_back.emit(self.My_signal)
#
#     def begin(self):  # 这里test就是槽函数, 当点击按钮时执行 test 函数中的内容, 注意有一个参数为 self
#         self.My_thread.start()  # 启动任务线程
#
#     def callback(self, Text):  # 这里的 i 就是任务线程传回的数据
#         self.textBrowser.append(Text)
#
#
# class MyThread(QThread):  # 建立一个任务线程类
#     signal = pyqtSignal(str)  # 设置触发信号传递的参数数据类型,这里是字符串
#     signal_back = pyqtSignal(MySignal)
#
#     def __init__(self):
#         super(MyThread, self).__init__()
#         self.message = MySignal()
#         self.signal_back.connect(self.get_message)
#
#     def get_message(self, Input):
#         self.message = Input
#         print(self.message.type)
#         print(self.message.message)
#
#     def run(self):  # 在启动线程后任务从这个函数里面开始执行
#         if self.message.type == 'try':
#             print("in")
#             for i in range(10):
#                 self.signal.emit(self.message.message + "--" + str(i))  # 任务线程发射信号用于与图形化界面进行交互
#                 time.sleep(1)
#             self.signal.emit("done")

# from subprocess import Popen, PIPE
# from re import findall
#
# class MyQueue(object):
#     def __init__(self, List):
#         self.queue = List
#         self.queue.append(None)
#
#     def is_empty(self):
#         return len(self.queue) == 0
#
#     def get_cycle(self):
#         self.queue.append(self.queue.pop(0))
#         return self.queue[-1]
#
#     def queue_init(self):
#         while self.get_cycle() is not None:
#             continue


# from psutil import pids, Process
#
#
# def proc_exist(process_name):
#     pl = pids()
#     for pid in pl:
#         if Process(pid).name() == process_name:
#             return pid
#
#
# name = 'Nox.exe'
# if isinstance(proc_exist(name), int):
#     print('{} is running'.format(name))
# else:
#     print('no such process...')

def ch_utf_tran(input_, Flag=True):
    if Flag:
        return str(input_.encode('unicode_escape'))[2:-1]
    else:
        return input_.encode('utf-8').decode('unicode_escape')
        # return input_.decode('unicode_escape')


if __name__ == '__main__':
    # aft = ch_utf_tran("high-高级", True)
    # # aft = str(aft)
    # print(aft, type(aft))
    # aft = ch_utf_tran(aft, False)
    aft = ch_utf_tran('high-\\u9ad8\\u7ea7',False)
    print(aft, type(aft))
    # cannot_find = 'unable to connect'
    # have_error = 'error'
    #
    # adb_path = "E:/Application/ys/Nox/bin/nox_adb.exe"
    # address = "127.0.0.1:6200"
    #
    # out = Popen("{} connect {}".format(adb_path, address), stdout=PIPE)
    # out = out.stdout.read().decode('utf-8')
    # print(out)
    #
    # result_cannot_find = findall(cannot_find, out)
    # result_error = findall(have_error, out)
    # print(result_cannot_find, result_error)
