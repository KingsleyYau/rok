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

    def create_troop(self, full_load=False):
        new_troops_button_pos = self.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)[2]
        if new_troops_button_pos is None:
            self.set_text(insert="没有发现创建部队按钮, 没有更多队列")
            self.bot.snashot_update_event()
            return False
        
        self.set_text(insert="创建部队, {}".format(new_troops_button_pos))
        self.tap(new_troops_button_pos, 5 * self.bot.config.tapSleep)
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
        if match_button_pos is None:
            self.set_text(insert="没有发现行军按钮")
            self.bot.snashot_update_event()
            return False
        
        self.set_text(insert="开始行军, {}".format(match_button_pos))
        self.tap(match_button_pos, 5 * self.bot.config.tapSleep)
        self.bot.snashot_update_event()
        
        match_button_pos = self.gui.check_any(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)[2]
        if match_button_pos is not None:
            self.set_text(insert="没有足够部队行军")
            self.bot.snashot_update_event()
            return False
        
        return True
        
    def do(self, next_task=TaskName.BREAK):
        self.set_text(title='采集资源', remove=True)
        self.back_to_map_gui()
        self.call_idle_back()
        full_load, cur, total = self.gui.troop_already_full()
        if full_load:
            self.set_text(insert="没有更多队列")
            return next_task
        else:
            self.set_text(insert="当前队列数量:{}/{}".format(cur, total))
                 
        gathering_count = 0       
        if self.bot.config.gatherAllianceResource:
            try:
                self.set_text(insert='优先采集联盟矿')
                self.menu_should_open(True)
                self.set_text(insert='打开联盟中心')
                alliance_btn_pos = (930, 670)
                self.tap(alliance_btn_pos, self.bot.config.tapSleep)
                
                found = False               
                self.set_text(insert='寻找领土')
                _, _, territory_pos = self.gui.check_any(ImagePathAndProps.TERRITORY_IMG_PATH.value, times=3)
                if territory_pos is not None:
                    self.set_text(insert='打开领土, {}'.format(territory_pos))
                    self.tap(territory_pos, 2 * self.bot.config.tapSleep)
                    self.bot.snashot_update_event()
                    for i in range(2):
                        self.bot.snashot_update_event()
                        territory_gathering_pos = self.gui.check_any(ImagePathAndProps.TERRITORY_GATHERING_IMG_PATH.value, times=3)[2]
                        if territory_gathering_pos is not None:
                            self.set_text(insert='定位联盟矿, {}'.format(territory_gathering_pos))
                            self.tap((territory_gathering_pos[0] + 5, territory_gathering_pos[1] - 20), 2 * self.bot.config.tapSleep)
                            self.bot.snashot_update_event()
                
                            pos = (640, 320)
                            self.set_text(insert='打开联盟矿, {}'.format(pos))
                            self.tap(pos)
                            gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
                            self.tap(gather_button_pos, 2 * self.bot.config.tapSleep)
                            self.bot.snashot_update_event()
                
                            found = True
                            gathering_count = gathering_count + 1
                            gather_join_pos = self.gui.check_any(ImagePathAndProps.TERRITORY_GATHER_JOIN_IMG_PATH.value)[2]
                            if gather_join_pos is None:
                                self.set_text(insert="没有找到加入按钮, 可能已经在采集")
                                break
                            self.set_text(insert="加入联盟矿{}".format(gather_join_pos))
                            self.tap(gather_join_pos, 2 * self.bot.config.tapSleep)
                            self.bot.snashot_update_event()
                
                            if not self.create_troop(True):
                                return next_task
                            break
                
                        self.set_text(insert='第{}次尝试打开联盟资源中心'.format(i+1))   
                        self.bot.snashot_update_event()
                        territory_tab_pos = self.gui.check_any(ImagePathAndProps.TERRITORY_RESOURCE_IMG_PATH.value)[2]
                        if territory_tab_pos is not None:
                            self.tap(territory_tab_pos, 2 * self.bot.config.tapSleep)
                if not found:
                    self.set_text(insert='没有发现联盟矿')   
                    
            except Exception as e:
                traceback.print_exc()
                pass
        
        if self.bot.config.gatherWildResource:
            self.set_text(insert='采集野外资源')
    
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
            try:
                self.back_to_home_gui()
                self.back_to_map_gui()
                self.swipe((360, 600), (200, 400))
                
                resourse_code = self.get_min_resource()
                self.back_to_map_gui()
                self.swipe((480, 320), (800, 320))
                chose_icon_pos = self.get_resource_pos(resourse_code)
    
                if self.bot.config.holdOneQuerySpace:
                    space = self.check_query_space()
                    if space <= 1:
                        self.set_text(insert="保留一队空闲, 停止")
                        return next_task
    
                # tap on magnifier
                magnifier_pos = (60, 540)
                level = 0
                retry_count = 0
                repeat = False
                first_time = True
                
                total_search_count = 0
                
                # for i in range(10):
                while gathering_count < self.bot.config.gatherMaxTroops and total_search_count < 10:
                    total_search_count = total_search_count + 1
                    if retry_count > 4:
                        self.set_text(insert="{}次策略没有找到可用资源点".format(retry_count))
                        break
                    
                    if level > 2:
                        self.set_text(insert="{}次没有找到可用资源点".format(level))
                        new_resourse_code = self.get_next_resource(resourse_code)
                        self.set_text(insert="改变搜索策略, {}=>{}".format(
                            self.get_resource_name(resourse_code), 
                            self.get_resource_name(new_resourse_code)
                            )
                        )
                        chose_icon_pos = self.get_resource_pos(new_resourse_code)
                        resourse_code = new_resourse_code
                        level = 0
                        retry_count = retry_count + 1
                        should_decreasing_lv = False
                        first_time = True
                            
                    if self.bot.config.holdOneQuerySpace:
                        space = self.check_query_space()
                        if space <= 1:
                            self.set_text(insert="保留一队空闲, 停止")
                            break

                    # 打开搜索资源界面
                    self.set_text(insert="开始搜索{}".format(self.get_resource_name(resourse_code)))
                    self.back_to_map_gui()
                    self.tap(magnifier_pos)
                    self.tap(chose_icon_pos)
                    
                    if should_decreasing_lv:
                        dec_pos = self.gui.check_any(ImagePathAndProps.DECREASING_BUTTON_IMAGE_PATH.value)[2]
                        if dec_pos is not None:
                            self.set_text(insert="点击降级{}, 当前等级{}".format(dec_pos, 6 - level))
                            self.tap(dec_pos)
                        self.bot.snashot_update_event()
                    else:
                        if first_time:
                            inc_pos = self.gui.check_any(ImagePathAndProps.INCREASING_BUTTON_IMAGE_PATH.value)[2]
                            if inc_pos is not None:
                                self.set_text(insert="还原搜索等级, 当前等级{}".format(6 - level))
                                for i in range(3):
                                    self.tap((inc_pos[0] - 33, inc_pos[1]))
                            first_time = False
                        self.bot.snashot_update_event()
                    
                    search_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)[2]
                    self.set_text(insert="点击搜索{}".format(search_pos))
                    self.tap(search_pos, 3 * self.bot.config.tapSleep)
                    self.bot.snashot_update_event()
                    
                    self.set_text(insert="打开资源点")
                    self.tap((640, 320), self.bot.config.tapSleep)
                    self.bot.snashot_update_event()
                    
                    coordinate = ''
                    _, _, resource_xy_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_IMG_PATH.value)
                    if resource_xy_pos is not None:
                        src = cv2.imdecode(np.asarray(self.bot.gui.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR)
                        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
                        src = src[int(resource_xy_pos[1])-5:int(resource_xy_pos[1] + 20), int(resource_xy_pos[0]+140):int(resource_xy_pos[0]+140+100)]
                        coordinate = img_to_string_eng(src).replace('\n', '').replace(',', '')
                        self.set_text(insert="发现资源点, 坐标, {}".format(coordinate))
                    
                    # check is same pos
                    if len(coordinate) > 0:
                        if coordinate in last_resource_pos:
                            if repeat:
                                self.set_text(insert="资源点已经处理过, 坐标, {}, 降级, 等级{}=>等级{}".format(coordinate, 6 - level, 6 - level - 1))
                                repeat = False
                                level = level + 1
                                should_decreasing_lv = True
                            else:
                                self.set_text(insert="资源点已经处理过, 坐标, {}, 再试一次".format(coordinate))
                                repeat = True
                            self.bot.snashot_update_event()
                            continue
                        
                        last_resource_pos.append(coordinate)

                        gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
                        if gather_button_pos is None:
                            self.set_text(insert="资源点没有发现采集按钮, 可能正在采集")
                            continue
                        
                        should_decreasing_lv = False
                        self.set_text(insert="开始第{}次采集资源点{}, 坐标, {}".format(gathering_count + 1, gather_button_pos, coordinate))
                        self.tap(gather_button_pos, 2 * self.bot.config.tapSleep)
                        
                        if not self.create_troop():
                            return next_task
                        
                        gathering_count = gathering_count + 1
                        full_load, cur, total = self.gui.troop_already_full()
                        if full_load:
                            self.set_text(insert="没有更多队列")
                            return next_task
                        else:
                            self.set_text(insert="当前队列数量:{}/{}".format(cur, total))
                    else:
                        self.set_text(insert="没有更多资源点, 降级, 当前等级{}".format(6 - level))
                        should_decreasing_lv = True
                        level = level + 1
                    # self.swipe((200, 320), (800, 320))
                    
                self.bot.snashot_update_event()
            except Exception as e:
                traceback.print_exc()
                return next_task
        return next_task

    def get_resource_pos(self, resourse_code):
        resource_icon_pos = [
            (450, 640),
            (640, 640),
            (830, 640),
            (1030, 640)
        ]
        chose_icon_pos = resource_icon_pos[0]
        if resourse_code == Resource.FOOD.value:
            chose_icon_pos = resource_icon_pos[0]
        elif resourse_code == Resource.WOOD.value:
            chose_icon_pos = resource_icon_pos[1]
        elif resourse_code == Resource.STONE.value:
            chose_icon_pos = resource_icon_pos[2]
        elif resourse_code == Resource.GOLD.value:
            chose_icon_pos = resource_icon_pos[3]
        return chose_icon_pos
            
    def get_next_resource(self, resourse_code):
        if resourse_code == Resource.GOLD.value:
            new_resourse_code = Resource.FOOD.value
        elif resourse_code == Resource.FOOD.value:
            new_resourse_code = Resource.STONE.value
        elif resourse_code == Resource.STONE.value:
            new_resourse_code = Resource.WOOD.value
        elif resourse_code == Resource.WOOD.value:
            new_resourse_code = Resource.GOLD.value
        return new_resourse_code
    
    def get_resource_name(self, resourse_code):
        res_names = [
            '玉米',
            '木头',
            '石头',
            '金矿',
            ]
        chose_name = res_names[0]
        if resourse_code == Resource.FOOD.value:
            chose_name = res_names[0]
        elif resourse_code == Resource.WOOD.value:
            chose_name = res_names[1]
        elif resourse_code == Resource.STONE.value:
            chose_name = res_names[2]
        elif resourse_code == Resource.GOLD.value:
            chose_name = res_names[3]
        return chose_name
    
    def get_min_resource(self):
        res_names = [
            '玉米',
            '木头',
            '石头',
            '金矿',
            '宝石',
            ]
        self.tap((725, 20))
        result = self.gui.resource_amount_image_to_string()
        tips = "玉米: {}, 木头: {}, 石头: {}, 金矿: {}, 宝石: {}".format(result[0], result[1], result[2], result[3], result[4])
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
            diff.append(((result[i] if result[i] > -1 else 0) / res) - (ratio[i] / ras))

        diff = ['{:.4f}'.format(i) for i in diff]
        m = np.argmin(diff)
        self.set_text(insert='最需要的资源是{}, {}'.format(res_names[m], diff))
        return m

    def check_query_space(self):
        found, _, _ = self.gui.check_any(ImagePathAndProps.HAS_MATCH_QUERY_IMAGE_PATH.value)
        curr_q, max_q = self.gui.match_query_to_string()
        if curr_q is None:
            return self.max_query_space
        return max_q - curr_q
