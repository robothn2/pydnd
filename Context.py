#coding: utf-8
from common import CsvLoader
import os

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
ctx['protosSpell'] = loadScriptsFolder('Spell')
ctx['protosCreature'] = CsvLoader.loadCsvFile(r'data/beastiary.csv')
ctx['secondsPerTurn'] = 8.0
ctx['secondsPerRound'] = 8.0
ctx['Abilities'] = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
ctx['Skills'] = ['Appraise', 'Bluff', 'Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap',
                    'CraftWeapon', 'Diplomacy', 'DisableDevice','Heal', 'Hide', 'Intimidate', 'Listen',
                    'Lore', 'MoveSilently', 'Parry', 'Perform', 'Search', 'SetTrap', 'SleightOfHand',
                    'Spellcraft', 'Spot', 'Survival', 'Taunt', 'Tumble', 'UseMagicDevice']