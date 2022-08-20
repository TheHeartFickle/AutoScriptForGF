from ast import Not
from gc import collect
from os import system
from json import dump, load
from os import listdir, system  # , chdir
from random import random
from subprocess import PIPE, Popen
import sys
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
)
from numpy import asarray, ones, uint8, zeros

# adb shell am start com.sunborn.girlsfrontline.cn/com.sunborn.girlsfrontline.MainActivity #启动少前
# adb shell am force-stop com.sunborn.girlsfrontline.cn #退出少前
# adb shell input keyevent 3 #返回桌面
# adb shell input keyevent 4

shape = ()
path = './resource'
photo_path = '{}/template_photo'.format(path)
cfg = '{}/Profile.json'.format(path)

system("cd ..")
with open(cfg, 'r', encoding='utf-8') as file:  # 从Profile.json配置文件读取配置
    file_dict = load(file)

adb_path = file_dict['adb_path']
address = file_dict['connect_address']
file_name = listdir(photo_path)
img_dict = {}  # 保存图片的字典，key为文件名

for i in range(len(file_name)):
    img_name = file_name[i][:-4]
    img = imread(photo_path + '/' + file_name[i])
    img_dict[img_name] = img

system("cd modules")


class CV_image(object):
    def __init__(self, image=None):
        self.image = image

    def shape(self):
        return self.image.shape[:2][::-1]  # 返回长高

    def show(self, window_name, window_size=None):
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
        width, height = self.shape()
        if area != {}:
            areas = area['areas']
            img_bgr = self.image[areas[0][1] : areas[1][1], areas[0][0] : areas[1][0]]
        else:
            img_bgr = self.image

        img_gray = cvtColor(img_bgr, COLOR_BGR2GRAY)
        sift = SIFT_create()  # 准备工作

        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(img_gray, None)  # 耗时最久语句
        # 原理：根据模板和原图的灰度图对原图的匹配值进行计算(maybe

        if kp1 is None or kp2 is None or des1 is None or des2 is None:
            del img_gray, sift
            return None  # 无匹配值

        FLANN_INDEX_KDTREE = 0
        indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        searchParams = dict(checks=50)
        flann = FlannBasedMatcher(indexParams, searchParams)
        matches = flann.knnMatch(des1, des2, k=2)
        matchesMask = [[0, 0] for i in range(len(matches))]
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:  # 通过0.7系数来决定匹配的有效关键点数量
                matchesMask[i] = [1, 0]

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
        return int(x + width / 2), int(y + height / 2)


def get_image(color=True):  # 把模拟器的截图传送至img
    global shape
    while 1:
        out = Popen(
            '{} -s {} shell screencap -p'.format(adb_path, address), stdout=PIPE
        )
        out = out.stdout.read().replace(b'\r\n', b'\n')
        out = asarray(bytearray(out), dtype='uint8')
        try:
            out[0] = out[0]
            break
        except:
            continue
    image = imdecode(out, IMREAD_COLOR)
    if not color:
        image = cvtColor(image, COLOR_BGR2GRAY)
    if shape == ():
        shape = (image.shape[1], image.shape[0])
    return image


# def waiting(image_name, **point):
#     image = img_dict[image_name]  # 从字典中读取图片
#     flag = True
#     x, y = 0, 0
#     while flag:  # 直到指定图像在图片中展示，否则等待2秒
#         for i in range(10):
#             loc = find_image(image, True)
#             if loc is not None:
#                 x = loc[0]
#                 y = loc[1]
#                 flag = False
#                 break
#             else:
#                 collect()
#                 sleep(2)
#         if type(point) == tuple:
#             Click(point)
#         collect()
#     del image
#     return x, y  # 返回图像中心坐标


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


def Click(Tuple, mult=1):
    x0, y0 = Tuple[0], Tuple[1]
    if x0 > shape[0] or y0 > shape[1]:
        pass
    else:
        system(
            "{} -s {} shell input tap {} {}".format(
                adb_path, address, int(x0 * mult), int(y0 * mult)
            )
        )


def go_back():
    system("{} -s {} shell input keyevent BACK".format(adb_path, address))


# pix_0_hit = (615, 1160)  # 这两个点用于框选打手弹药口粮信息
# pix_1_hit = (910, 1270)
# pix_0_tank = (950, 1100)  # 这两个点用于框选抗伤人形血量信息
# pix_1_tank = (1240, 1160)
# # system('adb shell am start com.sunborn.girlsfrontline.cn/com.sunborn.girlsfrontline.MainActivity')
# print([int(pix_0_hit[1] * mult), int(pix_1_hit[1] * mult),
#       int(pix_0_hit[0] * mult), int(pix_1_hit[0])])
# img = image_transmission()[int(pix_0_tank[1] * mult):int(pix_1_tank[1] * mult),
#                            int(pix_0_tank[0] * mult):int(pix_1_tank[0] * mult)]
if __name__ == '__main__':
    start = time()
    img = CV_image(get_image())
    img.find(img_dict["icon_vv"], areas=((270, 430), (570, 1130)))
    time0 = time() - start
    print("time0:", time0)
    #
    # after = time()
    # find_image("icon_vv")
    # time1 = time() - after
    # print("time1:", time1)
    # print(round(100 * (time0 / time1), 3), "%")
    print("Done")
