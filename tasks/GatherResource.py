import traceback

from filepath.constants import MAP
from filepath.file_relative_paths import BuffsImageAndProps, ItemsImageAndProps, ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName, Resource
from utils import log, device_log, img_to_string, img_to_string_eng
import cv2
import numpy as np

class GatherResource(Task):

    def __init__(self, bot):
        super().__init__(bot)
        self.max_query_space = 5

    def create_troop(self):
        new_troops_button_pos = self.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)[2]
        if new_troops_button_pos is None:
            self.set_text(insert="没有更多队列采集")
            self.bot.snashot_update_event()
            return False
        
        self.set_text(insert="创建部队")
        self.tap(new_troops_button_pos, 10)
        self.bot.snashot_update_event()
        
        if self.bot.config.gatherResourceNoSecondaryCommander:
            self.set_text(insert="移除副将")
            self.tap((473, 501))
            self.bot.snashot_update_event()
            
        self.set_text(insert="开始行军")
        match_button_pos = self.gui.check_any(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)[2]
        self.tap(match_button_pos)
        self.bot.snashot_update_event()
        return True
        
    def do(self, next_task=TaskName.BREAK):
        self.set_text(title='采集资源', remove=True)
        
        try:
            self.back_to_home_gui()
            self.menu_should_open(True)
            self.set_text(insert='优先采集联盟矿')
            self.set_text(insert='打开联盟中心')
            alliance_btn_pos = (1030, 670)
            self.tap(alliance_btn_pos)
            territory_pos = (785, 405)
            self.tap(territory_pos)
            for i in range(2):
                self.bot.snashot_update_event()
                territory_gathering_pos = self.gui.check_any(ImagePathAndProps.TERRITORY_GATHERING_IMG_PATH.value)[2]
                if territory_gathering_pos is not None:
                    self.set_text(insert='定位联盟矿{}'.format(territory_gathering_pos))
                    self.tap((territory_gathering_pos[0] + 5, territory_gathering_pos[1] - 20))
                    self.bot.snashot_update_event()
        
                    self.set_text(insert='打开联盟矿')
                    self.tap((640, 320))
                    gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
                    self.tap(gather_button_pos)
                    self.bot.snashot_update_event()
        
                    gather_join_pos = self.gui.check_any(ImagePathAndProps.TERRITORY_GATHER_JOIN_IMG_PATH.value)[2]
                    if gather_join_pos is None:
                        self.set_text(insert="没有找到加入按钮, 可能已经在采集")
                        break
                    self.tap(gather_join_pos)
                    self.bot.snashot_update_event()
        
                    if not self.create_troop():
                        return next_task
                    break
        
                self.set_text(insert='打开联盟资源中心')   
                territory_tab_pos = self.gui.check_any(ImagePathAndProps.TERRITORY_IMG_PATH.value)[2]
                if territory_tab_pos is not None:
                    self.tap(territory_tab_pos)
        
        except Exception as e:
            traceback.print_exc()
            pass
        
        self.set_text(insert='采集野外资源')
        # self.call_idle_back()

        if self.bot.config.useGatheringBoosts:
            b_buff_props = BuffsImageAndProps.ENHANCED_GATHER_BLUE.value
            p_buff_props = BuffsImageAndProps.ENHANCED_GATHER_PURPLE.value
            b_item_props = ItemsImageAndProps.ENHANCED_GATHER_BLUE.value
            p_item_props = ItemsImageAndProps.ENHANCED_GATHER_PURPLE.value
            has_blue = self.has_buff(MAP, b_buff_props)
            has_purple = self.has_buff(MAP, p_buff_props)
            if not has_blue and not has_purple:
                self.set_text(insert='当前没有采集加速, 尝试使用')
                self.use_item(MAP, [b_item_props, p_item_props])
            else:
                self.set_text(insert="采集加速已经生效")

        last_resource_pos = []
        coordinate = ''
        should_decreasing_lv = False
        resource_icon_pos = [
            (450, 640),
            (640, 640),
            (830, 640),
            (1030, 640)
        ]
        try:
            chose_icon_pos = resource_icon_pos[0]
            self.back_to_map_gui()
            self.swipe((320, 720), (200, 400))
            
            resourse_code = self.get_min_resource()
            self.back_to_map_gui()

            if resourse_code == Resource.FOOD.value:
                chose_icon_pos = resource_icon_pos[0]
                self.set_text(insert="搜索玉米")

            elif resourse_code == Resource.WOOD.value:
                chose_icon_pos = resource_icon_pos[1]
                self.set_text(insert="搜索木头")

            elif resourse_code == Resource.STONE.value:
                chose_icon_pos = resource_icon_pos[2]
                self.set_text(insert="搜索石头")

            elif resourse_code == Resource.GOLD.value:
                chose_icon_pos = resource_icon_pos[3]
                self.set_text(insert="搜索金矿")

            if self.bot.config.holdOneQuerySpace:
                space = self.check_query_space()
                if space <= 1:
                    self.set_text(insert="保留一队空闲, 停止!")
                    return next_task

            # tap on magnifier
            magnifier_pos = (60, 540)
            self.tap(magnifier_pos)
            self.tap(chose_icon_pos)
            search_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)[2]
            dec_pos = self.gui.check_any(ImagePathAndProps.DECREASING_BUTTON_IMAGE_PATH.value)[2]
            inc_pos = self.gui.check_any(ImagePathAndProps.INCREASING_BUTTON_IMAGE_PATH.value)[2]
            self.tap((inc_pos[0] - 33, inc_pos[1]))
            self.bot.snashot_update_event()
            repeat_count = 0
            for i in range(10):
                # open search resource
                if len(last_resource_pos) > 0:
                    self.back_to_map_gui()

                    if self.bot.config.holdOneQuerySpace:
                        space = self.check_query_space()
                        if space <= 1:
                            self.set_text(insert="保留一队空闲, 停止!")
                            return next_task

                    self.tap(magnifier_pos)
                    self.tap(chose_icon_pos)

                # decreasing level
                if should_decreasing_lv:
                    self.set_text(insert="没有更多资源点, 降级")
                    self.tap(dec_pos)

                for j in range(5):
                    self.tap(search_pos, 8)
                    is_found, _, _ = self.gui.check_any(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)
                    if not is_found:
                        break
                    self.set_text(insert="没有更多资源点, 降级 [{}]".format(j))
                    self.tap(dec_pos)

                self.set_text(insert="发现资源点")
                self.tap((640, 320), 2 * self.bot.config.tapSleep)
                self.bot.snashot_update_event()
                
                coordinate = ''
                _, _, resource_xy_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_IMG_PATH.value)
                if resource_xy_pos is not None:
                    src = cv2.imdecode(np.asarray(self.bot.gui.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR)
                    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
                    src = src[int(resource_xy_pos[1])-5:int(resource_xy_pos[1] + 20), int(resource_xy_pos[0]+140):int(resource_xy_pos[0]+140+100)]
                    coordinate = img_to_string_eng(src).replace('\n', '')
                    self.set_text(insert="发现资源点, 坐标, {}".format(coordinate))
                
                # check is same pos
                # new_resource_pos = self.gui.resource_location_image_to_string()
                if len(coordinate) > 0:
                    if coordinate in last_resource_pos:
                        should_decreasing_lv = True
                        repeat_count = repeat_count + 1
                        self.set_text(insert="资源点正在采集, {}".format(coordinate))
                        self.bot.snashot_update_event()
                        if repeat_count > 4:
                            self.set_text(insert="stuck! end task")
                            break
                        else:
                            self.swipe((400, 180), (800, 400))
                            continue
                    last_resource_pos.append(coordinate)
                    
                should_decreasing_lv = False
                gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
                if gather_button_pos is None:
                    self.set_text(insert="没有发现采集按钮, 可能资源点正在采集")
                    self.swipe((400, 180), (800, 400))
                    continue
                self.tap(gather_button_pos, 8)
                
                if not self.create_troop():
                    return next_task
                repeat_count = 0
                self.swipe((400, 180), (800, 400))
                
            self.bot.snashot_update_event()
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task

    def get_min_resource(self):
        res_names = [
            '玉米',
            '木头',
            '石头',
            '金矿',
            ]
        self.tap((725, 20))
        result = self.gui.resource_amount_image_to_string()
        tips = "玉米: {}, 木头: {}, 石头: {}, 金矿: {}".format(result[0], result[1], result[2], result[3])
        self.set_text(insert=tips)
        
        ratio = [
            self.bot.config.gatherResourceRatioFood,
            self.bot.config.gatherResourceRatioWood,
            self.bot.config.gatherResourceRatioStone,
            self.bot.config.gatherResourceRatioGold
        ]

        ras = sum(ratio)
        res = sum(result[:4])

        diff = []
        for i in range(4):
            diff.append((ratio[i] / ras) - ((result[i] if result[i] > -1 else 0) / res))

        m = 0
        for i in range(len(result[:4])):
            if diff[m] < diff[i]:
                m = i
        self.set_text(insert='最少的资源是{}'.format(res_names[m]))
        return m

    def check_query_space(self):
        found, _, _ = self.gui.check_any(ImagePathAndProps.HAS_MATCH_QUERY_IMAGE_PATH.value)
        curr_q, max_q = self.gui.match_query_to_string()
        if curr_q is None:
            return self.max_query_space
        return max_q - curr_q
