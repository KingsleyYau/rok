import adb
import time
import os, errno
import json
import traceback
from PIL import Image
import re
from gui.creator import load_bot_config
from gui.creator import load_building_pos
from gui.creator import write_device_config, load_device_config
from bot_related.bot import Bot
from tasks.constants import BuildingNames
from filepath.file_relative_paths import ImagePathAndProps
from utils import log, img_to_string, img_to_string_eng, resize
from api.run_config import RunConfig
from bot_related import aircve as aircv

from tasks.Task import Task
from tasks.GetRankingList import GetRankingList

import cv2
import numpy as np
from paddleocr import PaddleOCR

from config import NONE

def ranking(bot, filepath = ''):
    if len(filepath) == 0:
        today = time.strftime("%Y-%m-%d", time.localtime())
        filepath = 'web/ranking/ranking_list_{}.json'.format(today)
    task = GetRankingList(bot)    
    task.do(filepath=filepath)
    return 

def monitor(bot, task, filepath):
    # log('监控城寨')
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    monitor_count = {}
    gathering = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            line = f.readline()
            monitor_count = json.loads(line)
            gathering = monitor_count['gathering']
            # log('已经统计的集结',gathering)
    except BaseException as e:
        log(e)  
        
    if not 'start_time' in monitor_count:
        monitor_count['start_time'] = start_time    
        
    try:
        found = False
        
        war_main_pos = bot.gui.check_any(ImagePathAndProps.ALLIANCE_WAR_MAIN_PATH.value)[2]
        if war_main_pos is None:
            task.back_to_map_gui()
        
            task.menu_should_open(True)
            log('打开联盟中心')
            alliance_btn_pos = (930, 670)
            task.tap(alliance_btn_pos, 10)
        
            war_pos = bot.gui.check_any(ImagePathAndProps.ALLIANCE_WAR_IMG_PATH.value)[2]
            if war_pos is not None:
                log('打开战争界面')
                task.tap(war_pos, 10)
        else:
            # log('已经打开战争界面')
            pass
                
        imsch = bot.gui.get_curr_device_screen_img_cv()
        imsch_gray = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
        cancel_pos = (415, 155)
        cancel_box = (cancel_pos[0], cancel_pos[1], cancel_pos[0] + 320, cancel_pos[1] + 35)
        cancel_name = bot.gui.text_from_img_box(imsch_gray, cancel_box)
        if len(cancel_name) > 0 :
            player_names = re.findall('^(.+)取消.*$', cancel_name)
            log('发现通知, {}, player_names: {}'.format(cancel_name, player_names))
            
            if len(player_names) > 0:
                player_name = player_names[0].replace('\[', '').replace('\]', '')
                
                last_identify = None
                max_time = 0
                for identify in gathering:
                    gethering_item = gathering[identify]
                    if player_name == gethering_item['player_name']:
                        add_time = time.mktime(time.strptime(gethering_item['add_time'], "%Y-%m-%d %H:%M:%S"))
                        if add_time > max_time:
                            max_time = add_time
                            last_identify = identify
                
                if last_identify is not None:
                    log('取消集结', last_identify, gathering[last_identify])
                    gathering.pop(last_identify)
                
        for i in range(1,3):
            # 用户名
            player_name_pos = (310, 185 * i)
            player_name_box = (player_name_pos[0], player_name_pos[1], player_name_pos[0] + 200, player_name_pos[1] + 35)
            player_name = bot.gui.player_name(box=player_name_box, imsch=imsch)
            
            # 用户坐标
            player_pos = (190, 185 * i + 95)
            player_box = (player_pos[0], player_pos[1], player_pos[0] + 100, player_pos[1] + 30)
            player_xy = bot.gui.text_from_img_box(imsch_gray, player_box)
            # player_xy_x = re.findall('^X:(.*)Y:.*$', player_xy)[0]
            # player_xy_y = re.findall('^X:.*Y:(.*)$', player_xy)[0]
            
            # 集结名称
            dst_pos = (850, 185 * i)
            dst_box = (dst_pos[0], dst_pos[1], dst_pos[0] + 130, dst_pos[1] + 35)
            dst = bot.gui.text_from_img_box(imsch_gray, dst_box)
            is_count = (dst.find('城寨') != -1)
            
            # 集结坐标
            xy_pos = (985, 185 * i + 95)
            xy_box = (xy_pos[0], xy_pos[1], xy_pos[0] + 100, xy_pos[1] + 30)
            xy = bot.gui.text_from_img_box(imsch_gray, xy_box)
            # xy_x = re.findall('^X:(.*)Y:.*$', xy)[0]
            # xy_y = re.findall('^X:.*Y:(.*)$', xy)[0]
            
            # 集结状态
            status_pos = (610, 185 * i + 80)
            status_box = (status_pos[0], status_pos[1], status_pos[0] + 60, status_pos[1] + 25)
            status = bot.gui.text_from_img_box(imsch_gray, status_box)
            status = re.sub('^[^a-zA-Z0-9_\u4e00-\u9fa5]+$', '', status)
            
            # log('当前集结, {}, {}, {} => {}, {}'.format(i, player_name, player_xy, xy, dst))
            if (len(player_name)>0) and len(dst)>0 and (len(xy)>0):
                # log('发现集结,{},{},{}'.format(player_name, xy, status))
                time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item = {'player_name':player_name, 'player_xy':player_xy, 'xy':xy, 'dst':dst, 'add_time':time_string}
                        # 'player_xy_x':player_xy_x,'player_xy_y':player_xy_y,'xy_x':xy_x,'xy_y':xy_y}
                
                identify = player_xy+'-'+xy
                if not identify in gathering:
                    if (status == "准备中" or status == "等待中") and is_count:
                        found = True
                        gathering[identify] = item
                        log('新增集结,{},{}'.format(item,status))
                    else:
                        # log('其他集结信息,{},{}'.format(item, status))
                        pass
                else:
                    old_item = gathering[identify]
                    if old_item['player_name'] == item['player_name']:
                        # log('重复集结,{}'.format(item))
                        pass
                    else:
                        log('更新集结信息,{}'.format(item))
                        gathering[identify] = item
            else:
                break
                 
        if not found:
            # log('没有新增集结') 
            pass
            
    except Exception as e:
        traceback.print_exc()
        log(e)
    
    gathering_count = {}
    for gethering_item in gathering.values():
        player_name = gethering_item['player_name']
        if player_name in gathering_count:
            item = gathering_count[player_name]
            item['count'] = item['count'] + 1
            gathering_count[player_name] = item
        else:
            item = {'player_xy':gethering_item['player_xy'], 'count':1}
            gathering_count[player_name] = item
    # log('统计寨子, 开始统计时间 {}, {}'.format(monitor_count['start_time'], gathering_count))   
        
    try:        
        if gathering is not None:
            with open(filepath, 'w', encoding='utf-8') as wf:
                monitor_count['gathering'] = gathering
                monitor_count['gathering_count'] = gathering_count
                line = json.dumps(monitor_count, ensure_ascii=False)
                wf.writelines([line])
                wf.truncate()
          
    except BaseException as e:
        log(e)  
    return gathering
            
