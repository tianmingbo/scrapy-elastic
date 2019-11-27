# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class Boss1Spider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/']

    def parse(self, response):
        all_type_url = response.xpath('//div[@class="menu_box"][1]//a/@href').getall()
        for type in all_type_url:
            yield Request(type, callback=self.parse_job_list)
        # print(response.status)

    def parse_job_list(self, response):
        job_list = response.xpath('//a[@class="position_link"]/@href').getall()
        for job_link in job_list:
            yield Request(job_link, callback=self.parse_detail)

    def parse_detail(self, response):
        print('detail')