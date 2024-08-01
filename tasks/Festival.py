from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
import traceback

from tasks.constants import TaskName


class Festival(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.ALLIANCE):
        self.set_text(title='收集免费活动礼物', remove=True)
        try:
            self.back_to_home_gui()
            self.set_text(insert='打开活动中心')
            self.tap((1220, 100))

            for i in range(20):
                _, _, free_btn_pos = self.gui.check_any(ImagePathAndProps.FREE_BUTTON_PATH.value)
                if free_btn_pos is None:
                    break
                self.set_text(insert='领取礼物 {}'.format(free_btn_pos))
                self.tap(free_btn_pos)
                _, _, comfirm_pos = self.gui.check_any(
                    ImagePathAndProps.CONFIRM_BUTTON_PATH.value
                    )
                if comfirm_pos is not None:
                    self.tap(comfirm_pos)

        except Exception as e:
            traceback.print_exc()
            return TaskName.ALLIANCE
        return next_task
