import traceback
import math

from filepath.constants import MAP
from filepath.file_relative_paths import BuffsImageAndProps, ItemsImageAndProps, ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName, Resource
from utils import log, device_log
import time
from cv2 import edgePreservingFilter

class GatherDiamond(Task):

    def __init__(self, bot):
        super().__init__(bot)
        self.max_query_space = 5
        
    def get_kilometer(self, count):
        edge = (count // 2)
        max_kilometer = int(math.sqrt((pow(edge, 2) + pow(edge, 2))) * 5)
        return max_kilometer
    
    def do(self, next_task=TaskName.BREAK):
        self.set_text(title='采集宝石', remove=True)
        self.back_to_home_gui()
        self.back_to_map_gui()
        self.bot.snashot_update_event()
        
        result = self.gui.resource_amount_image_to_string()
        if result and len(result) > 4:
            self.set_text(title='采集宝石, 当前宝石: {}'.format(result[4]), remove=True)
        try:
            size_count = 1
            size_step = size_count
            src = (880, 320)
            dst = (400, 320)
            count = 0
            total_count = self.bot.config.gatherDiamondMaxRange
            direction = 'S'
            
            max_kilometer = self.get_kilometer(total_count)
            self.set_text(insert="开始寻找宝石, 一共{}次, 最大范围约{}公里".format(total_count, max_kilometer))
            self.set_text(insert="寻找宝石")
            
            while count < total_count:
                size_step = size_count
                while size_step > 0:
                    self.set_text(replace="寻找宝石, {}/{}次, {}/{}步, {}, 距离约{}公里".format(count, total_count, size_count-size_step, size_count, direction, self.get_kilometer(count)), index=0)
                    self.swipe(src, dst, 1)
                    time.sleep(1)
                    size_step = size_step - 1
                    self.bot.snashot_update_event()
                    
                    _, _, diamond_pos = self.bot.gui.check_any(ImagePathAndProps.DIAMOND_IMG_PATH.value)
                    if diamond_pos is not None:
                        self.set_text(insert="发现宝石, {}, {}/{}次, {}步, {}, 距离约{}公里".format(diamond_pos, count, total_count, size_count, direction, self.get_kilometer(count)), index=1)
                        self.tap(diamond_pos)
                        self.bot.snashot_update_event()
                        
                        gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
                        if gather_button_pos is None:
                            self.set_text(insert="没有发现采集按钮, 可能宝石正在采集", index=1)
                            continue
                        self.tap(gather_button_pos, 5)
                        self.bot.snashot_update_event()
                
                        new_troops_button_pos = self.bot.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)[2]
                        if new_troops_button_pos is None:
                            self.set_text(insert="没有更多队列采集", index=1)
                            return 
                        self.set_text(insert="创建部队", index=1)
                        self.tap(new_troops_button_pos, 5)
                        self.bot.snashot_update_event()
                        
                        match_button_pos = self.bot.gui.check_any(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)[2]
                        self.set_text(insert="开始行军", index=1)
                        self.tap(match_button_pos)
                    
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
                    
                count = count + 1           
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
                    
            self.set_text(insert="没有发现更多宝石, 可以加大搜索范围")
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task