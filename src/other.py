from base import *

first_humanoid = (200, 445)  # 第一个待选人形位置
distance = 315  # 狗粮水平间距
rec_13_4 = (1610, 980)  # 13-4后仓库满了拆狗粮
go_back = (180, 95)  # 返回
recycle_humanoid = (165, 750)  # 资源回收位置
auto_select = (2125, 1225)  # 智能选择/确认
strengthen_confirm = (2130, 1360)
recycle_confirm = (2060, 1525)  # 回收按钮
recycle_confirm_again = (1385, 1330)
go_out_to_battle = (2060, 1435)
logistics_confirm = (1345, 1100)  # 继续后勤支援
go_to_fight = (1675, 975)
achievement_confirm = (1400, 1500)
mission = (170, 275)  # 作战任务
mission_pt1 = (440, 1575)
mission_pt2 = (440, 250)
ep_14 = (440, 1500)
in_mission = False


def recycle_():
    print(get_time() + "Start recycle_")
    print('开始回收')
    Click(rec_13_4, True)
    pos_stand = waiting('stand_by')
    print('进入工厂')
    had_recycle = False  # 2星人形是否检查回收
    cfg = '{}/Profile.json'.format(path)

    system("cd ..")
    with open(cfg, 'r', encoding='utf-8') as file:  # 从Profile.json配置文件读取配置
        file_dict = load(file)
    # print("file:", file_dict['skip_strengthen'])
    if file_dict['skip_strengthen'] == "True":
        skip = True
    else:
        skip = False
    while 1:
        # print("mem:", skip)
        if skip == True:
            print("跳过强化")
            break
        print('强化-选择待强化人形')
        Click(pos_stand)
        sleep(2)
        print('强化-确认待强化人形')
        Click(first_humanoid, True)
        sleep_(2)
        loc = find_image(img_dict['stand_by_2'], True)
        if loc is not None:  # 仍有待强化人形
            print('强化-选择狗粮')
            Click(loc)
            sleep_(2)
            print('强化-自动选择狗粮')
            Click(auto_select, True)
            sleep(2)
            print('强化-确认狗粮')
            Click(auto_select, True)
            sleep_(2)
            loc = find_image(img_dict['retire'], True)
            if loc is None:  # 2星人形已用完
                print('狗粮用尽')
                Click(go_back, True)
                had_recycle = True
                sleep(2)
                break
            else:
                print('强化-确认强化')
                Click(strengthen_confirm, True)
                sleep(2)
                loc = find_image('confirm', True)
                if loc is not None:  # 人形不够强化
                    print('强化-狗粮不足')
                    Click(loc)
                    sleep(2)
                    Click(find_image('retire'))
                    sleep(2)
                    break
            sleep(2)
        else:  # 所有待强化人形强化完毕，退出强化循环
            print('强化-强化完毕')
            Click(go_back, True)
            sleep(2)
            break
    waiting('retire')
    print('回收-进入回收')
    Click(recycle_humanoid, True)
    sleep(3)
    pos_stand2 = find_image('stand_by_2')
    while 1:
        print('回收-选择待回收人形')

        Click(pos_stand2)
        sleep(2)
        loc = find_image('retire', True)
        if loc is not None:  # 没进入人形回收界面，离开工厂
            print('强化-人形拆解完毕')
            Click(go_back, True)
            break
        else:  # 进入人形回收界面，开始回收人形
            if had_recycle:  # 2星人形回收完毕,开始回收3星人形
                print('回收-回收3星及以上人形')
                for i in range(6):
                    x = first_humanoid[0] + i * distance
                    y = first_humanoid[1]
                    Click((x, y), True)
                    sleep(0.1)
                    Click((x, int(y + distance * 1.9)), True)
                    sleep(0.1)
                print('强化-确认回收人形')
                Click(auto_select, True)  # 确认回收人形
            else:  # 回收两星人形
                print('回收-回收2星人形')
                Click(auto_select, True)
                sleep(2)
                print('强化-确认回收人形')
                Click(auto_select, True)
            sleep(3)
            loc = find_image('retire', True)  # 检查是否回到工厂
            if loc is not None:  # 成功确认待回收人形
                print('回收-确认回收人形')
                Click(recycle_confirm, True)
                sleep(2)
                Click(recycle_confirm_again, True)
                sleep(3)
                had_recycle = True
            else:  # 没有成功确认待回收人形
                if had_recycle:  # 所有人形回收完毕
                    print('回收-回收完毕')
                    Click(go_back, True)
                    sleep(2)
                    Click(go_back, True)
                    break
                else:  # 两星人形被拆完了
                    had_recycle = True
                    print('回收-回收3星及以上人形')
                    for i in range(6):
                        x = first_humanoid[0] + i * distance
                        y = first_humanoid[1]
                        Click((x, y), True)
                        sleep(0.1)
                        Click((x, int(y + distance * 1.9)), True)
                        sleep(0.1)
                    print('强化-确认回收人形')
                    Click(auto_select, True)
                    sleep(3)
                    loc = find_image('retire', True)  # 检查是否回到工厂
                    if loc is not None:  # 成功确认待回收人形
                        print('回收-确认回收人形')
                        Click(recycle_confirm, True)
                        sleep(2)
                        Click(recycle_confirm_again, True)
                        sleep(3)
                        had_recycle = True
                    else:  # 所有人形回收完毕
                        print('回收-回收完毕')
                        Click(go_back, True)
                        sleep(2)
                        Click(go_back, True)
                        break
    collect()
    print(get_time() + "End recycle_")


def go_fight():
    global in_mission
    print(get_time() + "Start go_fight")
    while 1:
        loc = find_image(img_dict['campaign'], True)
        if loc is not None:
            break
        Click(go_out_to_battle, True)
        sleep(1)
        Click(logistics_confirm, True)
        sleep(1)
        Click(achievement_confirm, True)
        sleep(1)
        Click(go_to_fight, True)
        sleep(5)

    print(get_time() + " End  go_fight")


if __name__ == '__main__':
    # waiting('stand_by', 0.8)
    # recycle_()
    go_fight()
