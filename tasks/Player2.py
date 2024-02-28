from tasks.Task import Task
from tasks.constants import TaskName
from filepath.file_relative_paths import ImagePathAndProps

class Player2(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.BREAK):
        self.set_text(title='Change Player2', remove=True)

        self.back_to_map_gui()
        # 打开设置
        self.tap((50, 50))
        self.tap((990, 570))
        # 角色管理
        self.tap((560, 380), 2 * self.bot.config.tapSleep)
        self.bot.snashot_update_event()
        # 切换角色
        self.tap((800, 240))
        _, _, yes_pos = self.bot.gui.check_any(ImagePathAndProps.YES_BUTTON_PATH.value)
        self.bot.snashot_update_event()
        if yes_pos is not None:
            self.tap(yes_pos)
            self.stopRok()
        else:
            self.set_text(insert='当前已是角色2, 无需切换')
            
        return next_task
