#coding=utf-8

import os
import time
from pydub import AudioSegment

def convert_format(in_memory_audio, _out_format="wav"):
    '''convert memoryfile(mp3) to bytes(wav)

    codes below may be hard to understand
    u should read source code of pydub
    '''
    ase = AudioSegment.from_mp3(in_memory_audio)
    return ase._data


class LikeFile(object):

    def __init__(self, content):

        self.content = content

    def read(self):

        return self.content

    def close(self):

        pass

        