from django.shortcuts import render
from django.http import HttpResponse

from .models import Author, Poetry
from .serializers import PoetrySerializer

from rest_framework import viewsets
from rest_framework.views import APIView

# Create your views here.

# def index(request):
#   pass



# class PoetrySetView(viewsets.ModelViewSet):

#     queryset = Poetry.objects.all()[:5]
#     serializer_class = PoetrySerializer


class PoetryView(APIView):

    def get(self, request, format=None):

        return HttpResponse("hello, world")

    # def post
