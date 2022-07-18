import cv2

# 手部 跟踪模块
from cvzone.HandTrackingModule import HandDetector

import time
# import numpy as np
# import cvzone
# from pynput.keyboard import Key, Controller
# # 控制微信的模块
from weixin import Wechat

wechat = Wechat()
weixin_state = 0
state = []
preState = []
beginTime = 0
curTime = 0
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)
# 设置成像为1280*720，默认为640*480
cap.set(3, 960)
cap.set(4, 600)
#
while True:
    success, frame = cap.read()
    # if not success:
    #     break
    frame = cv2.flip(frame, 1)  # 水平翻转
    frame = detector.findHands(frame)  # 找到手
    lmlist, _ = detector.findPosition(frame)  # lmlist为存着手关节坐标的列表
    if lmlist:  # cannot unpack non-iterable NoneType object,if是必要的
        d, _, _ = detector.findDistance(8, 12, frame, draw=False)
        curTime = time.perf_counter()
        state = detector.fingersUp()
        cv2.putText(frame, str(state), (20, 580), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        if curTime - beginTime >= 2 and state != preState:
            # if state == [1, 1, 1, 1, 1]:
            #     if weixin_state你好 != 1:
            #         wechat.open_wechat()
            #         weixin_state = 1
            # elif state == [0, 0, 0, 0, 0]:
            #     if weixin_state != 0:
            #         wechat.close_wechat()
            #         weixin_state = 0
            if state == [1, 1, 0, 0, 0]:
                wechat.send()
                beginTime = curTime
            elif state == [1, 0, 0, 0, 0]:
                wechat.search_name("文件传输助手")
                beginTime = curTime

            elif state == [0, 1, 0, 0, 0]:
                wechat.read_txt("你好")
                beginTime = curTime
            elif state == [0, 1, 1, 0, 0]:
                wechat.read_img()
                beginTime = curTime
            elif state == [0, 1, 1, 1, 0]:
                wechat.read_vedio()
                beginTime = curTime
            elif state == [0, 1, 1, 1, 1]:
                wechat.emoji("doge")
                beginTime = curTime
            # else:
            #     pass
        if state != preState:
            beginTime = curTime
            preState = state
        state = detector.fingersUp()
        cv2.putText(frame, 'state='+str(state), (20, 500), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        cv2.putText(frame, 'preState='+str(preState), (20, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.imshow("video", frame)
    if cv2.waitKey(1) == 13:  # Enter
        break