def find_player(bot, task, server, expected_pos):
    log('寻找玩家', server, expected_pos)
    task.tap((300, 100))
    task.back_to_map_gui(help=False)
    log('打开坐标搜索界面')
    
    _, _, bookmark_pos = bot.gui.check_any_gray(
        ImagePathAndProps.SEARCH_BOOKMARK_IMAGE_PATH.value
    )
    task.tap((bookmark_pos[0] - 30, 6))
    
    imsch = bot.gui.get_curr_device_screen_img_cv()
    _, _, server_pos = bot.gui.check_any_gray(
        ImagePathAndProps.SEARCH_SERVER_IMAGE_PATH.value,
        imsch=imsch
    )
    log('输入服务器', server)
    task.text(server_pos[0] - 25, server_pos[1] + 10, server, 1)
    
    log('输入X坐标', expected_pos[0])
    x_pos = (590, 131)
    task.text(x_pos[0], x_pos[1], expected_pos[0], 1, False)
    
    log('输入Y坐标', expected_pos[1])
    y_pos = (750, 131)
    task.text(y_pos[0], y_pos[1],  expected_pos[1], 1, False)
    
    _, _, search_pos = bot.gui.check_any_gray(
        ImagePathAndProps.SEARCH_BUTTON_IMAGE_PATH.value,
        imsch=imsch
    )
    # snapshot(bot, img=imsch)
    log('点击搜索')
    task.tap(search_pos, 8)
    
    log('点击城堡')
    player_name = ""
    
    pos_items = [
        [630, 360], [615, 360], [645, 360],
        [630, 350], [615, 350], [645, 350],
        [630, 340], [615, 340], [645, 340]
        ]
    
    for pos in pos_items:
        task.tap(pos)
        # task.tap((615 + i * 10, 335 + i * 5))
        imsch = bot.gui.get_curr_device_screen_img_cv()
        _, _, player_title_pos = bot.gui.check_any(
            ImagePathAndProps.TITLE_BUTTON_PATH.value,
            imsch=imsch
        )
        
        if player_title_pos:
            # log('寻找玩家成功', server, expected_pos)
            box = (int(player_title_pos[0]) + 124, int(player_title_pos[1]) + 42, int(player_title_pos[0]) + 124 + 230, int(player_title_pos[1]) + 42 + 36)
            player_name = bot.gui.player_name(box, imsch)
            log('寻找玩家成功', server, expected_pos, player_name, box)
            x0, y0, x1, y1 = box
            img = imsch[y0:y1, x0:x1]
            snapshot(bot, img=img)
            task.tap(player_title_pos, 2 * bot.config.tapSleep)
            return True, player_name

    log('寻找玩家失败', server, expected_pos)
    return False, None
            
