#coding: utf-8

import json

class CombatManager:
    def __init__(self, unit):
        self.owner = unit
        self.enemies = []
        self.enemyCur = None

    def update(self, deltaTime):
        enemy = None
        if self.enemyCur and not self.enemyCur.getProp('dead'):
            enemy = self.enemyCur
        else:
            for u in self.enemies:
                if not u.getProp('dead'):
                    enemy = u
                    break

        if enemy:
            self.meleeAttack(self.owner, enemy)

    def addEnemy(self, enemy):
        if enemy not in self.enemies:
            self.enemies.append(enemy)

    def meleeAttack(self, caster, target):
        print('melee attack')

