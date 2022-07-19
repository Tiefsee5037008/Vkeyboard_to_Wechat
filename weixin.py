import pyautogui
import pyperclip
import time


class Wechat:
    img_name = r"C:\Users\Tiefsee2\project\img\img.png"
    video_name = r"C:\Users\Tiefsee2\project\video\video.mp4"
    def __init__(self):
        self.filepic = r"img\filepic.png"
        self.emojipic = r"img\emojipic.png"
        self.emoji_dic = {"doge": r"img\doge.png",
                          "smile": r"img\smile.png",
                          "kuxiao": r"img\kuxiao.png",
                          "wulian": r"img\wulian.png",
                          "chigua": r"img\chigua.png",
                          "good": r"img\good.png",
                          "ok": r"img\ok.png"}

    def open_wechat(self):
        # Ctrl + alt + w 打开微信
        pyautogui.hotkey('ctrl', 'alt', 'w')
        time.sleep(0.5)

    def close_wechat(self):
        pyautogui.hotkey('ctrl', 'alt', 'w')
        time.sleep(0.5)

    def search_name(self, name):
        # 搜索好友
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        # 复制好友昵称到粘贴板
        pyperclip.copy(name)
        time.sleep(1)
        # 模拟键盘 ctrl + v 粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # 回车进入好友消息界面
        pyautogui.press('enter')
        time.sleep(0.5)

    def send(self):
        # 发送消息
        pyautogui.press('enter')
        time.sleep(0.5)

    # 定义一个根据图标寻找像素位置并点击的函数
    def mapping_img(self, img, click):
        # 读入图片数据，返回图片中心点坐标
        box_location = pyautogui.locateCenterOnScreen(img)
        acc = 1
        while box_location is None:
            acc -= 1 / 1024
            print("\r confidence=",acc,end='')
            box_location = pyautogui.locateCenterOnScreen(img, confidence = acc)
        # 将鼠标移动到中心点位置
        pyautogui.moveTo(box_location)
        if click == 'double':
            pyautogui.doubleClick()
        else:
            pyautogui.leftClick(box_location)

    def read_txt(self, txt):
        pyperclip.copy(txt)
        pyautogui.hotkey('ctrl', 'v')

    def read_img(self, img=img_name):
        # 找到微信对话框的文件发送图标
        self.mapping_img(self.filepic, 'single')
        # 把传入的图片文件名复制，粘贴在文件名选框
        pyperclip.copy(img)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

    def read_video(self, video=video_name):
        self.mapping_img(self.filepic, 'single')
        pyperclip.copy(video)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

    def emoji(self, name):
        self.mapping_img(self.emojipic, 'single')
        time.sleep(1)
        self.mapping_img(self.emoji_dic[name], 'single')
        time.sleep(1)


if __name__ == '__main__':
    wechat = Wechat()
    wechat.open_wechat()
    wechat.search_name("文件传输助手")
    wechat.read_txt("测试")
    wechat.send()
    wechat.read_img()
    wechat.send()
    wechat.read_video()
    wechat.send()
    wechat.emoji(name="doge")
    wechat.send()
