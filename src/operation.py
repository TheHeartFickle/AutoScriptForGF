from base import *
from other import recycle_, go_fight

end_Click = (640, 240)  # 收尾用点击点
echelon_01 = (120, 560)  # 部署界面梯队一位置
echelon_02 = (120, 720)  # 部署界面梯队二位置
echelon_12 = (120, 400)  # 梯队编成界面梯队二位置
pix_0_hit = (615, 1160)  # 这两个点用于框选打手弹药口粮信息
pix_1_hit = (910, 1270)
pix_0_tank = (950, 1100)  # 这两个点用于框选抗伤人形血量信息
pix_1_tank = (1240, 1160)
repair = (1390, 1370)  # 人形修复
reapir_confirm = (1745, 1200)  # 人形修复确认
supply = (2110, 1225)  # 补给
planning = (135, 1500)  # 计划模式
spacing = 114514  # 路径点水平(垂直)距离

first_humanoid = (200, 445)  # 第一个待选人形位置
distance = 275  # 狗粮水平间距
rec_13_4 = (1610, 980)  # 13-4后仓库满了拆狗粮
go_back = (180, 95)  # 返回
recycle_humanoid = (165, 750)  # 资源回收位置
auto_select = (2125, 1225)  # 智能选择/确认
strengthen_confirm = (2130, 1360)
recycle_confirm = (2060, 1525)  # 回收按钮
recycle_confirm_again = (1090, 1345)
logistics_confirm = (1345, 1100)  # 继续后勤支援
go_to_fight = (1675, 975)
pos_airport, pos_command = [0, 0], [0, 0]  # 机场，指挥部
had_find = False
in_select_echelon = False
Mult = 114514


def init():
    global Mult
    while 1:
        try:
            img_test = get_image(True)
            h, w = img_test.shape
            Mult = h / 1728
            Mult_base = Mult
            print('Mult =', Mult)
            break
        except:
            print("try again")
            continue
    return Mult


def board_init():
    pos_airport = find_image('airport')
    pos_command = find_image('command')
    print(pos_airport, pos_command)
    if pos_airport[1] < pos_command[1]:
        print("init")
        point1 = (int(Mult * move0[0]), int(Mult * move0[1]))
        point2 = (int(Mult * move1[0]), int(Mult * move1[1]))
        Area(point1, point2).swipe(start="sw", end="ne")


def enter_13_4():  # 进入13-4，如果没有初始化则初始化棋盘并点击重型机场直到部署界面出现
    global pos_airport, pos_command, had_find, spacing, Mult
    print(get_time() + "Start enter_13-4")
    print('操作:等待13-4')
    Click(waiting('first_13_4'))
    sleep(2)
    print('操作:进入13-4')
    Click(waiting('second_13_4'))  # 此操作完成后判断人形仓库是否已满
    sleep(2)
    print('操作:判断仓库是否已满')
    loc = find_image(img_dict['go_to_strengthen'], True)
    if loc is not None:
        print('操作:仓库已满，开始回收')
        recycle_()
        sleep(2)
        go_fight()
        sleep(2)
        enter_13_4()
    print('操作:正常进入13-4')
    waiting('start_fight')
    board_init()
    if not had_find:
        print('操作:寻找机场和指挥部')
        pos_airport = find_image('airport')
        pos_command = find_image('command')
        spacing = int((pos_command[0] - pos_airport[0]) / 6.717)
        had_find = True
        print("spacing:%d" % spacing)
    print(get_time() + " End  enter_13_4")


def Check():  # 判断二队打手口粮弹药是否满,以及是否有大破人形
    global Mult
    print('操作:检测拖尸队状态')
    image = get_image(True)
    # Mult = image.shape[0] / 1728
    # print(Mult)
    image_hit = image[
        int(pix_0_hit[1] * Mult) : int(pix_1_hit[1] * Mult),
        int(pix_0_hit[0] * Mult) : int(pix_1_hit[0] * Mult),
    ]
    image_tank = image[
        int(pix_0_tank[1] * Mult) : int(pix_1_tank[1] * Mult),
        int(pix_0_tank[0] * Mult) : int(pix_1_tank[0] * Mult),
    ]
    res_tank, image_tank = threshold(image_tank, 0, 255, THRESH_BINARY)
    res_hit, image_hit = threshold(image_hit, 0, 255, THRESH_BINARY)

    bitwise_not(image_tank, image_tank)
    contours, hierarchy = findContours(image_tank, RETR_TREE, CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=contourArea, reverse=True)[:5]  # 运用函数从图像中自动寻找最大的边框
    if len(contours) == 0:
        print('人形完好')
    else:
        cnt = contours[0]
        x, y, w, h = boundingRect(cnt)
        if w / x >= 0.625:
            print('操作:3号位人形重创,需要修复')
            Click(repair, Mult)
            sleep_(2)
            Click(reapir_confirm, Mult)
            print('操作:修复完成')
    Flag = True
    res_hit = image_hit.tolist()
    for pix_y in range(len(res_hit)):
        if Flag:
            for pix_x in range(len(res_hit[0])):
                if res_hit[pix_y][pix_x] < 30:
                    Flag = False
                    break
        else:
            break
    del image, image_hit, image_tank, res_hit, res_tank
    collect()
    return Flag


