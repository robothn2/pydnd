#coding: utf-8
from Character import *
from Creature import Creature
from Item import *
import Context
import time
from Models import create_weapon

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
    player.buildByBuilder(loadJsonFile(r'data/builders/TwoWeaponRanger.json'), 30)
    player.equipWeapon('MainHand', create_weapon(Context.ctx, 'Kukri', enhancement=3))
    player.equipWeapon('OffHand', create_weapon(Context.ctx, 'Kukri', enhancement=2, name='OHWeapon'))
    player.addBuff(player, Context.ctx['Spell']['Divine Favor'])
    player.addBuff(player, Context.ctx['Spell']['Barkskin'])
    player.addBuff(player, Context.ctx['Spell']['Cat\'s Grace'], ['Empower'])
    #player.buildByBuilder(loadJsonFile(r'data/builders/DragonMasterNegotiator.json'), 30)
    #player.equipWeapon('TwoHand', create_weapon(Context.ctx, 'Falchion', enhancement=3))
    player.applyAll()
    player.statistic()
    player.activate('Power Attack')

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
