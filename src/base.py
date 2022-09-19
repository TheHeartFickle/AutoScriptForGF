from ast import Not
from gc import collect
from msilib.schema import Error
from os import system
from json import dump, load, dumps
from os import listdir, system  # , chdir
from random import random
from subprocess import PIPE, Popen

# import sys
from time import localtime, sleep, time

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
from numpy import asarray, ones, uint8, zeros

# adb shell am start com.sunborn.girlsfrontline.cn/com.sunborn.girlsfrontline.MainActivity #启动少前
# adb shell am force-stop com.sunborn.girlsfrontline.cn #退出少前
# adb shell input keyevent 3 #返回桌面
# adb shell input keyevent 4

move0 = (1152, 864)
move1 = (1580, 744)


class Profile(object):
    def __init__(self, Path=None) -> None:
        self.path = Path
        if Path is not None:
            with open(Path, 'r', encoding='utf-8') as fr:
                self.dict = load(fr)
        else:
            raise EnvironmentError("请传路径")

    def refresh(self):
        with open(self.path, 'w', encoding='utf-8') as fr:
            dump(self.dict, fr)

    def show(self):
        return dumps(self.dict, ensure_ascii=False, indent=4)


class Initialization(Profile):
    def __init__(self) -> None:
        pass


class Point(object):
    def __init__(self, Pos=None) -> None:
        self.point = ()
        if Pos is not None:
            self.point = Pos

    def __call__(self, *args, **kwds):
        return self.point

    def click(self, Mult=None):
        if Mult is None:
            Click(self.point, 1)
        else:
            Click(self.point, Mult)


class Area(object):
    def __init__(self, Pos1=None, Pos2=None) -> None:
        self.nw = None  # 左上角
        self.se = None  # 右下角
        self.ne = None  # 右上角
        self.sw = None  # 左下角
        if Pos1 is not None and Pos2 is not None:
            self.nw = list(Pos1)
            self.se = list(Pos2)
            if Pos1[0] > Pos2[0]:  # Pos1的x坐标更大更靠右
                self.nw[0], self.se[0] = self.se[0], self.nw[0]
            if Pos1[1] > Pos2[1]:  # Pos1的y坐标更大更靠下
                self.nw[1], self.se[1] = self.se[1], self.nw[1]
            self.ne = [self.se[0], self.nw[1]]
            self.sw = [self.nw[0], self.se[1]]

    def direction(self, direction):
        if direction == "nw":
            return self.nw
        elif direction == "se":
            return self.se
        elif direction == "ne":
            return self.ne
        elif direction == "sw":
            return self.sw

    def __call__(self, *args, **kwds):
        return tuple(self.nw), tuple(self.se)

    def swipe(self, **kwds):
        point1 = self.direction(kwds["start"])
        point2 = self.direction(kwds["end"])
        # print(point1, point2)
        system(
            f"{adb_path} shell input swipe {point1[0]} {int(point1[1])} {int(point2[0])} {point2[1]}"
        )


Mult_base = None
shape = ()

path = './resource'
photo_path = f'{path}/template_photo'
profile = f'{path}/Profile.json'

cfg = Profile(profile)  # 从Profile.json配置文件读取配置

adb_path = cfg.dict['adb_path']
address = cfg.dict['address']
if cfg.dict['skip_strengthen'] == 'True':
    skip = True
else:
    skip = False

# 保存图片的字典，key为文件名
file_name = listdir(photo_path)
img_dict = {}

for ele in file_name:
    if ele[-4:] == '.png':
        img_name = ele[:-4]
        # print(f"{photo_path}/{ele}")
        img = imread(f"{photo_path}/{ele}")
        img_dict[img_name] = img


