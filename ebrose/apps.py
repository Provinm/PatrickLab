from django.apps import AppConfig
from django_redis import get_redis_connection

INIT_PIVOTS = ["花"]
DefaultRedis = get_redis_connection("default") # 存放 sql 查询诗句

class EbroseConfig(AppConfig):
    name = 'ebrose'

    def ready(self):
        # 把　月、花　的id 存到 DefaultRedis 中
        from .models import Sentence
        for pivot in INIT_PIVOTS:
            query = Sentence.objects.filter(text__contains=pivot)
            ids = []
            count = 0
            for s in query:
                if count > 300:
                    break
                else:
                    count += 1
                _id = s.poetry.id
                ids.append(_id)

            DefaultRedis.sadd(pivot, *ids)