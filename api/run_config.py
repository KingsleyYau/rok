class RunConfig:
    def __init__(self, config={}):
        self.name = config.get('name', '')
        self.running = config.get('running', False)
        self.diamond_add = config.get('diamond_add', 0)