from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
import traceback

from tasks.constants import TaskName


class ClaimQuests(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.ALLIANCE):
        super().set_text(title='Claim Quest and Daily Objective', remove=True)
        try:
            super().back_to_home_gui()
            super().tap((45, 170), 5)

            quests_tap_pos = (100, 180)
            daily_objectives_tap_pos = (100, 320)

            super().set_text(insert='Claim quest')
            super().tap(quests_tap_pos)
            for i in range(20):
                _, _, claim_btn_pos = self.gui.check_any(ImagePathAndProps.QUEST_CLAIM_BUTTON_IMAGE_PATH.value)
                if claim_btn_pos is None:
                    break
                super().set_text(insert='Tap claim button at ({}, {})'.format(x, y))
                super().tap(claim_btn_pos)

            super().set_text(insert='Claim Daily Objective')
            super().tap(daily_objectives_tap_pos)
            for i in range(20):
                _, _, claim_btn_pos = self.gui.check_any(ImagePathAndProps.QUEST_CLAIM_BUTTON_IMAGE_PATH.value)
                if claim_btn_pos is None:
                    break
                super().set_text(insert='Tap claim button at ({}, {})'.format(x, y))
                super().tap(claim_btn_pos)

            super().set_text(insert='Tap all chest')
            # chest position
            for pos in [(355, 200), (530, 200), (710, 200), (885, 200), (1050, 200)]:
                super().tap(pos)
        except Exception as e:
            traceback.print_exc()
            return TaskName.CLAIM_QUEST
        return next_task
