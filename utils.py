from filepath.tool_relative_paths import FilePaths

import numpy as np
import cv2
import pytesseract as tess
from paddleocr import PaddleOCR
import sys
import os

import inspect
import ctypes
import requests
import json
import traceback
import time
import numpy
from matplotlib.pyplot import box

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

def img_to_string(img):
    ocr = PaddleOCR(lang="ch", use_gpu=False, use_angle_cls=False, show_log=False)
    ocr_result = ocr.ocr(img, cls=False, det=False)
    line = ocr_result[0][0]
    result = line[0]
    # log('img_to_string', result)
    return result

def img_to_string_eng(img):
    # pil_image.save(resource_path("test.png"))
    # tess.pytesseract.tesseract_cmd = resource_path(FilePaths.TESSERACT_EXE_PATH.value)
    # result = tess.image_to_string(pil_image, lang='eng', config='--psm 6')
    # result = result.replace('\t', '').replace('\n', '').replace('\f', '')
    
    ocr = PaddleOCR(lang="en", use_gpu=False, use_angle_cls=False, show_log=False)
    ocr_result = ocr.ocr(img, cls=False, det=False)
    line = ocr_result[0][0]
    result = line[0]
    # log('img_to_string_eng', result)
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
 
def canny(img):
    d = img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # d = img_gray / 255
    
    scale=1
    adx = dx = cv2.Sobel(d, -1, 1, 0, scale=scale)
    # adx = cv2.convertScaleAbs(dx * 255)
    ady = dy = cv2.Sobel(d, -1, 0, 1, scale=scale)
    # ady = cv2.convertScaleAbs(dy * 255)
    
    adxy = cv2.addWeighted(adx, 0.5, ady, 0.5, 0)
    
    # hist = cv2.calcHist([adxy], [0], None, [256], [0, 256]).ravel()
    hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256]).ravel()
    adxy_max = np.max(adxy)
    
    total = adxy.shape[0] * adxy.shape[1] * .99
    bin_sum = 0
    i = 0
    # for bin_hist in hist:
    for i in range(len(hist)):
        bin_hist = hist[i]
        bin_sum += bin_hist
        # print('i:', i, 'bin_hist', bin_hist)
        if bin_sum >= total:
            break;
        # i += 1
        
    upper = i #(i + 1) * adxy_max / 255
    lower = .3 * upper
    last_result = cv2.Canny(img_gray, lower, upper)
    
    return last_result   
 
def fix_max_contours(img, fill=True):
    _, img_thresh = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # opencv2返回两个值：contours, hierarchy
    # opencv3会返回三个值：img, countours, hierarchy
    contours = cnts[0] if len(cnts) == 2 else cnts[1]
    hierarchy = cnts[1] if len(cnts) == 2 else cnts[2]
    hierarchy = np.squeeze(hierarchy)
    
    max_area = 0
    max_index = 0
    max_c = contours[0]
    # print('len(contours):', len(contours))
    for i in range(len(contours)):
        c = contours[i]
        h = hierarchy[i]
        area = cv2.contourArea(c)
        if area > max_area:
            max_area = area
            max_index = i
            
    for i in range(len(contours)):
        c = contours[i]
        h = hierarchy[i]
        if i == max_index:
            max_c = c
            if fill:
                cv2.drawContours(img, [c], -1, 255, thickness=cv2.FILLED)
        else:
            cv2.drawContours(img_thresh, [c], -1, 0, thickness=cv2.FILLED)
            
    img_result = cv2.bitwise_and(img, img_thresh)

    return img_result, max_c

def resize(img, new_size, padding=True, fixScale=32):
    w = img.shape[1]
    h = img.shape[0]
    
    n_w = new_size[0]
    n_h = new_size[1]
    
    scale = w / h
    scale_n = n_w / n_h
    
    out_w = n_w
    out_h = n_h
    
    top, bottom, left, right = (0, 0, 0, 0)
    delta = 0
    
    # print("resize {} => {}, padding:".format(scale, scale_n), padding)
    
    if not padding:
        if scale > scale_n:
            out_w = (int)(n_h / h * w)
            if fixScale > 0:
                out_w = (int)(out_w / fixScale) * fixScale
                out_h = (int)(out_w / scale)
            delta = out_h - out_w
            left = delta // 2
            right = delta - left
        elif scale < scale_n:
            out_h = (int)(n_w / w * h)
            if fixScale > 0:
                out_h = (int)(out_h / fixScale) * fixScale
                out_w = (int)(out_h * scale)
            delta = n_h - n_w
            top = delta // 2
            bottom = delta - top
        
        # print("resize {}x{} => {}x{}".format(w, h, out_w, out_h))
        img = cv2.resize(img, (out_w, out_h), interpolation=cv2.INTER_CUBIC)
    else:
        if scale > scale_n:
            out_w = (int)(n_h / h * w)
            if fixScale > 0:
                out_w = (int)(out_w / fixScale) * fixScale
                out_h = (int)(out_w / scale)
            delta = n_w - out_w
            left = delta // 2
            right = delta - left
        elif scale < scale_n:
            out_h = (int)(n_w / w * h)
            if fixScale > 0:
                out_h = (int)(out_h / fixScale) * fixScale
                out_w = (int)(out_h * scale)
            delta = n_h - out_h
            top = delta // 2
            bottom = delta - top
        
        # print("resize {}x{} => {}x{}".format(w, h, out_w, out_h))
        img = cv2.resize(img, (out_w, out_h), interpolation=cv2.INTER_CUBIC)
        
        # print("padding {},{},{},{} delta:{}".format(top, bottom, left, right, delta))
        BLACK = [0,0,0]
        # WHITE = [255,255,255]
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value = BLACK)
    
    return img

def is_dark(img, thresh=100):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    avg = cv2.mean(img_gray)[0]
    print('is_dark', avg)
    if avg < thresh:
        return True, avg;
    return False, avg