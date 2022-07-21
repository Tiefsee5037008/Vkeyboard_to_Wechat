import cv2  # 图像处理
import pyautogui as pg  # 用于唤起弹窗
from cvzone.HandTrackingModule import HandDetector  # 手部跟踪模块
import time  # 用于计时
import numpy as np
import cvzone
# from pynput.keyboard import Controller  # 用于模拟键盘输入，暂时废弃
import weixin
from weixin import Wechat  # 控制微信的模块
import translate  # 翻译模块
wechat = Wechat()
background = cv2.imread(r'backgrounds\1.jpg')


def Exit():
    """
    用于实现到程序出口的跳转
    """
    cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()


def do_wechat(text):
    """
    微信的响应函数
    :param text: 要处理的指令
    :return: None
    """
    if text == 'img':
        wechat.open_close_wechat()
        wechat.search_name("文件传输助手")
        wechat.read_img()
        wechat.send()
        wechat.open_close_wechat()  # 打开微信窗口搜索指定好友发送指定图片并关闭窗口
    elif text == 'video':
        wechat.open_close_wechat()
        wechat.search_name("文件传输助手")
        wechat.read_video()
        wechat.send()
        wechat.open_close_wechat()  # 打开微信窗口搜索指定好友发送指定视频并关闭窗口
    elif text in wechat.emoji_dic:
        wechat.open_close_wechat()
        wechat.search_name("文件传输助手")
        wechat.emoji(text)
        wechat.send()
        wechat.open_close_wechat()  # 打开微信窗口搜索指定好友发送指定表情并关闭窗口
    elif text == 'start':
        weixin.Main()
    else:
        wechat.open_close_wechat()
        wechat.search_name("文件传输助手")
        wechat.read_txt(translate.Main(finalText))  # 当遇到未识别指令时，统一认为是文本输入
        wechat.send()
        wechat.open_close_wechat()  # 打开微信窗口搜索指定好友发送指定文本并关闭窗口


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 设置摄像头属性
cap.set(3, 1280)
cap.set(4, 720)
# cap.set(5, 60)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# 设置手部检测器属性
detector = HandDetector(detectionCon=0.8, maxHands=2)

# 特殊字符列表
specialList = ['Backspace', 'Clear', 'Space', 'CapsLk', 'Shift', 'Enter', 'Esc']

# def is_special(ch):
#     return ch in specialList


# 键盘关键字
keys = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Space'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\''],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Clear'],
        ['CapsLk', 'Shift', 'Enter', 'Esc']]


class Button:
    """
    按钮类
    """

    def __init__(self, pos, name, size=None):
        """
        按钮类的构造函数，其中push域用来指示按压状态，初始时为False（未按压）
        :param pos: 按钮位置
        :param name: 按钮显示的名称，不一定是可见字符
        :param size: 按钮框的大小，默认为60*60
        """
        if size is None:
            size = [60, 60]
        self.pos = pos
        self.name = name
        self.size = size
        self.push = False

    def next_position(self, dis):
        """
        用来计算偏移位置
        :param dis: 下一个按钮相对此按钮的偏移距离
        :return: 下一个按钮的位置（按左上角计）
        """
        return [self.pos[0] + dis[0], self.pos[1] + dis[1]]


buttonList = []
finalText = ''
# 以下预留为Button类型
CapsLk = 0
Shift = 0
Clear = 0
# 循环创建buttonList对象列表
for j in range(len(keys)):
    for x, key in enumerate(keys[j]):
        # 为每个按钮设置位置和大小
        if key == 'Backspace':
            buttonList.append(Button([100 * x + 30, 100 * j + 50], key, [200, 60]))
        elif key == 'Space':
            buttonList.append(Button([100 * x + 30, 100 * j + 50], key, [120, 60]))
        elif key == 'Clear':
            Clear = Button([100 * x + 30, 100 * j + 50], key, [120, 60])
            buttonList.append(Clear)
        elif key == 'CapsLk':
            CapsLk = Button([200 * x + 30, 100 * j + 50], key, [150, 60])
            buttonList.append(CapsLk)
        elif key == 'Shift':
            Shift = Button([200 * x + 30, 100 * j + 50], key, [120, 60])
            buttonList.append(Shift)
        elif key == 'Enter':
            buttonList.append(Button([200 * x + 30, 100 * j + 50], key, [120, 60]))
        elif key == 'Esc':
            buttonList.append(Button(Clear.next_position([0, 100]), key, [100, 60]))  # 将Esc设置在Clear正下方
        else:  # 普通按钮放在最后
            buttonList.append(Button([100 * x + 30, 100 * j + 50], key))

