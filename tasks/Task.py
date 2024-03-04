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
from utils import aircv_rectangle_to_box, stop_thread, log, device_log
from enum import Enum

import config
import traceback
import time
import random

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
                break
            else:
                self.set_text(insert='切换视觉[城市], 当前界面{}, {}, loop_count:{}'.format(gui_name, pos, loop_count))
                if gui_name == GuiName.MAP.name:
                    self.tap(pos)
                elif gui_name == GuiName.WINDOW.name:
                    self.back()
                elif gui_name != GuiName.HELLO_WROLD_IMG.name:
                    self.back()
            loop_count = loop_count + 1
            if loop_count > 20:
                self.set_text(insert='程序可能卡死, 重启'.format(loop_count))
                self.stopRok()
                break;
            time.sleep(1)
        return loop_count

    def find_home(self):
        has_green_home, _, pos = self.gui.check_any(
            ImagePathAndProps.GREEN_HOME_BUTTON_IMG_PATH.value
        )
        if not has_green_home:
            return None
        self.tap(pos)

    def home_gui_full_view(self):
        self.set_text(insert='切换视觉[全城市]')
        self.tap((60, 540), 5)
        self.tap((1105, 200), 5)
        self.tap((1220, 35), 5)

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
            self.tap((c_x, c_y))
        elif not should_open and is_open:
            self.tap((c_x, c_y))

    # Map
    def back_to_map_gui(self):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name()
            gui_name, pos = ["UNKNOW", None] if result is None else result
            if gui_name == GuiName.MAP.name:
                break
            else:
                self.set_text(insert='切换视觉[地图], 当前界面{}, {}'.format(gui_name,pos))
                if gui_name == GuiName.HOME.name:
                    self.tap(pos)
                elif gui_name == GuiName.WINDOW.name:
                    self.back()
                elif gui_name != GuiName.HELLO_WROLD_IMG.name:
                    self.back()
            loop_count = loop_count + 1
            if loop_count > 20:
                self.set_text(insert='程序可能卡死, 重启'.format(loop_count))
                self.stopRok()
                break;
            time.sleep(1)
        return loop_count

    def get_curr_gui_name(self):
        if not self.isRoKRunning():
            str='ROK还没运行, 尝试启动'
            self.set_text(insert=str)
            self.bot.snashot_update_event()
            self.stopRok()
            self.runOfRoK()
            time.sleep(20)
        pos_list = None
        pos_free = (400 + int(50 * (0.5 - random.random())), 400 + int(50 * (0.5 - random.random())))
        
        for i in range(0, 1):
            self.bot.snashot_update_event()
            
            _, _, comfirm_pos = self.gui.check_any(
                    ImagePathAndProps.CONFIRM_BUTTON_PATH.value
                    )
            if comfirm_pos is not None:
                device_log(self.device, '发现确定按钮, 点击', comfirm_pos)
                self.tap(comfirm_pos)
             
            _, _, cancel_pos = self.gui.check_any(
                    ImagePathAndProps.CANCEL_BUTTON_PATH.value
                    )
            if cancel_pos is not None:
                device_log(self.device, '发现取消按钮, 点击', cancel_pos)
                self.tap(cancel_pos)
            
            result = self.gui.get_curr_gui_name()
            gui_name, pos = ["UNKNOW", None] if result is None else result
            device_log(self.device, '获取当前界面', gui_name, pos)  
            
            self.bot.snashot_update_event()
               
            if gui_name == GuiName.VERIFICATION_VERIFY.name:
                self.tap(pos, 5)
                pos_list = self.pass_verification()
            elif gui_name == GuiName.HELLO_WROLD_IMG.name:
                self.set_text(insert='欢迎界面, 点击任意地方, {}'.format(pos_free))
                self.tap(pos_free)
                time.sleep(self.bot.config.restartSleep)
            # elif gui_name == GuiName.VERIFICATION_CLOSE_REFRESH_OK.name and pos_list is None:
            #     pos_list = self.pass_verification()
            # elif (gui_name == GuiName.MAP.name) | (gui_name == GuiName.HOME.name):
            #     device_log(self.device, '[地图/城市]界面, 不需要处理')
            # else:
            #     device_log(self.device, '未知界面, 点击任意地方', pos_free)
            #     self.tap(pos_free)
            return result
        if not pos_list:
            raise Exception("Could not pass verification")

    def pass_verification(self):
        pos_list = None
        try:
            self.set_text(insert="pass verification")
            box = (400, 0, 880, 720)
            ok = [780, 680]
            img = self.gui.get_curr_device_screen_img()
            img = img.crop(box)
            if config.global_config.method == HAO_I:
                pos_list = haoi.solve_verification(img)
            elif config.global_config.method == TWO_CAPTCHA:
                pos_list = twocaptcha.solve_verification(img)

            if pos_list is None:
                self.set_text(insert="fail to pass verification")
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
        has, _, _ = self.gui.check_any(buff_img_props)
        return has

    def use_item(self, using_location, item_img_props_list):
        # Where to use the item
        if using_location == HOME:
            self.back_to_home_gui()
        elif using_location == MAP:
            self.back_to_map_gui()
        else:
            return False

        items_icon_pos = (930, 675)
        use_btn_pos = (980, 600)

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
            # open menu
            self.menu_should_open(True)
            # open items window
            self.tap(items_icon_pos)
            # tap on tab
            self.tap(tabs_pos[tab_name])
            # find item, and tap it
            _, _, item_pos = self.gui.check_any(item_img_props)
            if item_pos is None:
                continue
            self.set_text(insert='使用增益道具, {},{}'.format(path, item_pos))
            self.tap(item_pos, 5)
            # tap on use Item
            self.tap(use_btn_pos)
            self.bot.snashot_update_event()
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
        
    def text(self, x, y, text):
        self.tap((x, y))
        cmd = "input keyevent KEYCODE_MOVE_END"
        self.device.shell(cmd)
        for i in range(8):
            cmd = "input keyevent KEYCODE_DEL"
            self.device.shell(cmd)
        # self.device.shell(cmd)
        
        cmd = "input text {}".format(text)
        str = self.device.shell(cmd)
        device_log(self.device, cmd)
        
        cmd = "input keyevent KEYCODE_ENTER"
        self.device.shell(cmd)
        
    # edit by seashell-freya, github: https://github.com/seashell-freya
    def isRoKRunning(self):
        # cmd = "dumpsys window windows | grep mCurrentFocus"
        cmd = "dumpsys activity top"
        str = self.device.shell(cmd)
        ret = (str.find("com.lilithgames.rok.offical.cn/com.harry.engine.MainActivity") != -1) | \
              (str.find('com.lilithgames.rok.offical.cn/com.lilith.sdk.special.uiless.domestic.UILessDomesticSwitchActivity') != -1)
        # device_log(self.device, 'isRoKRunning', cmd, ret)
        # return True
        return ret

    def runOfRoK(self):
        cmd = "am start -n com.lilithgames.rok.offical.cn/com.harry.engine.MainActivity"
        device_log(self.device, 'runOfRoK', cmd)
        str = self.device.shell(cmd)
        time.sleep(30)

    def stopRok(self):
        cmd = "am force-stop com.lilithgames.rok.offical.cn"
        device_log(self.device, 'stopRok', cmd)
        str = self.device.shell(cmd)

    def set_text(self, **kwargs):
        dt_string = datetime.now().strftime("[%H:%M:%S]")
        title = "title"
        text_list = "text_list"
        insert = "insert"
        remove = "remove"
        replace = "replace"
        index = "index"
        append = "append"

        if title in kwargs:
            self.bot.text[title] = kwargs[title]
            device_log(self.device, kwargs[title])

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

        if remove in kwargs and kwargs.get(remove, False):
            self.bot.text[text_list].clear()

        self.bot.text_update_event(self.bot.text)

    def do(self, next_task):
        return next_task
