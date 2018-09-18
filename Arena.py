#coding: utf-8
from Character import *
from Creature import Creature
from Item import *
import Context
import time

class Arena:
    def __init__(self):
        self.units = []

    def addUnit(self, unit):
        self.units.append(unit)

    def update(self, deltaTime):
        self.units = [x for x in self.units if not x.isDead()]
        for unit in self.units:
            unit.update(deltaTime)

if __name__ == '__main__':
    builder = loadJsonFile(r'data/builders/builder1.json')
    player = Character(Context.ctx)
    player.buildByBuilder(builder, 30)
    player.setProp('WeaponMainHand', Weapon(Context.ctx, {'name': 'DemoWeapon','BaseItem': 'Kukri', 'Enhancement': 3}))
    player.setProp('WeaponOffHand', Weapon(Context.ctx, {'name': 'DemoOffhandWeapon','BaseItem': 'Kukri', 'Enhancement': 2}))
    player.statistic()

    arena = Arena()
    arena.addUnit(player)

    deltaInSeconds = 0.05
    while not player.isDead():
        if len(arena.units) == 1:
            monster = Creature(Context.ctx, 'adult red dragon')
            arena.addUnit(monster)
            player.addEnemy(monster)
            monster.addEnemy(player)

        arena.update(deltaInSeconds)
        time.sleep(deltaInSeconds)
