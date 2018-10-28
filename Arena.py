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
        self.units = [x for x in self.units if not x.isDead()] # remove dead units
        for unit in self.units:
            unit.update(deltaTime)

if __name__ == '__main__':
    player = Character(Context.ctx)
    #player.buildByBuilder(loadJsonFile(r'data/builders/TwoWeaponRanger.json'), 30)
    #player.equipWeapon('MainHand', Weapon(Context.ctx, {'BaseItem': 'Kukri', 'Enhancement': 3}))
    #player.equipWeapon('OffHand', Weapon(Context.ctx, {'name': 'OHWeapon','BaseItem': 'Kukri', 'Enhancement': 2}))
    #player.addBuff(player, Context.ctx['Spell']['DivineFavor'])
    #player.addBuff(player, Context.ctx['Spell']['Barkskin'])
    #player.addBuff(player, Context.ctx['Spell']['CatGrace'])
    player.buildByBuilder(loadJsonFile(r'data/builders/DragonMasterNegotiator.json'), 30)
    player.equipWeapon('TwoHand', Weapon(Context.ctx, {'BaseItem': 'Falchion', 'Enhancement': 3}))
    player.statistic()
    player.activate('PowerAttack')

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
