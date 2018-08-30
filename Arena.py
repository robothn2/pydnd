#coding: utf-8
import Character
import Creature
import Feats
import Object
from common import CsvLoader

ctx = Object.Object()
ctx['protosFeats'] = CsvLoader.loadCsvFile(r'data/feats.csv')
ctx['protosCreatures'] = CsvLoader.loadCsvFile(r'data/beastiary.csv')

class Room:
    def __init__(self):
        self.units = []

    def addUnit(self, unit):
        self.units.append(unit)

    def update(self, deltaTime):
        for unit in self.units:
            unit.update(deltaTime)

    def getAliveUnits(self):
        return 2

if __name__ == '__main__':
    player = Character.Character(ctx)
    player.buildLevel1('human', 'female', 20, 'Lora', 'Craft', 'Ranger', 'Chaotic Neutral', 'Leira',
                     {'str': 16, 'dex': 14, 'con':10, 'int': 16, 'wis': 8, 'cha':  18},
                     {'Heal': 4, 'Intimidate': 4, 'Hide':4, 'MoveSilent': 4, 'Spot': 4, 'Listen': 4, 'Tumble': 4, 'Spellcraft': 4, 'UseMagicDevice': 4},
                     ['FavordEnemy:Humans', 'Dodge'])

    monster = Creature.Creature(ctx, 'zombie')

    room = Room()
    room.addUnit(player)
    room.addUnit(monster)
    player.setEnemy(monster)

    while room.getAliveUnits() > 1:
        room.update(20)
