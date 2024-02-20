from tasks.Task import Task
import traceback

from tasks.constants import TaskName, BuildingNames


class Collecting(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.CLAIM_QUEST):
        super().set_text(title='收集城内资源/治疗部队/帮助盟友', remove=True)
        super().set_text(insert='回到城市')

        try:
            super().back_to_home_gui()
            super().home_gui_full_view()

            super().menu_should_open(False)

            pos_e = (105, 125)
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
                x, y = self.bot.building_pos[name]
                self.set_text(insert='tap {} at position ({},{})'.format(name, x, y))
                self.tap(self.bot.building_pos[name])
                self.tap(pos_e)

        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task
