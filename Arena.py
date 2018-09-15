#coding: utf-8
from Character import *
from Creature import Creature
from Item import *
from common import CsvLoader
import time, os

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
ctx['protosBackground'] = loadScriptsFolder('Background')
ctx['protosDeity'] = loadScriptsFolder('Deity')
ctx['protosDomain'] = loadScriptsFolder('Domain')
ctx['protosFeat'] = loadScriptsFolder('Feat')
ctx['protosClass'] = loadScriptsFolder('Class')
ctx['protosRace'] = loadScriptsFolder('Race')
ctx['protosWeapon'] = loadScriptsFolder('Weapon')
ctx['protosCreature'] = CsvLoader.loadCsvFile(r'data/beastiary.csv')
ctx['secondsPerTurn'] = 8.0

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
    #print(builder)
    player = Character(ctx)
    player.buildByBuilder(builder, 30)
    player.setProp('WeaponMainHand', Weapon(ctx, {'name': 'DemoWeapon','BaseItem': 'Kukri', 'Enhancement': 3}))
    player.setProp('WeaponOffHand', Weapon(ctx, {'name': 'DemoOffhandWeapon','BaseItem': 'Kukri', 'Enhancement': 2}))
    player.statistic()

    monster = Creature(ctx, 'adult red dragon')

    room = Room()
    room.addUnit(player)
    room.addUnit(monster)
    player.addEnemy(monster)
    monster.addEnemy(player)

    deltaInSeconds = 0.05
    while not player.getProp('dead') and not monster.getProp('dead'):
        room.update(deltaInSeconds)
        time.sleep(deltaInSeconds)