class CV_image(object):
    def __init__(self, image=None):
        self.image = image

    def shape(self):
        return self.image.shape[:2][::-1]  # 返回宽高

    def show(self, window_name, window_size=None, *areas):
        print(areas)
        if areas != {}:
            print(True)
        namedWindow(window_name, WINDOW_KEEPRATIO)
        if window_size is not None:
            resizeWindow(window_name, window_size[0], window_size[1])
        else:
            resizeWindow(window_name, self.shape()[0], self.shape()[1])
        imshow(window_name, self.image)
        waitKey(0)
        destroyWindow(window_name)

    def find(
        self, template, threshold=None, **area
    ):  # areas仅支持输入左上角和右下角的坐标(x1,y1),(x2,y2)->[y1:y2,x1:x2]
        self.image = get_image()
        area_flag = area != {}
        if area_flag:
            areas = area['areas']
            img_bgr = self.image[areas[0][1] : areas[1][1], areas[0][0] : areas[1][0]]
        else:
            img_bgr = self.image
        # mid = CV_image(img_bgr)
        # mid.show("img0")
        width, height = img_bgr.shape[:2][::-1]
        img_gray = cvtColor(img_bgr, COLOR_BGR2GRAY)
        sift = SIFT_create()  # 准备工作

        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(img_gray, None)  # 耗时最久语句
        # 原理：根据模板和原图的灰度图对原图的匹配值进行计算(maybe

        if kp1 is None or kp2 is None or des1 is None or des2 is None:
            del img_gray, img_bgr, sift
            return None  # 无匹配值

        FLANN_INDEX_KDTREE = 0
        try:
            indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            searchParams = dict(checks=50)
            flann = FlannBasedMatcher(indexParams, searchParams)
            matches = flann.knnMatch(des1, des2, k=2)
            matchesMask = [[0, 0] for i in range(len(matches))]
            for i, (m, n) in enumerate(matches):
                if m.distance < 0.7 * n.distance:  # 通过0.7系数来决定匹配的有效关键点数量
                    matchesMask[i] = [1, 0]
        except:
            print(indexParams, searchParams)
            exit()

        # drawPrams = dict(matchColor=(0, 255, 0), singlePointColor=(255, 0, 0), matchesMask=matchesMask, flags=0)
        # img3 = drawMatchesKnn(template, kp1, img_gray, kp2, matches, None, **drawPrams)
        # img3:图像匹配可视化,运行时注释掉节约性能

        img_inited = zeros((height, width), uint8)  # 二值化图像
        img_inited.fill(0)
        # List = []
        for ele in matches:  # 通过在纯黑图像上画白点来寻找最大矩形，可设计算法优化(还优化个啥，又不是时间大头)
            if matchesMask[ele[0].queryIdx] == [1, 0]:
                point = (
                    int(kp2[ele[0].trainIdx].pt[0]),
                    int(kp2[ele[0].trainIdx].pt[1]),
                )
                circle(img_inited, point, 20, 255, -1)
                # List.append(point)
        # print(List)

        kernel = ones((5, 5), uint8)  # 膨胀
        img_inited = dilate(img_inited, kernel=kernel, iterations=2)

        contours, hierarchy = findContours(
            img_inited, RETR_TREE, CHAIN_APPROX_SIMPLE
        )  # 寻找最大边框
        contours = sorted(contours, key=contourArea, reverse=True)[:5]

        if len(contours) == 0:
            return None
        cnt = contours[0]
        x, y, width, height = boundingRect(cnt)  # 返回最大边框左上角点和宽高
        # print(x, y, width, height)

        kp_num = 0
        for ele in matches:
            if matchesMask[ele[0].queryIdx] == [1, 0]:
                if (
                    x <= kp2[ele[0].trainIdx].pt[0] <= x + width
                    and y <= kp2[ele[0].trainIdx].pt[1] <= y + height
                ):
                    kp_num += 1  # 判断有多少点落在最大的矩形内部
        kp_per = kp_num / len(matches)

        # rectangle(self.image, (x, y), (x + width, y + height), (0, 0, 255), 4)  # 绘制矩形
        # aft = CV_image(self.image)
        # aft.show("img", (800, 600))
        if threshold is not None:  # 如果threshold为None则没有阈值要求
            if kp_per < threshold:
                return None
        if area_flag:
            return int(x + width / 2 + areas[0][0]), int(y + height / 2 + areas[0][1])
        else:
            return int(x + width / 2), int(y + height / 2)

    def wait(self, template, threshold=None, **area):
        area_flag = area != {}

        while 1:
            if area_flag:
                areas = area['areas']
                # print(template, threshold, areas)
                res = self.find(template, threshold, areas)
            else:
                # print(template, threshold)
                res = self.find(template, threshold)
            if res is None:
                sleep(3)
                continue
            else:
                return res