def change_humanoid():  # 换打手
    global Mult
    # print(Mult)
    print(get_time() + 'Start change_humanoid')
    Click(echelon_02, Mult)
    pos = waiting('cancel')
    if Check():
        print('操作:拖尸队状态正常且不需换打手')
        Click(pos)
        sleep(2)
        print(get_time() + "Full  supply")
        return 0  # 第二梯队打手满补给，取消换打手开始计划模式
    else:
        print('操作:拖尸队状态正常且需换打手')
        Click(echelon_01, Mult)
        sleep(2)
        print('操作:确认当前打手信息')
        loc = find_image(img_dict['icon_vv'], True)
        if loc is not None:
            print(get_time() + "start vv2uzi")
            print('操作:点击队伍编成')
            Click(find_image('team_info'))
            waiting('go_back')
            print('操作:点击vv')
            Click(waiting('icon_vv'))
            sleep(2)
            print('操作:点击uzi')
            Click(waiting('icon_uzi'))
            sleep_(2)
            print('操作:回到棋盘')
            Click(go_back, Mult)
            print(get_time() + "end   vv2uzi")
        else:
            print(get_time() + "start uzi2vv")
            print('操作:点击队伍编成')
            Click(waiting('team_info'))
            sleep_(5)
            print('操作:点击第二梯队')
            Click(echelon_12, Mult)
            print('操作:点击vv')
            Click(waiting('icon_vv'))
            print('操作:点击uzi')
            Click(waiting('icon_uzi'))
            sleep_(2)
            print('操作:回到棋盘')
            Click(go_back, Mult)
            print(get_time() + "end   uzi2vv")
    waiting('start_fight')
    board_init()
    print(get_time() + ' End  change_humanoid')


def plan():  # 计划模式
    global pos_airport, pos_command, Mult
    print(get_time() + "Start plan")
    pos = waiting('start_fight')
    Click(pos_airport)
    print('操作:点击重型机场')
    Click(waiting('confirm'))
    print('操作:确认补给打手队')
    sleep(2)
    Click(pos_command)
    sleep_(2)
    print('操作:点击指挥部')
    Click(waiting('confirm'))
    print('操作:确认拖尸队')
    sleep_(1)
    Click(pos)
    print('操作:开始作战')
    sleep_(3)
    Click(pos_airport)
    print('操作:点击重型机场')
    sleep_(2)
    Click(pos_airport)
    print('操作:点击重型机场')
    sleep_(2)
    Click(supply, Mult)
    print('操作:补给')
    sleep_(3)
    Click(pos_command)
    print('操作:点击指挥部')
    sleep_(2)
    Click(planning, Mult)
    print('操作:进入计划模式')
    sleep_(2)
    Click((pos_command[0] - int(Mult * spacing), pos_command[1]))
    print('操作:点击指挥部左侧路径点')
    sleep_(1)
    Click((pos_command[0], pos_command[1] + int(3 * Mult * spacing)))
    print('操作:点击敌方指挥部')
    sleep_(1)
    Click((pos_command[0], pos_command[1] + int(2 * Mult * spacing)))
    print('操作:点击敌方指挥部上侧路径点')
    sleep_(1)
    Click(pos)
    # Click((pos[0] + int(spacing * Mult), pos[1]))
    print('操作:开始计划模式')
    print(get_time() + " End  plan")


def settlement():  # 成果结算到13-4
    print(get_time() + "Start settlement")
    while 1:
        Click(end_Click, Mult)
        loc = find_image(img_dict['first_13_4'], True)
        if loc is not None:
            break
    print(get_time() + " End  settlement")


def main():
    global in_select_echelon
    collect()
    go_fight()
    enter_13_4()
    print('操作:点击机场')
    Click(pos_airport)
    sleep(3)
    if not in_select_echelon:
        print('操作:在选择重装界面，进入选择梯队界面')
    Click(find_image('select_echelon'))
    print('操作:进入选择梯队界面')
    in_select_echelon = True
    sleep(1)
    change_humanoid()
    plan()
    print('开始休眠:150秒')
    sleep(150)  # 拖尸基本都要这么多时间，少点waiting节约内存(毕竟我也不知道哪里会内存泄露)
    collect()
    print('启动')
    waiting('settlement')
    settlement()
    collect()


if __name__ == '__main__':
    init()
    for _ in range(52):
        print('==========================================')
        print('===============第' + ' ' + str(_ + 1) + ' ' + '次执行===============')
        print('==========================================')
        main()
        # try:
        #     main()
        # except MemoryError:
        #     print("memoryError")
        # except:
        #     print("error")
    #     else:
    #         collect()
