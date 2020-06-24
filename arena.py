#coding: utf-8
from player import Player, load_json_file
from creature import Creature
from context import ctx
from models import create_weapon
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
  player = Player(ctx)
  player.buildByBuilder(load_json_file(r'data/builders/TwoWeaponRanger.json'), 30)
  player.equipWeapon('MainHand', create_weapon(ctx, 'Kukri', enhancement=3))
  player.equipWeapon('OffHand', create_weapon(ctx, 'Kukri', enhancement=2, name='OHWeapon'))
  player.addBuff(player, ctx['Spell']['Divine Favor'])
  player.addBuff(player, ctx['Spell']['Barkskin'])
  player.addBuff(player, ctx['Spell']['Cat\'s Grace'], metaMagics=['Empower'])
  #player.buildByBuilder(load_json_file(r'data/builders/DragonMasterNegotiator.json'), 30)
  #player.equipWeapon('TwoHand', create_weapon(Context.ctx, 'Falchion', enhancement=3))
  player.applyAll()
  player.statistic()
  player.active('Power Attack')
  player.castSpell('Divine Might', player, metaMagics=['Empower'])

  arena = Arena()
  arena.addUnit(player)

  deltaInSeconds = 0.05
  while not player.isDead():
    if len(arena.units) == 1:
      monster = Creature(ctx, 'adult red dragon')
      arena.addUnit(monster)
      player.addEnemy(monster)
      monster.addEnemy(player)

    arena.update(deltaInSeconds)
    time.sleep(deltaInSeconds)
