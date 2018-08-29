#coding: utf-8

import json

class CombatManager:
    def __init__(self, unit):
        self.owner = unit
        self.enemies = {}

    def update(self, deltaTime):
        pass
