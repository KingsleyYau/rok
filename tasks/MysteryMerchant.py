from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
import traceback

from tasks.constants import TaskName


class MysteryMerchant(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.MYSTERY_MERCHANT.value):
        self.set_text(title='神秘商店', remove=True)
        self.back_to_home_gui()
        self.home_gui_full_view()
        self.bot.snashot_update_event()
        
        pos = self.gui.check_any(ImagePathAndProps.MERCHANT_ICON_IMAGE_PATH.value)[2]
        if pos is None:
            self.set_text(insert='没有发现神秘商店', index=0)
            # 铭文商店
            pos = self.gui.check_any(ImagePathAndProps.MERCHANT_ICON2_IMAGE_PATH.value)[2]
            if pos is not None:
                self.set_text(insert='打开驿站{}'.format(pos))
                self.tap(pos)
            return next_task
        
        self.set_text(insert='打开驿站{}'.format(pos))
        self.tap(pos)
        
        pos = self.gui.check_any(ImagePathAndProps.MERCHANT_SHOP_IMAGE_PATH.value)[2]
        if pos is None:
            return next_task
        self.set_text(insert='打开神秘商店{}'.format(pos))

        while True:
            self.bot.snashot_update_event()
            for i in range(5):
                self.set_text(insert='使用食物购买道具')
                list = self.gui.find_all_image_props(ImagePathAndProps.MERCHANT_BUY_WITH_FOOD_IMAGE_PATH.value)
                for buy_with_food_btn in list:
                    self.tap(buy_with_food_btn['result'])

                self.set_text(insert='使用木头购买道具')
                list = self.gui.find_all_image_props(ImagePathAndProps.MERCHANT_BUY_WITH_WOOD_IMAGE_PATH.value)
                for buy_with_wood_btn in list:
                    self.tap(buy_with_wood_btn['result'])

                self.set_text(insert='上拉更多道具')
                self.swipe((730, 575), (730, 475), 1, 1000)

            # tap on free refresh
            found, _, pos = self.gui.check_any(ImagePathAndProps.MERCHANT_FREE_BTN_IMAGE_PATH.value)
            if not found:
                return next_task
            self.set_text(insert='刷新')
            self.tap(pos)

