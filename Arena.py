#coding: utf-8
from Character import *
from Creature import Creature
from Weapon import Weapon
from common import CsvLoader
import time

def loadScriptsFolder(scriptFolderName):
    protos = {}
    for folder, _, fileNames in os.walk(scriptFolderName, followlinks=False):
        for fileName in fileNames:
            (name, extension) = os.path.splitext(fileName)
            if extension != '.py':
                continue
            mod = __import__(scriptFolderName + '.' + name)
            # print(dir(mod))
            proto = eval('mod.' + name)
            # print(dir(proto))
            protos[name] = proto
    return protos

ctx = {}
ctx['protosFeat'] = loadScriptsFolder('Feat')
ctx['protosClass'] = loadScriptsFolder('Class')
ctx['protosRace'] = loadScriptsFolder('Races')
ctx['protosWeapon'] = loadScriptsFolder('Weapons')
ctx['protosCreature'] = CsvLoader.loadCsvFile(r'data/beastiary.csv')

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
    player.buildByBuilder(builder, 30)
    #weapon = Weapon()

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
