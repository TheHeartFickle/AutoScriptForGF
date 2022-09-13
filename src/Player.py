from gc import collect
from os import system
from json import dump, load, dumps
from os import listdir, system
from random import random
from subprocess import PIPE, Popen
from unittest.mock import patch
from numpy import asarray, ones, uint8, zeros
from time import localtime, sleep, time
from PyQt5.QtCore import QThread, pyqtSignal

from cv2 import (
    CHAIN_APPROX_SIMPLE,
    COLOR_BGR2GRAY,
    IMREAD_COLOR,
    RETR_TREE,
    WINDOW_KEEPRATIO,
    FlannBasedMatcher,
    SIFT_create,
    boundingRect,
    circle,
    contourArea,
    cvtColor,
    destroyAllWindows,
    destroyWindow,
    dilate,
    drawMatchesKnn,
    findContours,
    imdecode,
    imread,
    imshow,
    namedWindow,
    rectangle,
    resizeWindow,
    waitKey,
    bitwise_not,
    threshold,
    THRESH_BINARY,
)


class SettingInitialization(object):
    def __init__(self, Path=None) -> None:
        self.path = Path
        self.dict = None
        self.read()

    def get_details(self):
        self.adb_path = self.dict['adb_path']
        self.address = self.dict['address']
        self.skip_strengthen = self.dict['skip_strengthen']
        self.check_list = self.dict['check_list']
        self.time = self.dict['time']
        self.done_index = self.dict['done_index']
        self.produce_doll = self.dict['produce_doll']
        self.produce_equipment = self.dict['produce_equipment']
        self.kinetic_profile_0 = self.dict['kinetic_profile_0']
        self.kinetic_profile_1 = self.dict['kinetic_profile_1']
        self.shape = self.dict['2304x1728']

    def read(self):
        if self.path is not None:
            with open(self.path, 'r', encoding='utf-8') as fr:
                self.dict = load(fr)
        else:
            raise EnvironmentError("请传路径")

    def refresh(self, **kwargs):
        try:
            key = kwargs['key']
            self.dict[key] = self.key
        except:
            pass
        with open(self.path, 'w', encoding='utf-8') as fr:
            dump(self.dict, fr)

    def show(self):
        return dumps(self.dict, ensure_ascii=False, indent=4)


# def Click(Tuple, mult_=None):
#     if mult_ is None:
#         mult = 1
#     else:
#         mult = mult_
#     x0, y0 = Tuple[0], Tuple[1]
#     if x0 > shape[0] or y0 > shape[1]:
#         print(Tuple, "点不在屏幕内")
#     else:
#         system(
#             f"{adb_path} -s {address} shell input tap {int(x0 * mult)} {int(y0 * mult)}"
#         )


# class Point(object):
#     def __init__(self, Pos=None) -> None:
#         self.point = ()
#         if Pos is not None:
#             self.point = Pos

#     def __call__(self, *args, **kwds):
#         return self.point

#     def click(self, Mult=None):
#         if Mult is None:
#             Click(self.point, 1)
#         else:
#             Click(self.point, Mult)


# class Area(object):
#     def __init__(self, Pos1=None, Pos2=None) -> None:
#         self.nw = None  # 左上角
#         self.se = None  # 右下角
#         self.ne = None  # 右上角
#         self.sw = None  # 左下角
#         if Pos1 is not None and Pos2 is not None:
#             self.nw = list(Pos1)
#             self.se = list(Pos2)
#             if Pos1[0] > Pos2[0]:  # Pos1的x坐标更大更靠右
#                 self.nw[0], self.se[0] = self.se[0], self.nw[0]
#             if Pos1[1] > Pos2[1]:  # Pos1的y坐标更大更靠下
#                 self.nw[1], self.se[1] = self.se[1], self.nw[1]
#             self.ne = [self.se[0], self.nw[1]]
#             self.sw = [self.nw[0], self.se[1]]

#     def direction(self, direction):
#         if direction == "nw":
#             return self.nw
#         elif direction == "se":
#             return self.se
#         elif direction == "ne":
#             return self.ne
#         elif direction == "sw":
#             return self.sw

#     def __call__(self, *args, **kwds):
#         return tuple(self.nw), tuple(self.se)

#     def swipe(self, **kwds):
#         point1 = self.direction(kwds["start"])
#         point2 = self.direction(kwds["end"])
#         # print(point1, point2)
#         system(
#             f"{adb_path} shell input swipe {point1[0]} {int(point1[1])} {int(point2[0])} {point2[1]}"
#         )


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
        pass


class Player(object):
    def __init__(self):
        self.name = None
        self.running = False


def test(**kwargs):
    if kwargs["test"] == 1:
        tar = "out"
    else:
        tar = "in"
    for i in range(10):
        sleep(1)
        print(tar + i)


if __name__ == '__main__':
    path = 'resource/Profile.json'
    s = SettingInitialization(path)
