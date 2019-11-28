__author__ = '田明博'
__date__ = '2019/11/27 17:53'
import redis

redis_cli = redis.StrictRedis(password="123456")
redis_cli.zincrby("search_keywords_set", 1, 'java架构')
redis_cli.zincrby("search_keywords_set", 1, 'c')
redis_cli.zincrby("search_keywords_set", 1, 'c')
redis_cli.zincrby("search_keywords_set", 1, 'py')
opn_search = redis_cli.zrevrange("search_keywords_set", 0, -1, withscores=True)
top=[]
for obj in opn_search:
    keyword,score=obj
    top.append(keyword.decode('utf-8'))
print(top)
