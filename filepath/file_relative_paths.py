from enum import Enum
from filepath.constants import *


class StrImagePosition(Enum):
    WINDOWS_TITLE = (305, 68, 975, 100)

class BuffsImageAndProps(Enum):
    ENHANCED_GATHER_BLUE = [
        "resource/buffs/enhanced_gathering_blue.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        BOOSTS,
    ]
    ENHANCED_GATHER_PURPLE = [
        "resource/buffs/enhanced_gathering_purple.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        BOOSTS,
    ]


class ItemsImageAndProps(Enum):
    ENHANCED_GATHER_BLUE = [
        "resource/items/enhanced_gathering_blue.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        BOOSTS,
    ]
    ENHANCED_GATHER_PURPLE = [
        "resource/items/enhanced_gathering_purple.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        BOOSTS,
    ]


class ImagePathAndProps(Enum):
    MAP_BUTTON_IMG_PATH = [
        "resource/map_button.png",
        (1280, 720),
        (10, 602, 113, 709),
        0.98,
        25,
        HOME,
    ]
    HOME_BUTTON_IMG_PATH = [
        "resource/home_button.png",
        (1280, 720),
        (10, 602, 113, 709),
        0.98,
        25,
        MAP,
    ]
    GREEN_HOME_BUTTON_IMG_PATH = [
        "resource/green_home_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        GREEN_HOME,
    ]
    WINDOW_IMG_PATH = [
        "resource/window.png",
        (1280, 720),
        (1065, 56, 1128, 112),
        0.70,
        25,
        WINDOW,
    ]
    WINDOW_TITLE_MARK_IMG_PATH = [
        "resource/window_title_mark.png",
        (1280, 720),
        (1065, 56, 1128, 112),
        0.70,
        25,
        WINDOW_TITLE,
    ]
    BUILDING_TITLE_MARK_IMG_PATH = [
        "resource/building_title_left.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        BUILDING_TITLE,
    ]
    BUILDING_INFO_BUTTON_IMG_PATH = [
        "resource/building_info_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        BUILDING_INFO,
    ]
    MENU_OPENED_IMAGE_PATH = [
        "resource/menu_opened.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        MENU_OPENED_IMAGE,
    ]
    MENU_BUTTON_IMAGE_PATH = [
        "resource/menu_button.png",
        (1280, 720),
        (1204, 646, 1257, 693),
        0.90,
        25,
        MENU_IMAGE,
    ]
    QUEST_CLAIM_BUTTON_IMAGE_PATH = [
        "resource/quests_claim_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        CLAIM_BUTTON,
    ]
    BARRACKS_BUTTON_IMAGE_PATH = [
        "resource/barracks_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        BARRACKS_BUTTON,
    ]
    ARCHER_RANGE_BUTTON_IMAGE_PATH = [
        "resource/archery_range_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ARCHER_RANGE_BUTTON,
    ]
    STABLE_BUTTON_IMAGE_PATH = [
        "resource/stable_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        STABLE_BUTTON,
    ]
    SIEGE_WORKSHOP_BUTTON_IMAGE_PATH = [
        "resource/siege_workshop_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SIEGE_WORKSHOP_BUTTON,
    ]
    TRAINING_UPGRADE_BUTTON_IMAGE_PATH = [
        "resource/training_upgrade_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        TRAINING_UPGRADE_BUTTON,
    ]
    TRAIN_BUTTON_IMAGE_PATH = [
        "resource/train_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        TRAIN_BUTTON,
    ]
    UPGRADE_BUTTON_IMAGE_PATH = [
        "resource/upgrade_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        UPGRADE_BUTTON,
    ]
    SPEED_UP_BUTTON_IMAGE_PATH = [
        "resource/speed_up_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SPEED_UP,
    ]
    DECREASING_BUTTON_IMAGE_PATH = [
        "resource/decreasing_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        DECREASING,
    ]
    INCREASING_BUTTON_IMAGE_PATH = [
        "resource/increasing_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        INCREASING,
    ]
    LOCK_BUTTON_IMAGE_PATH = [
        "resource/lock_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        LOCK,
    ]
    RESOURCE_SEARCH_BUTTON_IMAGE_PATH = [
        "resource/resource_search_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        RESOURCE_SEARCH,
    ]
    RESOURCE_GATHER_BUTTON_IMAGE_PATH = [
        "resource/resource_gather_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        RESOURCE_GATHER,
    ]
    NEW_TROOPS_BUTTON_IMAGE_PATH = [
        "resource/new_troops_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        NEW_TROOPS,
    ]
    TROOPS_MATCH_BUTTON_IMAGE_PATH = [
        "resource/troops_match_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        TROOPS_MATCH,
    ]
    VERIFICATION_CHEST_BUTTON_IMAGE_PATH = [
        "resource/verification_chest_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        VERIFICATION_CHEST,
    ]
    VERIFICATION_VERIFY_BUTTON_IMAGE_PATH = [
        "resource/verification_verify_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        VERIFICATION_VERIFY,
    ]
    VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH = [
        "resource/verification_close_refresh_ok_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        VERIFICATION_CLOSE_REFRESH_OK,
    ]
    GIFTS_CLAIM_BUTTON_IMAGE_PATH = [
        "resource/alliance_gifts_claim_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        GIFTS_CLAIM,
    ]
    TECH_RECOMMEND_IMAGE_PATH = [
        "resource/alliance_tech_recommend.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        TECH_RECOMMEND,
    ]
    TECH_DONATE_BUTTON_IMAGE_PATH = [
        "resource/alliance_tech_donate.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        TECH_DONATE,
    ]
    MATERIALS_PRODUCTION_BUTTON_IMAGE_PATH = [
        "resource/materials_production_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        MATERIALS_PRODUCTION,
    ]
    TAVERN_BUTTON_BUTTON_IMAGE_PATH = [
        "resource/tavern_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        TAVERN_BUTTON,
    ]
    TAVERN_BUTTON_BUTTON2_IMAGE_PATH = [
        "resource/tavern_button2.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        TAVERN_BUTTON2,
    ]
    CHEST_OPEN_BUTTON_IMAGE_PATH = [
        "resource/chest_open_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        CHEST_OPEN,
    ]
    CHEST_CONFIRM_BUTTON_IMAGE_PATH = [
        "resource/chest_confirm_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        CHEST_CONFIRM,
    ]
    ATTACK_BUTTON_POS_IMAGE_PATH = [
        "resource/attack_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ATTACK_BUTTON,
    ]
    HOLD_POS_CHECKED_IMAGE_PATH = [
        "resource/hold_posistion_checked.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        HOLD_POS_CHECKED,
    ]
    HOLD_POS_UNCHECK_IMAGE_PATH = [
        "resource/hold_position_unchecked.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        HOLD_POS_UNCHECK,
    ]
    UNSELECT_BLUE_ONE_SAVE_BUTTON_IMAGE_PATH = [
        "resource/unselect_save_blue_one.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.95,
        25,
        UNSELECT_BLUE_ONE,
    ]
    SELECTED_BLUE_ONE_SAVE_BUTTON_IMAGE_PATH = [
        "resource/selected_save_blue_one.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.95,
        25,
        SELECTED_BLUE_ONE,
    ]
    SAVE_SWITCH_BUTTON_IMAGE_PATH = [
        "resource/switch_save.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SAVE_SWITCH,
    ]
    VICTORY_MAIL_IMAGE_PATH = [
        "resource/victory_mail.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        VICTORY_MAIL,
    ]
    DEFEAT_MAIL_IMAGE_PATH = [
        "resource/defeat_mail.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        DEFEAT_MAIL,
    ]
    RETURN_BUTTON_IMAGE_PATH = [
        "resource/return_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        RETURN_BUTTON,
    ]
    HOLD_ICON_IMAGE_PATH = [
        "resource/hold_icon.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        HOLD_ICON,
    ]
    HOLD_ICON_SMALL_IMAGE_PATH = [
        "resource/hold_icon_small.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        HOLD_ICON_SMALL,
    ]
    MARCH_BAR_IMAGE_PATH = [
        "resource/march_bar.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        MARCH_BAR,
    ]
    HEAL_ICON_IMAGE_PATH = [
        "resource/heal_icon.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        HEAL_ICON,
    ]
    DAILY_AP_CLAIM_BUTTON_IMAGE_PATH = [
        "resource/daily_ap_claim.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        DAILY_AP_CLAIM,
    ]
    USE_AP_BUTTON_IMAGE_PATH = [
        "resource/use_ap.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        USE_AP,
    ]
    SCOUT_BUTTON_IMAGE_PATH = [
        "resource/scout_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SCOUT_BUTTON,
    ]
    SCOUT_EXPLORE_BUTTON_IMAGE_PATH = [
        "resource/explore_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        EXPLORE_BUTTON,
    ]
    SCOUT_EXPLORE2_BUTTON_IMAGE_PATH = [
        "resource/explore_button2.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        EXPLORE_BUTTON2,
    ]
    SCOUT_SEND_BUTTON_IMAGE_PATH = [
        "resource/scout_send_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SEND_BUTTON,
    ]
    MAIL_EXPLORATION_REPORT_IMAGE_PATH = [
        "resource/mail_exploration_report.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        MAIL_EXPLORATION_REPORT,
    ]
    MAIL_SCOUT_BUTTON_IMAGE_PATH = [
        "resource/mail_scout_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        MAIL_SCOUT_BUTTON,
    ]
    INVESTIGATE_BUTTON_IMAGE_PATH = [
        "resource/investigate_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        INVESTIGATE_BUTTON,
    ]
    GREAT_BUTTON_IMAGE_PATH = [
        "resource/great_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        GREAT_BUTTON,
    ]
    SCOUT_IDLE_ICON_IMAGE_PATH = [
        "resource/scout_idle_icon.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        IDLE_ICON,
    ]
    SCOUT_ZZ_ICON_IMAGE_PATH = [
        "resource/scout_zz_icon.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        ZZ_ICON,
    ]
    MERCHANT_ICON_IMAGE_PATH = [
        "resource/merchant_icon.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        MERCHANT_ICON,
    ]
    MERCHANT_ICON2_IMAGE_PATH = [
        "resource/merchant_icon2.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        MERCHANT_ICON2,
    ]
    MERCHANT_SHOP_IMAGE_PATH = [
        "resource/merchant_shop.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        MERCHANT_SHOP,
    ]
    MERCHANT_FREE_BTN_IMAGE_PATH = [
        "resource/merchant_free_btn.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        MERCHANT_FREE_BTN,
    ]
    MERCHANT_BUY_WITH_WOOD_IMAGE_PATH = [
        "resource/merchant_buy_with_wood.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        MERCHANT_BUY_WITH_WOOD,
    ]
    MERCHANT_BUY_WITH_FOOD_IMAGE_PATH = [
        "resource/merchant_buy_with_food.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        MERCHANT_BUY_WITH_FOOD,
    ]
    HAS_MATCH_QUERY_IMAGE_PATH = [
        "resource/has_match_query.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        HAS_MATCH_QUERY,
    ]
    VERIFICATION_VERIFY_TITLE_IMAGE_PATH = [
        "resource/verification_verify_title.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        VERIFICATION_VERIFY_TITLE,
    ]
    SUNSET_CANYON_IMAGE_PATH = [
        "resource/sunset_canyon.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SUNSET_CANYON_BTN,
    ]
    SUNSET_CANYON_OK_IMAGE_PATH = [
        "resource/sunset_canyon_ok.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SUNSET_CANYON_OK_BTN,
    ]
    LOST_CANYON_IMAGE_PATH = [
        "resource/lost_canyon.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SUNSET_CANYON_BTN,
    ]
    LOST_CANYON_OK_IMAGE_PATH = [
        "resource/lost_canyon_ok.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        LOST_CANYON_OK_BTN,
    ]
    SKIP_BATTLE_CHECKED_IMAGE_PATH = [
        "resource/skip_battle_checked.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SKIP_BATTLE_CHECKED,
    ]
    ITEM_VIP1_IMAGE_PATH = [
        "resource/items/resources/vip1.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ITEM_VIP1,
    ]
    ITEM_VIP2_IMAGE_PATH = [
        "resource/items/resources/vip2.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ITEM_VIP2,
    ]
    ITEM_GEMS1_IMAGE_PATH = [
        "resource/items/resources/gems1.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ITEM_GEMS1,
    ]
    ITEM_GEMS2_IMAGE_PATH = [
        "resource/items/resources/gems2.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ITEM_GEMS2,
    ]
    ITEM_GEMS3_IMAGE_PATH = [
        "resource/items/resources/gems3.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ITEM_GEMS3,
    ]
    ITEM_RESOURCE_PACK1_IMAGE_PATH = [
        "resource/items/resources/resource_pack1.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ITEM_RESOURCE_PACK1,
    ]
    ITEM_EXCESS_RESOURCE_PROMPT_YES_IMAGE_PATH = [
        "resource/items/resources/excess_resource_prompt_yes.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ITEM_EXCESS_RESOURCE_PROMPT_YES,
    ]
    ITEM_EXCESS_RESOURCE_PROMPT_NO_IMAGE_PATH = [
        "resource/items/resources/excess_resource_prompt_no.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        ITEM_EXCESS_RESOURCE_PROMPT_NO,
    ]
    SEARCH_ICON_SMALL_IMAGE_PATH = [
        "resource/search_icon_small.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        SEARCH_ICON_SMALL
    ]   
    SEARCH_BUTTON_IMAGE_PATH = [
        "resource/search_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        SEARCH_BUTTON
    ]
    SEARCH_SERVER_IMAGE_PATH = [
        "resource/search_server.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        SEARCH_SERVER
    ]
    SEARCH_BOOKMARK_IMAGE_PATH = [
        "resource/search_bookmark.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        SEARCH_BOOKMARK
    ]      
    SEARCH_X_IMAGE_PATH = [
        "resource/search_x.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        SEARCH_X
    ]
    SEARCH_Y_IMAGE_PATH = [
        "resource/search_y.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        SEARCH_Y
    ]
    TITLE_BUTTON_PATH = [
        "resource/title_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        TITLE_BUTTON
    ]
    TITLE_CHECK_BUTTON_PATH = [
        "resource/title_check_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        TITLE_CHECK_BUTTON
    ]
    CONFIRM_BUTTON_PATH = [
        "resource/confirm.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CONFIRM_BUTTON,
    ]
    CONTINUE_BUTTON_PATH = [
        "resource/continue.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CONTINUE_BUTTON,
    ]  
    CONFIRM_UPDATE_BUTTON_PATH = [
        "resource/confirm_update.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CONFIRM_UPDATE_BUTTON,
    ] 
    CANCEL_BUTTON_PATH = [
        "resource/cancel.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CANCEL_BUTTON,
    ] 
    LOGIN_OTHER_BUTTON_PATH = [
        "resource/login_other.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        LOGIN_OTHER_BUTTON,
    ] 
    DIAMOND_IMG_PATH = [
        "resource/diamond.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        DIAMOND_IMG,
    ] 
    TERRITORY_IMG_PATH = [
        "resource/territory.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        TERRITORY_IMG,
    ]    
    TERRITORY_RESOURCE_IMG_PATH = [
        "resource/territory_resource.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        TERRITORY_RESOURCE_IMG,
    ]
    TERRITORY_GATHERING_IMG_PATH = [
        "resource/territory_gathering.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        TERRITORY_GATHERING_IMG,
    ]
    TERRITORY_GATHER_JOIN_IMG_PATH = [
        "resource/territory_gather_join.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        TERRITORY_GATHER_JOIN_IMG,
    ]
    FORBIDDEN_IMG_PATH = [
        "resource/forbidden.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        FORBIDDEN_IMG,
    ]    
    HELP_IMG_PATH = [
        "resource/help.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        HELP_IMG,
    ]  
    HELP2_IMG_PATH = [
        "resource/help2.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        HELP2_IMG,
    ]  
    GIFT_IMG_PATH = [
        "resource/gift.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        GIFT_IMG,
    ]   
    TECHNOLOGY_IMG_PATH = [
        "resource/technology.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        TECHNOLOGY_IMG,
    ] 
    YES_BUTTON_PATH = [
        "resource/yes.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        YES_BUTTON,
    ]    
    NO_BUTTON_PATH = [
        "resource/no.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        NO_BUTTON,
    ] 
    RESOURCE_IMG_PATH = [
        "resource/resource.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        RESOURCE_IMG,
    ]
    CLEAR_BUTTON_PATH = [
        "resource/clear.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CLEAR_BUTTON,
    ]
    MAX_BUTTON_PATH = [
        "resource/max.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        MAX_BUTTON,
    ]
    KILO_IMG_PATH = [
        "resource/kilo.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        KILO_IMG,
    ]
    FREE_BUTTON_PATH = [
        "resource/free.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        FREE_BUTTON,
    ]
    CONTACT_US_BUTTON_PATH = [
        "resource/contact_us.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CONTACT_US_BUTTON,
    ]
    CHANGE_ROLE_BUTTON_PATH = [
        "resource/change_role.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CHANGE_ROLE_BUTTON,
    ]
    BUILDING_UPGRADE_BUTTON_PATH = [
        "resource/building_upgrade.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        BUILDING_UPGRADE_BUTTON,
    ]   
    BUILDING_UPGRADE_FORWARD_BUTTON_PATH = [
        "resource/building_upgrade_forward.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        BUILDING_UPGRADE_FORWARD_BUTTON,
    ]      
    BUILDING_UPGRADE_CONFIRM_BUTTON_PATH = [
        "resource/building_upgrade_confirm.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        BUILDING_UPGRADE_CONFIRM_BUTTON,
    ]    
    ALLIANCE_WAR_IMG_PATH = [
        "resource/alliance_war.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        ALLIANCE_WAR_IMG,
    ]  
    ALLIANCE_WAR_MAIN_PATH = [
        "resource/alliance_war_main.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        ALLIANCE_WAR_MAIN,
    ]  
    JOIN_TROOP_IMG_PATH = [
        "resource/alliance_join_troop.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        JOIN_TROOP_IMG,
    ] 
    CLOSEAPP_BUTTON_PATH = [
        "resource/closeapp.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CLOSEAPP_BUTTON,
    ]
    CLOSE_LEFT_TASK_BUTTON_PATH = [
        "resource/close_left_task.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        CLOSE_LEFT_TASK_BUTTON,
    ] 
    DOWNLOAD_IMG_PATH = [
        "resource/download.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        DOWNLOAD_IMG,
    ]  
    DOWNLOAD_BUTTON_PATH = [
        "resource/download_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        DOWNLOAD_BUTTON,
    ]
    DOWNLOAD_BUTTON_CLOSE_PATH = [
        "resource/download_button_close.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.80,
        25,
        DOWNLOAD_BUTTON_CLOSE,
    ]
    RANKING_BUTTON_PATH = [
        "resource/ranking_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        RANKING_BUTTON,
    ]
    RANKING_POWER_TITLE_PATH = [
        "resource/ranking_power_title.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        RANKING_POWER_TITLE,
    ]
    PLAYER_DETAIL_TITLE_PATH = [
        "resource/player_detail_title.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        PLAYER_DETAIL_TITLE,
    ]
    PLAYER_MORE_INFO_PATH = [
        "resource/player_more_info.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        PLAYER_MORE_INFO,
    ]
    PLAYER_MORE_INFO_KILL_PATH = [
        "resource/player_more_info_kill.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        PLAYER_MORE_INFO_KILL,
    ] 
    DEAD_BARRACKS_IMG_PATH = [
        "resource/dead_barracks.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        DEAD_BARRACKS_IMG,
    ]
    DEAD_SIEGE_IMG_PATH = [
        "resource/dead_siege.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        DEAD_SIEGE_IMG,
    ]
    DEAD_ARCHERY_IMG_PATH = [
        "resource/dead_archery.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        DEAD_ARCHERY_IMG,
    ]
    DEAD_STABLE_IMG_PATH = [
        "resource/dead_stable.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        DEAD_STABLE_IMG,
    ] 
    SETTING_BUTTON_PATH = [
        "resource/setting_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.7,
        25,
        SETTING_BUTTON,
    ]
    CHANGE_USER_BUTTON_PATH = [
        "resource/setting_change_user_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.7,
        25,
        CHANGE_USER_BUTTON,
    ]
    EDIT_BUTTON_PATH = [
        "resource/edit_button.png",
        (1280, 720),
        (10, 602, 113, 709),
        0.8,
        25,
        EDIT_BUTTON,
    ]
    EDIT_BUTTON_2_PATH = [
        "resource/edit_button_2.png",
        (1280, 720),
        (10, 602, 113, 709),
        0.8,
        25,
        EDIT_BUTTON_2,
    ]
    EDIT_BUTTON_3_PATH = [
        "resource/edit_button_3.png",
        (1280, 720),
        (10, 602, 113, 709),
        0.8,
        25,
        EDIT_BUTTON_3,
    ]
    
