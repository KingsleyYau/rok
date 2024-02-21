import traceback

from filepath.constants import MAP
from filepath.file_relative_paths import BuffsImageAndProps, ItemsImageAndProps, ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName, Resource
from utils import log, device_log

class GatherResource(Task):

    def __init__(self, bot):
        super().__init__(bot)
        self.max_query_space = 5

    def do(self, next_task=TaskName.BREAK):
        magnifier_pos = (60, 540)
        self.set_text(title='采集野外资源', remove=True)
        self.call_idle_back()

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
                self.tap((640, 320), 8)
                self.bot.snashot_update_event()
                
                # check is same pos
                new_resource_pos = self.gui.resource_location_image_to_string()
                if len(new_resource_pos) > 0:
                    if new_resource_pos in last_resource_pos:
                        should_decreasing_lv = True
                        repeat_count = repeat_count + 1
                        self.set_text(insert="资源点正在采集")
                        self.bot.snashot_update_event()
                        if repeat_count > 4:
                            self.set_text(insert="stuck! end task")
                            break
                        else:
                            continue
                    last_resource_pos.append(new_resource_pos)
                should_decreasing_lv = False
                gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
                self.tap(gather_button_pos, 8)
                pos = self.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)[2]
                if pos is None:
                    self.set_text(insert="没有更多队列采集")
                    self.bot.snashot_update_event()
                    return next_task
                
                new_troops_button_pos = pos
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
                repeat_count = 0
                self.swipe(300, 720, 400, 360, 1)
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
        self.set_text(
            insert="玉米: {}, 木头: {}, 石头: {}, 金矿: {}".format(result[0], result[1], result[2], result[3]))

        ratio = [
            self.bot.config.gatherResourceRatioFood,
            self.bot.config.gatherResourceRatioWood,
            self.bot.config.gatherResourceRatioStone,
            self.bot.config.gatherResourceRatioGold
        ]

        ras = sum(ratio)
        res = sum(result)

        diff = []
        for i in range(4):
            diff.append((ratio[i] / ras) - ((result[i] if result[i] > -1 else 0) / res))

        m = 0
        for i in range(len(result)):
            if diff[m] < diff[i]:
                m = i
        device_log(self.bot.device, 'get_min_resource, {}'.format(res_names[m]))
        return m

    def check_query_space(self):
        found, _, _ = self.gui.check_any(ImagePathAndProps.HAS_MATCH_QUERY_IMAGE_PATH.value)
        curr_q, max_q = self.gui.match_query_to_string()
        if curr_q is None:
            return self.max_query_space
        return max_q - curr_q
