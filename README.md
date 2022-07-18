## 项目性质
This project is done by university students only to meet their courses' requirements.

##配置说明
- 环境：Python 3.9 & Pycharm 或 Jupyter Notebook & Python 3.6
- 安装包时请选择cvzone==1.4.1, mediapipe <= 0.8.8（已验证：0.8.3和0.8.8）

##参考
- 基于 [【OpenCV 实现AI虚拟键盘】](https://blog.csdn.net/weixin_44692055/article/details/121576593) 
和[pyautogui实战--自动给好友群发文本消息、图片消息](https://blog.csdn.net/m0_49710816/article/details/124166333)

##我们做了什么
- 优化了键盘布局，完善了更全面的键盘功能

##使用说明
- 请根据自己的项目保存位置修改`weixin.py`开头的两个绝对路径
- `keyboard.py`为程序入口
- 键盘点击的触发条件是中指和食指伸直（向上），其他手指弯曲（推荐单指移动，双指点击）
- `img`目录下是作为识别目标的各图标，如果一直识别不了可以在本地环境下重新采样
- `backgrounds`目录下是预计用于测试的虚拟背景（还未实现）