import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, FileResponse

from .models import Author, Poetry
from .serializers import PoetrySerializer

from rest_framework import viewsets
from rest_framework.views import APIView

from .aip import AipSpeech
from .utils import convert_format, LikeFile

_Logger = logging.getLogger(__file__)

APP_ID = "11759968"
API_KEY = "reR65KYW8omwyQk9fhVXbGMx"
SECRETE_KEY = "xBPDPtfSvwA2dOuFii5VoHyPbeIdUTH3"

class PoetryView(APIView):

    def get(self, request, format=None):

        return HttpResponse("hello, world")


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
        baidu_asr = AipSpeech(APP_ID, API_KEY, SECRETE_KEY)
        audio_bytes = request.data.get("file")
        audio_bytes = convert_format(audio_bytes)
        res = baidu_asr.asr(audio_bytes)
        return JsonResponse(res)


class TTSView(APIView):

    def get(self, request, *args, **kw):
        text = request.query_params.get("text", "")
        if not text:
            return JsonResponse({"err": "empty text"})

        baidu_tts = AipSpeech(APP_ID, API_KEY, SECRETE_KEY)
        content = baidu_tts.synthesis(text)
        if isinstance(content, dict):
            return JsonResponse(content)
        else:
            response = HttpResponse(content_type="audio/mp3")
            response.write(content)
            return response
            

class SearchView(APIView):
    '''用户搜索相应的令词，返回所有含该令词的诗句
    '''

    def get(self, request, *args, **kw):

        pivot = request.query_params.get("text", "")

        if not pivot:
            return JsonResponse({"err", "empty text"})

        # 现在 redis 中寻找

        # 然后在 mongo 中寻找
        return HttpResponse("hello world")
