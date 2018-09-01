#coding: utf-8

import json
import CombatManager

class Unit:
    def __init__(self, ctx):
        self.ctx = ctx
        self.props = {'dead': False}
        self.combat = CombatManager.CombatManager(self)

    def update(self, deltaTime):
        print('Unit.update', deltaTime)
        self.combat.update(deltaTime)

    def setProp(self, key, value):
        self.props[key] = value
    def getProp(self, key):
        if key in self.props:
            return self.props[key]
        return None

    def addEnemy(self, enemy):
        self.combat.addEnemy(enemy)

