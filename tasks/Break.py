import traceback

from tasks.Task import Task
from tasks.constants import TaskName

import time


class Break(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.COLLECTING):
        try:
            super().set_text(title='Break', remove=True)
            # super().call_idle_back()
            super().back_to_map_gui()
            # super().home_gui_full_view()
            # super().heal_troops()
            
            res_names = [
                '玉米',
                '木头',
                '石头',
                '金矿',
                '砖石'
            ]
            result = self.gui.resource_amount_image_to_string()
            tips = "玉米: {}, 木头: {}, 石头: {}, 金矿: {}, 砖石: {}".format(result[0], result[1], result[2], result[3], result[4])
            self.set_text(insert=tips)
            
            super().set_text(insert='0/{} seconds'.format(self.bot.config.breakTime))
            progress_time = max(self.bot.config.breakTime // 100, 1)

            
            # stop game if config set true
            if self.bot.config.terminate:
                super().set_text(insert='关闭ROK')
                super().stopRok()
            self.bot.snashot_update_event()
            
            count = 0
            for i in range(self.bot.config.breakTime):
                time.sleep(1)
                count = count + 1
                if count % progress_time == 0:
                    super().set_text(replace='{}/{} seconds'.format(count, self.bot.config.breakTime), index=0)
                    self.bot.snashot_update_event()
            return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task

    def do_no_wait(self, next_task = TaskName.COLLECTING):
        try:
            super().call_idle_back()
            super().heal_troops()
            return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task
