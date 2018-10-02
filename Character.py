#coding: utf-8

from Skills import *
from Unit import *
from Apply import *
from Abilities import *
import Damages
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
        self.builder = {'name': '', **abilities_parse(8, 8, 8, 8, 8, 8)}
        self.calc.addSource('ArmorClass.Natural', name='Character', calcInt=10)

    def getName(self):
        return self.builder['name']

    def buildLevel1(self, props, cls, abilities, skills, feats):
        if cls not in self.ctx['protosClass']:
            return False
        self.props.update({**props, **abilities_parse(abilities)})
        self.setProp('classes', {cls: {'level': 1, 'proto': self.ctx['protosClass'][cls]}})
        self.setProp('skills', skills_parse(skills))
        self.addFeats(feats)

        self._applyAll()
        return True

    def buildByBuilder(self, builder, levelRequest):
        if not isinstance(builder, dict):
            return False
        if levelRequest < 1:
            return False

        self.builder = builder
        print('loading builder:', builder['builderName'])
        '''
        'name': 'Lora',
        'race': 'Yuan-ti Pureblood',
        'gender': 'female',
        'age': 20,
        'deity': 'Leira',
        'alignment': 'ChaoticNeutral',
        'background': 'WildChild',
        'abilities': {'Str': 16, 'Dex': 12, 'Con': 10, 'Int': 14, 'Wis': 8, 'Cha': 16},
       '''
        for key in builder.keys():
            if key in ['', 'race', 'gender', 'age', 'deity', 'alignment', 'background']:
                self.props[key] = builder[key]

        race_apply(self)
        for k, v in builder['abilities'].items():
            self.modifier.updateSource(('Abilities', k, 'Base', 'Builder'), int(v))

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

            # check class name existence
            cls = levelEntry['class']
            if cls not in self.ctx['protosClass']:
                warnings.warn('unknown character class: %s at level %d' % (cls, level))
                return False
            clsProto = self.ctx['protosClass'][cls]

            # add ability
            if 'ability' in levelEntry:
                self.modifier.updateSource(('Abilities', levelEntry['ability'], 'Base', 'LevelUp:%d'%level), 1)

            if 'classes' not in self.props:
                self.props['classes'] = {}
            classesEntry = self.props['classes']
            if cls not in classesEntry:
                classesEntry[cls] = {'level': 0, 'proto': clsProto}
            clsEntry = classesEntry[cls]
            clsEntry['level'] += 1

            # apply class feats/abilities by level
            clsProto.applyLevelUp(self, clsEntry['level'], levelEntry)

            # add feats
            if 'feats' in levelEntry:
                for _, featEntry in enumerate(levelEntry['feats']):
                    if type(featEntry) == str:
                        self.addFeat(featEntry, levelEntry.get('featsHint'))
                    elif len(featEntry) == 2:
                        self.addFeat(featEntry[0], featEntry[1])

            # update skills
            for skillName,skillLevel in levelEntry['skills'].items():
                self.modifier.updateSource(('Skills', skillName, 'Base', 'Builder'), skillLevel)

        return True

    def _applyAll(self):
        race_apply(self)
        classes_apply(self)
        buffs_apply(self)
        feats_apply(self)
        abilities_apply(self)
        skills_apply(self)
        weapon_apply(self)

        self.setProp('ac', self.modifier.sumSource(('ArmorClass')))
        self.setProp('ab', self.modifier.sumSource(('AttackBonus')))
        self.setProp('hp', self.modifier.sumSource(('HitPoint')))

    def printProp(self, key):
        print(key, ':', self.calc.calcValue(key), ',', self.modifier.getSource(key))

    def statistic(self):
        self._applyAll()
        print('== statistics for character', self.getName())
        print('Feats:', self.modifier.getSource('Feats'))
        print('Abilities:', self.modifier.getSource('Abilities'))
        self.printProp('AttackBonus')
        self.printProp('ArmorClass')
        self.printProp('HitPoint')
        self.printProp('SpellResistance')
        self.printProp('Reduction')
        self.printProp('SpellCasting')
        print('BAB:', self.modifier.sumSource(('AttackBonus', 'Base')))
        print('Attacks:', self.modifier.getSource('Attacks'))

    def getAttackBonus(self, target):
        # ab from Buff, Feats, Str, except Weapon, Base
        result = Damages.Result('AttackBonus')
        result.addAdditionalSources(self.modifier)
        result.addAdditionalSources(self.modifierBuff)
        result.addConditionalTargetSources(self.modifier, self, target)
        return result.calcTotal()

    def getArmorClass(self, target):
        # ac from Buff, Feats, Dex, Armor, Shield
        result = Damages.Result('ArmorClass')
        result.addBaseSources(self.modifier)
        result.addAdditionalSources(self.modifier)
        result.addAdditionalSources(self.modifierBuff)
        result.addConditionalTargetSources(self.modifier, self, target)
        print('getArmorClass', result.modifier)
        return result.calcTotal()


    def addXP(self, xp):
        xpOld = self.getProp('xp')
        xpNew = xpOld + xp
        self.setProp('xp', xpNew)
        print(self.getName(), 'received xp', xp, ',total', xpNew)

if __name__ == '__main__':
    builder = loadJsonFile(r'data/builders/builder1.json')
    player = Character(__import__('Context').ctx)
    player.buildByBuilder(builder, 30)
    player.addFeat('FavoredEnemy', [['FavoredEnemy', 'Dragons']])
    player.addFeat('FavoredEnemy', 'Elves')
    player.addFeat('Dodge', 'Elves')
    print('Feats:', player.modifier.getSource('Feats'))
