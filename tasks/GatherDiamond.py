import traceback
import math

from filepath.constants import MAP
from filepath.file_relative_paths import BuffsImageAndProps, ItemsImageAndProps, ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName, Resource
from utils import log, device_log
import time
from cv2 import edgePreservingFilter
from utils import log, device_log, img_to_string, img_to_string_eng
import cv2
import numpy as np

class GatherDiamond(Task):

    def __init__(self, bot):
        super().__init__(bot)
        self.max_query_space = 5
        
    def get_kilometer(self, count):
        step_kilometer = 4
        edge = math.ceil(count / 4)
        edge = edge * step_kilometer
        max_kilometer = math.ceil(math.sqrt((pow(edge, 2) + pow(edge, 2))))
        return max_kilometer
    
    def create_troop(self):
        new_troops_button_pos = self.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)[2]
        if new_troops_button_pos is None:
            self.set_text(insert="没有更多队列采集")
            self.bot.snashot_update_event()
            return False
        
        self.set_text(insert="创建部队", index=1)
        self.tap(new_troops_button_pos, 2 * self.bot.config.tapSleep)
        self.bot.snashot_update_event()
        
        if self.bot.config.gatherResourceNoSecondaryCommander:
            self.set_text(insert="移除副将", index=1)
            self.tap((473, 501))
            self.bot.snashot_update_event()
            
        self.set_text(insert="开始行军", index=1)
        match_button_pos = self.gui.check_any(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)[2]
        self.tap(match_button_pos, 2 * self.bot.config.tapSleep)
        self.bot.snashot_update_event()
        return True
    
    def do(self, next_task=TaskName.BREAK):
        self.set_text(title='采集宝石', remove=True)
        self.back_to_home_gui()
        self.back_to_map_gui()
        self.bot.snashot_update_event()
        
        self.swipe((400, 320), (800, 320))
        self.swipe((800, 320), (400, 320))
        
        result = self.gui.resource_amount_image_to_string()
        if result and len(result) > 4:
            if self.bot.diamond > 0:
                self.bot.diamond_add = int(result[4]) - self.bot.diamond
            try:
                self.bot.diamond = int(result[4])
            except Exception as e:
                device_log(self.device, '解析宝石数量出错{}'.format(e))
            self.set_text(title='采集宝石, 当前宝石: {}, 打工获得宝石: {}'.format(result[4], self.bot.diamond_add), remove=True)
        try:
            if self.gui.troop_already_full():
                self.set_text(insert="没有更多队列采集")
                return next_task
                                
            size_count = 1
            size_step = size_count
            src = (880, 320)
            dst = (400, 320)
            count = 0
            total_count = self.bot.config.gatherDiamondMaxRange
            direction = 'S'
            
            max_kilometer = self.get_kilometer(total_count)
            last_resource_pos = []
            self.set_text(insert="开始寻找宝石, 一共{}次".format(total_count,))
            self.set_text(insert="寻找宝石")
        
            while count < total_count:
                size_step = size_count
                while size_step > 0:
                    self.set_text(replace="寻找宝石, {}/{}次, {}/{}步, {}, 当前距离{}公里".format(count, total_count, size_count-size_step, size_count, direction, self.gui.get_kilometer()), index=0)
                    self.swipe(src, dst, 1)
                    size_step = size_step - 1
                    self.bot.snashot_update_event()
                    
                    _, _, diamond_pos = self.bot.gui.check_any(ImagePathAndProps.DIAMOND_IMG_PATH.value)
                    if diamond_pos is not None:
                        self.set_text(insert="发现宝石, {}, {}/{}次, {}步, {}, 当前距离{}公里".format(diamond_pos, count, total_count, size_count, direction, self.gui.get_kilometer()), index=1)
                        self.tap(diamond_pos, 2 * self.bot.config.tapSleep)
                        self.bot.snashot_update_event()
                        
                        coordinate = ''
                        _, _, resource_xy_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_IMG_PATH.value)
                        if resource_xy_pos is not None:
                            src = cv2.imdecode(np.asarray(self.bot.gui.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR)
                            src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
                            src = src[int(resource_xy_pos[1])-5:int(resource_xy_pos[1] + 20), int(resource_xy_pos[0]+140):int(resource_xy_pos[0]+140+100)]
                            coordinate = img_to_string_eng(src).replace('\n', '').replace(',', '')
                            self.set_text(insert="发现宝石, 坐标:{}".format(coordinate), index=1)
                            
                        gather = True
                        if len(coordinate) > 0:
                            if coordinate in last_resource_pos:
                                self.set_text(insert="宝石正在采集, 跳过, 坐标:{}".format(coordinate), index=1)
                                self.bot.snashot_update_event()
                                gather = False
                            else:
                                last_resource_pos.append(coordinate)
                    
                        if gather:
                            gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
                            if gather_button_pos is None:
                                self.set_text(insert="没有发现采集按钮, 可能宝石正在采集", index=1)
                                
                            else:
                                self.tap(gather_button_pos, 2 * self.bot.config.tapSleep)
                                self.bot.snashot_update_event()
                        
                                if not self.create_troop():
                                    return next_task
                                
                                if self.gui.troop_already_full():
                                    self.set_text(insert="没有更多队列采集")
                                    return next_task
                    
                    if direction == 'S':
                        src = (640, 600)
                        dst = (640, 120)
                    elif direction == 'W':
                        src = (400, 320)
                        dst = (880, 320)
                    elif direction == 'N':
                        src = (640, 120)
                        dst = (640, 600)
                    else:
                        src = (880, 320)
                        dst = (400, 320)
                    
                if (count) % 2 == 0:
                    if direction == 'S':
                        direction = 'W'
                    elif direction == 'W':
                        direction = 'N'
                    elif direction == 'N':
                        direction = 'E'
                    else:
                        direction = 'S'
                    size_count = size_count + 1
                    # self.set_text(insert="改变方向, {}, {}/{}次, {}步, 距离约{}公里".format(direction, count, total_count, size_count, self.get_kilometer(count)))
                count = count + 1    
            self.set_text(insert="没有发现更多宝石, 可以加大搜索范围")
            
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task
