# BiliLive
-------------
这是B站直播间https://live.bilibili.com/1598896的源码  
当前是一个2020年的考研倒计时
![blive](https://static.isdut.cn/ii/images/2019/03/09/7a2b04458fe174fca938571bad4051a2.jpg)
### 原理
opencv和Pillow生成倒计时的图片，使用ffmpeg进行rtmp推流

### 使用方法
```bash
git clone https://github.com/isdut/BiliLive.git
cd BiliLive
#安装依赖模块
pip install -r requirements.txt --ignore-installed
#修改run.py文件
python run.py
```
修改画面可修改**BiliLive**类的**make_image**函数

### 注意事项
本程序中使用的字体有：
- 命运石之门辉光灯字体  
- 濑户字体  

如果侵犯了您的版权，请联系开发者，十分感谢

### TODO
鸽了

## License
MIT