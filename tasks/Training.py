import traceback

from bot_related.bot_config import TrainingAndUpgradeLevel
from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames
from tasks.constants import TaskName
from tasks.Task import Task


class Training(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.GATHER):
        super().set_text(title='[训练/升级]部队', remove=True)
        super().back_to_home_gui()
        super().home_gui_full_view()
        try:
            soldier_icon_pos = [
                (630, 175),
                (730, 175),
                (830, 175),
                (930, 175),
                (1030, 175),
            ]

            for config in [
                [
                    ImagePathAndProps.BARRACKS_BUTTON_IMAGE_PATH.value,
                    self.bot.config.trainBarracksTrainingLevel,
                    self.bot.config.trainBarracksUpgradeLevel,
                    self.bot.building_pos[BuildingNames.BARRACKS.value],
                    BuildingNames.BARRACKS.value,
                ],
                [
                    ImagePathAndProps.ARCHER_RANGE_BUTTON_IMAGE_PATH.value,
                    self.bot.config.trainArcheryRangeTrainingLevel,
                    self.bot.config.trainArcheryRangeUpgradeLevel,
                    self.bot.building_pos[BuildingNames.ARCHERY_RANGE.value],
                    BuildingNames.ARCHERY_RANGE.value
                ],
                [
                    ImagePathAndProps.STABLE_BUTTON_IMAGE_PATH.value,
                    self.bot.config.trainStableTrainingLevel,
                    self.bot.config.trainStableUpgradeLevel,
                    self.bot.building_pos[BuildingNames.STABLE.value],
                    BuildingNames.STABLE.value,
                ],
                [
                    ImagePathAndProps.SIEGE_WORKSHOP_BUTTON_IMAGE_PATH.value,
                    self.bot.config.trainSiegeWorkshopTrainingLevel,
                    self.bot.config.trainSiegeWorkshopUpgradeLevel,
                    self.bot.building_pos[BuildingNames.SIEGE_WORKSHOP.value],
                    BuildingNames.SIEGE_WORKSHOP.value
                ]
            ]:
                super().set_text(insert='选择{}训练营'.format(config[4]))
                super().back_to_home_gui()
                upgraded = False
                super().tap(config[3])
                self.bot.snashot_update_event()
                
                _, _, pos = self.gui.check_any(config[0])
                if pos is None:
                    continue
                super().tap(pos)
                _, _, pos = self.gui.check_any(ImagePathAndProps.SPEED_UP_BUTTON_IMAGE_PATH.value)
                if pos is not None:
                    continue
                if config[2] != TrainingAndUpgradeLevel.DISABLED.value:
                    max = config[2] if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value \
                        else TrainingAndUpgradeLevel.T4.value
                    min = config[2] - 1 if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value else -1
                    for i in range(max, min, -1):
                        super().tap(soldier_icon_pos[i])
                        # check has upgrade button, if has then tap it
                        _, _, pos = self.gui.check_any(ImagePathAndProps.TRAINING_UPGRADE_BUTTON_IMAGE_PATH.value)
                        if pos is None:
                            if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value:
                                break
                            else:
                                continue
                        super().set_text(insert='升级T{}{}'.format(i + 1, config[4]))
                        super().tap(pos)
                        self.bot.snashot_update_event()

                        # check has train button if has then tap it
                        _, _, pos = self.gui.check_any(ImagePathAndProps.UPGRADE_BUTTON_IMAGE_PATH.value)
                        super().tap(pos)
                        upgraded = True

                if not upgraded and (
                        config[1] != TrainingAndUpgradeLevel.DISABLED.value):
                    for i in range(config[1], -1, -1):
                        super().tap(soldier_icon_pos[i])
                        self.bot.snashot_update_event()
                        
                        _, _, pos = self.gui.check_any(ImagePathAndProps.TRAIN_BUTTON_IMAGE_PATH.value)
                        if pos is None:
                            continue
                        super().set_text(insert='训练T{}{}'.format(i + 1, config[4]))
                        super().tap(pos)
                        break
            self.bot.snashot_update_event()
        except Exception as e:
            traceback.print_exc()
            return TaskName.TRAINING
        return next_task
