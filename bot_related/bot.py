import threading

# import traceback
from threading import Lock
import time
import adb
from tasks.Items import Items
from tasks.LostCanyon import LostCanyon
from tasks.Task import *
from bot_related.bot_config import BotConfig
from bot_related.device_gui_detector import GuiDetector, GuiName

from filepath.file_relative_paths import (
    ImagePathAndProps,
    VERIFICATION_CLOSE_REFRESH_OK,
    VERIFICATION_VERIFY_TITLE,
)
from tasks.Alliance import Alliance
from tasks.Barbarians import Barbarians
from tasks.Break import Break
from tasks.ClaimQuests import ClaimQuests
from tasks.ClaimVip import ClaimVip
from tasks.Collecting import Collecting
from tasks.GatherResource import GatherResource
from tasks.LocateBuildings import LocateBuilding
from tasks.Materials import Materials
from tasks.Restart import Restart
from tasks.Scout import Scout
from tasks.ScreenShot import ScreenShot
from tasks.Tavern import Tavern
from tasks.Training import Training
from tasks.MysteryMerchant import MysteryMerchant
from tasks.SunsetCanyon import SunsetCanyon
from tasks.GatherDiamond import GatherDiamond
from tasks.Festival import Festival
from tasks.AutoChangePlayer import AutoChangePlayer
from tasks.ChangePlayer import ChangePlayer
from tasks.GetPlayerName import GetPlayerName
from tasks.UpgradeBuildings import UpgradeBuildings
from tasks.AutoFillTroop import AutoFillTroop
from tasks.constants import TaskName
from utils import stop_thread
import random

DEFAULT_RESOLUTION = {"height": 720, "width": 1280}

