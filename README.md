# BiliLive
-------------
这是B站直播间https://live.bilibili.com/1598896 的源码  
当前是一个2020年的考研倒计时
![blive](https://static.isdut.cn/ii/images/2019/03/09/7a2b04458fe174fca938571bad4051a2.jpg)
### 原理
opencv和Pillow生成倒计时的图片，使用ffmpeg进行rtmp推流

### 运行环境
python3 ubuntu

### 使用方法
1 克隆程序代码
```bash
git clone https://github.com/kamino-space/BiliLive.git
cd BiliLive
```
2 安装依赖
```bash
pip install -r requirements.txt
```
3 安装需要的软件包
```bash
sudo apt-get update
sudo apt-get -y build-essential libasound2-dev pulseaudio jackd2 alsa-utils dbus-x11 mpg123 systemd
```
4 编译安装支持alsa的ffmpeg
```bash
cd /usr/src
git clone https://git.ffmpeg.org/ffmpeg.git
cd ffmpeg
./configure --disable-x86asm
make
sudo make install
```
5 添加到系统服务(非必须)
```bash
sudo cp yourpath/BiliLive/service/bililive.service /usr/lib/systemd/system/bililive.service
sudo service start bililive
```
6 启动程序
```bash
cd yourpath/BiliLive
cp config/config.sample.json config/config.json
vi config/config.json
python bililive.py
```
**请不要使用root用户运行程序**

修改画面可修改**BiliLive**类的**make_image**函数

### 注意事项
本程序中使用的字体有：
- 命运石之门辉光灯字体  
- 濑户字体  
- 思源字体  

如果侵犯了您的版权，请联系开发者，十分感谢

### TODO
背景音乐问题

## License
MIT