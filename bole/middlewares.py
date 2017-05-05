# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
from scrapy import signals
from fake_useragent import UserAgent
logger = logging.getLogger(__name__)


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.per_proxy = crawler.settings.get('RANDOM_UA_PER_PROXY', False)
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
        self.proxy2ua = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)

        if self.per_proxy:
            proxy = request.meta.get('proxy')
            if proxy not in self.proxy2ua:
                self.proxy2ua[proxy] = get_ua()
                logger.debug('Assign User-Agent %s to Proxy %s'
                             % (self.proxy2ua[proxy], proxy))
            request.headers.setdefault('User-Agent', self.proxy2ua[proxy])
        else:
            ua = get_ua()
            request.headers.setdefault('User-Agent', get_ua())


from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse  #传递js加载后的源代码,不会返回给download
class JSPageMiddleware(object):
    #通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == "JobBole":
            try:
                spider.browser.get(request.url)
            except TimeoutException:
                print('30秒timeout之后，直接结束本页面')
                spider.browser.execute_script('window.stop()')
            import time
            time.sleep(3)
            print("访问:{0}".format(request.url))

            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)
            '''编码默认是unicode'''