class Bot:
    def __init__(self, device, config={}):
        self.daemon_thread = None
        self.curr_thread = None
        self.device = device
        self.gui = GuiDetector(device)
        self.text_update_event = lambda v: v
        self.text = {"name":"", "title": "", "text_list": []}

        self.building_pos_update_event = lambda **kw: kw
        self.config_update_event = lambda **kw: kw
        self.snashot_update_event = lambda **kw: kw

        # get screen resolution
        str = device.shell("wm size").replace("\n", "")
        height, width = list(map(int, str[(str.find(":") + 1) : len(str)].split("x")))
        self.resolution = {"height": height, "width": width}

        self.building_pos = {}

        self.config = BotConfig(config)
        self.curr_task = TaskName.BREAK

        self.task = Task(self)

        # tasks
        self.restart_task = Restart(self)
        self.break_task = Break(self)
        self.mystery_merchant_task = MysteryMerchant(self)
        self.alliance_task = Alliance(self)
        self.barbarians_task = Barbarians(self)
        self.claim_quests_task = ClaimQuests(self)
        self.claim_vip_task = ClaimVip(self)
        self.collecting_task = Collecting(self)
        self.gather_resource_task = GatherResource(self)
        self.locate_building_task = LocateBuilding(self)
        self.materials_task = Materials(self)
        self.scout_task = Scout(self)
        self.tavern_task = Tavern(self)
        self.training = Training(self)
        self.sunset_canyon = SunsetCanyon(self)
        self.lost_canyon = LostCanyon(self)
        self.items_task = Items(self)
        self.gather_diamond_task = GatherDiamond(self)
        self.festival_task = Festival(self)
        self.upgradeBuildings = UpgradeBuildings(self)
        self.autoFillTroop = AutoFillTroop(self)
        # Other task
        self.screen_shot_task = ScreenShot(self)
        self.auto_change_task = AutoChangePlayer(self)
        self.change_player_task = ChangePlayer(self)
        self.get_player_name_task = GetPlayerName(self)
        
        self.player_round_count = 0
        self.round_count = 0
        self.diamond = 0
        self.diamond_add = 0
        self.player_name = ""

    def start(self, fn):
        if self.daemon_thread is not None and self.daemon_thread.is_alive():
            stop_thread(self.daemon_thread)
            print("daemon_thread: {}", self.daemon_thread.is_alive())

        if self.curr_thread is not None and self.curr_thread.is_alive():
            stop_thread(self.curr_thread)
            print("curr_thread: {}", self.curr_thread.is_alive())
        self.daemon(fn)

    def stop(self):
        if self.daemon_thread is not None and self.daemon_thread.is_alive():
            stop_thread(self.daemon_thread)
            print("daemon_thread: {}", self.daemon_thread.is_alive())

        if self.curr_thread is not None and self.curr_thread.is_alive():
            stop_thread(self.curr_thread)
            print("curr_thread: {}", self.curr_thread.is_alive())
        self.player_name = ""

    def get_city_image(self):
        return self.screen_shot_task.do_city_screen()

    def do_task(self, curr_task=TaskName.COLLECTING):
        random_tasks = [
            [self.mystery_merchant_task, "enableMysteryMerchant"],
            [self.alliance_task, "allianceAction", "allianceDoRound"],
            [self.barbarians_task, "attackBarbarians"],
            [self.claim_quests_task, "claimQuests", "questDoRound"],
            [self.claim_vip_task, "enableVipClaimChest", "vipDoRound"],
            [self.collecting_task, "enableCollecting"],
            [self.materials_task, "enableMaterialProduce", "materialDoRound"],
            [self.scout_task, "enableScout"],
            [self.tavern_task, "enableTavern"],
            [self.training, "enableTraining", "trainingDoRound"],
            [self.sunset_canyon, "enableSunsetCanyon"],
            [self.lost_canyon, "enableLostCanyon"],
            [self.items_task, "useItems"],
            [self.festival_task, "enableFestival"],
            [self.upgradeBuildings, "enableUpgradeBuilding"],
        ]
        
        priority_tasks = [
            [self.autoFillTroop, "enableAutoFillTroop"],
            [self.gather_diamond_task, "gatherDiamond"],
            [self.gather_resource_task, "gatherResource"],
        ]
        
        try:
            if self.config.autoChangePlayer:
                curr_task = self.change_player_task.do()
        except Exception as e:
            traceback.print_exc()
            nickname = '{}-{}-{}'.format(self.device.save_file_prefix, self.device.nickname, self.device.serial) if len(self.device.nickname)>0 else '{}-{}'.format(self.device.save_file_prefix, self.device.serial)
            self.task.set_text(insert="try to reconect {}".format(nickname))
            adb.bridge.reconnect(self.device)
            time.sleep(10)

        if self.building_pos is None:
            curr_task = TaskName.INIT_BUILDING_POS
        else:
            self.config.hasBuildingPos = True

        while True:
            # Check verification before every task
            try:
                hour = time.strftime("%H", time.localtime())
                if int(hour) >= 11 and int(hour) < 6:
                    device_log(self.device, "休息时间...")
                    if self.task.isRoKRunning():
                        self.task.stopRok()
                    time.sleep(300)
                    continue
            
                self.task.get_curr_gui_name()

                random.shuffle(random_tasks)
                # tasks = priority_tasks + random_tasks
                tasks = random_tasks
                        
                player_round_count = self.round_count
                self.round_count = self.round_count + 1
                if self.config.autoChangePlayer:
                    player_round_count = player_round_count // self.config.playerCount
                
                if len(self.device.nickname) == 0:
                    self.get_player_name_task.do(TaskName.COLLECTING)
    
                # init building position if need
                if (
                    not self.config.hasBuildingPos
                    or curr_task == TaskName.INIT_BUILDING_POS
                ):
                    self.task.set_text(
                        insert="building positions not saved - recalculating"
                    )
                    curr_task = self.locate_building_task.do(next_task=TaskName.COLLECTING)
    
                for task in tasks:
                    if len(task) == 2:
                        if getattr(self.config, task[1]):
                            curr_task = task[0].do()
                    else:
                        if (
                            getattr(self.config, task[1])
                            and player_round_count % getattr(self.config, task[2]) == 0
                        ):
                            curr_task = task[0].do()
    
                if self.config.enableStop:
                    curr_task = self.restart_task.do()
                else:
                    if (self.config.enableBreak and player_round_count % self.config.breakDoRound == 0):
                        breakTime = int(random.uniform(int(self.config.breakTime * 3 / 4), self.config.breakTime))
                        progress_time = max(breakTime // 10, 1)
                        start = time.time()
                        now = start
                        last = 0
                        diff = self.config.checkTaskTime
                        # for i in range(breakTime):
                        
                        self.player_round_count = player_round_count
                        self.break_task.set_text(title='休息', remove=True)
                        self.break_task.set_text(insert='开始休息 {} seconds'.format(breakTime))
                        
                        self.break_task.back_to_map_gui()
                        imsch = self.gui.get_curr_device_screen_img_cv()
                        download_pos = self.gui.check_any(ImagePathAndProps.DOWNLOAD_IMG_PATH.value, imsch=imsch)[2]
                        if download_pos is not None:
                            self.break_task.set_text(insert='发现下载倒计时, 点击'.format(download_pos))
                            self.break_task.tap(download_pos)
                            imsch = self.gui.get_curr_device_screen_img_cv()
                        download_button_pos = self.gui.check_any(ImagePathAndProps.DOWNLOAD_BUTTON_PATH.value, imsch=imsch)[2]
                        if download_button_pos is not None:
                            self.break_task.set_text(insert='发现下载按钮, 点击'.format(download_button_pos))
                            self.break_task.tap(download_button_pos)
                            
                        while now - start <= breakTime:
                            self.break_task.back_to_map_gui()
                            if now - last > diff:
                                full_load, cur, total = self.gui.troop_already_full()
                                self.break_task.set_text(insert='已经休息 {}/{} seconds, 队列数量:{}/{}'.format(int(now - start), breakTime, cur, total))
                                self.snashot_update_event()
                                if not full_load:
                                    for task in priority_tasks:
                                        if len(task) == 2:
                                            if getattr(self.config, task[1]):
                                                task[0].do()
                                    self.break_task.back_to_map_gui()
                                    full_load, cur, total = self.gui.troop_already_full()
                                    self.snashot_update_event()
                                now = time.time()
                                last = now
                                self.break_task.set_text(title='休息')
                                self.break_task.set_text(insert='继续休息 {}/{} seconds, 队列数量:{}/{}'.format(int(now - start), breakTime, cur, total))
                            time.sleep(60)
                            now = time.time()
                        self.break_task.set_text(insert='结束休息 {}/{} seconds'.format(int(now - start), breakTime))  
                                              
                        if self.config.terminate:
                            self.break_task.set_text(insert='关闭ROK')
                            self.stopRok()
                            self.snashot_update_event()
                              
                        # curr_task = self.break_task.do()
                        if self.config.autoChangePlayer:
                            curr_task = self.auto_change_task.do()
                    else:
                        curr_task = self.break_task.do_no_wait()
                        curr_task = self.restart_task.do() 
                
            except Exception as e:
                traceback.print_exc()
                nickname = '{}-{}-{}'.format(self.device.save_file_prefix, self.device.nickname, self.device.serial) if len(self.device.nickname)>0 else '{}-{}'.format(self.device.save_file_prefix, self.device.serial)
                self.task.set_text(insert="try to reconect {}".format(nickname))
                adb.bridge.reconnect(self.device)
                time.sleep(10)
        return

    def daemon(self, fn):
        def run():
            main_thread = threading.Thread(target=fn)
            self.curr_thread = main_thread
            main_thread.start()

            while True:
                if self.daemon_thread is None or not main_thread.is_alive():
                    break
                time.sleep(60)
                found, _, pos = self.gui.check_any(
                    ImagePathAndProps.VERIFICATION_VERIFY_TITLE_IMAGE_PATH.value
                )
                if found:
                    found, _, pos = self.gui.check_any(
                        ImagePathAndProps.VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH.value
                    )
                    if not found:
                        stop_thread(main_thread)
                        time.sleep(1)
                        main_thread = threading.Thread(target=fn)
                        self.curr_thread = main_thread
                        main_thread.start()

        daemon_thread = threading.Thread(target=run)
        daemon_thread.start()
        self.daemon_thread = daemon_thread
