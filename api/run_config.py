class RunConfig:
    def __init__(self, config={}):
        self.name = config.get('name', '')
        self.running = config.get('running', False)
        self.diamond_add = config.get('diamond_add', 0)
        
    TITLE_ITEMS = {
        'train':{'name':'公爵','title_check_pos':(505, 380)},
        'judge':{'name':'法官','title_check_pos':(280, 380)},
        'architect':{'name':'建筑师','title_check_pos':(735, 380)},
        'scientist':{'name':'科学家','title_check_pos':(965, 380)},
    }