__author__ = '田明博'
__date__ = '2019/11/27 17:53'
import redis
redis_cli = redis.StrictRedis(password='123456')
redis_cli.incr("lagou_count")