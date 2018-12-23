#coding=utf-8

import os
import time
import string
import random
from pydub import AudioSegment

def convert_format(in_memory_audio, _out_format="wav"):
    '''convert memoryfile(mp3) to bytes(wav)

    codes below may be hard to understand
    u should read source code of pydub
    '''
    ase = AudioSegment.from_mp3(in_memory_audio)
    return ase._data


def gen_cookie(k:int = 8):
    ascii_le = string.ascii_letters
    digits = string.digits
    str_dir = ascii_le + digits
    lst_dir = list(str_dir * 10)
    cookie = ''.join(random.sample(lst_dir,k))
    return cookie