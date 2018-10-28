#coding: utf-8

from Skills import *
from Unit import *
from Apply import *
from Abilities import *
import CalcResult
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
        if cls not in self.ctx['Class']:
            return False
        self.props.update({**props, **abilities_parse(abilities)})
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

        race_apply(self, builder['race'])
        for k, v in builder['abilities'].items():
            self.calc.addSource('Ability.%s.Base' % k, name='Builder', calcInt=int(v))

        '''
        'levels': [
            {'level': 1, 'class': 'Ranger', 'feats': ['FavoredEnemy(Humans)', 'Dodge'],
             'skills': {'CraftWeapon': 4, 'Heal': 4, 'Hide': 4, 'Intimidate': 2, 'MoveSilently': 4, 'Spellcraft': 1,
                        'Spot': 4, 'Tumble': 2, 'UseMagicDevice': 2}},
       '''

        classLevels = self.calc.getProp('Class.Level')
        for i, levelEntry in enumerate(builder['levels']):
            level = i + 1
            if level > levelRequest:
                break

            # check class name existence
            cls = levelEntry['class']
            if cls not in self.ctx['Class']:
                warnings.warn('unknown character class: %s at level %d' % (cls, level))
                return False
            clsProto = self.ctx['Class'][cls]

            # add ability
            if 'ability' in levelEntry:
                self.calc.addSource('Ability.%s.Base' % levelEntry['ability'], name='LevelUp:%d'%level, calcInt=1)

            # update Class.Level, bab, SavingThrows, HitPoint
            clsLevel = classLevels.calcSingleSource(cls, self, None)
            clsLevel += 1
            self.calc.addSource('Class.Level', name=cls, calcInt=clsLevel)
            clsSpellType = clsProto.proto.get('SpellType')
            if clsSpellType:
                self.calc.addSource('Caster.Level', name=cls, calcInt=clsLevel)
            self.calc.addSource('AttackBonus.Base', name=cls, calcInt=int(clsLevel * float(clsProto.proto['BaseAttackBonus'])))
            self.calc.addSource('SavingThrow.Fortitude', name=cls, calcInt=int(clsLevel * float(clsProto.proto['FortitudePerLevel'])))
            self.calc.addSource('SavingThrow.Reflex', name=cls, calcInt=int(clsLevel * float(clsProto.proto['ReflexPerLevel'])))
            self.calc.addSource('SavingThrow.Will', name=cls, calcInt=int(clsLevel * float(clsProto.proto['WillPerLevel'])))
            self.calc.addSource('HitPoint', name=cls, calcInt=clsLevel*int(clsProto.proto['HitDie']))

            # apply class feats/abilities by level
            clsProto.levelUp(self, clsLevel, levelEntry)

            # add feats
            if 'feats' in levelEntry:
                for _, featEntry in enumerate(levelEntry['feats']):
                    if type(featEntry) == str:
                        self.addFeat(featEntry, levelEntry.get('featsHint'))
                    elif len(featEntry) == 2:
                        self.addFeat(featEntry[0], featEntry[1])

            # update skills
            for skillName,skillLevel in levelEntry['skills'].items():
                self.calc.addSource('Skill.%s'% skillName, name='Builder', calcInt=skillLevel)

        return True

    def equipWeapon(self, hand, weapon):
        if hand == 'TwoHand':
            self.unequipWeapon('TwoHand')
            self.unequipWeapon('MainHand')
            self.unequipWeapon('OffHand')
        elif hand == 'MainHand':
            self.unequipWeapon('TwoHand')
            self.unequipWeapon('MainHand')
        else:
            self.unequipWeapon('TwoHand')
            self.unequipWeapon('OffHand')

        weapon.apply(self, hand)

    def unequipWeapon(self, hand):
        weaponExist = self.calc.getObject(('Weapon', hand))
        if weaponExist:
            weaponExist.unapply(self, hand)

    def _applyAll(self):
        feats_apply(self)

        self.setProp('hp', self.calc.calcPropValue('HitPoint', self, None))

    def statistic(self):
        self._applyAll()
        print('== statistics for character', self.getName())
        print('Feats:', self.modifier.getSource('Feats'))
        print('Abilities:', self.calc.getProp('Ability'))
        self.printProp('AttackBonus.Base')
        self.printProp('ArmorClass')
        self.printProp('HitPoint')
        self.printProp('SpellResistance')
        self.printProp('SavingThrow.Fortitude')
        self.printProp('SavingThrow.Reflex')
        self.printProp('SavingThrow.Will')

        #self.printProp('Reduction')
        print('Attacks:', self.calc.calcPropValue('Attacks', self, None))

    def addXP(self, xp):
        xpOld = self.getProp('xp')
        xpNew = xpOld + xp
        self.setProp('xp', xpNew)
        print(self.getName(), 'received xp', xp, ',total', xpNew)

if __name__ == '__main__':
    builder = loadJsonFile(r'data/builders/TwoWeaponRanger.json')
    player = Character(__import__('Context').ctx)
    player.buildByBuilder(builder, 30)
    player.addFeat('FavoredEnemy', [['FavoredEnemy', 'Dragons']])
    player.addFeat('FavoredEnemy', 'Elves')
    player.addFeat('Dodge', 'Elves')
    print('Feats:', player.modifier.getSource('Feats'))
