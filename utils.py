from filepath.file_relative_paths import FilePaths

import cv2
import pytesseract as tess
import sys
import os

import inspect
import ctypes
import requests
import json
import traceback
import time

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def build_command(program_path, *args):
    return [program_path, *args]


def img_to_string(pil_image):
    # pil_image.save(resource_path("test.png"))
    tess.pytesseract.tesseract_cmd = resource_path(FilePaths.TESSERACT_EXE_PATH.value)
    result = tess.image_to_string(pil_image, lang='chi_sim', config='--psm 6') \
        .replace('\t', '').replace('\n', '').replace('\f', '')
    log('img_to_string', result)
    return result

def img_to_string_eng(pil_image):
    # pil_image.save(resource_path("test.png"))
    tess.pytesseract.tesseract_cmd = resource_path(FilePaths.TESSERACT_EXE_PATH.value)
    result = tess.image_to_string(pil_image, lang='eng', config='--psm 6')
    log('img_to_string_eng', result)
    result = result.replace('\t', '').replace('\n', '').replace('\f', '')
    return result

def img_remove_background_and_enhance_word(cv_image, lower, upper):
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lower, upper)


def aircv_rectangle_to_box(rectangle):
    return rectangle[0][0], rectangle[0][1], rectangle[3][0], rectangle[3][1]


def bot_print(msg):
    print(msg)


def get_last_info(domain):
    try:
        url = domain + '/main/docs/version.json'
        resp_text = requests.get(url).text
        return json.loads(resp_text)
    except Exception as e:
        traceback.print_exc()
        return {}

def log(*args):
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('[{}] {}'.format(time_string, args))
    
def device_log(device, *args):
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('[{}] {}({}) - {}'.format(time_string, f"{device.name.replace(':', '_')}", device.nickname, args))    
