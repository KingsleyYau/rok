from PIL import Image
from filepath.file_relative_paths import ImagePathAndProps
from filepath.file_relative_paths import GuiCheckImagePathAndPropsOrdered
from filepath.tool_relative_paths import FilePaths
from utils import resource_path
from utils import img_to_string, img_to_string_eng
from utils import img_remove_background_and_enhance_word
from utils import bot_print

from enum import Enum
import traceback
import numpy as np
import cv2
from bot_related import aircve as aircv
import io
from utils import log, device_log
from filepath.constants import HELLO_WROLD_IMG
import re
import time
# small percentage are more similar
def cal_similarity(image1, image2):
    res = cv2.absdiff(image1, image2)
    # --- convert the result to integer type ---
    res = res.astype(np.uint8)
    # --- find percentage difference based on number of pixels that are not zero ---
    percentage = (np.count_nonzero(res) * 100) / res.size

    return percentage


class GuiName(Enum):
    HOME = 0
    MAP = 1
    WINDOW = 2
    WINDOW_TITLE = 3
    VERIFICATION_CHEST = 4
    VERIFICATION_VERIFY = 5
    VERIFICATION_VERIFY_TITLE = 6
    VERIFICATION_CLOSE_REFRESH_OK = 7
    HELLO_WROLD_IMG = 8


