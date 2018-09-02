#coding=utf-8

'''
导入 唐诗宋词的脚本
'''
import os
import json


class ImportSC(object):

	def __init__(self, path):

		self.path = path

	def _get_all_files(self):

		for root, dirs, files in os.walk(self.path):
			pass