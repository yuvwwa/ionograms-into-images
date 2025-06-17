from . import ionogram
import json
import subprocess
import importlib.resources
import os
import io

# По JSON попробовать:
# https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

reader_name = "ionreader-driver"
if os.name == "nt":
    reader_name += ".exe"

ret = ''

def decode_pasp_string(input_str : str):
    '''
    Сконвертировать строку паспорта в Юникод
    (Актуально для Windows)
    '''
    return bytes(input_str, 'cp1251').decode('utf-8')

def read_ionogram(path: str) -> ionogram.Ionogram:
    cmd = ''

    with importlib.resources.path(__package__, reader_name) as exe:
        cmd = [
            str(exe),
            path
        ]

    ret = subprocess.check_output(cmd, text=True).replace(
        '\n', '').replace('\t', '')

    j = json.loads(ret)

    ion_obj = ionogram.Ionogram.from_dict(j)

    return ion_obj

# Почитать по чтению ресурса из пакета
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
# https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
# https://importlib-resources.readthedocs.io/en/latest/using.html
