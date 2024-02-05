import adb
import time

from bot_related.bot import Bot
from tasks.constants import BuildingNames
from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
from utils import log

def find_player(bot, task, server, expected_pos):
    log('寻找玩家', expected_pos)
    # task.back_to_home_gui()
    task.back_to_map_gui()
    task.double_tap(640, 360)
    _, _, pos = bot.gui.check_any(
        ImagePathAndProps.SEARCH_ICON_SMALL_IMAGE_PATH.value
    )
    task.tap(pos[0], pos[1], 1)
    
    _, _, server_pos = bot.gui.check_any(
        ImagePathAndProps.SEARCH_SERVER_IMAGE_PATH.value
    )
    task.text(server_pos[0] - 25, server_pos[1] + 10, server)
    
    _, _, x_pos = bot.gui.check_any(
        ImagePathAndProps.SEARCH_X_IMAGE_PATH.value
    )
    task.text(x_pos[0] + 25, x_pos[1] + 10, expected_pos[0])
    
    _, _, y_pos = bot.gui.check_any(
        ImagePathAndProps.SEARCH_Y_IMAGE_PATH.value
    )
    task.text(y_pos[0] + 25, y_pos[1] + 10,  expected_pos[1])
    
    _, _, search_pos = bot.gui.check_any(
        ImagePathAndProps.SEARCH_BUTTON_IMAGE_PATH.value
    )
    task.tap(search_pos[0], search_pos[1], 10)
    
    task.tap(640, 360)
    _, _, player_pos = bot.gui.check_any(
        ImagePathAndProps.TITLE_BUTTON_PATH.value
    )
    task.tap(player_pos[0], player_pos[1])
    log('寻找玩家,成功', player_pos)
    
def judge(bot, task, server, expected_pos):
    title_expected_pos = (280, 380)
    log('申请头衔,法官', expected_pos)
    find_player(bot, task, server, expected_pos)
    finish_title(bot, task, title_expected_pos)
    
def train(bot, task, server, expected_pos):
    title_expected_pos = (505, 380)
    log('申请头衔,公爵', expected_pos)
    find_player(bot, task, server, expected_pos)
    finish_title(bot, task, title_expected_pos)
    
def architect(bot, task, server, expected_pos):
    title_expected_pos = (735, 380)
    log('申请头衔,大建筑师', expected_pos)
    find_player(bot, task, server, expected_pos)
    finish_title(bot, task, title_expected_pos)

def scientist(bot, task, server, expected_pos):
    title_expected_pos = (965, 380)
    log('申请头衔,大科学家', expected_pos)
    find_player(bot, task, server, expected_pos)
    finish_title(bot, task, title_expected_pos)      
            
def finish_title(bot, task, title_expected_pos):
    log('发放头衔', title_expected_pos)
    _, _, title_check_pos = bot.gui.check_any(
        ImagePathAndProps.TITLE_CHECK_BUTTON_PATH.value
    )
    log('title_check_pos', title_check_pos, 'title_expected_pos', title_expected_pos)
    if title_check_pos is None or abs(title_check_pos[0]-title_expected_pos[0]) > 30:
        log('发放头衔,成功', title_expected_pos)
        task.tap(title_expected_pos[0], title_expected_pos[1]) 
    else:
        log('头衔已经发放,跳过', title_check_pos)
    _, _, ok_pos = bot.gui.check_any(
        ImagePathAndProps.LOST_CANYON_OK_IMAGE_PATH.value
    )
    task.tap(ok_pos[0], ok_pos[1])     
    
def run_api(args):
    print(args)
    adb.bridge = adb.enable_adb('192.168.88.140', 9037)
    device = adb.bridge.get_device('192.168.88.140', 9999)
    bot = Bot(device)
    task = Task(bot)
    expected_pos = (args.x, args.y)
    if args.title == 'train':
        train(bot, task, args.server, expected_pos)
    elif args.title == 'judge':
        judge(bot, task, args.server, expected_pos)
    elif args.title == 'architect':
        architect(bot, task, args.server, expected_pos)
    elif args.title == 'scientist':
        scientist(bot, task, args.server, expected_pos)