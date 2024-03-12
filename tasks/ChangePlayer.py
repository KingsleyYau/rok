from tasks.Task import Task
from tasks.constants import TaskName
from filepath.file_relative_paths import ImagePathAndProps
import time

class ChangePlayer(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.BREAK):
        self.set_text(title='检查当前玩家', remove=True)
        self.back_to_map_gui()
        self.set_text(insert='打开个人中心')
        # 打开设置
        self.tap((50, 50), 2 * self.bot.config.tapSleep)
        self.bot.snashot_update_event()

        player_name = self.bot.gui.player_name()
        self.set_text(insert='读取玩家名字, {}'.format(player_name))
        # self.set_text(name=player_name)
        self.device.nickname = player_name
        self.bot.config_update_event(config=self.bot.config, prefix=self.device.save_file_prefix)
        
        # 打开设置
        self.set_text(insert='打开设置')
        self.tap((990, 570))
        # 角色管理 
        self.set_text(insert='打开角色管理')
        self.tap((560, 380), 2 * self.bot.config.tapSleep)
        self.bot.snashot_update_event()
        
        # 判断是否当前角色
        playerIndex = self.bot.config.playerIndex % self.bot.config.playerCount
        x = playerIndex % 2 + 1
        y = playerIndex // 2
        pos = ((400 * x, 230 + 110 * y))
        self.set_text(insert='目标玩家 {}, {}'.format(playerIndex, pos))
        self.tap(pos)
        _, _, yes_pos = self.bot.gui.check_any(ImagePathAndProps.YES_BUTTON_PATH.value)
        self.bot.snashot_update_event()
        if yes_pos is not None:
            self.tap(yes_pos)
            self.set_text(insert='切换角色, {}'.format(playerIndex))
            _, _, contact_us_pos = self.bot.gui.check_any(ImagePathAndProps.CONTACT_US_BUTTON_PATH.value)
            if contact_us_pos is not None:
                self.set_text(insert='该账号已被封, 无法切换')
                self.bot.stop()
            else:
                self.device.nickname = ""
                self.set_text(insert='切换角色, {}, 成功, 重启'.format(playerIndex))
                time.sleep(self.bot.config.restartSleep)
            self.bot.snashot_update_event()
        else:
            self.set_text(insert='已是当前角色, 无需切换')
            
        return next_task
