import pyautogui
import pyperclip
import time
cd = 0.3  # 动作间的冷却时间


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

    @staticmethod
    def open_close_wechat():
        # Ctrl + alt + w 打开微信
        pyautogui.hotkey('ctrl', 'alt', 'w')
        time.sleep(cd)

    @staticmethod
    def search_name(name):
        # 搜索好友
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(cd)
        # 复制好友昵称到粘贴板
        pyperclip.copy(name)
        time.sleep(cd)
        # 模拟键盘 ctrl + v 粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(cd)
        # 回车进入好友消息界面
        pyautogui.press('enter')
        time.sleep(cd)

    @staticmethod
    def send():
        # 发送消息
        pyautogui.press('enter')
        time.sleep(cd)

    # 定义一个根据图标寻找像素位置并点击的函数
    @staticmethod
    def mapping_img(img, click):
        # 读入图片数据，返回图片中心点坐标
        box_location = pyautogui.locateCenterOnScreen(img)
        acc = 1
        while box_location is None:  # 当定位图片失败时，逐步尝试降低置信度
            acc -= 1 / 32
            print("\r confidence=", acc, end='')
            box_location = pyautogui.locateCenterOnScreen(img, confidence=acc)
        # 将鼠标移动到中心点位置
        pyautogui.moveTo(box_location)
        if click == 'double':
            pyautogui.doubleClick(box_location)
        else:
            pyautogui.leftClick(box_location)

    @staticmethod
    def read_txt(txt):
        pyperclip.copy(txt)
        pyautogui.hotkey('ctrl', 'v')

    def read_img(self, img=img_name):
        # 找到微信对话框的文件发送图标
        self.mapping_img(self.filepic, 'single')
        # 把传入的图片文件名复制，粘贴在文件名选框
        pyperclip.copy(img)
        time.sleep(cd)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(cd)
        pyautogui.press('enter')
        time.sleep(cd)

    def read_video(self, video=video_name):
        self.mapping_img(self.filepic, 'single')
        pyperclip.copy(video)
        time.sleep(cd)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(cd)
        pyautogui.press('enter')
        time.sleep(cd)

    def emoji(self, name):
        self.mapping_img(self.emojipic, 'single')
        time.sleep(cd)
        self.mapping_img(self.emoji_dic[name], 'single')
        time.sleep(cd)


def Main():
    wechat = Wechat()
    wechat.open_close_wechat()
    wechat.search_name("文件传输助手")
    wechat.read_txt("测试")
    wechat.send()
    wechat.read_img()
    wechat.send()
    wechat.read_video()
    wechat.send()
    for name in wechat.emoji_dic.keys():
        wechat.emoji(name)
        wechat.send()
    wechat.open_close_wechat()


if __name__ == '__main__':
    Main()
