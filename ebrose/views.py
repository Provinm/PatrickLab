import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Author, Poetry
from .serializers import PoetrySerializer

from rest_framework import viewsets
from rest_framework.views import APIView

from .aip import AipSpeech
from .utils import convert_format

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

        print(request.data)

        baidu_asr = AipSpeech(APP_ID, API_KEY, SECRETE_KEY)
        audio_bytes = request.data.get("file")
        audio_bytes = convert_format(audio_bytes)
        # print(f"{dir(audio_bytes)}")
        # audio_bytes = audio_bytes.read()
        # print(type(audio_bytes))
        res = baidu_asr.asr(audio_bytes)
        print(f"get res {res}")
        return JsonResponse(res)
        # audio_stream = request.
        # return HttpResponse("hello, world")