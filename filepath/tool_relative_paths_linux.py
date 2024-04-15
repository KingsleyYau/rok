from enum import Enum

class FilePaths(Enum):
    TEST_SRC_FOLDER_PATH = "script/capture/"
    TEST_CURR_SCREEN_CAP_PATH = "test_screen_caps/current_cap.png"
    ADB_EXE_PATH = "adb/adb"
    TESSERACT_EXE_PATH = "/usr/bin/tesseract"
    TESSDATA_CHI_SIM_PATH = "tessdata/chi_sim.traineddata"
    SAVE_FOLDER_PATH = "save/"
