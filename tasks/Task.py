from bot_related.device_gui_detector import GuiName, GuiDetector
from bot_related.bot_config import TrainingAndUpgradeLevel, BotConfig
from bot_related import haoi, twocaptcha
from config import HAO_I, TWO_CAPTCHA
from tasks.constants import TaskName, BuildingNames
from filepath.file_relative_paths import (
    ImagePathAndProps,
    BuffsImageAndProps,
    ItemsImageAndProps,
)
from datetime import datetime
from utils import aircv_rectangle_to_box, stop_thread, log, device_log, is_dark
from enum import Enum

import config
import traceback
import time
import random
import adb
import cv2
import numpy as np
import utils

from filepath.constants import RESOURCES, SPEEDUPS, BOOSTS, EQUIPMENT, OTHER, MAP, HOME
from time import sleep

class Task:

    center = (640, 360)

    def __init__(self, bot):
        self.bot = bot
        self.device = bot.device
        self.gui = bot.gui

    def call_idle_back(self):
        self.set_text(insert="收回空闲队列")
        self.back_to_map_gui()
        while True:
            _, _, commander_pos = self.gui.check_any(
                ImagePathAndProps.HOLD_ICON_SMALL_IMAGE_PATH.value
            )
            if commander_pos is not None:
                x, y = commander_pos
                self.tap((x - 10, y - 10))
                self.tap(self.center)
                self.tap(self.center)
            else:
                return
            _, _, return_btn_pos = self.gui.check_any(
                ImagePathAndProps.RETURN_BUTTON_IMAGE_PATH.value
            )
            if return_btn_pos is not None:
                self.tap(return_btn_pos)
            else:
                return

    def heal_troops(self):
        self.set_text(insert="治疗部队")
        heal_button_pos = (960, 590)
        self.back_to_home_gui()
        self.home_gui_full_view()
        self.tap(self.bot.building_pos[BuildingNames.HOSPITAL.value])
        self.tap((285, 20))
        _, _, heal_icon_pos = self.gui.check_any(
            ImagePathAndProps.HEAL_ICON_IMAGE_PATH.value
        )
        if heal_icon_pos is None:
            return
        self.tap(heal_icon_pos[0])
        self.tap(heal_button_pos[0])
        self.tap(self.bot.building_pos[BuildingNames.HOSPITAL.value])
        self.tap(self.bot.building_pos[BuildingNames.HOSPITAL.value])

    # Home
    def back_to_home_gui(self):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name()
            gui_name, pos = ["UNKNOW", None] if result is None else result
            if gui_name == GuiName.HOME.name:
                free_pos = (400 + int(50 * (0.5 - random.random())), 500 + int(50 * (0.5 - random.random())))
                self.tap(free_pos)
                
                imsch = self.gui.get_curr_device_screen_img_cv()
                left_task_pos = self.gui.check_any(ImagePathAndProps.CLOSE_LEFT_TASK_BUTTON_PATH.value, imsch=imsch)[2]
                if left_task_pos is not None:
                    self.set_text(insert='切换视觉[home], 当前界面[{}], {}, 发现左侧菜单打开, 关闭'.format(gui_name, left_task_pos))
                    self.tap(left_task_pos)
                    
                help_pos = self.gui.check_any(ImagePathAndProps.HELP2_IMG_PATH.value, imsch=imsch)[2]
                if help_pos is not None:
                    self.set_text(insert='切换视觉[home], 当前界面[{}], {}, 发现帮助按钮, 点击'.format(gui_name, help_pos))
                    self.tap(help_pos)
                    
                break
            else:
                self.set_text(insert='切换视觉[home], 当前界面[{}], {}, loop_count:{}'.format(gui_name, pos, loop_count))
                if gui_name == GuiName.MAP.name:
                    self.tap(pos)
                elif gui_name == GuiName.WINDOW.name:
                    self.back()
                elif gui_name != GuiName.HELLO_WROLD_IMG.name and gui_name != GuiName.VERIFICATION_CLOSE_REFRESH_OK.name and gui_name != GuiName.HELLO_WROLD_2_IMG.name:
                    self.back()
            loop_count = loop_count + 1
            if loop_count > 20:
                self.set_text(insert='程序可能卡死, 重启'.format(loop_count))
                self.stopRok()
                break;
            # time.sleep(self.bot.config.tapSleep)
        return loop_count

    def find_home(self):
        has_green_home, _, pos = self.gui.check_any(
            ImagePathAndProps.GREEN_HOME_BUTTON_IMG_PATH.value
        )
        if not has_green_home:
            return None
        self.tap(pos)

    def home_gui_full_view(self):
        self.set_text(insert='切换视觉[full home]')
        edit_button_pos = self.gui.check_any(ImagePathAndProps.EDIT_BUTTON_PATH.value)[2]
        if edit_button_pos is not None:
            self.tap(edit_button_pos, 2)
            
            edit_button_2_pos = self.gui.check_any(ImagePathAndProps.EDIT_BUTTON_2_PATH.value)[2]
            if edit_button_2_pos is not None:
                self.tap(edit_button_2_pos, 2)
                
            edit_button_3_pos = self.gui.check_any(ImagePathAndProps.EDIT_BUTTON_3_PATH.value)[2]
            if edit_button_3_pos is not None:
                self.tap(edit_button_3_pos, 2)   
                
            self.back()
            self.back()
                    
        # self.tap((60, 540), 2 * self.bot.config.tapSleep)
        # self.tap((1105, 200), 2 * self.bot.config.tapSleep)
        # self.tap((1220, 35), 2 * self.bot.config.tapSleep)

    # Building Position
    def find_building_title(self):
        result = self.gui.has_image_props(
            ImagePathAndProps.BUILDING_TITLE_MARK_IMG_PATH.value
        )
        if result is None:
            return None
        x0, y0, x1, y1 = aircv_rectangle_to_box(result["rectangle"])
        return x0, y0, x1, y1

    # Menu
    def menu_should_open(self, should_open=False):
        # close menu if open
        (
            path,
            size,
            box,
            threshold,
            least_diff,
            gui,
        ) = ImagePathAndProps.MENU_BUTTON_IMAGE_PATH.value
        x0, y0, x1, y1 = box
        c_x, c_y = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
        is_open, _, _ = self.gui.check_any(
            ImagePathAndProps.MENU_OPENED_IMAGE_PATH.value
        )
        if should_open and not is_open:
            self.set_text(insert='打开菜单')
            self.tap((c_x, c_y), 2 * self.bot.config.tapSleep)
        elif not should_open and is_open:
            self.set_text(insert='关闭菜单')
            self.tap((c_x, c_y), 2 * self.bot.config.tapSleep)

    # Map
    def back_to_map_gui(self, help=True):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name()
            gui_name, pos = ["UNKNOW", None] if result is None else result
            if gui_name == GuiName.MAP.name:
                if help:
                    imsch = self.gui.get_curr_device_screen_img_cv()
                    help_pos = self.gui.check_any(ImagePathAndProps.HELP2_IMG_PATH.value, imsch=imsch)[2]
                    if help_pos is not None:
                        self.set_text(insert='切换视觉[map], 当前界面[{}], {}, 发现帮助按钮, 点击'.format(gui_name,help_pos))
                        self.tap(help_pos)
                break
            else:
                self.set_text(insert='切换视觉[map], 当前界面[{}], {}, loop_count:{}'.format(gui_name,pos,loop_count))
                if gui_name == GuiName.HOME.name:
                    self.tap(pos)
                elif gui_name == GuiName.WINDOW.name:
                    self.back()
                elif gui_name != GuiName.HELLO_WROLD_IMG.name and gui_name != GuiName.VERIFICATION_CLOSE_REFRESH_OK.name and gui_name != GuiName.HELLO_WROLD_2_IMG.name:
                    self.back()
            loop_count = loop_count + 1
            if loop_count > 20:
                self.set_text(insert='程序可能卡死, 重启'.format(loop_count))
                self.stopRok()
                break;
            time.sleep(self.bot.config.tapSleep)
        return loop_count

    def get_curr_gui_name(self):
        try:
            if not self.isRoKRunning():
                str='ROK还没运行, 尝试启动'
                self.set_text(insert=str)
                
                self.stopRok()
                self.runOfRoK()
                self.set_text(insert='等待{}秒'.format(self.bot.config.welcomeSleep))
                time.sleep(self.bot.config.welcomeSleep)
            pos_list = None
            pos_free = (400 + int(50 * (0.5 - random.random())), 400 + int(50 * (0.5 - random.random())))
            
            for i in range(0, 30):
                imsch = self.gui.get_curr_device_screen_img_cv()
                if self.check_common_button(imsch):
                    time.sleep(5)
                    imsch = self.gui.get_curr_device_screen_img_cv()
                result = self.gui.get_curr_gui_name(imsch)
                gui_name, pos = ["UNKNOW", None] if result is None else result
                dark, avg = is_dark(imsch[180:540, 320:960], 70)
                device_log(self.device, '获取当前界面 {}, {}, 亮度:{}'.format(gui_name, pos, avg))  
                if dark:
                    self.set_text(insert='当前界面过暗, 可能断线加载中, 点击任意地方, {}, 继续等待...'.format(pos_free))     
                    self.tap(pos_free, 10)
                    continue
                elif gui_name == GuiName.VERIFICATION_CLOSE_REFRESH_OK.name:
                    self.set_text(insert='发现验证界面, 开始验证'.format())
                    self.verify(pos)
                elif gui_name == GuiName.HELLO_WROLD_IMG.name:
                    self.set_text(insert='欢迎界面, 点击任意地方, {}'.format(pos_free))
                    self.set_text(insert='等待{}秒'.format(self.bot.config.restartSleep))
                    
                    start = time.time()
                    now = start
                    while now - start <= self.bot.config.restartSleep:
                        self.tap(pos_free, 10)
                        now = time.time()
                        self.set_text(insert='已经等待{}秒...'.format(int(now - start)))
                        self.check_common_button()
                elif gui_name == GuiName.HELLO_WROLD_2_IMG.name:
                    self.set_text(insert='欢迎界面, 继续等待...')
                    time.sleep(20)
                # else:
                #     device_log(self.device, '未知界面, 点击任意地方', pos_free)
                #     self.tap(pos_free)
                return result
            if not pos_list:
                raise Exception("Could not pass verification")
        except Exception as e:
            traceback.print_exc()
            adb.bridge.reconnect(self.device)
            return None
    
    def check_common_button(self, imsch=None):
        if imsch is None:
            imsch = self.gui.get_curr_device_screen_img_cv()
        closeapp_pos = self.gui.check_any(
                ImagePathAndProps.CLOSEAPP_BUTTON_PATH.value,
                imsch=imsch
                )[2]
        if closeapp_pos is not None:
            device_log(self.device, '发现程序卡死按钮, 点击', closeapp_pos)
            self.tap(closeapp_pos, self.bot.config.tapSleep)
            return True
            
        continue_pos = self.gui.check_any(
                ImagePathAndProps.CONTINUE_BUTTON_PATH.value,
                imsch=imsch
                )[2]
        if continue_pos is not None:
            device_log(self.device, '发现继续按钮, 点击', continue_pos)
            self.tap(continue_pos, self.bot.config.tapSleep)   
            return True
            
        comfirm_pos = self.gui.check_any(
                ImagePathAndProps.CONFIRM_BUTTON_PATH.value,
                imsch=imsch
                )[2]
        if comfirm_pos is not None:
            device_log(self.device, '发现确定按钮, 点击', comfirm_pos)
            self.tap(comfirm_pos, self.bot.config.tapSleep)
            return True
        
        comfirm_update_pos = self.gui.check_any(
                ImagePathAndProps.CONFIRM_UPDATE_BUTTON_PATH.value,
                imsch=imsch
                )[2]
        if comfirm_update_pos is not None:
            device_log(self.device, '发现确定按钮, 点击', comfirm_update_pos)
            self.tap(comfirm_update_pos, self.bot.config.tapSleep)
            return True
         
        cancel_pos = self.gui.check_any(
                ImagePathAndProps.CANCEL_BUTTON_PATH.value,
                imsch=imsch
                )[2]
        if cancel_pos is not None:
            device_log(self.device, '发现取消按钮, 点击', cancel_pos)
            self.tap(cancel_pos, self.bot.config.tapSleep)
            return True
        
        download_button_pos = self.gui.check_any(ImagePathAndProps.DOWNLOAD_BUTTON_PATH.value, imsch=imsch)[2]
        if download_button_pos is not None:
            device_log(self.device, '发现下载按钮, 点击', download_button_pos)
            self.tap(download_button_pos)
            return True
        
        download_button_close_pos = self.gui.check_any(ImagePathAndProps.DOWNLOAD_BUTTON_CLOSE_PATH.value, imsch=imsch)[2]
        if download_button_close_pos is not None:
            device_log(self.device, '发现关闭按钮, 点击', download_button_close_pos)
            self.tap(download_button_close_pos)
            return True
                            
        return False
                    
    def pass_verification(self):
        pos_list = None
        try:
            self.set_text(insert="pass verification, {}".format(config.global_config.method))
            box = (400, 0, 880, 720)
            ok = [780, 680]
            img = self.gui.get_curr_device_screen_img()
            img = img.crop(box)
            if config.global_config.method == HAO_I:
                pos_list = haoi.solve_verification(img)
            elif config.global_config.method == TWO_CAPTCHA:
                pos_list = twocaptcha.solve_verification(img)

            if pos_list is None:
                self.set_text(insert="fail to pass verification, {}".format(config.global_config.method))
                return None

            for pos in pos_list:
                self.tap((400 + pos[0], pos[1]))
            self.tap((780, 680), 5)

        except Exception as e:
            self.tap((100, 100))
            traceback.print_exc()

        return pos_list

    def has_buff(self, checking_location, buff_img_props):
        path, size, box, threshold, least_diff, tab_name = buff_img_props
        self.set_text(insert='检查是否存在增益, {}'.format(path))
        # Where to check
        if checking_location == HOME:
            self.back_to_home_gui()
        elif checking_location == MAP:
            self.back_to_map_gui()
        else:
            return False
        # Start Checking
        has, _, _ = self.gui.check_any(buff_img_props, imsch = self.gui.get_curr_device_screen_img_cv())
        return has

    def use_item(self, using_location, item_img_props_list):
        # Where to use the item
        if using_location == HOME:
            self.back_to_home_gui()
        elif using_location == MAP:
            self.back_to_map_gui()
        else:
            return False

        items_icon_pos = (830, 675)
        use_btn_pos = (980, 600)

        # open menu
        self.menu_should_open(True)
        
        # open items window
        self.set_text(insert='选择增益道具分栏{}'.format(items_icon_pos))
        self.tap(items_icon_pos)
          
        
        for item_img_props in item_img_props_list:
            path, size, box, threshold, least_diff, tab_name = item_img_props
            self.set_text(insert='寻找增益道具, {}'.format(path))
            tabs_pos = {
                RESOURCES: (250, 80),
                SPEEDUPS: (435, 80),
                BOOSTS: (610, 80),
                EQUIPMENT: (790, 80),
                OTHER: (970, 80),
            }

            # tap on tab
            self.tap(tabs_pos[tab_name])
            
            # find item, and tap it
            _, _, item_pos = self.gui.check_any(item_img_props)
            if item_pos is None:
                continue
            self.set_text(insert='使用增益道具, {},{}'.format(path, item_pos))
            self.tap(item_pos)
            # tap on use Item
            self.tap(use_btn_pos)
            
            return True
        self.set_text(insert='没有对应的增益道具')
        return False

    # Action
    def back(self, sleep_time=-1):
        if sleep_time == -1:
            sleep_time = self.bot.config.tapSleep
        device_log(self.device, 'back', sleep_time)
        cmd = "input keyevent 4"
        self.device.shell(cmd)
        time.sleep(sleep_time)

    # duration is in milliseconds
    def swipe(self, pos1, pos2, times=1, duration=300):
        cmd = "input swipe {} {} {} {} {}".format(pos1[0], pos1[1], pos2[0], pos2[1], duration)
        for i in range(times):
            self.device.shell(cmd)
            device_log(self.device, 'swipe', cmd)
            if self.bot.config.swipeSleep > 0:
                time.sleep(self.bot.config.swipeSleep / 1000)
            # time.sleep(duration / 1000 + 0.2)

    # def zoom(self, x_f, y_f, x_t, y_t, times=1, duration=300, zoom_type="out"):
    #     device_log(self.device, 'zoom', zoom_type)
    #     cmd_hold = "input swipe {} {} {} {} {}".format(
    #         pos2[0], pos2[1], x_t, y_t, duration + 1000
    #     )
    #     # cmd_hold = "input tap {} {} {}".format(
    #     #     x_t, y_t, duration + 1000
    #     # )
    #     if zoom_type == "out":
    #         cmd_swipe = "input swipe {} {} {} {} {}".format(
    #             x_f, y_t, x_f, y_t, duration
    #         )
    #     else:
    #         cmd_swipe = "input swipe {} {} {} {} {}".format(
    #             x_t, y_t, x_f, y_f, duration
    #         )
    #
    #     for i in range(times):
    #         device_log(self.device, 'cmd_hold', cmd_hold)
    #         self.device.shell(cmd_hold)
    #         device_log(self.device, 'cmd_swipe', cmd_swipe)
    #         self.device.shell(cmd_swipe)
    #         time.sleep(duration / 1000 + 0.5 + 0.2)

    def tap(self, pos, sleep_time=-1, long_press_duration=-1):
        if sleep_time == -1:
            sleep_time = self.bot.config.tapSleep
        cmd = None
        if long_press_duration > -1:
            cmd = "input swipe {} {} {} {} {}".format(pos[0], pos[1], pos[0], pos[1], long_press_duration)
            sleep_time = long_press_duration / 1000 + 0.2
        else:
            cmd = "input tap {} {}".format(pos[0], pos[1])
        
        str = self.device.shell(cmd)
        device_log(self.device, cmd)
        time.sleep(sleep_time)
                
    def double_tap(self, pos):
        device_log(self.device, 'double_tap', pos)
        self.tap(pos, 0.1)
        self.tap(pos, 0.1)
        time.sleep(1)
        
    def text(self, x, y, text, sleep_time=-1, remove_all = True):
        if sleep_time == -1:
            sleep_time = self.bot.config.tapSleep
            
        self.tap((x, y))
        cmd = "input keyevent KEYCODE_MOVE_END"
        self.device.shell(cmd)
        if remove_all:
            for i in range(6):
                cmd = "input keyevent KEYCODE_DEL"
                self.device.shell(cmd)
        
        cmd = "input text {}".format(text)
        str = self.device.shell(cmd)
        device_log(self.device, cmd, str)
        
        #cmd = "input keyevent KEYCODE_ENTER"
        self.tap((1, 1))
                
    # edit by seashell-freya, github: https://github.com/seashell-freya
    def isRoKRunning(self):
        # cmd = "dumpsys window windows | grep mCurrentFocus"
        cmd = "dumpsys activity top"
        str = self.device.shell(cmd)
        ret = (str.find("com.lilithgames.rok.offical.cn/com.harry.engine.MainActivity") != -1) | \
              (str.find('com.lilithgames.rok.offical.cn/com.lilith.sdk.special.uiless.domestic.UILessDomesticSwitchActivity') != -1) | \
              (str.find('com.lilithgames.rok.offical.cn/com.lilith.sdk.special.uiless.domestic.UILessDomesticAutoLoginActivity') != -1)
                         
        # device_log(self.device, 'isRoKRunning', cmd, ret)
        # return True
        return ret

    def runOfRoK(self):
        cmd = "am start -n com.lilithgames.rok.offical.cn/com.harry.engine.MainActivity"
        device_log(self.device, 'runOfRoK', cmd)
        str = self.device.shell(cmd)

    def stopRok(self):
        cmd = "am force-stop com.lilithgames.rok.offical.cn"
        device_log(self.device, 'stopRok', cmd)
        str = self.device.shell(cmd)

    def set_text(self, **kwargs):
        dt_string = datetime.now().strftime("[%H:%M:%S]")
        name = 'name'
        title = "title"
        text_list = "text_list"
        insert = "insert"
        remove = "remove"
        replace = "replace"
        index = "index"
        append = "append"
        
        if name in kwargs:
            self.bot.text[name] = kwargs[name]
            device_log(self.device, kwargs[name])
         
        if remove in kwargs and kwargs.get(remove, False):
            self.bot.text[text_list].clear()   

        if title in kwargs:
            text = '{}, 当前玩家:{}, 当前回合:{}, 玩家回合:{}'.format(kwargs[title], self.bot.config.playerCount, self.bot.round_count, self.bot.player_round_count)
            self.bot.text[title] = text
            device_log(self.device, text)

        if replace in kwargs:
            self.bot.text[text_list][kwargs[index]] = (
                dt_string + " " + kwargs[replace].lower()
            )
            device_log(self.device, f"\t* {dt_string} {kwargs[replace].lower()}")

        if insert in kwargs:
            self.bot.text[text_list].insert(
                kwargs.get(index, 0), dt_string + " " + kwargs[insert].lower()
            )
            device_log(self.device, f"\t* {dt_string} {kwargs[insert].lower()}")

        if append in kwargs:
            self.bot.text[text_list].append(dt_string + " " + kwargs[append].lower())
            device_log(self.device, f"\t* {dt_string} {kwargs[append].lower()}")

        self.bot.text_update_event(self.bot.text)

    def do(self, next_task):
        return next_task
    
    def verify(self, pos):
        img = self.gui.get_curr_device_screen_img_cv()
        img = cv2.medianBlur(img, 5)
    
        img1_x = 430
        # img1_x = 490
        img1 = img[200:440, img1_x:570]
        img_result1 = utils.canny(img1)
        img_result1, c1 = utils.fix_max_contours(img_result1)
        c1 = np.squeeze(c1)
        min_1 = np.min(c1, axis=0)
        start = min_1[0] + img1_x
      
        img2_x = img1_x + 230
        img2 = img[200:440, img2_x:825]
        img_result2 = utils.canny(img2)
        img_result2, c2 = utils.fix_max_contours(img_result2)
        c2 = np.squeeze(c2)
        min_2 = np.min(c2, axis=0)
        end = min_2[0] + img2_x
        
        self.set_text(insert='尝试滑动验证, min_1[0]:{}, min_2[0]:{}, {} => {}'.format(min_1[0], min_2[0], start, end))
        self.swipe((start, pos[1]-55), (end, pos[1]-55), 1, 1000)
        time.sleep(10)