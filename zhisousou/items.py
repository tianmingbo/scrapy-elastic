# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


class ZhisousouItem(scrapy.Item):
    title = scrapy.Field()  # 职位名称
    salary = scrapy.Field()  # 薪水
    job_city = scrapy.Field()  # 工作城市
    work_years = scrapy.Field()  # 工作年限
    degree_need = scrapy.Field()  # 学历要求
    job_type = scrapy.Field()  # 工作类型
    job_need = scrapy.Field()  # 职位要求
    job_responsibility = scrapy.Field()  # 岗位职责
    job_advantage = scrapy.Field()  # 职位优势
    job_url = scrapy.Field()  # 工作链接，发布于哪个公司
    publish_time = scrapy.Field()  # 发布时间
    company_name = scrapy.Field()  # 公司名称
    company_url = scrapy.Field()  # 公司链接
    crawl_time = scrapy.Field()  # 爬取时间
