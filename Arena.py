#coding: utf-8
from Character import Character
from Creature import Creature
from Object import Object
from common import CsvLoader
import time

ctx = Object()
ctx['protosFeat'] = CsvLoader.loadCsvFile(r'data/feats.csv')
ctx['protosCreature'] = CsvLoader.loadCsvFile(r'data/beastiary.csv')
ctx['protosClass'] = CsvLoader.loadCsvFile(r'data/classes.csv')

class Room:
    def __init__(self):
        self.units = []

    def addUnit(self, unit):
        self.units.append(unit)

    def update(self, deltaTime):
        for unit in self.units:
            unit.update(deltaTime)

if __name__ == '__main__':
    player = Character(ctx)
    player.buildLevel1({'race':'human', 'gender':'female', 'age':20, 'name':'Lora', 'deity':'Leira',
                        'alignment':'ChaoticNeutral'},
                        'Ranger',
                        {'Str': 16, 'Dex': 14, 'Con':10, 'Int': 16, 'Wis': 8, 'Cha':  18},
                        {'Heal': 4, 'Intimidate': 4, 'Hide':4, 'MoveSilent': 4, 'Spot': 4, 'Listen': 4, 'Tumble': 4, 'Spellcraft': 4, 'UseMagicDevice': 4},
                        ['FavoredEnemy:Undead', 'Dodge'])

    monster = Creature(ctx, 'badger')

    room = Room()
    room.addUnit(player)
    room.addUnit(monster)
    player.addEnemy(monster)
    monster.addEnemy(player)

    deltaInSeconds = 2.0
    while not player.getProp('dead') and not monster.getProp('dead'):
        room.update(deltaInSeconds)
        time.sleep(deltaInSeconds)
