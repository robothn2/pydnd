#coding: utf-8
from common import CsvLoader
import os

def loadScriptsFolder(protos, scriptFolderPath, skipFilenames = []):
    dotedPath = scriptFolderPath.replace('/', '.')
    for folder, _, fileNames in os.walk(scriptFolderPath, followlinks=False):
        for fileName in fileNames:
            (name, extension) = os.path.splitext(fileName)
            #print(name, extension)
            if extension != '.py':
                continue
            if name in skipFilenames:
                print('  skip file:', fileName)
                continue

            mod = __import__(dotedPath + '.' + name, fromlist=['register'])
            #print(dir(mod))
            mod.register(protos)

ctx = {
    'secondsPerTurn': 6.0,
    'secondsPerRound': 6.0,
    'Abilities': ('Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha'),

    'Background': {},
    'Deity': {},
    'Domain': {},
    'FeatGroup': {},
    'Feat': {},
    'Class': {},
    'Race': {},
    'Weapon': {},
    'Spell': {},
    'Buff': {},
    'Skill': {},
    'Creature': {},
}

loadScriptsFolder(ctx, 'data/nwn2/Race')
loadScriptsFolder(ctx, 'data/nwn2/Class')
loadScriptsFolder(ctx, 'data/nwn2/Domain')
loadScriptsFolder(ctx, 'data/nwn2/Deity')
loadScriptsFolder(ctx, 'data/nwn2/Feat')
loadScriptsFolder(ctx, 'data/nwn2/Spell')
loadScriptsFolder(ctx, 'data/nwn2/Weapon')
ctx['Skill'] = CsvLoader.loadCsvFile(r'data/skills.csv')
ctx['Creature'] = CsvLoader.loadCsvFile(r'data/beastiary.csv')
