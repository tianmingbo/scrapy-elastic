# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ..items import XuanItem


class XuanjianghuiSpider(scrapy.Spider):
    name = 'xuanjianghui'
    allowed_domains = ['http://zzuli.goworkla.cn']
    start_urls = ['http://zzuli.goworkla.cn/module/campustalk/nid-1670']

    def parse(self, response):
        item_loader = ItemLoader(item=XuanItem(), response=response)
        all_xuan = response.xpath('//div[@class="infoTips"]')
        all_company_detail = response.xpath('//a[@class="inner-list"]/@href').getall()
        all_company_detail = ['http://zzuli.goworkla.cn' + detail for detail in all_company_detail]
        count = 0
        for xuan in all_xuan:
            img = xuan.xpath('./div//img/@src').get()
            infos = xuan.xpath('./div[2]/p//text()').getall()
            from_school = response.xpath('//div[@class="top-logo"]/a//@alt').get()
            item_loader.add_value('img', img)
            item_loader.add_value('title', infos[0])
            item_loader.add_value('address', infos[1][7:])
            item_loader.add_value('time', infos[2][7:])
            item_loader.add_value('status', infos[4])
            item_loader.add_value('detail_url', all_company_detail[count])  # 详情链接
            item_loader.add_value('from_school', from_school)
            item_loader.add_value('city', '郑州')
            count += 1

        item_xuan = item_loader.load_item()
        print(item_xuan)
        return item_xuan
