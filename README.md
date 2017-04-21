## 学习笔记 ##
本项目爬取伯乐在线的全部文章，主要是记录几个常用的模版可以反复使用

> 1. **loader机制和item处理**
> 2. **异步存入数据库模版**
> 3. 爬取图片存放目录记录
> 4. main.py的模版
> 5. md5加密函数
> 6. scrapy框架中自动下载图片


## 问题----欢迎留言提出问题 ##

> 1.暂时没有很大的问题解决不了，后期如果遇到再贴出来


## 调试中遇到的问题记录 ##
>1.**TypeError：'Failure' object is not subscriptable**

如图：
![](http://i.imgur.com/ddOAtQ1.png)

**解决方法**： 添加一个try，except，因为有些图片加载不出来

![](http://i.imgur.com/bpGaPzh.png)

>2.**pymysql.err.InterfaceError: (0, '')**

那是因为scrapy异步的存储的原因，太快。

**解决方法**：只要放慢爬取速度就能解决，setting.py中设置 **DOWNLOAD_DELAY = 2**

----------

如果本项目对你有用请给我一颗star，万分感谢。