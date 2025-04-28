from tasks.Task import Task
from tasks.constants import TaskName
import random

class ClaimVip(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.CLAIM_QUEST):
        vip_pos = (150, 65)
        vip_point_chest = (1010, 180)
        vip_free_chest = (920, 400)
        super().set_text(title='收集VIP', remove=True)
        super().back_to_home_gui()
        # tap on vip
        super().set_text(insert='打开VIP')
        super().tap(vip_pos)
        # tap on vip point chest
        super().set_text(insert='收集VIP积分')
        super().tap(vip_point_chest, 5)
        super().tap(vip_point_chest)
        # tap on anywhere
        pos_free = (400 + int(50 * (0.5 - random.random())), 400 + int(50 * (0.5 - random.random())))
        super().tap(pos_free)
        # tap on free chest
        super().set_text(insert='收集VIP礼物')
        super().tap(vip_free_chest)
        return next_task
