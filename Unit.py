#coding: utf-8

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
        #armor class
        ac = 0
        for acType in self.modifier['ArmorClass'].values():
            for acSource in acType.values():
                ac += acSource
        self.setProp('ac', ac)

        #attack bonus
        ab = 0
        for abType in self.modifier['AttackBonus'].values():
            for abSource in abType.values():
                ab += abSource
        self.setProp('ab', ab)

        #hp
        hp = int(self.getProp('hp'))
        for hpSource in self.modifier['HitPoint'].values():
            hp += hpSource
        self.setProp('hp', hp)

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