def get_image(gray=False):  # 把模拟器的截图传送至img
    global shape
    while 1:
        out = Popen(f'{adb_path} -s {address} shell screencap -p', stdout=PIPE)
        out = out.stdout.read().replace(b'\r\n', b'\n')
        out = asarray(bytearray(out), dtype='uint8')
        try:
            out[0] = out[0]
            break
        except:
            print("try again")
            continue
    image = imdecode(out, IMREAD_COLOR)
    if gray:
        image = cvtColor(image, COLOR_BGR2GRAY)
    if shape == ():
        shape = (image.shape[1], image.shape[0])
        Mult_base = shape[1] / 1728
    return image


def sleep_(secs):
    sleep(secs + random())


def get_time():
    asc = localtime(time())
    return "{}-{}  {}:{}:{} ".format(
        str(asc.tm_mon).zfill(2),
        str(asc.tm_mday).zfill(2),
        str(asc.tm_hour).zfill(2),
        str(asc.tm_min).zfill(2),
        str(asc.tm_sec).zfill(2),
    )


def Click(Tuple, mult_=None):
    if mult_ is None:
        mult = 1
    else:
        mult = mult_
    x0, y0 = Tuple[0], Tuple[1]
    if x0 > shape[0] or y0 > shape[1]:
        print(Tuple, "点不在屏幕内")
    else:
        system(
            f"{adb_path} -s {address} shell input tap {int(x0 * mult)} {int(y0 * mult)}"
        )


def go_back():
    system(f"{adb_path} -s {address} shell input keyevent BACK")


IMAGE = CV_image()


def find_image(img_name, Flag=False):
    if type(img_name) == str:
        img = img_dict[img_name]
    else:
        img = img_name
    if Flag:
        res = IMAGE.find(img, threshold=0.15)
    else:
        res = IMAGE.find(img)
    return res


def waiting(img_name):
    if type(img_name) == str:
        img = img_dict[img_name]
    else:
        img = img_name
    res = IMAGE.wait(img, threshold=0.15)
    return res


# pix_0_hit = (615, 1160)  # 这两个点用于框选打手弹药口粮信息
# pix_1_hit = (910, 1270)
# pix_0_tank = (950, 1100)  # 这两个点用于框选抗伤人形血量信息
# pix_1_tank = (1240, 1160)


def test1():
    start = time()
    img = CV_image()
    # img.show("img", (800, 600))
    print(img.find(img_dict["icon_vv"], areas=((270, 430), (570, 1130))))
    time0 = time() - start
    print("time0:", time0)
    #
    # after = time()
    # find_image("icon_vv")
    # time1 = time() - after
    # print("time1:", time1)
    # print(round(100 * (time0 / time1), 3), "%")
    print("Done")


def test2():
    point1 = (1152, 864)
    point2 = (1602, 754)
    # point1, point2 = point2, point1
    system(
        f"{adb_path} shell input swipe {point1[0]} {point1[1]} {point2[0]} {point2[1]}"
    )


if __name__ == '__main__':
    # ar = Area((1152, 864), (1602, 744))
    # ar.swipe(start="sw", end="ne")
    # img = CV_image(get_image())
    # img.show("img", (800, 600), areas=ar())
    pass