def finish_title(bot, task, server, title_item, expected_pos, player_name):
    title_expected_pos = title_item['title_check_pos']
    log('选择头衔', title_item['name'], expected_pos)
    
    imsch = bot.gui.get_curr_device_screen_img_cv()
    _, _, title_check_pos = bot.gui.check_any(
        ImagePathAndProps.TITLE_CHECK_BUTTON_PATH.value,
        imsch=imsch
    )
    
    # log('title_check_pos', title_check_pos, 'title_expected_pos', title_expected_pos)
    if title_check_pos is None or abs(title_check_pos[0]-title_expected_pos[0]) > 30:
        task.tap(title_expected_pos)
        # time.sleep(30) 
    else:
        log('已经拥有头衔', title_item['name'], expected_pos)
        
    _, _, ok_pos = bot.gui.check_any(
        ImagePathAndProps.LOST_CANYON_OK_IMAGE_PATH.value,
        imsch=imsch
    )
    task.tap(ok_pos)
    log('发放头衔成功', title_item['name'], server, expected_pos, player_name)
    # snapshot(bot)
    
    return True

def load_run_config(prefix):
    file_path = 'run/{}.json'.format(prefix)
    try:
        with open(file_path, encoding='utf-8') as f:
            config_dict = json.load(f)
            config = RunConfig(config_dict)
    except Exception as e:
        traceback.print_exc()
        config = RunConfig()
    return config

def write_run_config(config, prefix):
    file_path = 'run/{}.json'.format(prefix)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(config.__dict__, f, indent=2, ensure_ascii=False)   
        
def snapshot(bot, name='screencap', img=None):
    if img is None:
        # img = bot.gui.get_curr_device_screen_img().resize((640, 360))
        img = bot.gui.get_curr_device_screen_img_cv()
    if img is not None:
        # cv2.resize(img, (360, 640), interpolation=cv2.INTER_LINEAR)
        output_path = 'web/{}.jpg'.format(name)
        # img = img.convert('RGB')
        # img.save('web/{}.jpg'.format(name))
        cv2.imwrite(output_path, img)
    return
            
def start_work(bot, name):
    def on_snashot_update():
        # snapshot(bot, name, img)
        return
    
    bot.config = load_bot_config(name)
    bot.building_pos = load_building_pos(name)
    bot.snashot_update_event = on_snashot_update
    bot.start(bot.do_task)
    # snapshot(bot, name)
    return True
 
