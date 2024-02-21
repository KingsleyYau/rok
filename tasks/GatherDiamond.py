import traceback

from filepath.constants import MAP
from filepath.file_relative_paths import BuffsImageAndProps, ItemsImageAndProps, ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName, Resource
from utils import log, device_log
import time

class GatherDiamond(Task):

    def __init__(self, bot):
        super().__init__(bot)
        self.max_query_space = 5

    def do(self, next_task=TaskName.BREAK):
        self.set_text(title='采集宝石', remove=True)
        self.call_idle_back()

        # if self.bot.config.useGatheringBoosts:
        #     b_buff_props = BuffsImageAndProps.ENHANCED_GATHER_BLUE.value
        #     p_buff_props = BuffsImageAndProps.ENHANCED_GATHER_PURPLE.value
        #     b_item_props = ItemsImageAndProps.ENHANCED_GATHER_BLUE.value
        #     p_item_props = ItemsImageAndProps.ENHANCED_GATHER_PURPLE.value
        #     has_blue = self.has_buff(MAP, b_buff_props)
        #     has_purple = self.has_buff(MAP, p_buff_props)
        #     if not has_blue and not has_purple:
        #         self.set_text(insert='当前没有采集加速, 尝试使用')
        #         self.use_item(MAP, [b_item_props, p_item_props])
        #     else:
        #         self.set_text(insert="采集加速已经生效")
                
        self.back_to_home_gui()
        self.back_to_map_gui()
        self.bot.snashot_update_event()
        
        try:
            size_count = 1
            src = (960, 320)
            dst = (320, 320)
            count = 0
            total_count = 30
            direction = 'S'
            self.set_text(insert="开始寻找宝石... {}".format(total_count))
            
            while count < total_count:
                size_step = size_count
                while size_step > 0:
                    self.set_text(insert="寻找宝石... {},{}".format(count, size_step))
                    self.swipe(src, dst, 1)
                    time.sleep(1)
                    size_step = size_step - 1
                    self.bot.snashot_update_event()
                    
                    _, _, diamond_pos = self.bot.gui.check_any(ImagePathAndProps.DIAMOND_IMG_PATH.value)
                    if diamond_pos is not None:
                        self.set_text(insert="发现宝石, {}".format(diamond_pos))
                        self.tap(diamond_pos)
                        
                        gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
                        self.tap(gather_button_pos, 8)
                
                        new_troops_button_pos = self.bot.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)[2]
                        if new_troops_button_pos is None:
                            self.set_text(insert="没有更多队列采集")
                            return 
                        self.set_text(insert="创建部队")
                        self.tap(new_troops_button_pos, 10)
                        match_button_pos = self.bot.gui.check_any(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)[2]
                        self.set_text(insert="开始行军")
                        self.tap(match_button_pos)
                    
                    if direction == 'S':
                        src = (640, 480)
                        dst = (640, 240)
                    elif direction == 'W':
                        src = (320, 320)
                        dst = (960, 320)
                    elif direction == 'N':
                        src = (640, 240)
                        dst = (640, 480)
                    else:
                        src = (960, 320)
                        dst = (320, 320)
                    
                count = count + 1           
                if (count) % 2 == 0:
                    size_count = size_count + 1
                    if direction == 'S':
                        direction = 'W'
                    elif direction == 'W':
                        direction = 'N'
                    elif direction == 'N':
                        direction = 'E'
                    else:
                        direction = 'W'
                    self.set_text(insert="改变方向 {},{},{}".format(count, size_count, direction))
            self.set_text(insert="没有发现更多宝石, 可以加大搜索范围")
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task
