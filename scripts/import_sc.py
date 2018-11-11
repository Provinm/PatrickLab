#coding=utf-8

'''
导入 唐诗宋词的脚本
'''

# obsoled run django

import os
import django
import sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PatrickLab.settings")

django.setup()


import json

from ebrose.models import Author, Poetry

class ImportSC(object):
    '''
    analyse all data from "https://github.com/chinese-poetry/chinese-poetry"
    sort and insert them into db.
    '''
    def __init__(self, path):

        self.path = path
        self._poet_slots = ["author", "paragraphs", "dynasty", "title", "rhythmic", "_type"]

    def _get_all_files(self):
        '''extract all files from project 
        sort them in a dict
        {
            "poet": {
                "tang": [],
                "song": [],
                "other": []
            },
            "ci": {
                "tang": [],
                "song": [],
                "other": []
            },

            # ...
        }

        '''
        files_dict = {}
        for root, dirs, files in os.walk(self.path):
            for f in files:
                if not f.endswith(".json"):
                    continue
                path = os.path.join(root, f)
                # 处理唐诗
                if "poet" in f:
                    if "tang" in f:
                        files_dict.setdefault("poet", {}).setdefault("tang", []).append(path)

                    elif "song" in f:
                        files_dict.setdefault("poet", {}).setdefault("song", []).append(path)

                    else:
                        files_dict.setdefault("poet", {}).setdefault("other", []).append(path)

                # 宋词
                elif "ci" in f:
                    if "tang" in f:
                        files_dict.setdefault("ci", {}).setdefault("tang", []).append(path)
                    elif "song" in f:
                        files_dict.setdefault("ci", {}).setdefault("song", []).append(path)
                    else:
                        files_dict.setdefault("ci", {}).setdefault("other", []).append(path)

                # 诗经
                elif "shijing" in f:

                    files_dict.setdefault("shijing", {}).setdefault("other", []).append(path)

                # 论语
                elif "lunyu" in f:
                    files_dict.setdefault("lunyu", {}).setdefault("other", []).append(path)

        return files_dict


    def _analysis_single(self, _type, _dy, _data):
        '''analyse and extract data

        :param _type: str, ci or shi or else
        :param _data: dict, a dict contains info of a poet
        '''

        # update type and dynasty
        # _data.update({"_type": _type})
        # _data.update({"dynasty": _dy})
        # print(_data)

        # get auther instance
        author, _ = Author.objects.get_or_create(name=_data.get("author", ""))
        # update author info

        # create new poet object
        if _type == "ci":
            _data.update({"author": author, "dynasty": _dy, "_type": "C"})

        elif _type == "poet":
            _data.update({"author": author, "dynasty": _dy, "_type": "S"})

        elif _type == "shijing":
            _data.update({"author": author, "dynasty": _dy, "_type": "J"})
            _data["paragraphs"] = _data["content"] 

        else:
            return

        new_dct = {}
        for key, value in _data.items():
            if key in self._poet_slots:
                new_dct[key] = value

        Poetry.objects.create(**new_dct)

    def _analyse_bulk(self, _type, _dy, _bulk):
        '''bulk analysis
        '''
        for item in _bulk:
            try:
                self._analysis_single(_type, _dy, item)
            except Exception as e:
                print(f"[ERROR] err happened when insert data err = {e}")
                break


    def _extract_from_file(self, file_path):
        '''extract data and convert to json
        '''
        path = os.path.abspath(file_path)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:

            data = f.read()

        return json.loads(data)


    def run(self):

        files_dict = self._get_all_files()
        for _type, out_dict in files_dict.items():
            for dynasty, files_list in out_dict.items():
                for f_path in files_list:
                    print(f_path)
                    data = self._extract_from_file(f_path)
                    self._analyse_bulk(_type, dynasty, data)


if __name__ == "__main__":

    file_path = r"/home/zhouxin/Documents/projects/chinese-poetry"
    isc = ImportSC(file_path)
    isc.run()









        
        
