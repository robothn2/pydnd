#coding: utf-8
from common import CsvLoader
import os

def loadScriptsFolder(scriptFolderPath, skipFilenames = []):
    dotedPath = scriptFolderPath.replace('/', '.')
    protos = {}
    for folder, _, fileNames in os.walk(scriptFolderPath, followlinks=False):
        for fileName in fileNames:
            (name, extension) = os.path.splitext(fileName)
            if extension != '.py':
                continue
            if name in skipFilenames:
                print('  skip file:', fileName)
                continue
            mod = __import__(dotedPath + '.' + name)
            # print(dir(mod))
            proto = eval('mod.' + name)
            # print(dir(proto))
            protos[name] = proto
    return protos

ctx = {}
ctx['protosBackground'] = loadScriptsFolder('Background')
ctx['protosDeity'] = loadScriptsFolder('Deity')
ctx['protosDomain'] = loadScriptsFolder('Domain')
ctx['protosFeat'] = loadScriptsFolder('Feat', ['Protos'])
ctx['protosClass'] = loadScriptsFolder('Class')
ctx['protosRace'] = loadScriptsFolder('Race')
ctx['protosWeapon'] = loadScriptsFolder('Weapon')
ctx['protosSpell'] = loadScriptsFolder('Spell', ['Protos'])
ctx['protosCreature'] = CsvLoader.loadCsvFile(r'data/beastiary.csv')
ctx['protosSkill'] = CsvLoader.loadCsvFile(r'data/skills.csv')
ctx['secondsPerTurn'] = 8.0
ctx['secondsPerRound'] = 8.0
ctx['Abilities'] = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
