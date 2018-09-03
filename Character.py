#coding: utf-8

from Skills import *
from Feats import *
from Unit import *
from Classes import *
import json
import warnings

def loadJsonFile(builderJsonFile):
    with open(builderJsonFile, encoding='utf-8') as f:
        builder = json.load(f)
        if len(builder) == 0:
            warnings.warn('fail to read builder file: %s' % builderJsonFile)
            return None
        return builder

class Character(Unit):
    def __init__(self, ctx):
        super(Character, self).__init__(ctx)
        self.ctx = ctx
        self.props = { **self.props, 'name': 'NoName',
                      **abilities_parse(10, 10, 10, 10, 10, 10)}

    def buildLevel1(self, props, cls, abilities, skills, feats):
        if cls not in self.ctx['protosClass']:
            return False
        self.props = {**self.props, **props, **abilities_parse(abilities)}
        self.setProp('classes', {cls: {'level': 1, 'proto': self.ctx['protosClass'][cls]}})
        self.setProp('skills', skills_parse(skills))
        self.setProp('feats', feats_parse(feats, self.ctx['protosFeat']))
        self.setProp('buffs', {})

        self._applyAll()
        return True

    def buildByBuilder(self, builder, levelRequest):
        if not isinstance(builder, dict):
            return False
        if levelRequest < 1:
            return False

        print('loading builder:', builder['name'])
        '''
        'charName': 'Lora',
        'race': 'Yuan-ti Pureblood',
        'gender': 'female',
        'age': 20,
        'deity': 'Leira',
        'alignment': 'ChaoticNeutral',
        'background': 'WildChild',
        'abilities': {'Str': 16, 'Dex': 14, 'Con': 10, 'Int': 16, 'Wis': 8, 'Cha': 18},
       '''
        self.props = {**self.props, 'name': builder['charName'], **builder['abilities']}
        for key in builder.keys():
            if key in ['race', 'gender', 'age', 'deity', 'alignment', 'background']:
                self.props[key] = builder[key]

        '''
        'levels': [
            {'level': 1, 'class': 'Ranger', 'feats': ['FavoredEnemy(Humans)', 'Dodge'],
             'skills': {'CraftWeapon': 4, 'Heal': 4, 'Hide': 4, 'Intimidate': 2, 'MoveSilently': 4, 'Spellcraft': 1,
                        'Spot': 4, 'Tumble': 2, 'UseMagicDevice': 2}},
       '''
        for i, levelEntry in enumerate(builder['levels']):
            level = i + 1
            if level > levelRequest:
                break

            # add ability
            if 'ability' in levelEntry:
                self.modifier.addSource(levelEntry['ability'], 1, ('LevelUp:%d'%level))

            # add class level
            cls = levelEntry['class']
            if 'classes' not in self.props:
                self.props['classes'] = {cls: {'level': 1, 'proto': self.ctx['protosClass'][cls]}}
                continue
            classesEntry = self.props['classes']
            if cls not in classesEntry:
                classesEntry[cls] = {'level': 1, 'proto': self.ctx['protosClass'][cls]}
                continue
            classesEntry[cls]['level'] += 1

            # todo: apply class feats by level

            # add feats
            if 'feats' in levelEntry:
                for _, featName in enumerate(levelEntry['feats']):
                    if featName in self.ctx['protosFeat']:
                        self.props['feats'][featName] = self.ctx['protosFeat'][featName]

            # update skills
            if 'skills' in self.props:
                self.props['skills'].update(levelEntry['skills'])
            else:
                self.props['skills'] = levelEntry['skills']

        self._applyAll()
        return True

    def _applyAll(self):
        classes_apply(self.getProp('classes'), self.modifier)
        Unit._applyAll(self)
        Unit._postApplyAll(self)
        print(self.modifier)
        print(self.props)

