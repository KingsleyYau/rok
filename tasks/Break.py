import traceback

from tasks.Task import Task
from tasks.constants import TaskName

import time
import random

class Break(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.COLLECTING):
        try:
            super().set_text(title='Break', remove=True)
            # super().call_idle_back()
            super().back_to_map_gui()
            
            breakTime = int(random.uniform(self.bot.config.breakTime//2, self.bot.config.breakTime))
            super().set_text(insert='0/{} seconds'.format(breakTime))
            progress_time = max(breakTime // 20, 1)
            
            # stop game if config set true
            if self.bot.config.terminate:
                super().set_text(insert='关闭ROK')
                super().stopRok()
            
            count = 0
            for i in range(breakTime):
                time.sleep(1)
                count = count + 1
                if count % progress_time == 0:
                    full_load, cur, total = self.gui.troop_already_full()
                    super().set_text(replace='{}/{} seconds, 采集部队数量:{}/{}'.format(count, breakTime, cur, total), index=0)
            return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task

    def do_no_wait(self, next_task = TaskName.COLLECTING):
        try:
            super().call_idle_back()
            # super().heal_troops()
            return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task