class GuiDetector:

    def __init__(self, device):
        self.debug = False
        self.__device = device

    def get_curr_device_screen_img_byte_array(self):
        img = self.__device.screencap()
        return img

    def get_curr_device_screen_img_cv(self):
        img = self.__device.screencap()
        img = cv2.imdecode(np.asarray(img, dtype=np.uint8), cv2.IMREAD_COLOR)
        return img
    
    def get_curr_device_screen_img(self):
        return Image.open(io.BytesIO(self.__device.screencap()))

    def save_screen(self, file_name):
        image = Image.open(io.BytesIO(self.__device.screencap()))
        image.save(resource_path(FilePaths.TEST_SRC_FOLDER_PATH.value + file_name))

    def get_curr_gui_name(self):
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                     cv2.IMREAD_COLOR)
        for image_path_and_props in GuiCheckImagePathAndPropsOrdered:
            result = self.check_any(image_path_and_props.value, imsch=imsch)
            if result[0]:
                return [result[1], result[2]]
        if not result[0]:
            return self.get_hello_world_gui()
        return None

    def get_hello_world_gui(self):
        result = self.check_any_gray(
            ImagePathAndProps.HELLO_WROLD_IMG_PATH.value
        )
        # device_log(self.__device, 'get_hello_world_gui', result)
        if result[0]:
            return [result[1], result[2]]
        return None
    
    def get_windows_name(self):
        path, size, box, threshold, least_diff, gui = ImagePathAndProps.WINDOW_TITLE_MARK_IMG_PATH.value

        imsch = cv2.resize(
            cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR),
            size
        )
        imsrc = cv2.imread(resource_path(path))

        # find 2 window title mark location
        result = aircv.find_all_template(imsrc, imsch, threshold)

        # get box position from result
        x0, x1, y0, y1 = 0, 0, 0, 0
        if result is not None and len(result) == 2:
            x0 = result[0]['rectangle'][2][0] + 50
            x1 = result[1]['rectangle'][0][0] - 50
            y0 = result[0]['rectangle'][0][1]
            y1 = result[0]['rectangle'][1][1]
        else:
            return None
        # crop image for ocr
        title_image = imsch[y0:y1, x0:x1]
        title_image = img_remove_background_and_enhance_word(title_image, np.array([0, 0, 160]),
                                                             np.array([255, 255, 255]))
        title_image = Image.fromarray(title_image)
        return img_to_string(title_image)
    
    def get_kilometer(self):
        kilo = -1
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR)
        try:
            pos = self.check_any(ImagePathAndProps.KILO_IMG_PATH.value)[2]
            if pos is not None:
                # device_log(self.__device, 'get_kilometer', pos)
                box = (int(pos[0]) - 46, int(pos[1]) - 8, int(pos[0]) - 15, int(pos[1]) + 9)
                # device_log(self.__device, 'get_kilometer', box)
                x0, y0, x1, y1 = box
                imdst = imsch[y0:y1, x0:x1]
                # kilo_image = Image.fromarray(imdst)
                # kilo_image.save('script/kilo.png')
                imdst = cv2.cvtColor(imdst, cv2.COLOR_BGR2GRAY)
                _, imdst = cv2.threshold(imdst, 190, 255, cv2.THRESH_BINARY)
                # cv2.imwrite('script/kilo_v.png', imdst)
                
                kilo_image = Image.fromarray(imdst)
                rec = img_to_string_eng(kilo_image).replace(' ', '').replace(',', '')
                rec = re.sub('[^0-9]', '', rec)
                if len(rec) > 0:
                    kilo = int(rec)
                # device_log(self.__device, 'get_kilometer', kilo)
        except Exception as e:
            device_log(self.__device, 'get_kilometer', e)
            traceback.print_exc()
        return kilo

    def player_name(self, box=None, imsch=None):
        name = ""
        if box is None:
            box = (485, 182, 645, 212)
        try:
            if imsch is None:
                imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            x0, y0, x1, y1 = box
            imdst = imsch[y0:y1, x0:x1]
            # troop_image = Image.fromarray(imdst)
            # _, imdst = cv2.threshold(imdst, 190, 255, cv2.THRESH_BINARY)
            # cv2.imwrite('script/troop_image_v.png', imdst)
            troop_image = Image.fromarray(imdst)
            name = img_to_string(troop_image).replace(' ', '').replace('\n', '')
            device_log(self.__device, 'player_name, {}'.format(name))
        except Exception as e:
            device_log(self.__device, 'player_name', e)
            traceback.print_exc()
        return name
        
    def troop_already_full(self):
        box = (1205, 160, 1245, 180)
        try:
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            x0, y0, x1, y1 = box
            imdst = imsch[y0:y1, x0:x1]
            # troop_image = Image.fromarray(imdst)
            _, imdst = cv2.threshold(imdst, 190, 255, cv2.THRESH_BINARY)
            # cv2.imwrite('script/troop_image_v.png', imdst)
            troop_image = Image.fromarray(imdst)
            rec = img_to_string_eng(troop_image).replace(' ', '').replace(',', '').replace('\n', '')
            if len(rec) > 1:
                device_log(self.__device, '检查队列数量, {}/{}'.format(rec[0], rec[-1]))
                rec = rec.replace('s', '5').replace('S', '5')
                return rec[0].lower() == rec[-1].lower(), rec[0], rec[-1]
        except Exception as e:
            device_log(self.__device, '检查队列数量', e)
            traceback.print_exc()
        return False, -1, -1
    
    def resource_amount_image_to_string(self):
        result_list = []
        boxes = [
            (695, 10, 770, 34), (820, 10, 890, 34), (943, 10, 1015, 34), (1065, 10, 1140, 34), (1182, 10, 1245, 34)
        ]
        try:
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            i = 0
            for box in boxes:
                x0, y0, x1, y1 = box
                imdst = imsch[y0:y1, x0:x1]
                resource_image = Image.fromarray(imdst)
                # resource_image.save('capture/resource_{}.png'.format(i))
                i = i + 1
                try:
                    # 英文识别
                    rec = img_to_string_eng(resource_image).replace(' ', '').replace(',', '').replace('1Z', '')  
                    # 中文识别
                    rec_unit = img_to_string(resource_image).replace(' ', '').replace(',', '')
                    
                    # 没有小数, 直接使用中文识别
                    if (rec.find('.') == -1):
                        rec = rec_unit
                    # 删除以下字符
                    # 1.非数字开头
                    # 2.非数字/小数点
                    # 3.非数字结尾
                    rec = re.sub('^\D+|[^0-9.]|\D+$', '', rec)   
                    
                    # 处理单位
                    unit = 1 
                    if (rec_unit.find('亿') != -1) or (rec_unit.find('仁') != -1) or (rec_unit.find('伍') != -1):
                        unit = 100000000
                    elif rec_unit.find('万') != -1:
                        unit = 10000
                    else:
                        unit = 1
                        rec = rec.replace('.', '')
                    # rec = rec.replace('亿', '').replace('万', '').replace('仁', '').replace('伍', '')
                    count = int(float(rec) * unit)
                    device_log(self.__device, 'resource_amount_image_to_string', 'rec:{}, unit:{}, count:{}'.format(rec, unit, count))
                    result_list.append(count)
                except Exception as e:
                    result_list.append(-1)
                    device_log(self.__device, 'resource_amount_image_to_string', e)
                    traceback.print_exc()
        except Exception as e:
            device_log(self.__device, 'resource_amount_image_to_string', e)
            traceback.print_exc()
        return result_list

    def materilal_amount_image_to_string(self):
        result_list = []
        boxes = [
            (710, 245, 800, 264),
            (820, 245, 900, 264),
            (910, 245, 990, 264),
            (1000, 245, 1100, 264),
        ]
        i=0
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR)
        imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
        for box in boxes:
            x0, y0, x1, y1 = box
            device_log(self.__device, 'materilal_amount_image_to_string', box)
            imdst = imsch[y0:y1, x0:x1]
            ret, imths = cv2.threshold(imdst, 215, 255, cv2.THRESH_BINARY)
            resource_image = Image.fromarray(imths)
            i=i+1
            try:
                result_list.append(int(img_to_string_eng(resource_image)
                                       .replace(',', '')
                                       ))
            except Exception as e:
                result_list.append(-1)
        return result_list

    def resource_location_image_to_string(self):
        x0, y0, x1, y1 = (885, 190, 1035, 207)

        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
        imsch = imsch[y0:y1, x0:x1]
        ret, imsch = cv2.threshold(imsch, 215, 255, cv2.THRESH_BINARY)
        resource_image = Image.fromarray(imsch)
        result = ''.join(c for c in img_to_string(resource_image) if c.isdigit())
        return result

    def match_query_to_string(self):
        x0, y0, x1, y1 = (1211, 162, 1242, 179)

        try:
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            imsch = imsch[y0:y1, x0:x1]
            ret, imsch = cv2.threshold(imsch, 215, 255, cv2.THRESH_BINARY)
            resource_image = Image.fromarray(imsch)
            result = ''.join(c for c in img_to_string(resource_image) if c.isdigit())
            return int(result[0]), int(result[1])
        except Exception as e:
            return None, None

    def barbarians_level_image_to_string(self):
        try:
            x0, y0, x1, y1 = (106, 370, 436, 384)
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            imsch = imsch[y0:y1, x0:x1]
            # ret, imsch = cv2.threshold(imsch, 165, 255, cv2.THRESH_BINARY)
            resource_image = Image.fromarray(imsch)
            str = img_to_string(resource_image)
            if self.debug:
                cv2.imshow('imsch', imsch)
                print(str)
                cv2.waitKey(0)
            result = int(''.join(c for c in str if c.isdigit()))
        except Exception as e:
            traceback.print_exc()
            return -1
        if result > 99:
            return -1
        return result

    def get_building_name(self, box):
        x0, y0, x1, y1 = box
        title_image = self.get_curr_device_screen_img().crop(box)
        s = img_to_string(title_image)
        title_image.save(resource_path('{}title_x_{}_y_{}.png'.format(FilePaths.TEST_SRC_FOLDER_PATH.value, x0, y0)))
        bot_print("Building <{}> on position [({}, {}), ({}, {})] ".format(s, x0, y0, x1, y1))

    def check_any(self, *props_list, imsch = None):
        try:
            if imsch is None:
                imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                     cv2.IMREAD_COLOR)
            for props in props_list:
                path, size, box, threshold, least_diff, gui = props
                imsrc = cv2.imread(resource_path(path))
    
                result = aircv.find_template(imsrc, imsch, threshold, True)
                # device_log(self.__device, 'check_any', path, threshold, result)
                
                if self.debug:
                    cv2.imshow('imsrc', imsrc)
                    cv2.imshow('imsch', imsch)
                    cv2.waitKey(0)
    
                if result is not None:
                    return True, gui, result['result']
        except Exception as e:
            traceback.print_exc()

        return False, None, None
    
    def check_any_gray(self, *props_list, bgremove=True):
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)

        for props in props_list:
            path, size, box, threshold, least_diff, gui = props
            # device_log(self.__device, 'check_any_gray', path, threshold)
            imsrc = cv2.imread(resource_path(path))
            result = aircv.find_template(imsrc, imsch, threshold, False, bgremove)

            if result is not None:
                return True, gui, result['result']

        return False, None, None
    
    def has_image_props(self, props):
        path, size, box, threshold, least_diff, gui = props
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        imsrc = cv2.imread(resource_path(path))
        result = aircv.find_template(imsrc, imsch, threshold, True)
        return result

    def find_all_image_props(self, props, max_cnt=3):
        path, size, box, threshold, least_diff, gui = props
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        imsrc = cv2.imread(resource_path(path))
        result = aircv.find_all_template(imsrc, imsch, threshold, max_cnt, True)
        return result

    def has_image_cv_img(self, cv_img, threshold=0.90):
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        result = aircv.find_template(cv_img, imsch, threshold, True)

        return result

    def get_image_in_box(self, box=(0, 0, 1280, 720)):
        """
        :param box: The crop rectangle, as a (left, upper, right, lower)-tuple.
        """
        x0, y0, x1, y1 = box
        img = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                           cv2.IMREAD_COLOR)
        return img[y0:y1, x0:x1]

    def sunset_canyon_attempts_image_to_string(self):
        try:
            # Free attempts
            x0, y0, x1, y1 = (820, 90, 855, 120)
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            imsch = imsch[y0:y1, x0:x1]
            resource_image = Image.fromarray(imsch)
            str = img_to_string(resource_image)
            free_attempts = int(str.split('/')[0])

            # Tickets
            x0, y0, x1, y1 = (970, 90, 995, 120)
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            imsch = imsch[y0:y1, x0:x1]
            resource_image = Image.fromarray(imsch)
            str = img_to_string(resource_image)
            ticket_attempts = int(str)
        except Exception as e:
            traceback.print_exc()
            return -1, -1
        if free_attempts > 99 or ticket_attempts > 99:
            return -1, -1
        return free_attempts, ticket_attempts

    def lost_canyon_attempts_image_to_string(self):
        try:
            # Free attempts
            x0, y0, x1, y1 = (800, 90, 840, 120)
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            imsch = imsch[y0:y1, x0:x1]
            resource_image = Image.fromarray(imsch)
            str = img_to_string(resource_image)
            free_attempts = int(str.split('/')[0])
        except Exception as e:
            traceback.print_exc()
            return -1
        if free_attempts > 99:
            return -1
        return free_attempts
