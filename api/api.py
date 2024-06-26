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
    snapshot(bot, img=imsch)
    log('点击搜索')
    task.tap(search_pos, 8)
    
    log('点击城堡')
    player_name = ""
    for i in range(4):
        task.tap((615 + i * 10, 335 + i * 8))
        imsch = bot.gui.get_curr_device_screen_img_cv()
        _, _, player_title_pos = bot.gui.check_any(
            ImagePathAndProps.TITLE_BUTTON_PATH.value,
            imsch=imsch
        )
        
        if player_title_pos:
            # log('寻找玩家成功', server, expected_pos)
            box = (int(player_title_pos[0]) + 129, int(player_title_pos[1]) + 46, int(player_title_pos[0]) + 129 + 230, int(player_title_pos[1]) + 44 + 36)
            player_name = bot.gui.player_name(box, imsch)
            log('寻找玩家成功', server, expected_pos, player_name)
            snapshot(bot, img=imsch)
            task.tap(player_title_pos)
            return True, player_name

    log('寻找玩家失败', server, expected_pos)
    snapshot(bot, img=imsch)
    return False, None
            
def finish_title(bot, task, title_item, expected_pos, player_name):
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
    log('发放头衔成功', title_item['name'], expected_pos, player_name)
    snapshot(bot)
    
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
        cv2.resize(img, (360, 640), interpolation=cv2.INTER_LINEAR)
        output_path = 'web/{}.jpg'.format(name)
        # img = img.convert('RGB')
        # img.save('web/{}.jpg'.format(name))
        cv2.imwrite(output_path, img)
    return
            
def start_work(bot, name):
    def on_snashot_update(img):
        snapshot(bot, name, img)
        return
    
    bot.config = load_bot_config(name)
    bot.building_pos = load_building_pos(name)
    bot.snashot_update_event = on_snashot_update
    bot.start(bot.do_task)
    snapshot(bot, name)
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
        
def run_api(args, bot=None):
    adb.bridge = adb.enable_adb('127.0.0.1', 5037)
    
    device_name = 'request_title'
    if bot is None:
        bot = get_bot(args.device_name)
        
    task = Task(bot)
    expected_pos = (args.x, args.y)
    
    run_type = 'request_title'
    if (args.run_type is not None) and (len(run_type) > 0):
        run_type = args.run_type
    
    if run_type == 'request_title':
        title_item = RunConfig.TITLE_ITEMS[args.title]
        if title_item is not None:
            log('申请头衔', title_item['name'])
            found, player_name = find_player(bot, task, args.server, expected_pos)
            if found:
                return finish_title(bot, task, title_item, expected_pos, player_name), player_name
        return False, ""
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
                
        config = load_run_config(device_name)
        config.name = device_name
        log('config', config)
        
        if config.running and args.run:
            log('正在打工, 无需重新开始', config.name)
            return False, ""
        
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
        return True, ""
    
    elif run_type == 'change_player':
        return change_player(task, bot, device_name, args.player), ""
    
    return False, ""