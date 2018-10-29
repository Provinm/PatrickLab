#coding=utf-8

from .models import Author, Poetry
from rest_framework import serializers


class PoetrySerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Poetry
		fields = ("title", "paragraphs")