def change_player(task, bot, device_name, i):
    return False
    # if i == 1:
    #     task = Player1(bot)
    #     bot.start(task.do)
    # elif i == 2:
    #     task = Player2(bot)
    #     bot.start(task.do)    

def get_bot(device_name = 'request_title'):
    adb.bridge = adb.enable_adb('127.0.0.1', 5037)
    name = None
    ip = None
    port = None
    nickname = None
    devices_config = load_device_config()
    for config in devices_config:
        name = config.get('name', 'None')
        if device_name == name:
            nickname = config.get('nickname', 'None')
            ip = config['ip']
            port = config['port']
            break
    
    device = adb.bridge.get_device(ip, port)
    if device is None:
        log('没有对应配置, {}:{}', ip, port)
        return None
    device.name = name
    device.nickname = nickname
    device.save_file_prefix = name
    log('device:', device)
    bot = Bot(device)
    
    return bot
        
def api(args, bot=None):
    run_type = 'request_title'
    if (args.run_type is not None) and (len(run_type) > 0):
        run_type = args.run_type
        
    if run_type == 'get_dead_info':
        get_dead_info(args.api_file)
        return False, ""    
    else:
        adb.bridge = adb.enable_adb('127.0.0.1', 5037)
        if bot is None:
            bot = get_bot(args.device_name)
            
        bot.config = load_bot_config(bot.device.name)    
        task = Task(bot)
        
        if run_type == 'request_monitor':
            monitor(bot, task, args.api_monitor_file)
            return False, ""
        elif run_type == 'ranking':
            ranking(bot, args.api_file)
            return False, ""
        elif run_type == 'get_dead_info':
            get_dead_info(args.api_file)
            return False, ""
        elif run_type == 'request_title':
            title_item = RunConfig.TITLE_ITEMS[args.title]
            if title_item is not None:
                log('申请头衔', title_item['name'])
                expected_pos = (args.x, args.y)
                found, player_name = find_player(bot, task, args.server, expected_pos)
                if found:
                    return finish_title(bot, task, args.server, title_item, expected_pos, player_name), player_name
            return False, ""
        elif run_type == 'request_stop':
            try:
                config = load_run_config(bot.device.name)
                config.name = bot.device.name
                config.running = False;
                log('config', config)
                write_run_config(config, bot.device.name)
            
                log('停止打工', config.name)    
                bot.stop()
                task.stopRok()
                os.remove('run/{}.jpg'.format(bot.device.name))
                return True, ""
            except BaseException as e:
                log(e)   
            return False, ""
                
        elif run_type == 'request_bot':
            try:
                os.mkdir('run')
            except BaseException as e:
                if e.errno != errno.EEXIST:
                    print(e)
                    
            config = load_run_config(bot.device.name)
            config.name = bot.device.name
            config.running = True;
            log('config', config)
            write_run_config(config, bot.device.name)
            
            log('开始打工', config.name)
            config.diamond_add = 0
            start_work(bot, bot.device.name)
            
            while config.running:
                time.sleep(1)
                config = load_run_config(bot.device.name)
                
            config.diamond_add = bot.diamond_add
            write_run_config(config, bot.device.name)   
            log('打工结束', config.name)    
            bot.stop()
            
            file_path = 'run/{}.jpg'.format(bot.device.name)
            os.remove(file_path)
            return True, ""
        
        elif run_type == 'change_player':
            return change_player(task, bot, bot.device.name, args.player), ""
    
    return False, ""

