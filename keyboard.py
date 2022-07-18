import cv2
import pyautogui as pg
# 手部 跟踪模块
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np
import cvzone
from pynput.keyboard import Key, Controller
# 控制微信的模块
from weixin import Wechat

wechat = Wechat()


def do_wechat(text):
    if text == 'open':
        wechat.open_wechat()
    elif text == 'img':
        wechat.read_img()
    elif text == 'vedio':
        wechat.read_vedio()
    elif text in wechat.emoji_dic:
        wechat.emoji(text)
    elif text == 'send':
        wechat.send()
    else: pass


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)
# 识别手势
detector = HandDetector(detectionCon=0.8)
keyboard = Controller()
specialList = ['\b', 'Clear', ' ', 'CapsLk', 'Shift', 'Enter', 'Esc']


def isSpecial(ch):
    return ch in specialList


# 键盘关键字
# keys = [['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 'Clear'],
#         ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\b'],
#         ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', ' '],
#         ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\''],
#         ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

# keys = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\b'],
#         ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ' '],
#         ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 'Clear'],
#         ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'enter']]

keys = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\b'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', ' '],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\''],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Clear'],
        ['CapsLk', 'Shift', 'Enter', 'Esc']]


class Button():
    def __init__(self, pos, text, name, size=[60, 60]):
        self.pos = pos
        self.text = text
        self.name = name
        self.size = size
        self.push = False

    # def draw(self, img):
    #     x, y = self.pos
    #     w, h = self.size
    #     cv2.rectangle(img, self.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
    #     cv2.putText(img, self.text, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    #     return img
    def nextPosition(self, dis):
        return [self.pos[0] + self.size[0] + dis[0], self.pos[1] + dis[1]]


buttonList = []
finalText = ''
CapsLk = 0  # 预留为Button类型
Shift = 0  # 预留为Button类型
Clear = 0  # 预留为Button类型
for j in range(len(keys)):
    for x, key in enumerate(keys[j]):
        # 循环创建buttonList对象列表
        if key == '\b':
            buttonList.append(Button([100 * x + 30, 100 * j + 50], key, 'Backspace', [200, 60]))
        elif key == ' ':
            buttonList.append(Button([100 * x + 30, 100 * j + 50], key, 'Space', [120, 60]))
        elif key == 'Clear':
            Clear = Button([100 * x + 30, 100 * j + 50], key, 'Clear', [120, 60])
            buttonList.append(Clear)
        elif key == 'CapsLk':
            CapsLk = Button([200 * x + 30, 100 * j + 50], key, 'CapsLk', [150, 60])
            buttonList.append(CapsLk)
        elif key == 'Shift':
            Shift = Button([200 * x + 30, 100 * j + 50], key, 'Shift', [120, 60])
            buttonList.append(Shift)
        elif key == 'Enter':
            buttonList.append(Button([200 * x + 30, 100 * j + 50], key, 'Enter', [120, 60]))
        elif key == 'Esc':
            buttonList.append(Button(Clear.nextPosition([-120, 100]), key, 'Esc', [100, 60]))
        else:
            buttonList.append(Button([100 * x + 30, 100 * j + 50], key, key))


def drawAll(img, buttonList):
    img1 = np.zeros_like(img, np.uint8)
    out = img.copy()
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img1, (x, y, w, h), 20, rt=0)
        if button.push == False:
            cv2.rectangle(img1, button.pos, (x + w, y + h), (255, 144, 30), cv2.FILLED)
        else:
            cv2.rectangle(img1, button.pos, (x + w, y + h), (255, 72, 15), cv2.FILLED)
        cv2.putText(img1, button.name, (x + 10, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    # img=cv2.addWeighted(img,0.5,img1,0.5,0)
    mask = img1.astype(bool)
    out[mask] = cv2.addWeighted(img, 0.5, img1, 0.5, 0)[mask]
    return out


count = 0
prex = 0
prey = 0
tCur = 0
tPre = 0
Top = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
       ';': ':', '\'': '""',
       ',': '<', '.': '>', '/': '?'}


def realChar(ch):
    if ch.isalpha():
        return ch.upper() if CapsLk.push else ch.lower()
    elif isSpecial(ch) == False:
        return Top[ch] if Shift.push else ch
    else:
        return ch


if __name__ == '__main__':
    while cap.isOpened():
        success, img = cap.read()
        # 识别手势
        if success == False:
            break
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img)
        img = drawAll(img, buttonList)
        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), cv2.FILLED)  # 修改外矩形
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                    d1, _, _ = detector.findDistance(8, 12, img, draw=False)
                    fingerUpList = detector.fingersUp()
                    cv2.putText(img, str(fingerUpList), (20, 700), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
                    if len(lmList) > 8 and fingerUpList == [0, 1, 1, 0, 0] and d1 < 70:
                        num1 = int(lmList[8][0])
                        num2 = int(lmList[8][1])
                        tCur = time.perf_counter()
                        if (num1 - prex) * (num1 - prex) + (num2 - prey) * (num2 - prey) > 200 and tCur - tPre >= 1:
                            tPre = tCur
                            # keyboard.press(button.text)
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.name, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 3)
                            if button.text == 'Clear':
                                count = 0
                                finalText = ''
                            elif button.text == 'CapsLk':
                                CapsLk.push = False if CapsLk.push else True
                            elif button.text == 'Shift':
                                Shift.push = False if Shift.push else True
                            elif button.text == 'Enter':
                                do_wechat(finalText)
                            elif button.text == 'Esc':
                                a = pg.confirm(text='Sure to Exit?', title='Exit Confirm', buttons=['OK', 'Cancel'])
                                if a == 'OK':
                                   cv2.waitKey(1)
                                   cap.release()
                                   cv2.destroyAllWindows()
                            elif button.text != '\b':
                                count += 1
                                finalText += realChar(button.text)
                            elif button.text == '\b':
                                count -= 1
                                finalText = finalText[:count]
                            cv2.putText(img, 'count=' + str(count), (20, 700), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

            prex = int(lmList[8][0])
            prey = int(lmList[8][1])
            print("\r当前文本：", finalText, end='')
            fingerUpList = detector.fingersUp()
            cv2.putText(img, str(fingerUpList), (20, 700), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
        cv2.putText(img, 'count=' + str(count), (1000, 670), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        cv2.rectangle(img, (20, 550), (800, 650), (255, 200, 135), cv2.FILLED)
        cv2.putText(img, finalText, (20, 590), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
        cv2.namedWindow("Image", cv2.WINDOW_FREERATIO)
        cv2.imshow("Image", img)
        res = cv2.waitKey(1)
        # if res == 13:  # Enter
        #     break
    cap.release()
    cv2.destroyAllWindows()
