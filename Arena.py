#coding: utf-8
from Character import *
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
    builder = loadJsonFile(r'data/builders/builder1.json')
    print(builder)
    player = Character(ctx)
    player.buildByBuilder(builder, 5)

    monster = Creature(ctx, 'zombie')

    room = Room()
    room.addUnit(player)
    room.addUnit(monster)
    player.addEnemy(monster)
    monster.addEnemy(player)

    deltaInSeconds = 2.0
    while not player.getProp('dead') and not monster.getProp('dead'):
        room.update(deltaInSeconds)
        time.sleep(deltaInSeconds)
