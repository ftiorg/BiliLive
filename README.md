# BiliLive
-------------
这是B站直播间https://live.bilibili.com/1598896 的源码  
当前是一个2020年的考研倒计时
![blive](https://static.isdut.cn/ii/images/2019/03/09/7a2b04458fe174fca938571bad4051a2.jpg)
### 原理
opencv和Pillow生成倒计时的图片，使用ffmpeg进行rtmp推流

### 使用方法
建议使用Docker部署
```bash
git clone https://github.com/isdut/BiliLive.git
cd BiliLive
docker build -t bililive:0.2 .
docker run -v $(pwd)/config:/app/config bililive:0.2
```
修改画面可修改**BiliLive**类的**make_image**函数

### 注意事项
本程序中使用的字体有：
- 命运石之门辉光灯字体  
- 濑户字体  

如果侵犯了您的版权，请联系开发者，十分感谢

### TODO
背景音乐解决方案
1. ffmpeg -i xxx.mp3 切歌替换文件(应该失败)
2. nginx搭个rtmp服务器，音乐推上去再用ffmpeg拉回来(服务器就搭不好)
3. 简单的http服务器  

## License
MIT