def get_dead_info(input_path):
    img = cv2.imread(input_path)
    img = resize(img, (1280, 720), padding=False, fixScale=0)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_gray = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
    
    ocr = PaddleOCR(lang="ch", use_gpu=False, use_angle_cls=False, show_log=False)
    ocr_result = ocr.ocr(img_gray, cls=False, det=True)
    
    src_types = [
        {'name':'barracks',
         'path':ImagePathAndProps.DEAD_BARRACKS_IMG_PATH.value[0],
        },
        {'name':'siege',
         'path':ImagePathAndProps.DEAD_SIEGE_IMG_PATH.value[0],
        },
        {'name':'archery',
         'path':ImagePathAndProps.DEAD_ARCHERY_IMG_PATH.value[0],
        },
        {'name':'stable',
         'path':ImagePathAndProps.DEAD_STABLE_IMG_PATH.value[0],
        },
    ]
    
    result = {
        'barracks':{
            't4':0,
            't5':0,
        },
        'siege':{
            't4':0,
            't5':0,
        },
        'archery':{
            't4':0,
            't5':0,
        },
        'stable':{
            't4':0,
            't5':0,
        },
        }
    i=0
    for item in ocr_result[0]:
        rect = item[0]
        value = item[1][0].replace(',','').replace('.','')
        l = int(rect[0][0])
        t = int(rect[0][1])
        r = int(rect[2][0])
        b = int(rect[2][1])
        if True:    
            # print(item)
            src = img[t:b, l:r]
            src_type_img = img[t-15:b+15, l-40:l+10]
            src_level_img = img[t-21:b-10, l-93:l-48]
            
            # src_level_img_gray = cv2.cvtColor(src_level_img, cv2.COLOR_BGR2GRAY)
            # src_level_img_bin = cv2.adaptiveThreshold(src_level_img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 1)
            # src_level_img_bin = cv2.cvtColor(src_level_img_bin, cv2.COLOR_GRAY2BGR)
            # src_level_img = cv2.bitwise_and(src_level_img, src_level_img_bin)
            
            src_hsv = cv2.cvtColor(src_level_img, cv2.COLOR_BGR2HSV)
            pmin=(125, 43, 46)
            pmax=(155, 255, 255)
            img_purple = cv2.inRange(src_hsv, pmin, pmax)
            _, img_purple = cv2.threshold(img_purple, 0, 1, cv2.THRESH_BINARY)
            radio_purple = np.sum(img_purple) / (img_purple.shape[0] * img_purple.shape[1])    
            # print('shape purple', img_purple.shape, np.sum(img_purple), radio_purple)
            
            ymin=(11, 43, 46)
            ymax=(25, 255, 255)
            img_orange = cv2.inRange(src_hsv, ymin, ymax)
            _, img_orange = cv2.threshold(img_orange, 0, 1, cv2.THRESH_BINARY)
            radio_orange = np.sum(img_orange) / (img_orange.shape[0] * img_orange.shape[1])
            # print('shape img_orange', img_orange.shape, np.sum(img_orange), radio_orange)          

            img_type = "unknow"
            if radio_purple > 0.2:
                img_type = 't4'
            elif radio_orange > 0.2:
                img_type = 't5'
            # if max(radio_purple, radio_orange) > 0.2:
            #     if radio_purple > radio_orange:
            #         img_type = 't4'
            #     else:
            #         img_type = 't5'
            # print('img_type', i, img_type) 
            
            # cv2.imwrite('/Users/max/Documents/Git/rok/script/capture/t_{}.png'.format(i), src, [int(cv2.IMWRITE_JPEG_QUALITY), 1])
            # cv2.imwrite('/Users/max/Documents/Git/rok/script/capture/t_type_{}.png'.format(i), src_type_img, [int(cv2.IMWRITE_JPEG_QUALITY), 1])
            # cv2.imwrite('/Users/max/Documents/Git/rok/script/capture/t_level_{}.png'.format(i), src_level_img, [int(cv2.IMWRITE_JPEG_QUALITY), 1])
            # cv2.imwrite('/Users/max/Documents/Git/rok/script/capture/t_orange_{}.png'.format(i), img_orange, [int(cv2.IMWRITE_JPEG_QUALITY), 1])
            # cv2.imwrite('/Users/max/Documents/Git/rok/script/capture/t_purple_{}.png'.format(i), img_purple, [int(cv2.IMWRITE_JPEG_QUALITY), 1])
            
            for src_type in src_types:
                src_img = cv2.imread(src_type['path'])
                try:
                    src_type_result = aircv.find_template(src_img, src_type_img, 0.8, rgb=True)
                    if src_type_result is not None:
                        if img_type in result[src_type['name']].keys():
                            result[src_type['name']][img_type] = int(value)
                            break
                except Exception as e:
                    traceback.print_exc()
            i=i+1
    result = json.dumps(result, ensure_ascii=False)
    print(result)
    return 