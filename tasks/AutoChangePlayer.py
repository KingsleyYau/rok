from tasks.Task import Task
from tasks.constants import TaskName
from filepath.file_relative_paths import ImagePathAndProps
import time

class AutoChangePlayer(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.BREAK):
        self.set_text(title='自动切换玩家', remove=True)
        self.back_to_map_gui()
        # self.back_to_home_gui()
        # 打开个人中心
        self.set_text(insert='打开个人中心')
        self.tap((50, 50), 2 * self.bot.config.tapSleep)
        # 打开设置
        self.set_text(insert='打开设置')
        self.tap((990, 570), 2 * self.bot.config.tapSleep)
        # 角色管理
        self.set_text(insert='打开角色管理')
        self.tap((560, 380), 2 * self.bot.config.tapSleep)
        
        # 切换角色
        for i in range(0, self.bot.config.playerCount):
            playerIndex = (self.bot.config.playerIndex + 1) % self.bot.config.playerCount
            x = playerIndex % 2 + 1
            y = playerIndex // 2
            pos = ((400 * x, 230 + 110 * y))
            self.set_text(insert='当前角色 {}, 目标角色 {}, {}'.format(self.bot.config.playerIndex, playerIndex, pos))
            for j in range(0, 3):
                self.tap(pos, 2 * self.bot.config.tapSleep)
                _, _, yes_pos = self.bot.gui.check_any(ImagePathAndProps.YES_BUTTON_PATH.value)
                if yes_pos is not None:
                    self.set_text(insert='切换角色, {} => {}'.format(self.bot.config.playerIndex, playerIndex))
                    self.tap(yes_pos)
                    
                    _, _, contact_us_pos = self.bot.gui.check_any(ImagePathAndProps.CONTACT_US_BUTTON_PATH.value)
                    if contact_us_pos is None:
                        self.bot.config.playerIndex = playerIndex
                        self.set_text(insert='切换角色, {}, 成功, 重启'.format(playerIndex))
                        self.device.nickname = ""
                        self.bot.config_update_event(config=self.bot.config, prefix=self.device.save_file_prefix)
                        time.sleep(self.bot.config.welcomeSleep)
                        return next_task
                    else:
                        self.set_text(insert='目标角色被封, {}, 跳过'.format(playerIndex))
                        self.bot.config.playerIndex = playerIndex
                        self.back()
                        self.back()
                        break
                else:
                    self.set_text(insert='第{}次, 没有发现确定按钮, 目标角色, {}'.format(j+1, playerIndex))
                    self.check_common_button()
                    
            self.set_text(insert='没有发现确定按钮, 目标角色, {}, 跳过'.format(playerIndex))        
            self.bot.config.playerIndex = playerIndex
            
        return next_task
