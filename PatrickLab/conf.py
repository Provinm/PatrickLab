#coding=utf-8

import os

CONST = {
    "EBROSE_SECRET_KEY": "n1e!h(cc0@d_n0ur$f9b4mcq49j$c@w3o5#(9(=b5b#1%i0^-4",
    "DJANGO_MYSQL_USER": "zhouxin",
    "DJANGO_MYSQL_PASSWORD": "782744680",
    "DATABASE_NAME": "ebrose",
    "DJANGO_DEBUG_SWITCH": "true"
}


def set_env():
    '''set os environment varibles
    '''
    print("begin ")
    for key, val in CONST.items():
        os.environ[key] = val

