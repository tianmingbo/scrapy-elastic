__author__ = '田明博'
__date__ = '2019/11/27 20:40'

# -*- coding: utf-8 -*-

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])  # 连接服务器


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        # 避免报错
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class JobType(DocType):
    '''
    Text：
        会分词，然后进行索引
        支持模糊、精确查询
        不支持聚合

    keyword：
        不进行分词，直接索引
        支持模糊、精确查询
        支持聚合
    '''
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    salary = Keyword()
    job_city = Text(analyzer="ik_max_word")
    work_years = Keyword()
    degree_need = Keyword()
    job_type = Keyword()
    job_need = Keyword()
    job_responsibility = Keyword()
    job_advantage = Keyword()
    job_url = Keyword()
    publish_time = Keyword()
    company_name = Text(analyzer="ik_max_word")
    company_url = Keyword()

    class Meta:
        index = "lagou"  # 索引===数据库
        doc_type = "job"  # 类型===表名


if __name__ == "__main__":
    JobType.init()  # 根据定义的类，生成mappings
