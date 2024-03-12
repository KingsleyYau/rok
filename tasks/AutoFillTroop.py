import traceback

from filepath.constants import MAP
from filepath.file_relative_paths import BuffsImageAndProps, ItemsImageAndProps, ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName, Resource
from utils import log, device_log, img_to_string, img_to_string_eng
import cv2
import numpy as np

class AutoFillTroop(Task):

    def __init__(self, bot):
        super().__init__(bot)
        self.max_query_space = 5

    def create_troop(self, full_load=False):
        new_troops_button_pos = self.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)[2]
        if new_troops_button_pos is None:
            self.set_text(insert="没有更多队列")
            self.bot.snashot_update_event()
            return False
        
        self.set_text(insert="创建部队{}".format(new_troops_button_pos))
        self.tap(new_troops_button_pos, 3 * self.bot.config.tapSleep)
        self.bot.snashot_update_event()
        
        if self.bot.config.gatherResourceNoSecondaryCommander:
            self.set_text(insert="移除副将")
            self.tap((473, 501))
            self.bot.snashot_update_event()
        
        if full_load:
            self.set_text(insert="最大化部队")
            clear_button_pos = self.gui.check_any(ImagePathAndProps.CLEAR_BUTTON_PATH.value)[2]
            if clear_button_pos is not None:
                self.tap(clear_button_pos)
            max_button_pos = self.gui.check_any(ImagePathAndProps.MAX_BUTTON_PATH.value)[2]
            if max_button_pos is not None:
                self.tap(max_button_pos)
            self.bot.snashot_update_event()
                
        match_button_pos = self.gui.check_any(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)[2]
        self.set_text(insert="开始行军{}".format(match_button_pos))
        self.tap(match_button_pos)
        self.bot.snashot_update_event()
        
        no_button_pos = self.gui.check_any(ImagePathAndProps.NO_BUTTON_PATH.value)[2]
        if no_button_pos is not None:
            self.set_text(insert="集结太远, 放弃加入{}".format(no_button_pos))
            self.tap(no_button_pos)
            self.bot.snashot_update_event()
        
        return True
        
    def do(self, next_task=TaskName.BREAK):
        self.set_text(title='自动填集结', remove=True)
        self.back_to_home_gui()
        full_load, cur, total = self.gui.troop_already_full()
        if full_load:
            self.set_text(insert="没有更多队列")
            return next_task
        else:
            self.set_text(insert="当前队列数量:{}/{}".format(cur, total))
                        
        try:
            self.menu_should_open(True)
            self.set_text(insert='打开联盟中心')
            alliance_btn_pos = (1030, 670)
            self.tap(alliance_btn_pos, 2 * self.bot.config.tapSleep)
            
            found = False
            self.bot.snashot_update_event()
            _, _, war_pos = self.gui.check_any(ImagePathAndProps.ALLIANCE_WAR_IMG_PATH.value)
            if war_pos is not None:
                self.set_text(insert='打开战争{}'.format(war_pos))
                self.tap(war_pos, 2 * self.bot.config.tapSleep)
                for i in range(5):
                    self.set_text(insert='第{}次寻找集结'.format(i+1))
                    self.bot.snashot_update_event()
                    join_troop_pos = self.gui.check_any(ImagePathAndProps.JOIN_TROOP_IMG_PATH.value)[2]
                    if join_troop_pos is not None:
                        found = True
                        self.set_text(insert='发现集结, 点击加入{}'.format(join_troop_pos))
                        self.tap(join_troop_pos, 2 * self.bot.config.tapSleep)
                        self.bot.snashot_update_event()
            
                        if not self.create_troop(False):
                            break
                    else:
                        break
                     
            if not found:
                self.set_text(insert='没有发现集结')   
                
        except Exception as e:
            traceback.print_exc()
        return next_task