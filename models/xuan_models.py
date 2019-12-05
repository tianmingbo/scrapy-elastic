__author__ = '田明博'
__date__ = '2019/12/3 16:22'
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


class XuanType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    # 宣讲会根据题目和城市搜索
    title = Text(analyzer="ik_max_word")
    city = Text(analyzer="ik_max_word")
    img = Keyword()
    address = Keyword()
    time = Keyword()
    status = Keyword()
    detail_url = Keyword()
    from_school = Keyword()

    class Meta:
        index = "xuan"  # 索引===数据库
        doc_type = "info"  # 类型===表名


if __name__ == "__main__":
    XuanType.init()  # 根据定义的类，生成mappings
