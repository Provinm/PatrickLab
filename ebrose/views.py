import copy
import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, FileResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection

from .models import Author, Poetry, Sentence
from .serializers import PoetrySerializer

from .aip import AipSpeech
from .utils import convert_format, gen_cookie

_Logger = logging.getLogger(__file__)

APP_ID = "11759968"
API_KEY = "reR65KYW8omwyQk9fhVXbGMx"
SECRETE_KEY = "xBPDPtfSvwA2dOuFii5VoHyPbeIdUTH3"

SessionRedis = get_redis_connection("session") # 存放登录的 cookie 和 pivot
DefaultRedis = get_redis_connection("default") # 存放 sql 查询诗句
# ProcessRedis = get_redis_connection("process") # 存放用户和电脑的交互过程数据
RemainRedis = get_redis_connection("remain")   # 某用户和server剩余的可说的 poetry id
BaiDuClient = AipSpeech(APP_ID, API_KEY, SECRETE_KEY)

'''定义的 ret 值

0 : 正常
200X: 百度　asr / tts 除了问题
    2000: asr 无结果
300x: 后端服务问题
    3000: 用户未登录
    3001: 用户说的诗句不在数据库中
    3002: 用户说的诗句已经在历史中

'''

DEFAULT_RES = {
    "ret": 0,
    "msg": "",
    "data": ""
}


def exist_or_create(pivot: str, cookie: str):
    '''查看 redis 中是否存在 pivot 

    否则创建当前的 pivot
    '''

    is_existed = DefaultRedis.exists(pivot)  # Returns the number of names that exist
    if not is_existed:
        query = Sentence.objects.filter(text__contains=pivot)
        for q in query:
            DefaultRedis.sadd(pivot, q.id)
            RemainRedis.sadd(cookie, q.id)

    else:
        members = DefaultRedis.smembers(pivot)
        RemainRedis.sadd(cookie, *members)
        
    return True


class PoetryView(APIView):

    def get(self, request, format=None):

        return HttpResponse("hello, world")


class PivotView(APIView):
    '''用户匿名登录,并初始化 pivot 数据

    不要求用户登录，所以在此自己记录一下用户发的　令词

    '''
    def get(self, request, *args, **kw):

        pivot = request.query_params.get("pivot")
        # print(pivot, type(pivot))
        # 初始化 pivot
        cookie = gen_cookie()
        # print(cookie)
        exist_or_create(pivot, cookie)
        SessionRedis.set(cookie, pivot)
        default_res = copy.copy(DEFAULT_RES)
        default_res["msg"] = "记录令成功"
        default_res["data"] = {"pivot": pivot,
                               "cookie": cookie}
        return Response(default_res)


class AsrView(APIView):
    '''ASR interface

    this interface accept audio file from client.
    method POST

    
    received audio -> encoding to wav -> send to baidu aip -> fuzzyx match -> return
    requests.post("/ebrose/asr", data={"audio": xxx})

    refer :
    https://docs.djangoproject.com/en/2.1/_modules/django/core/files/uploadedfile/#InMemoryUploadedFile

    '''
    def post(self, request, *args, **kw):
        
        user = request.query_params.get("cookie")
        default_res = copy.copy(DEFAULT_RES)
        if not user:
            default_res["msg"] = "未登录"
            default_res["ret"] = 3000
            return default_res

        pivot = SessionRedis.get(user)
        # 找出令词记录
        if pivot:

            audio_bytes = request.data.get("file")
            audio_bytes = convert_format(audio_bytes)
            res = BaiDuClient.asr(audio_bytes) or {}
            # 请求失败
            if res.get("err_no") == 2000:
                default_res["msg"] = res["err_msg"]
                default_res["ret"] = 2000

            # 请求成功
            else:
                raw_result = res.get("result")
                result = res.get("result", [""])[0]
                # 找出含有 pivot 的句子
                result = [i for i in result.split(",") if pivot in i] or [""]
                result = result[0]
                # ＃＃＃＃＃＃＃＃＃＃＃
                # 　鉴于目前的精力，实现模糊匹配一段字符串和完整的诗句这个算法有些困难
                #   目前采用包含匹配的模式进行契合　　
                # ＃＃＃＃＃＃＃＃＃＃＃
                # 如果用户说出含有 pivot 的句子字数大于1，　则认为有效
                # 这样的算法是有问题的，个人项目没有必要做到商业性的准确度
                if len(result) > 1:
                    query = Sentence.objects.filter(text__contains=result)
                    # 用户说的句子在数据库中
                    if len(query) > 0:
                        sentence = query[0]
                        poetry = sentence.poetry
                        # poetry_members = DefaultRedis.members(pivot)
                        _, _search_res = RemainRedis.sscan(pivot, match=poetry.id)
                        # 有查询结果
                        if _search_res:
                            _search_id = _search_res[0]
                            # 查看当前的 id 是否在历史记录中
                            # _, _process_res = ProcessRedis.sscan(user, match=_search_id)
                            # 在历史记录中
                            # if _process_res:
                            #     default_res["ret"] = 3002
                            #     default_res["msg"] = "诗句已经说过了"
                            # 没在历史记录中
                            # 向用户返回 poetry 数据
                            # else:
                            default_res["ret"] = 0
                            default_res["msg"] = "结果有效"
                            default_res["data"] = {"poetry": PoetrySerializer(poetry),
                                                   "raw": raw_result}
                            RemainRedis.srem(pivot, _search_id)

                        # pivot 不在 redis 记录中
                        else:
                            default_res["ret"] = 3002
                            default_res["msg"] = "诗句已经说过了"

                    # 用户说的句子不在数据库中
                    else:
                        default_res["ret"] = 3001
                        default_res["msg"] = "数据不在mysql中"

            return Response(default_res)

            

class TTSView(APIView):
    '''TTS

    发送 text 到百度服务，返回录音到小程序播放
    '''
    def get(self, request, *args, **kw):

        user = request.query_params.get("cookie")
        default_res = copy.copy(DEFAULT_RES)
        if not user:
            default_res["msg"] = "未登录"
            default_res["ret"] = 3000
            return default_res

        # 拿出令词
        pivot = SessionRedis.get(user)
        # 随机选一个含有 pivot 的 poetry
        _poetry_id = RemainRedis.spop(user)
        # 已经没有可用的诗句了
        if not _poetry_id:
            default_res["msg"] = "无剩余的可用的诗句"
            default_res["ret"] = 3004
            return default_res

        _poetry_id = int(_poetry_id.decode("utf-8"))
        poetry = Poetry.objects.get(pk=_poetry_id)

        text = ""
        for sentence in poetry.sentence:
            if pivot in sentence.text:
                text = sentence.text
                break

        # 请求百度 tts
        content = BaiDuClient.synthesis(text)
        if isinstance(content, dict):
            return JsonResponse(content)
        else:
            response = HttpResponse(content_type="audio/mp3")
            response.write(content)
            return response