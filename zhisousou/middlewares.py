# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse
import time
import random


class ZhisousouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 设置随机ip
class RandomIpMiddleware(object):
    with open(r'C:\Users\asus\Desktop\爬虫\scrapy教程\zhisousou\utils\ip.txt', 'r') as f:
        PROXIES = f.readlines()
    PROXIE = []
    for i in PROXIES:
        PROXIE.append('http://' + i.replace('\n', ''))

    def process_request(self, request, spider):
        proxy = random.choice(self.PROXIE)
        print(proxy)
        request.meta['proxy'] = proxy


class ZhisousouDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # def __init__(self):
    #     self.driver_path = r'D:\BaiduNetdiskDownload\geckodriver.exe'
    #     self.driver = webdriver.Firefox(executable_path=self.driver_path)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.name == 'zhilian' or spider.name == 'xuanjianghui':
            driver_path = r'D:\BaiduNetdiskDownload\geckodriver.exe'
            driver = webdriver.Firefox(executable_path=driver_path)
            driver.get(request.url)
            time.sleep(2)
            source = driver.page_source
            return HtmlResponse(url=driver.current_url, body=source, encoding='utf-8', request=request)
        else:
            return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
