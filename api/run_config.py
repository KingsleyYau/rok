class RunConfig:
    def __init__(self, config={}):
        self.name = config.get('name', '')
        self.running = config.get('running', False)