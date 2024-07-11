from tasks.Task import Task
from tasks.constants import TaskName
from filepath.file_relative_paths import ImagePathAndProps
import traceback

import re
import time
import json
import copy

class GetRankingList(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def get_unit_string(self, count):
        unit = ""
        if count >= 100000000:
            unit = '亿'
            count = count / 100000000.0
            unit_string = '{:.2f}{}'.format(count, unit)
        elif count >= 10000:
            unit = '万'
            count = int(count // 10000)
            unit_string = '{}{}'.format(count, unit)
        else:
            unit_string = '{}{}'.format(count, unit)
        return unit_string
        
    def do(self, next_task = TaskName.BREAK, filepath = 'ranking_list.json'):
        self.set_text(title='获取排行榜', remove=True)
        self.back_to_home_gui()
        
        self.set_text(insert='打开个人中心')
        self.tap((25, 25), 2 * self.bot.config.tapSleep)
        
        self.set_text(insert='打开排行榜')
        ranking_pos = self.gui.check_any(ImagePathAndProps.RANKING_BUTTON_PATH.value)[2]
        self.tap(ranking_pos, 2 * self.bot.config.tapSleep)
        
        self.set_text(insert='打开战力排行榜')   
        self.tap((320, 360), 2 * self.bot.config.tapSleep) 
            
        ranking_power_title_pos = self.gui.check_any(ImagePathAndProps.RANKING_POWER_TITLE_PATH.value)[2]
        if ranking_power_title_pos is not None:
            count = 300
            start_pos = (260, 200)
            step = 80
            self.set_text(insert='开始统计战力前{}位执政官'.format(count))
            
            ranking_list = []
            for i in range(0, count):
                player_id = ""
                player_name = ""
                if i < 4:
                    cur_pos = (start_pos[0], start_pos[1] + i * step)
                else:
                    cur_pos = (start_pos[0], start_pos[1] + 3 * step + 20)
                    pass
                self.set_text(insert='打开第{}位执政官'.format(i + 1)) 
                self.tap(cur_pos, 2 * self.bot.config.tapSleep)
                
                player_title_pos = self.gui.check_any(ImagePathAndProps.PLAYER_DETAIL_TITLE_PATH.value)[2]
                if player_title_pos is not None:
                    imsch = self.gui.get_curr_device_screen_img_cv()
                    player_id_box = (565, 153, 565 + 130, 153 + 34)
                    player_id = self.gui.text_from_img_box(imsch, player_id_box)
                    player_id = re.sub('[^0-9]', '', player_id)
                    # player_id = player_id.replace(')', '')
                    player_name = self.gui.player_name(imsch=imsch).replace('·', '').replace('.', '')
                    local_box = (1050, 120, 1050 + 60, 120 + 26)
                    local = self.gui.text_from_img_box(imsch, local_box).replace(',', '')
                    power_box = (705, 260, 705 + 150, 260 + 34)
                    power = self.gui.int_from_img_box(imsch, power_box)
                    killed_box = (885, 260, 885 + 180, 260 + 34)
                    killed = self.gui.int_from_img_box(imsch, killed_box)
                    
                    dead = 0
                    t4_killed = 0
                    t5_killed = 0
                    
                    player_more_info_pos = self.gui.check_any(ImagePathAndProps.PLAYER_MORE_INFO_PATH.value)[2]
                    if player_more_info_pos is not None:
                        self.tap(player_more_info_pos, 2 * self.bot.config.tapSleep)
                        
                        imsch = self.gui.get_curr_device_screen_img_cv()
                        dead_box = (930, 360, 930 + 120, 360 + 25)
                        dead = self.gui.int_from_img_box(imsch, dead_box)
                        
                        player_more_info_kill_pos = self.gui.check_any(ImagePathAndProps.PLAYER_MORE_INFO_KILL_PATH.value)[2]
                        if player_more_info_kill_pos is not None:
                            self.tap(player_more_info_kill_pos)
                            
                            imsch = self.gui.get_curr_device_screen_img_cv()
                            t4_killed_box = (657, 320, 657 + 100, 320 + 25)
                            t4_killed = self.gui.int_from_img_box(imsch, t4_killed_box)
                            t5_killed_box = (657, 357, 657 + 100, 357 + 25)
                            t5_killed = self.gui.int_from_img_box(imsch, t5_killed_box)
                            
                            self.back()
                        self.back()
                    
                    dkp = t4_killed * 0.15 + t5_killed * 0.25 + dead
                    self.set_text(insert='统计第{}位执政官, {}, {}, {}, 战力:{}, 击杀:{}, 阵亡:{}, t4:{}, t5:{}, dkp:{}'.format(i + 1, player_name, player_id, local, 
                                                                                      self.get_unit_string(power), self.get_unit_string(killed), self.get_unit_string(dead),
                                                                                      self.get_unit_string(t4_killed), self.get_unit_string(t5_killed),
                                                                                      self.get_unit_string(dkp)))
                    # 返回排行榜界面
                    self.tap((10, 10), 2 * self.bot.config.tapSleep)
                    player_item = {
                        'local':local,
                        'player_id':player_id,
                        'player_name':player_name,
                        'power':power,
                        'killed':killed,
                        'dead':dead,
                        'power_unit':self.get_unit_string(power),
                        'killed_unit':self.get_unit_string(killed),
                        'dead_unit':self.get_unit_string(dead),
                        't4':t4_killed,
                        't5':t5_killed,
                        't4_unit':self.get_unit_string(t4_killed),
                        't5_unit':self.get_unit_string(t5_killed),
                        'dkp':dkp,
                        'dkp_unit':self.get_unit_string(dkp),
                    }
                    ranking_list.append(player_item)
                if i % 5 == 0:
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            line = json.dumps(ranking_list, ensure_ascii=False)
                            f.writelines([line])
                            f.truncate()
                    except Exception as e:
                        traceback.print_exc()
                        
                ranking_list_killed = copy.deepcopy(ranking_list)
                for i in range(0, len(ranking_list_killed)):
                    for j in range(i + 1, len(ranking_list_killed)):
                        if ranking_list_killed[i]['killed'] < ranking_list_killed[j]['killed']:
                            tmp = ranking_list_killed[i]
                            ranking_list_killed[i] = ranking_list_killed[j]
                            ranking_list_killed[j] = tmp
                for i in range(0, len(ranking_list)):   
                    for j in range(0, len(ranking_list_killed)):   
                        if ranking_list[i]['player_id'] == ranking_list_killed[j]['player_id']:
                            ranking_list[i]['dv'] = i - j
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        line = json.dumps(ranking_list, ensure_ascii=False)
                        f.writelines([line])
                        f.truncate()     
                except Exception as e:
                    traceback.print_exc()   
                             
                ranking_power_title_pos = self.gui.check_any(ImagePathAndProps.RANKING_POWER_TITLE_PATH.value)[2]
                if ranking_power_title_pos is None:
                    self.set_text(insert='异常退出') 
                    break
                     
        return next_task
