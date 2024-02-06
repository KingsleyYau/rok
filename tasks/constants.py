from enum import Enum

DEFAULT_RESOLUTION = {'height': 720, 'width': 1280}


class BuildingNames(Enum):
    CITY_HALL = '市政厅'
    BARRACKS = '步兵'
    ARCHERY_RANGE = '弓兵'
    STABLE = '骑兵'
    SIEGE_WORKSHOP = '攻城车'
    BLACKSMITH = '铁匠铺'
    TAVERN = '酒馆'
    SHOP = '商店'
    ALLIANCE_CENTER = '联盟中心'
    ACADEMY = '研究所'
    STOREHOUSE = '仓库'
    TRADING_POST = '商栈'
    SCOUT_CAMP = '驿站'
    COURIER_STATION = 'courier_station'
    BUILDERS_HUT = "工人小屋"
    CASTLE = '城堡'
    HOSPITAL = '医院'
    FARM = '农场'
    LUMBER_MILL = '伐木场'
    QUARRY = '石矿'
    GOLDMINE = '金矿'
    WALL = '城墙'


class TrainingType(Enum):
    UPGRADE = 'upgrade'
    UPGRADE_AND_TRAIN = 'upgrade_and_train'
    TRAIN = 'train'
    NO_ACTION = 'no_action'


class TaskName(Enum):
    KILL_GAME = -2
    BREAK = -1
    NEXT_TASK = 0
    INIT_BUILDING_POS = 1
    COLLECTING = 2
    CLAIM_QUEST = 3
    TRAINING = 4
    GATHER = 5
    ALLIANCE = 6
    MATERIALS = 7
    TAVERN = 8
    VIP_CHEST = 9
    BARBARIANS = 10
    SCOUT = 11
    GATHER_GEM = 12
    MYSTERY_MERCHANT = 13


class Resource(Enum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3
