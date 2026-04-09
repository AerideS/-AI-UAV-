import numpy as np

class RiskField:
    def __init__(self, name, level, obstacles=None):
        self.name = name
        self.level = level
        self.obstacles = [] if obstacles is None else list(obstacles)