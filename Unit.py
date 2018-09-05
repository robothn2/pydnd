#coding: utf-8
import warnings
from common import Props
from Abilities import *
from CombatManager import CombatManager

class Unit:
    def __init__(self, ctx):
        self.ctx = ctx
        self.props = Props.Props({'dead': False, 'weapon': 'unarmed',
                                  'ac': 0, 'ab': 0, 'hp': 0,
                                  'feats': {}, 'buffs': {}})
        self.modifier = Props.Modifier({'ArmorClass': {'Natural': {'BaseArmor': 10}}, 'HitPoint': {}})
        self.combat = CombatManager(self)

    def update(self, deltaTime):
        self.combat.update(deltaTime)

    def setProp(self, key, value):
        self.props[key] = value

    def getProp(self, key):
        if key in self.props:
            return self.props[key]
        return None

    def _applyAll(self):
        abilities_apply(self.props, self.modifier)

    def _postApplyAll(self):
        self.setProp('ac', self.modifier.sumTypedSourceAll('ArmorClass'))
        self.setProp('ab', self.modifier.sumTypedSourceAll('AttackBonus'))
        self.setProp('hp', self.modifier.sumTypedSourceAll('HitPoint'))

    def addFeat(self, feats, featsHint = []):
        for _, featName in enumerate(feats):
            if featName not in self.ctx['protosFeat']:
                warnings.warn('unknown feat: %s' % featName)
                continue

            hitHint = False
            for _, featHintName in enumerate(featsHint):
                '''
                result = re.match(r'%s(?P<param>\w+)' % featName, featHintName)
                if not result:
                    continue

                result.group('param'), result.group('osver'), result.group('cid'), fileFullPath)
                '''
                if len(featHintName) > len(featName) and featName == featHintName[0:len(featName)]:
                    #todo: store extra param into list
                    self.props['feats'][featHintName] = []
                    hitHint = True
                    break

            if not hitHint:
                self.props['feats'][featName] = []

    def grantSpellClass(self, spellClass, className):
        if 'spells' not in self.props:
            self.props['spells'] = {}

        spellsEntry = self.props['spells']
        if spellClass not in spellsEntry:
            spellsEntry[spellClass] = {}

        spellsClassEntry = spellsEntry[spellClass]
        if className not in spellsClassEntry:
            spellsClassEntry[className] = {}

    def grantSpells(self, spellClass, className, spells):
        pass

    def addEnemy(self, enemy):
        self.combat.addEnemy(enemy)

    def applyDamage(self, damageTotal):
        hpOld = int(self.getProp('hp'))
        hpNew = hpOld - damageTotal
        if hpNew < 0:
            hpNew = 0
        print('hp of', self.getProp('name'), 'changed:', hpOld, '->', hpNew)
        self.setProp('hp', hpNew)
        if hpNew == 0:
            self.setProp('dead', True)
            print(self.getProp('name'), 'dead')
