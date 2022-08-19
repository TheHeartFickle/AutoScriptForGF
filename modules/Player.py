from modules.base import *

end_Click = (640, 240)  # 收尾用点击点
echelon_01 = (120, 560)  # 部署界面梯队一位置
echelon_02 = (120, 720)  # 部署界面梯队二位置
echelon_12 = (120, 400)  # 梯队编成界面梯队二位置
pix_0_hit = (615, 1160)  # 这两个点用于框选打手弹药口粮信息
pix_1_hit = (910, 1270)
pix_0_tank = (950, 1100)  # 这两个点用于框选抗伤人形血量信息
pix_1_tank = (1240, 1160)
repair = (1390, 1370)  # 人形修复
repair_confirm = (1745, 1200)  # 人形修复确认
supply = (2110, 1225)  # 补给
planning = (135, 1500)  # 计划模式
spacing = 130  # 路径点水平(垂直)距离

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

mult = 114514


class Node(object):
    def __init__(self):
        self.info = None
        self.left = None
        self.right = None


class Tree(object):
    def __init__(self):
        self.root = None


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


class Player(object):
    def __init__(self):
        self.name = None
        self.running = False

        self.My_signal = MySignal("image_name", "point")
        self.My_thread = MyThread()  # 实例化自己建立的任务线程类

        self.My_thread.signal.connect(self.callback)  # 设置任务线程发射信号触发的函数
        self.My_thread.signal_back.emit(self.My_signal)

    def starting(self, Type=None, Message=None):
        self.My_signal.valuation(Type, Message)
        self.My_thread.signal_back.emit(self.My_signal)
        self.My_thread.start()  # 启动任务线程

    def run(self):
        self.running = True

    def stop(self):
        self.running = False

    def callback(self, Text):  # 这里的 i 就是任务线程传回的数据
        print(Text)
        if Text == 'del_self':
            del self
