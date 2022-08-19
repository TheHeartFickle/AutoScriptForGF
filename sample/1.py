import winshell
from pathlib import Path

desktop = Path(winshell.desktop())
miniconda_base = Path(
    winshell.folder('CSIDL_LOCAL_APPDATA')) / 'Continuum' / 'miniconda3'
win32_cmd = str(Path(winshell.folder('CSIDL_SYSTEM')) / 'cmd.exe')
icon = str(miniconda_base / "Menu" / "Iconleak-Atrous-Console.ico")

my_working = str(Path(winshell.folder('CSIDL_PERSONAL')) / "py_work")
link_filepath = str(desktop / "python_working.lnk")

arg_str = "/K " + str(miniconda_base / "Scripts" / "activate.bat") + " " + str(
    miniconda_base / "envs" / "work")

with winshell.shortcut(link_filepath) as link:
    link.path = win32_cmd
    link.description = "Python(work)"
    link.arguments = arg_str
    link.icon_location = (icon, 0)
    link.working_directory = my_working





def find_image(image, *Flag):
    if type(image) == str:
        image = img_dict[image]
    img_target_bgr = get_image()
    h, w = img_target_bgr.shape[:2]
    img_target_gray = cvtColor(img_target_bgr, COLOR_BGR2GRAY)
    sift = SIFT_create()
    kp1, des1 = sift.detectAndCompute(image, None)
    kp2, des2 = sift.detectAndCompute(img_target_gray, None)
    if kp1 is None or kp2 is None or des1 is None or des2 is None:
        del img_target_bgr, img_target_gray, sift
        # print('无相似度')
        return None
    # print('sift|kp1-2,des1-2', len(kp1), len(kp2), len(des1), len(des2))
    FLANN_INDEX_KDTREE = 0
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    searchParams = dict(checks=50)
    flann = FlannBasedMatcher(indexParams, searchParams)
    matches = flann.knnMatch(des1, des2, k=2)
    matchesMask = [[0, 0] for i in range(len(matches))]
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:  # 通过0.7系数来决定匹配的有效关键点数量
            matchesMask[i] = [1, 0]

    drawPrams = dict(matchColor=(0, 255, 0),
                     singlePointColor=(255, 0, 0),
                     matchesMask=matchesMask,
                     flags=0)
    # 匹配结果图片
    img3 = drawMatchesKnn(image, kp1, img_target_gray,
                          kp2, matches, None, **drawPrams)
    img0 = zeros((h, w, 3), uint8)
    img0[:] = [0, 0, 0]
    for ele in matches:
        if matchesMask[ele[0].queryIdx] == [1, 0]:
            circle(img0, (int(kp2[ele[0].trainIdx].pt[0]), int(
                kp2[ele[0].trainIdx].pt[1])), 20, [255, 255, 255], -1)
    img0 = cvtColor(img0, COLOR_BGR2GRAY)
    kernel = ones((5, 5), uint8)
    img0 = dilate(img0, kernel=kernel, iterations=2)
    contours, hierarchy = findContours(img0, RETR_TREE, CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=contourArea, reverse=True)[
               :5]  # 运用函数从图像中自动寻找最大的边框
    if len(contours) == 0:
        del img_target_bgr, img_target_gray, sift, flann, matches, matchesMask, drawPrams, img3, img0
        # print('相似度过低')
        return None
    cnt = contours[0]
    x, y, w, h = boundingRect(cnt)
    kp_num = 0
    for ele in matches:
        if matchesMask[ele[0].queryIdx] == [1, 0]:
            if x <= kp2[ele[0].trainIdx].pt[0] <= x + w and y <= kp2[ele[0].trainIdx].pt[1] <= y + h:
                kp_num += 1  # 判断有多少点落在最大的矩形内部
    kp_per = kp_num / len(matches)
    # print('相似度：', round(100 * kp_per, 3))
    if kp_per < 0.15 and Flag:
        del img_target_bgr, img_target_gray, sift, flann, matches, matchesMask, drawPrams, img3, img0
        return None
    rectangle(img_target_bgr, (x, y), (x + w, y + h), (0, 0, 255), 4)  # 绘制矩形
    del img_target_bgr, img_target_gray, sift, flann, matches, matchesMask, drawPrams, img3, img0
    collect()
    # print('中心点:', int(x + w / 2), int(y + h / 2))
    return int(x + w / 2), int(y + h / 2)