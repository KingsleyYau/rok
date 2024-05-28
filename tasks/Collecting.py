from tasks.Task import Task
from tasks.constants import TaskName, BuildingNames
import traceback
import random

class Collecting(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.CLAIM_QUEST):
        super().set_text(title='收集城内资源/治疗部队/帮助盟友', remove=True)
        try:
            super().back_to_home_gui()
            super().home_gui_full_view()

            super().menu_should_open(False)

            pos_free = (105, 125)
            #pos_free = (pos_e[0] + int(10 * (0.5 - random.random())), pos_e[1] + int(10 * (0.5 - random.random())))
            for name in [
                BuildingNames.BARRACKS.value,
                BuildingNames.ARCHERY_RANGE.value,
                BuildingNames.STABLE.value,
                BuildingNames.SIEGE_WORKSHOP.value,
                BuildingNames.FARM.value,
                BuildingNames.LUMBER_MILL.value,
                BuildingNames.QUARRY.value,
                BuildingNames.GOLDMINE.value,
                BuildingNames.ALLIANCE_CENTER.value
            ]:
                self.set_text(insert='{} at position {}'.format(name, self.bot.building_pos[name]))
                self.tap(self.bot.building_pos[name])
                self.tap(pos_free)
            self.bot.snashot_update_event()
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task
