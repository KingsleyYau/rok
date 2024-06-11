import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName
import random

class Alliance(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.MATERIALS):
        super().set_text(title='联盟任务', remove=True)
        alliance_btn_pos = (1030, 670)
        try:
            random_tasks = ['HELP', 'GIFTS', 'TERRITORY', 'TECHNOLOGY']
            random.shuffle(random_tasks)
            
            for name in random_tasks:
                super().set_text(insert='回到联盟中心菜单')
                super().back_to_home_gui()
                super().menu_should_open(True)
                super().set_text(insert='打开联盟中心')
                super().tap(alliance_btn_pos)
                self.bot.snashot_update_event()
                if name == 'HELP':
                    super().set_text(insert='帮助盟友')
                    # super().tap((920, 400))  # enter the help page
                    _, _, help_pos = self.gui.check_any(ImagePathAndProps.HELP_IMG_PATH.value)
                    if help_pos is not None:
                        super().tap(help_pos)
                        # tap the help button if present, otherwise it will tap on empty space
                        super().tap((650, 650))  
                elif name == 'GIFTS':
                    super().set_text(insert='收集联盟礼物')
                    
                    _, _, gifts_pos = self.gui.check_any(ImagePathAndProps.GIFT_IMG_PATH.value)
                    if gifts_pos is not None:
                        super().tap(gifts_pos)
                    else:
                        super().set_text(insert='没有找到联盟礼物')
                        continue
                    self.bot.snashot_update_event()
                    # collecting rate gifts
                    super().set_text(insert='收集稀有礼物')
                    rate_pos = (930, 205)
                    super().tap(rate_pos)
                    for i in range(100):
                        _, _, pos = self.gui.check_any(ImagePathAndProps.GIFTS_CLAIM_BUTTON_IMAGE_PATH.value)
                        if pos is None:
                            super().set_text(insert='没有找到稀有礼物')
                            break
                        super().tap(pos)
                    self.bot.snashot_update_event()
                    
                    # collecting normal gifts
                    super().set_text(insert='收集普通礼物')
                    normal_pos = (670, 205)
                    super().tap(normal_pos)
                    self.bot.snashot_update_event()
                    
                    super().set_text(insert='一键收集普通礼物')
                    claim_all_pos = (1110, 205)
                    super().tap(claim_all_pos)
                    self.bot.snashot_update_event()
                    
                    comfirm_pos = self.gui.check_any(ImagePathAndProps.CONFIRM_BUTTON_PATH.value)[2]
                    if comfirm_pos is not None:
                        self.tap(comfirm_pos)
                                            
                    # collecting treasure of white crystal
                    super().set_text(insert='收集水晶箱子')
                    treasure = (330, 410)
                    super().tap(treasure)
                    self.bot.snashot_update_event()
                    
                elif name == 'TERRITORY':
                    super().set_text(insert='收集领土资源')
                    _, _, territory_pos = self.gui.check_any(ImagePathAndProps.TERRITORY_IMG_PATH.value)
                    if territory_pos is not None:
                        super().tap(territory_pos)
                        self.bot.snashot_update_event()
                        claim_pos = (1020, 140)
                        super().tap(claim_pos)

                elif name == 'TECHNOLOGY':
                    super().set_text(insert='捐献科技')
                    # technology_pos = (660, 560)
                    _, _, technology_pos = self.gui.check_any(ImagePathAndProps.TECHNOLOGY_IMG_PATH.value)
                    if technology_pos is not None:
                        super().tap(technology_pos)
                        self.bot.snashot_update_event()
                        _, _, recommend_image_pos = self.gui.check_any(ImagePathAndProps.TECH_RECOMMEND_IMAGE_PATH.value)
                        if recommend_image_pos is not None:
                            x, y = recommend_image_pos
                            super().tap((x, y + 60))
                            _, _, donate_btn_pos = self.gui.check_any(
                                ImagePathAndProps.TECH_DONATE_BUTTON_IMAGE_PATH.value)
                            if donate_btn_pos is not None:
                                for i in range(20):
                                    super().tap(donate_btn_pos)
                        else:
                            super().set_text(insert="没有找到推荐捐献科技")
                        
                self.bot.snashot_update_event()

        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task
