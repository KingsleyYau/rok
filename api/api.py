import adb
import time
import cv2
import os, errno
import json
import traceback

from gui.creator import load_bot_config
from gui.creator import load_building_pos
from gui.creator import write_device_config, load_device_config
from bot_related.bot import Bot
from tasks.constants import BuildingNames
from filepath.file_relative_paths import ImagePathAndProps
from utils import log
from api.run_config import RunConfig

from tasks.Task import Task

def find_player(bot, task, server, expected_pos):
    log('寻找玩家', server, expected_pos)
    task.back_to_map_gui()
    task.double_tap((400, 400))
    # _, _, pos = bot.gui.check_any_gray(
    #     ImagePathAndProps.SEARCH_ICON_SMALL_IMAGE_PATH.value
    # )
    # task.tap(pos[0])
    log('打开坐标搜索')
    task.tap((435, 6))
    
    _, _, server_pos = bot.gui.check_any_gray(
        ImagePathAndProps.SEARCH_SERVER_IMAGE_PATH.value
    )
    log('输入服务器', server)
    task.text(server_pos[0] - 25, server_pos[1] + 10, server)
    
    # _, _, x_pos = bot.gui.check_any_gray(
    #     ImagePathAndProps.SEARCH_X_IMAGE_PATH.value
    # )
    log('输入X坐标', expected_pos[0])
    x_pos = (590, 131)
    task.text(x_pos[0], x_pos[1], expected_pos[0])
    
    # _, _, y_pos = bot.gui.check_any_gray(
    #     ImagePathAndProps.SEARCH_Y_IMAGE_PATH.value
    # )
    log('输入Y坐标', expected_pos[1])
    y_pos = (750, 131)
    task.text(y_pos[0], y_pos[1],  expected_pos[1])
    
    _, _, search_pos = bot.gui.check_any_gray(
        ImagePathAndProps.SEARCH_BUTTON_IMAGE_PATH.value
    )
    log('点击搜索')
    task.tap(search_pos, 10)
    
    log('点击城堡')
    for i in range(2):
        task.tap((620, 340))
        _, _, player_pos = bot.gui.check_any(
            ImagePathAndProps.TITLE_BUTTON_PATH.value
        )
        if player_pos:
            task.tap(player_pos)
            return True

    log('寻找玩家失败', server, expected_pos)
    return False
            
def finish_title(bot, task, title_item):
    title_expected_pos = title_item['title_check_pos']
    log('选择头衔', title_item['name'])
    _, _, title_check_pos = bot.gui.check_any(
        ImagePathAndProps.TITLE_CHECK_BUTTON_PATH.value
    )
    log('title_check_pos', title_check_pos, 'title_expected_pos', title_expected_pos)
    if title_check_pos is None or abs(title_check_pos[0]-title_expected_pos[0]) > 30:
        task.tap(title_expected_pos)
        # time.sleep(30) 
    else:
        log('已经拥有头衔', title_item['name'])
    _, _, ok_pos = bot.gui.check_any(
        ImagePathAndProps.LOST_CANYON_OK_IMAGE_PATH.value
    )
    task.tap(ok_pos)
    log('发放头衔成功', title_item['name'])

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
        
def snapshot(bot, name):
    img = bot.gui.get_curr_device_screen_img().resize((480,270))
    if img is not None:
        try:
            os.mkdir('capture')
        except BaseException as e:
            if e.errno != errno.EEXIST:
                print(e)
        img = img.convert('RGB')
        img.save('run/{}.jpg'.format(name))
            
def start_work(bot, name):
    def on_snashot_update():
        snapshot(bot, name)
    
    bot.config = load_bot_config(name)
    bot.building_pos = load_building_pos(name)
    bot.snashot_update_event = on_snashot_update
    bot.start(bot.do_task)
    snapshot(bot, name)
    return True
 
def change_player(task, bot, device_name, i):
    return
    # if i == 1:
    #     task = Player1(bot)
    #     bot.start(task.do)
    # elif i == 2:
    #     task = Player2(bot)
    #     bot.start(task.do)    
                 
def run_api(args):
    log(args)
    adb.bridge = adb.enable_adb('127.0.0.1', 5037)
    
    device_name = 'request_title'
    if (args.device_name is not None) & (len(args.device_name) > 0):
        device_name = args.device_name
        
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
        return
    device.name = name
    device.nickname = nickname
    device.save_file_prefix = name
    log('device:', device)
            
    bot = Bot(device)
    task = Task(bot)
    expected_pos = (args.x, args.y)
    title_items = {
        'train':{'name':'公爵','title_check_pos':(505, 380)},
        'judge':{'name':'法官','title_check_pos':(280, 380)},
        'architect':{'name':'建筑师','title_check_pos':(735, 380)},
        'scientist':{'name':'科学家','title_check_pos':(965, 380)},
        }
    
    run_type = 'request_title'
    if (args.run_type is not None) and (len(run_type) > 0):
        run_type = args.run_type
    
    if run_type == 'request_title':
        title_item = title_items[args.title]
        if title_item is not None:
            log('申请头衔', title_item['name'])
            
            if find_player(bot, task, args.server, expected_pos):
                finish_title(bot, task, title_item)
    elif run_type == 'request_stop':
        try:
            config = load_run_config(device_name)
            config.name = device_name
            log('config', config)
            
            config.running = args.run;
            write_run_config(config, device_name)
        
            log('杀掉', config.name)    
            bot.stop()
            task.stopRok()
            os.remove('run/{}.jpg'.format(device_name))
        except BaseException as e:
            log(e)   
            
    elif run_type == 'request_bot':
        try:
            os.mkdir('run')
        except BaseException as e:
            if e.errno != errno.EEXIST:
                print(e)
                
        config = load_run_config(device_name)
        config.name = device_name
        log('config', config)
        
        if config.running and args.run:
            log('正在打工, 无需重新开始', config.name)
            return
        
        config.running = args.run;
        write_run_config(config, device_name)
        
        if config.running:
            log('开始打工', config.name)
            config.diamond_add = 0
            start_work(bot, device_name)
        
        while config.running:
            time.sleep(1)
            config = load_run_config(device_name)
        config.diamond_add = bot.diamond_add
        write_run_config(config, device_name)   
        log('停止打工', config.name)    
        bot.stop()
        
        file_path = 'run/{}.jpg'.format(device_name)
        os.remove(file_path)
        
    elif run_type == 'change_player':
        change_player(task, bot, device_name, args.player)