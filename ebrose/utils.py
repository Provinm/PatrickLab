#coding=utf-8

import os
import time
from pydub import AudioSegment

def convert_format(in_memory_audio, _out_format="pcm"):

    file_name = in_memory_audio.name.split("=")[-1]
    file_path = "."
    # ase = AudioSegment()

    path = os.path.abspath(os.path.join(file_path, file_name))
    print(f"save to {path}")
    with open(path, "wb+")as f:
        f.write(in_memory_audio.read())

    
    ase = AudioSegment.from_mp3(path)
    ase.export("321.pcm", format=_out_format)

    with open(path, "rb")as f:
        return f.read()




