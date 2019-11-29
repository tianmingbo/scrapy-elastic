# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import random
from scrapy.loader import ItemLoader

from ..items import ZhisousouItem


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://zhaopin.com/']

    def parse(self, response):
        # 获取所有职业类别
        type_list = response.xpath('//div[@class="zp-jobNavigater__pop--container"]//text()').getall()
        # 获取互联网类职业
        types = type_list[1:type_list.index(' ', 2)]
        addr_code = [530, 538, 765, 763, 531, 801, 653, 736, 600, 613, 635]
        addr_code = random.choice(addr_code)
        # for type in types:
        #     url = 'https://sou.zhaopin.com/?jl={}&kw={}&kt=3&sf=0&st=0'.format(addr_code, type)
        #     yield Request(url, callback=self.type_detail)

        url = 'https://sou.zhaopin.com/?jl={}&kw={}&kt=3&sf=0&st=0'.format(addr_code, 'Python')
        yield Request(url, callback=self.type_detail)


    def type_detail(self, response):
        job_lists = response.xpath('//a[@class="contentpile__content__wrapper__item__info"]/@href').getall()
        for job_url in job_lists:
            yield Request(job_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item_loader = ItemLoader(item=ZhisousouItem(), response=response)
        item_loader.add_xpath('title', '//h3[@class="summary-plane__title"]/text()')
        item_loader.add_xpath('salary', '//span[@class="summary-plane__salary"]/text()')
        item_loader.add_value('work_years', response.xpath('//ul[@class="summary-plane__info"]//text()').getall()[1])
        item_loader.add_value('job_city', response.xpath('//ul[@class="summary-plane__info"]//text()').getall()[0])
        item_loader.add_value('degree_need', response.xpath('//ul[@class="summary-plane__info"]//text()').getall()[2])
        item_loader.add_value('job_type', '全职')
        job_advantage = ','.join(response.xpath('//span[@class="highlights__content-item"]//text()').getall())
        item_loader.add_value('job_advantage', job_advantage)

        item_loader.add_xpath('job_need', '//div[@class="describtion__detail-content"]')
        item_loader.add_value('job_responsibility', '')

        item_loader.add_value('job_url', '来自智联招聘')
        publish_time = response.xpath('//span[@class="summary-plane__time"]/text()').get()[5:]
        item_loader.add_value('publish_time', publish_time)

        item_loader.add_xpath('company_name', '//a[@class="company__title"]/text()')
        company_url = response.xpath('//a[@class="company__title"]/@href').get()
        item_loader.add_value('company_url', company_url)

        job_item = item_loader.load_item()
        return job_item
