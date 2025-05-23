from tasks.Task import Task
from tasks.constants import TaskName
from filepath.file_relative_paths import ImagePathAndProps
import traceback

import re
import time
import json
import copy

from paddleocr import PaddleOCR

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
            
        ocr = PaddleOCR(lang="ch", use_gpu=False, use_angle_cls=False, show_log=False)
    
        power_total = 0
        kill_total = 0
        dead_total = 0
        ranking_power_title_pos = self.gui.check_any(ImagePathAndProps.RANKING_POWER_TITLE_PATH.value)[2]
        if ranking_power_title_pos is not None:
            count = 250
            start_pos = (260, 200)
            step = 80
            self.set_text(insert='开始统计战力前{}位执政官'.format(count))
            
            ranking_list = []
            istep = 0
            for i in range(0, count):
                player_id = ""
                player_name = ""
                if i < 4:
                    cur_pos = (start_pos[0], start_pos[1] + i * step)
                else:
                    cur_pos = (start_pos[0], start_pos[1] + istep * step + 20)
                    pass
                self.set_text(insert='打开第{}位执政官'.format(i + 1)) 
                self.tap(cur_pos, self.bot.config.tapSleep)
                
                window_title = ""
                for j in range(0, 5):
                    imsch = self.gui.get_curr_device_screen_img_cv()
                    window_title_box = (550, 60, 550 + 170, 60 + 50)
                    window_title = self.gui.text_from_img_box(imsch, window_title_box)
                    if len(window_title) > 0:
                        break
                    time.sleep(1)
                    
                # self.set_text(insert='打开第{}位执政官, 当前窗口:{}'.format(i + 1, window_title)) 
            
                # player_title_pos = self.gui.check_any(ImagePathAndProps.PLAYER_DETAIL_TITLE_PATH.value, times=3)[2]
                # if player_title_pos is not None:
                if window_title.find('资料') != -1:
                    istep = 3
                    imsch = self.gui.get_curr_device_screen_img_cv()
                    # 统计用户ID
                    player_id_box = (555, 143, 555 + 130, 143 + 34)
                    player_id = self.gui.text_from_img_box(imsch, player_id_box)
                    player_id = re.sub('[^0-9]', '', player_id)
                    # player_id = player_id.replace(')', '')
                    # 统计用户名
                    player_name = self.gui.player_name(imsch=imsch).replace('·', '').replace('.', '')
                    # local_box = (1050, 120, 1050 + 60, 120 + 26)
                    # local = self.gui.text_from_img_box(imsch, local_box).replace(',', '')
                    # 统计战力
                    power_box = (680, 255, 680 + 150, 255 + 34)
                    power = self.gui.int_from_img_box(imsch, power_box)
                    # 统计击杀
                    killed_box = (920, 260, 920 + 180, 260 + 32)
                    killed = self.gui.int_from_img_box(imsch, killed_box)
                    
                    dead = 0
                    t4_killed = 0
                    t5_killed = 0
                    
                    player_more_info_pos = self.gui.check_any(ImagePathAndProps.PLAYER_MORE_INFO_PATH.value, times=3)[2]
                    if player_more_info_pos is not None:
                        # 点击更多信息
                        self.tap(player_more_info_pos, self.bot.config.tapSleep)
                        
                        imsch = self.gui.get_curr_device_screen_img_cv()
                        # 统计阵亡
                        dead_box = (930, 365, 930 + 120, 365 + 25)
                        dead = self.gui.int_from_img_box(imsch, dead_box)
                        
                        player_more_info_kill_pos = self.gui.check_any(ImagePathAndProps.PLAYER_MORE_INFO_KILL_PATH.value, times=3)[2]
                        if player_more_info_kill_pos is not None:
                            # 点击具体击杀分信息
                            self.tap(player_more_info_kill_pos)
                            
                            imsch = self.gui.get_curr_device_screen_img_cv()
                            # 统计具体击杀
                            t4_killed_box = (657, 320, 657 + 100, 320 + 25)
                            t4_killed = self.gui.int_from_img_box(imsch, t4_killed_box)
                            t5_killed_box = (657, 357, 657 + 100, 357 + 25)
                            t5_killed = self.gui.int_from_img_box(imsch, t5_killed_box)
                            
                            self.back()
                        self.back()
                    
                    dkp = int(t4_killed * 0.15 + t5_killed * 0.3 + 0.8 * dead)
                    self.set_text(insert='统计第{}位执政官, {}, {}, 战力:{}, 击杀分:{}, 阵亡:{}, t4:{}, t5:{}, dkp:{}'.format(i + 1, player_name, player_id, 
                                                                                      self.get_unit_string(power), self.get_unit_string(killed), self.get_unit_string(dead),
                                                                                      self.get_unit_string(t4_killed), self.get_unit_string(t5_killed),
                                                                                      self.get_unit_string(dkp)))

                    
                    player_item = {
                        # 'local':local,
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
                    power_total = power_total + power
                    kill_total = kill_total + killed
                    dead_total = dead_total + dead
                else:
                    istep = istep + 1
                    
                if i % 5 == 0:
                    self.set_text(insert='当前总战力:{}, 总击杀:{}, 总阵亡:{}'.format(
                        self.get_unit_string(power_total), 
                        self.get_unit_string(kill_total), 
                        self.get_unit_string(dead_total))
                    )
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            jsonObj = {}
                            jsonObj['power_total'] = power_total
                            jsonObj['power_total_unit'] = self.get_unit_string(power_total)
                            jsonObj['kill_total'] = kill_total
                            jsonObj['kill_total_unit'] = self.get_unit_string(kill_total)
                            jsonObj['dead_total'] = dead_total
                            jsonObj['dead_total_unit'] = self.get_unit_string(dead_total)
                            jsonObj['ranking_list'] = ranking_list;
                            line = json.dumps(jsonObj, ensure_ascii=False)
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
                        jsonObj = {}
                        jsonObj['power_total'] = power_total
                        jsonObj['power_total_unit'] = self.get_unit_string(power_total)
                        jsonObj['kill_total'] = kill_total
                        jsonObj['kill_total_unit'] = self.get_unit_string(kill_total)
                        jsonObj['dead_total'] = dead_total
                        jsonObj['dead_total_unit'] = self.get_unit_string(dead_total)
                        jsonObj['ranking_list'] = ranking_list;
                        line = json.dumps(jsonObj, ensure_ascii=False)
                        f.writelines([line])
                        f.truncate()
                except Exception as e:
                    traceback.print_exc()   
                
                found = False
                for j in range(0, 3):
                    # 返回排行榜界面
                    self.tap((10, 10), self.bot.config.tapSleep)    
                            
                    imsch = self.gui.get_curr_device_screen_img_cv()            
                    window_title_box = (540, 27, 540 + 210, 27 + 36)
                    window_title = self.gui.text_from_img_box(imsch, window_title_box)
                    if window_title.find('战力排行榜') != -1:
                        found = True
                        break
                if not found:
                    self.set_text(insert='异常退出')
                    break
                # ranking_power_title_pos = self.gui.check_any(ImagePathAndProps.RANKING_POWER_TITLE_PATH.value, times=3)[2]
                # if ranking_power_title_pos is None:
                #     self.set_text(insert='异常退出')
                #     break
            self.set_text(insert='获取排行榜完成, 总战力:{}, 总击杀:{}, 总阵亡:{}'.format(power_total, kill_total, dead_total))
        return next_task