keyboard_visible = False  # 用于控制键盘是否可见

# Shift键对应的字符集映射
Top = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
       ';': ':', '\'': '""',
       ',': '<', '.': '>', '/': '?'}


def realChar(ch):
    """
    根据大小写锁定和Shift按键状态确定真实字符
    特殊字符返回本身
    :param ch: 字符名称，应是字符串，一般对应button.name域
    :return: 结合CapsLk和Shift得到的实际字符
    """
    if ch in specialList:
        return ch
    elif ch.isalpha():
        return ch.upper() if CapsLk.push else ch.lower()
    elif ch in Top:
        return Top[ch] if Shift.push else ch
    else:
        raise Exception('Unidentified character')


def drawAll(img, button_list):
    """
    :param img: 绘制的背景图像
    :param button_list: 按钮列表
    :return: 返回绘制后的图像
    """
    img1 = np.zeros_like(img, np.uint8)
    out = img.copy()
    alpha = 0.5  # 透明度
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img1, (x, y, w, h), 20, rt=0)
        if button.push:  # 按压状态按钮的绘制
            cv2.rectangle(img1, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)
        else:  # 未按压状态按钮的绘制
            cv2.rectangle(img1, button.pos, (x + w, y + h), (255, 144, 30), cv2.FILLED)
        cv2.putText(img1, realChar(button.name), (x + 10, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    mask = img1.astype(bool)  # 生成掩码
    out[mask] = cv2.addWeighted(img, alpha, img1, 1 - alpha, 0)[mask]  # 加权混合，实现透明效果
    return out


fpsReader = cvzone.FPS()  # 用于检测帧率
count = 0  # 字符计数，主要是为了提升用户不可见字符（如空格）的数量
prex = 0  #
prey = 0
# 用于设置时间cd
tCur = 0
tPre = 0
fingerlist = [[1, 0, 1, 1, 1],
              [0, 1, 1, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 1, 1, 0]]
fingerindex = None
time_state = False

if __name__ == '__main__':  # 程序入口
    while cap.isOpened():  # 检验摄像头状态
        success, img = cap.read()
        if not success:  # 检验图片是否成功接收
            break
        img = cv2.flip(img, 1)  # 翻转图像，使自身和摄像头中的自己呈镜像关系
        img = detector.findHands(img)  # 手部检测方法，找到手部位置
        lmList, box = detector.findPosition(img)  # 获得手部各关节位置
        if keyboard_visible:
            img = drawAll(img, buttonList)  # 在当前帧重新绘制全部按钮
            if lmList:  # 检测到手
                for button in buttonList:  # 遍历检测每个按钮
                    x, y = button.pos  # 获取按钮参数
                    w, h = button.size
                    if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:  # 选中条件：食指指尖在按钮矩形框范围内
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), cv2.FILLED)  # 选中后按钮框高亮显示
                        cv2.putText(img, realChar(button.name), (x + 10, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0),
                                    2)  # 高亮时文字深色显示
                        d1, _, _ = detector.findDistance(8, 12, img, draw=False)  # 获取食指和中指指尖距离
                        d2, _, _ = detector.findDistance(7, 11, img, draw=False)  # 获取食指和中指远指间关节关节距离
                        fingerUpList = detector.fingersUp()  # 获取手指向上状态
                        # 第二个条件为手势判断：只有食指和中指向上；第三个条件表示食指和中指并拢（采用相对距离）
                        if len(lmList) > 8 and fingerUpList == [0, 1, 1, 0, 0] and d1 <= 1.05 * d2:
                            # 获取本次点击中心坐标和时间戳
                            num1 = int(lmList[8][0])
                            num2 = int(lmList[8][1])
                            tCur = time.perf_counter()
                            # 第一个条件为空间阈值：两次点击间要移动一定距离（阈值大小与按钮大小有关）
                            # 第二个条件为时间阈值：两次点击间要隔一定时间（单位：秒）
                            if (num1 - prex) * (num1 - prex) + (num2 - prey) * (num2 - prey) > 200 and tCur - tPre >= 1:
                                tPre = tCur  # 更新时间戳
                                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 0),
                                              cv2.FILLED)  # 绘制输入成功高亮状态（较短暂，可靠反差色或延长时间改善）
                                cv2.putText(img, realChar(button.name), (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 3,
                                            (0, 0, 0), 3)
                                # 优先处理特殊按钮
                                if button.name == 'Clear':
                                    count = 0
                                    finalText = ''
                                elif button.name == 'CapsLk':
                                    CapsLk.push = not CapsLk.push
                                elif button.name == 'Shift':
                                    Shift.push = not Shift.push
                                elif button.name == 'Enter':
                                    do_wechat(finalText)
                                elif button.name == 'Esc':
                                    a = pg.confirm(text='Sure to Exit?', title='Exit Confirm',
                                                   buttons=['OK', 'Cancel'])  # 退出前确认
                                    if a == 'OK':
                                        Exit()
                                elif button.name == 'Space':
                                    count += 1
                                    finalText += ' '
                                elif button.name == 'Backspace':
                                    count -= 1
                                    finalText = finalText[:count]
                                else:  # 最后处理普通按钮
                                    count += 1
                                    finalText += realChar(button.name)
                            # 更新上次点击坐标
                            prex = int(lmList[8][0])
                            prey = int(lmList[8][1])
                # 输出调试信息
                print("\r当前文本：", finalText, end='')
                fingerUpList = detector.fingersUp()
                cv2.putText(img, str(fingerUpList), (20, 700), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
                d1, _, _ = detector.findDistance(8, 12, img, draw=False)
                d2, _, _ = detector.findDistance(7, 11, img, draw=False)
                if d2 > 0:
                    cv2.putText(img, 'd1/d2=' + str(d1 / d2), (50, 550), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

                if fingerUpList == [1, 0, 0, 0, 1]:  # 隐藏键盘条件：水平的“六”字手势
                    keyboard_visible = False
            #  输出用户提示信息
            fps, img = fpsReader.update(img, pos=(10, 40), color=(0, 255, 0), scale=2, thickness=2)  # 获取FPS
            cv2.putText(img, 'count:' + str(count), (1010, 670), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)  # 显示字符计数

            cv2.rectangle(img, (20, 550), (1000, 650), (255, 200, 135), cv2.FILLED)  # 绘制输入框背景长矩形
            cv2.putText(img, finalText, (20, 590), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)  # 绘制用户输入文本
        elif lmList:  # 进入手势控制模式
            fingerUpList = detector.fingersUp()
            cv2.putText(img, str(fingerUpList), (20, 700), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            tCur = time.perf_counter()
            if fingerUpList in fingerlist:
                if not time_state or fingerindex != fingerlist.index(fingerUpList):  # 当不在计时中或者切换手势的时候，重新计时
                    tPre = tCur
                    time_state = True
                    fingerindex = fingerlist.index(fingerUpList)
                if tCur - tPre >= 1:  # 防止误触
                    if fingerUpList == [1, 0, 1, 1, 1]:  # 显示键盘条件：水平的"OK"手势
                        keyboard_visible = True
                    elif fingerUpList == [0, 1, 0, 0, 0]:  # "1"字手势，发送图片
                        do_wechat('img')
                    elif fingerUpList == [0, 1, 1, 0, 0]:  # "2"字手势，发送视频
                        do_wechat('video')
                    elif fingerUpList == [0, 1, 1, 1, 0]:  # "3"字手势，发送“doge”
                        do_wechat('doge')

                    else:  # 其他的控制手势（待添加）
                        pass
                    time_state = False
        else:
            time_state = False
        cv2.namedWindow("img", cv2.WINDOW_FREERATIO)  # 设置窗口为自由纵横比
        cv2.imshow("img", img)  # 显示当前帧最终画面

        # 退出条件：27对应Esc键，第二个条件对应手动关闭窗口（右上角）
        if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("img", cv2.WND_PROP_VISIBLE) <= 0:
            break
    cap.release()
    cv2.destroyAllWindows()
