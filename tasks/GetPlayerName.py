from tasks.Task import Task
from tasks.constants import TaskName
from filepath.file_relative_paths import ImagePathAndProps

class GetPlayerName(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.BREAK):
        self.set_text(title='获取玩家信息', remove=True)
        self.back_to_map_gui()
        self.set_text(insert='打开玩家信息')
        # 打开设置
        self.tap((25, 25))
        self.bot.snashot_update_event()
        player_name = self.bot.gui.player_name()
        self.set_text(insert='读取玩家名字, {}'.format(player_name))
        self.set_text(name=player_name)
        self.bot.player_name = player_name
        return next_task
