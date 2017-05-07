# 相关代码已经修改调试成功----2017-4-21 #
2017-5-6更新：在scrapy中集成了selenium中的chrome（可以动态的抓取，虽然本项目其实用不到，但是可以借鉴到一些需要js加载才能抓取的项目中）
## 一、说明 ##
1.**目标网址**：[伯乐在线](http://blog.jobbole.com/all-posts/)

2.**实现**：如图字段的爬取

![](http://images2015.cnblogs.com/blog/1129740/201704/1129740-20170421165045212-1343267528.png)

![](http://images2015.cnblogs.com/blog/1129740/201704/1129740-20170421165114431-15645702.png)

![](http://images2015.cnblogs.com/blog/1129740/201704/1129740-20170421165148681-920566995.png)

![](http://i.imgur.com/e2v2i8h.png)

3.数据：存放在百度网盘，有需要的可以拿取 链接：[http://pan.baidu.com/s/1nvdnzpZ](http://pan.baidu.com/s/1nvdnzpZ) 密码：2j9l

![](http://images2015.cnblogs.com/blog/1129740/201704/1129740-20170421165249665-1896012238.png)


## 二、运行 ##

运行我就不多说了，直接运行main.py就好了，相关的参数变一下就好了。有点基础的应该都会。

## 三、学习笔记 ##
本项目爬取伯乐在线的全部文章，主要是记录几个常用的模版可以反复使用

> 1. **loader机制和item处理**
> 2. **异步存入数据库模版**
> 3. 爬取图片存放目录记录
> 4. main.py的模版
> 5. md5加密函数
> 6. scrapy框架中自动下载图片


## 四、问题----欢迎留言提出问题 ##

> 1.暂时没有很大的问题解决不了，后期如果遇到再贴出来


## 五、调试中遇到的问题记录 ##
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