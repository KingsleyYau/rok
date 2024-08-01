import traceback
from tasks.Task import Task
from tasks.constants import TaskName
from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames

class UpgradeBuildings(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.BREAK):
        self.set_text(title='升级建筑', remove=True)

        self.back_to_map_gui()
        self.back_to_home_gui()
        
        try:
            city_pos = (400, 230)
            self.set_text(insert='打开市政厅')
            self.tap(city_pos)
            
            for i in range(10):
                
                upgrade_pos = self.gui.check_any(ImagePathAndProps.BUILDING_UPGRADE_BUTTON_PATH.value)[2]
                if upgrade_pos is not None:
                    self.tap(upgrade_pos)
                    self.set_text(insert='打开建筑升级')
                    confirm_pos = self.gui.check_any(ImagePathAndProps.BUILDING_UPGRADE_CONFIRM_BUTTON_PATH.value)[2] 
                    if confirm_pos is not None:
                        self.set_text(insert='升级建筑')
                        
                        self.tap(confirm_pos)
                        break
                    else:
                        forward_pos = self.gui.check_any(ImagePathAndProps.BUILDING_UPGRADE_FORWARD_BUTTON_PATH.value)[2]
                        if forward_pos is not None:
                            self.set_text(insert='打开前置建筑')
                            
                            self.tap(forward_pos)
                        else:
                            break
                else:
                    self.set_text(insert='建筑升级中...')
                    break
            
        except Exception as e:
            traceback.print_exc()
        return next_task