class GuiCheckImagePathAndProps(Enum):
    VERIFICATION_VERIFY_BUTTON_IMAGE_PATH = [
        "resource/verification_verify_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.90,
        25,
        VERIFICATION_VERIFY,
    ]
    VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH = [
        "resource/verification_close_refresh_ok_button.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        VERIFICATION_CLOSE_REFRESH_OK,
    ]
    VERIFICATION_CLOSE_REFRESH_OK_BUTTON_2_IMAGE_PATH = [
        "resource/verification_close_refresh_ok_button_2.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.60,
        25,
        VERIFICATION_CLOSE_REFRESH_OK,
    ]
    MAP_BUTTON_IMG_PATH = [
        "resource/map_button_0.png",
        (1280, 720),
        (10, 602, 113, 709),
        0.8,
        25,
        HOME,
    ]
    HOME_BUTTON_IMG_PATH = [
        "resource/home_button_0.png",
        (1280, 720),
        (10, 602, 113, 709),
        0.8,
        25,
        MAP,
    ]
    WINDOW_IMG_PATH = [
        "resource/window.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.8,
        25,
        WINDOW,
    ]
    VERIFICATION_CHEST_IMG_PATH = [
        'resource/verification_chest_button.png',
        (1280, 720),
        (0, 0, 0, 0),
        0.8,
        25,
        VERIFICATION_CHEST]
    VERIFICATION_CHEST1_IMG_PATH = [
        'resource/verification_chest_button1.png',
        (1280, 720),
        (0, 0, 0, 0),
        0.9,
        25,
        VERIFICATION_CHEST1]
    HELLO_WROLD_IMG_PATH = [
        "resource/hellow_world.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        HELLO_WROLD_IMG
    ]
    HELLO_WROLD_2_IMG_PATH = [
        "resource/hellow_world_2.png",
        (1280, 720),
        (0, 0, 0, 0),
        0.70,
        25,
        HELLO_WROLD_2_IMG
    ]
      
    
GuiCheckHelloImagePathAndPropsOrdered = [
    GuiCheckImagePathAndProps.HELLO_WROLD_IMG_PATH,
    GuiCheckImagePathAndProps.HELLO_WROLD_2_IMG_PATH
]

GuiCheckImagePathAndPropsOrdered = [
    GuiCheckImagePathAndProps.VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH,
    GuiCheckImagePathAndProps.VERIFICATION_CLOSE_REFRESH_OK_BUTTON_2_IMAGE_PATH,
    # GuiCheckImagePathAndProps.VERIFICATION_VERIFY_BUTTON_IMAGE_PATH,
    # GuiCheckImagePathAndProps.VERIFICATION_CHEST_IMG_PATH,
    # GuiCheckImagePathAndProps.VERIFICATION_CHEST1_IMG_PATH,
    GuiCheckImagePathAndProps.MAP_BUTTON_IMG_PATH,
    GuiCheckImagePathAndProps.HOME_BUTTON_IMG_PATH,
    GuiCheckImagePathAndProps.WINDOW_IMG_PATH,
]
