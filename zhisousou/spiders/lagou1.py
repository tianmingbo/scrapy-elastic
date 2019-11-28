# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from datetime import datetime
from ..items import ZhisousouItem


class Lagou1Spider(CrawlSpider):
    name = 'lagou1'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.lagou.com/zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'https://www.lagou.com/jobs/.*'), follow=True, callback='parse_detail'),
    )

    def parse_item(self, response):
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item

    def parse_detail(self, response):
        # 数据解析
        item_loader = ItemLoader(item=ZhisousouItem(), response=response)
        item_loader.add_xpath('title', '//h1[@class="name"]/text()')
        item_loader.add_xpath('salary', '//span[@class="salary"]/text()')
        item_loader.add_xpath('work_years', '//dd[@class="job_request"]//span[3]/text()')
        item_loader.add_xpath('job_city', '//dd[@class="job_request"]//span[2]/text()')
        item_loader.add_xpath('degree_need', '//dd[@class="job_request"]//span[4]/text()')
        item_loader.add_xpath('job_type', '//dd[@class="job_request"]//span[5]/text()')
        item_loader.add_xpath('job_advantage', '//dd[@class="job-advantage"]//p/text()')
        all_job_desc = response.xpath('//dd[@class="job_bt"]//text()').getall()
        all_job_desc = ''.join(all_job_desc).replace('\n', '')
        item_loader.add_value('job_need', all_job_desc.split('任职要求：')[-1].strip())
        item_loader.add_value('job_responsibility', all_job_desc.split('岗位职责：')[1].split('任职要求：')[0].strip())
        item_loader.add_value('job_url', '来自拉勾网')
        publish_time = response.xpath('//p[@class="publish_time"]/text()').get().split('\xa0')[0]
        item_loader.add_value('publish_time', publish_time)
        company_name = response.xpath('//h4[@class="company"]/text()').get()[0:-2]
        item_loader.add_value('company_name', company_name)
        company_url = response.xpath('//h4[@class="c_feature_name"]/text()').getall()[3]
        item_loader.add_value('company_url', company_url)

        job_item = item_loader.load_item()
        return job_item
