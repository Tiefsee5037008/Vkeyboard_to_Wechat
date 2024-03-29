## 项目性质
*This project is done by some college students only to meet their course's requirement.*

## 配置说明
- 环境：Python 3.9 & Pycharm 或 Jupyter Notebook & Python 3.6
- 在运行前，请打开cmd输入以下命令安装依赖

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## References
[【OpenCV 实现AI虚拟键盘】](https://blog.csdn.net/weixin_44692055/article/details/121576593) 

[pyautogui实战--自动给好友群发文本消息、图片消息](https://blog.csdn.net/m0_49710816/article/details/124166333)

## 我们做了什么
- 优化了键盘布局，完善了更全面的键盘功能
- 融合了虚拟键盘、手势控制和微信交互
- 完成了某课程的大作业，获得了学分（将来时？）

## 使用说明
- 请根据自己的项目保存位置修改`weixin.py`开头的两个绝对路径
- `main.py`为程序入口
+ 键盘模式（默认模式）下：
    - 键盘点击的触发条件是中指和食指伸直且并拢（向上），其他手指弯曲
  
    ![Input](readme.assets/Input.png)
  
  （推荐单指移动，双指点击）
    - 推荐用左手点击左侧按钮，右手点击右侧按钮
    - `Enter`键可实现与微信的交互，根据输入的指令不同：
        + `img`：打开微信、向特定好友发送特定图片、关闭微信
            * 特定好友默认为文件传输助手，可在`weixin.py`中改变
        + `video`：打开微信、向特定好友发送特定视频、关闭微信
        + `表情代号`：打开微信、向特定好友发送特定表情、关闭微信
          * 需要对应表情在最近使用表情或第一页默认表情中
          * 表情代号及其对应的表情请参照img文件夹
        + 其他文本:翻译为中文并打开微信发送消息（需要设置对应快捷键为Enter键）
        + `start`：上面几个加起来（一整套演示程序）

    - 做水平“六”字手势隐藏键盘，进入手势控制模式。
  
    ![six](readme.assets/six.png)

+ 手势控制模式下：
    - 做水平“OK”手势显示键盘，切换到键盘模式
  
    ![OK](readme.assets/OK.png)
  
    - 做`“1”`字手势执行`img`对应操作
    - 做`“2”`字手势执行`video`对应操作
    - 做`“3”`字手势执行`表情代号`对应操作（默认设置了一种表情）
	

- `img`目录下是作为识别目标的各图标，如果出现识别不了的情况（由于电脑分辨率图标大小可能不同）可以在本地环境下重新采样
- 退出方式
	+ 直接关闭窗口 
	+ 敲击物理键盘`Esc`键
	+ 键盘模式下点击右下角`Esc`键
