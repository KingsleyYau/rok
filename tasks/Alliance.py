import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task

from tasks.constants import TaskName


class Alliance(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.MATERIALS):
        super().set_text(title='联盟任务', remove=True)
        alliance_btn_pos = (1030, 670)
        try:
            for name in ['HELP', 'GIFTS', 'TERRITORY', 'TECHNOLOGY']:
                super().back_to_home_gui()
                super().menu_should_open(True)
                super().set_text(insert='打开联盟中心')
                super().tap(alliance_btn_pos)
                self.bot.snashot_update_event()
                if name == 'HELP':
                    super().set_text(insert='帮助盟友')
                    super().tap((920, 400))  # enter the help page
                    super().tap((650, 650))  # tap the help button if present, otherwise it will tap on empty space

                elif name == 'GIFTS':
                    super().set_text(insert='收集水晶箱子')
                    # gifts_pos = (885, 560)
                    gifts_pos = (1050, 400)
                    rate_pos = (930, 205)
                    normal_pos = (670, 205)
                    claim_all_pos = (1110, 205)
                    treasure = (330, 410)
                    super().tap(gifts_pos)

                    # collecting rate gifts
                    super().set_text(insert='收集稀有礼物')
                    super().tap(rate_pos)
                    for i in range(20):
                        _, _, pos = self.gui.check_any(ImagePathAndProps.GIFTS_CLAIM_BUTTON_IMAGE_PATH.value)
                        if pos is None:
                            break
                        super().tap(pos)

                    # collecting normal gifts
                    super().set_text(insert='收集普通礼物')
                    super().tap(normal_pos)
                    super().tap(claim_all_pos)
                    # collecting treasure of white crystal
                    super().tap(treasure)

                elif name == 'TERRITORY':
                    super().set_text(insert='收集领土资源')
                    territory_pos = (785, 405)
                    claim_pos = (1020, 140)
                    super().tap(territory_pos)
                    super().tap(claim_pos)

                elif name == 'TECHNOLOGY':
                    super().set_text(insert='捐献科技')
                    technology_pos = (660, 560)
                    super().tap(technology_pos, 5)
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
