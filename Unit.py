#coding: utf-8

import json
from CombatManager import CombatManager

class Unit:
    def __init__(self, ctx):
        self.ctx = ctx
        self.props = {'dead': False, 'weapon': 'unarmed'}
        self.combat = CombatManager(self)

    def update(self, deltaTime):
        #print('Unit.update', deltaTime)
        self.combat.update(deltaTime)

    def setProp(self, key, value):
        self.props[key] = value
    def getProp(self, key):
        if key in self.props:
            return self.props[key]
        return None

    def addEnemy(self, enemy):
        self.combat.addEnemy(enemy)

    def applyDamage(self, damageTotal):
        hpOld = int(self.getProp('hp'))
        hpNew = hpOld - damageTotal
        if hpNew < 0:
            hpNew = 0
        print('hp of', self.getProp('name'), 'changed:', hpOld, '->', hpNew)
        self.setProp('hp', hpNew)
        if hpNew == 0:
            self.setProp('dead', True)
            print(self.getProp('name'), 'dead')
