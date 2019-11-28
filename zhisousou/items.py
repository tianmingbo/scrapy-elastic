# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import redis
import scrapy
from scrapy.loader.processors import MapCompose
from models.es_type import JobType

from elasticsearch_dsl.connections import connections

es = connections.create_connection(JobType._doc_type.using)  # 连接到es

redis_cli = redis.StrictRedis(password='123456')


def remove_splash(value):
    # 去除'/'
    return value.replace("/", "")


class ZhisousouItem(scrapy.Item):
    title = scrapy.Field()  # 职位名称
    salary = scrapy.Field()  # 薪水
    job_city = scrapy.Field(input_processor=MapCompose(remove_splash),)  # 工作城市
    work_years = scrapy.Field(input_processor=MapCompose(remove_splash), )  # 工作年限
    degree_need = scrapy.Field(input_processor=MapCompose(remove_splash), )  # 学历要求
    job_type = scrapy.Field()  # 工作类型
    job_need = scrapy.Field()  # 职位要求
    job_responsibility = scrapy.Field()  # 岗位职责
    job_advantage = scrapy.Field()  # 职位优势
    job_url = scrapy.Field()  # 工作链接，发布于哪个公司
    publish_time = scrapy.Field()  # 发布时间
    company_name = scrapy.Field()  # 公司名称
    company_url = scrapy.Field()  # 公司链接

    def save_to_es(self):
        #保存到es中
        job = JobType()
        job.title = self['title']
        job.salary = self["salary"]
        job.job_city = self["job_city"]
        job.work_years = self["work_years"]
        job.degree_need = self["degree_need"]
        job.job_type = self["job_type"]
        job.job_need = self["job_need"]
        job.job_responsibility = self["job_responsibility"]
        job.job_advantage = self["job_advantage"]
        job.job_url = self["job_url"]
        job.publish_time = self["publish_time"]
        job.company_name = self["company_name"]
        job.company_url = self["company_url"]
        # 搜索建议
        # article.suggest=[{"input":[],"weight":2}]  #搜索建议的格式
        job.suggest = gen_suggests(JobType._doc_type.index, ((job.title, 10), (job.job_city, 7)))

        job.save()

        redis_cli.incr("lagou_count")  # 每个网站爬取的数量，使用redis

        return


def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串，使用分析器进行分词，可以提供搜索建议
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            # 获取分析后的词，过滤单个词
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests
