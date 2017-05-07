# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
#信号量
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher #分发器
from scrapy import signals #信号量  作用当spider关闭的时候，退出chrome

from bole.items import JobBoleArticleItem,ArticleItemLoader
from bole.function import get_md5

class JobboleSpider(scrapy.Spider):
    name = "JobBole"
    allowed_domains = ["jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-postswwwww/']

    # def __init__(self):
    #     '''chrome放在spider中，防止每打开一个url就跳出一个chrome'''
    #     self.browser=webdriver.Chrome(executable_path='E:/chromedriver.exe')
    #     self.browser.set_page_load_timeout(30)
    #     super(JobboleSpider, self).__init__()
    #     dispatcher.connect(self.spider_close,signals.spider_closed)
    #
    # def spider_close(self,spider):
    #     #当爬虫退出的时候关闭Chrome
    #     print("spider closed")
    #     self.browser.quit()

    # 收集伯乐在线所有404的url以及404页面数
    handle_httpstatus_list = [404]

    def __init__(self, **kwargs):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    def parse(self, response):
        '''
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        '''

        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes=response.xpath('//*[@id="archive"]/div/div[1]/a')
        for post_node in post_nodes:
            image_url=post_node.xpath('img/@src').extract_first('')  #获取文章的列表的封面图片
            article_url=post_node.xpath('@href').extract_first('')   #获取文章的链接
            yield Request(
                url=parse.urljoin(response.url,article_url),
                meta={'front_image_url':image_url},
                callback=self.parse_detail
            )
            '''urljoin()是补全缺失的域名；meta是添加封面图片链接'''

        #提取下一页并交给scrapy进行下载
        next_page=response.xpath('//a[@class="next page-numbers"]/@href').extract_first('')
        if next_page:
            yield Request(url=parse.urljoin(response.url,next_page),callback=self.parse)

    def parse_detail(self,response):
        '''通过item loader加载item'''
        front_image_url=response.meta.get('front_image_url','')  #文章封面图，response.meta.get('front_image_url','') 前一个引号是自己定义的名称，后一个空着，这样如果就不会抛异常
        item_loader=ArticleItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',get_md5(response.url))
        item_loader.add_xpath('create_date','//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('front_image_url',[front_image_url])
        item_loader.add_xpath('praise_nums','//div[@class="post-adds"]/span/h10/text()')
        item_loader.add_xpath('comment_nums','//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath('fav_nums','//div[@class="post-adds"]/span[2]/text()')
        item_loader.add_xpath('tags','//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_xpath('content','//div[@class="entry"]')
        article_item=item_loader.load_item()
        yield article_item