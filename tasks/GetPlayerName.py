from tasks.Task import Task
from tasks.constants import TaskName
from filepath.file_relative_paths import ImagePathAndProps

import re
import time

class GetPlayerName(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.BREAK):
        self.set_text(title='获取玩家信息', remove=True)
        self.back_to_map_gui()
        self.set_text(insert='打开个人中心')
        # 打开个人中心
        self.tap((25, 25), 2 * self.bot.config.tapSleep)
        self.set_text(insert='读取玩家名字')
        for i in range(3):
            player_name = self.bot.gui.player_name()
            player_name = re.sub('^[^a-zA-Z0-9_\u4e00-\u9fa5]+$', '', player_name)
            if len(player_name) > 0:
                break
            time.sleep(self.bot.config.tapSleep)
        self.set_text(insert='读取到玩家名字, {}'.format(player_name))
        # self.set_text(name=player_name)
        self.device.nickname = player_name
        self.bot.snashot_update_event()
        self.bot.config_update_event(config=self.bot.config, prefix=self.device.save_file_prefix)
        return next_task
