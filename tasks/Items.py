import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task

from tasks.constants import TaskName


class Items(Task):
    def __init__(self, bot):
        super().__init__(bot)
        self.items_btn_pos = (925, 670)
        self.resources_btn_pos = (250, 80)
        self.speedups_btn_pos = (430, 80)
        self.boosts_btn_pos = (610, 80)
        self.equipment_btn_pos = (790, 80)
        self.other_btn_pos = (970, 80)

        self.minus_btn_pos = (870, 515)
        self.plus_btn_pos = (1020, 515)
        self.max_btn_pos = (1075, 515)
        self.use_btn_pos = (980, 600)

    def do(self, next_task=TaskName.MATERIALS):
        self.set_text(title='Items', remove=True)
        try:
            self.set_text(insert='Open items')
            self.use_vip()
            self.use_gems()
            self.use_daily_rss()
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task

    def use_vip(self):
        if not self.bot.config.useItemsVip:
            self.set_text(insert='Not opening VIP items')
            return
        self.set_text(insert='Opening VIP Items')
        # Reopen Items Window so that item values are reset to 1
        self.back_to_home_gui()
        self.menu_should_open(True)
        self.tap(self.items_btn_pos)
        self.tap(self.resources_btn_pos)
        for item in [ImagePathAndProps.ITEM_VIP1_IMAGE_PATH, ImagePathAndProps.ITEM_VIP2_IMAGE_PATH]:
            found = True
            while found:
                found, _, pos = self.gui.check_any(item.value)
                if not found:
                    break
                self.set_text(insert=f'Found VIP item at {pos}')
                self.tap(pos)
                self.tap(self.max_btn_pos)
                self.tap(self.use_btn_pos)
                # Tap in a random place just in case a popup opens
                self.tap((1100, 200))

    def use_gems(self):
        if not self.bot.config.useItemsGems:
            self.set_text(insert='Not opening Gems items')
            return
        self.set_text(insert='Opening Gems items')
        # Reopen Items Window so that item values are reset to 1
        self.back_to_home_gui()
        self.menu_should_open(True)
        self.tap(self.items_btn_pos)
        self.tap(self.resources_btn_pos)
        for item in [ImagePathAndProps.ITEM_GEMS1_IMAGE_PATH, ImagePathAndProps.ITEM_GEMS2_IMAGE_PATH,
                     ImagePathAndProps.ITEM_GEMS3_IMAGE_PATH]:
            found = True
            while found:
                found, _, pos = self.gui.check_any(item.value)
                if not found:
                    break
                self.set_text(insert=f'Found Gems item at {pos}')
                self.tap(pos)
                self.tap(self.max_btn_pos)
                self.tap(self.use_btn_pos)
                # Tap in a random place just in case a popup opens
                self.tap((1100, 200))

    def use_daily_rss(self):
        if not self.bot.config.useItemsDailyRss:
            self.set_text(insert='Not opening daily quest resource items')
            return
        self.set_text(insert='Opening daily quest resource items (lvl 1 resource pack only)')
        # Reopen Items Window so that item values are reset to 1
        self.back_to_home_gui()
        self.menu_should_open(True)
        self.tap(self.items_btn_pos)
        self.tap(self.resources_btn_pos)

        # Need to open only 5 items for daily quest
        for i in range(0, 5):
            found, _, pos = self.gui.check_any(ImagePathAndProps.ITEM_RESOURCE_PACK1_IMAGE_PATH.value)
            if not found:
                return
            self.set_text(insert=f'Found resource pack 1 chest at {pos}')
            self.tap(pos)
            self.tap(self.minus_btn_pos)
            self.tap(self.use_btn_pos)
            found, _, pos = self.gui.check_any(ImagePathAndProps.ITEM_EXCESS_RESOURCE_PROMPT_NO_IMAGE_PATH.value)
            if found:
                # Weird state where we are trying to open too many resources, exit without using resource pack
                self.back(0.5)
                return
            # Tap in a random place just in case a popup opens
            self.tap((1100, 200))
