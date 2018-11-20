#coding=utf-8

import os
import django
import sys
import json
import pickle

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PatrickLab.settings")

django.setup()

import logging
import redis
from ebrose.models import Author, Poetry
from ebrose.serializers import PoetrySerializer

_Logger = logging.getLogger(__name__)

class InitRedis(object):
    '''初始化 redis 服务

    从 mysql 中搜索 keys　关键词相关的诗词
    :param keys: list - [str, str, ...] 包含令词的 list
    '''

    def __init__(self, keys, redis_instance=None):
        self.redis = redis_instance or redis.Redis()
        self.keys = keys

    def _search_key_from_sql(self, key: str):
        '''搜索某个 key 所有
        '''        
        contents = Poetry.objects.filter(paragraphs__contains=key)
        serializer = PoetrySerializer(contents, many=True)
        # print(len(serializer.data))
        data = list(serializer.data)
        print(type(data))
        print(data[0])
        data = pickle.dumps(data)
        return data

    def run(self):
        '''将所有的令词以及其对应的 dict　存入 redis
        '''
        for _, key in enumerate(self.keys):
            value = self._search_key_from_sql(key)
            self.redis.set(key, value)
            _Logger.info(f"successfully set key = {key} value = {value}")


if __name__ == "__main__":

    keys = ["花"]
    r = InitRedis(keys)
    r.run()