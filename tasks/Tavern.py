import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames
from tasks.constants import TaskName
from tasks.Task import Task


class Tavern(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.TRAINING):
        super().set_text(title='酒馆', remove=True)
        super().set_text(insert='回到城市')
        super().back_to_home_gui()
        super().home_gui_full_view()
        tavern_pos = self.bot.building_pos[BuildingNames.TAVERN.value]

        # tap tavern building
        super().set_text(insert='打开酒馆({})'.format(tavern_pos))
        super().tap(tavern_pos)
        _, _, tavern_btn_pos = self.gui.check_any(ImagePathAndProps.TAVERN_BUTTON_BUTTON_IMAGE_PATH.value)
        if tavern_btn_pos is None:
            return next_task
        super().tap(tavern_btn_pos, 4)
        for i in range(20):
            _, _, open_btn_pos = self.gui.check_any(ImagePathAndProps.CHEST_OPEN_BUTTON_IMAGE_PATH.value)
            if open_btn_pos is None:
                return next_task
            super().set_text(insert="打开免费宝箱({})".format(open_btn_pos))
            super().tap(open_btn_pos, 4)
            _, _, confirm_btn_pos = self.gui.check_any(ImagePathAndProps.CHEST_CONFIRM_BUTTON_IMAGE_PATH.value)
            if confirm_btn_pos is None:
                return next_task
            super().tap(confirm_btn_pos, 4)
        return next_task
