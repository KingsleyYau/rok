import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames
from tasks.constants import TaskName
from tasks.Task import Task


class Materials(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.TAVERN):
        try:
            super().set_text(title='生产材料', remove=True)

            icon_pos = [
                (765, 230),
                (860, 230),
                (950, 230),
                (1045, 230)
            ]
            icon_name = [
                '皮革',
                '矿石',
                '乌木',
                '兽骨',
            ]
            super().back_to_home_gui()
            super().home_gui_full_view()
            
            super().set_text(insert='打开铁匠铺')
            blacksmith_pos = self.bot.building_pos[BuildingNames.BLACKSMITH.value]
            super().tap(blacksmith_pos)
            self.bot.snashot_update_event()
            
            _, _, product_btn_pos = self.gui.check_any(ImagePathAndProps.MATERIALS_PRODUCTION_BUTTON_IMAGE_PATH.value)
            if product_btn_pos is None:
                return next_task
            super().tap(product_btn_pos)
            self.bot.snashot_update_event()
            list_amount = self.gui.materilal_amount_image_to_string()
            super().set_text(insert='皮革: {}, 矿石: {}, 乌木: {}, 兽骨: {}'.format(
                list_amount[0], list_amount[1], list_amount[2], list_amount[3])
            )
            # 不生产兽骨
            min = 0
            for i in range(len(list_amount) - 1):
                if list_amount[min] > list_amount[i]:
                    min = i
            super().set_text(insert='生产最少材料, {}'.format(icon_name[min]))
            for i in range(5):
                super().tap(icon_pos[min])
            self.bot.snashot_update_event()
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task