#coding: utf-8

from Unit import Unit
from Apply import *
from Item import *
import warnings, copy, json

class Creature(Unit):
    def __init__(self, ctx, name):
        super(Creature, self).__init__(ctx)
        if name in ctx['Creature']:
            self.proto = copy.deepcopy(ctx['Creature'][name])
            self.props.update(self.proto)
        else:
            warnings.warn('unknown create name: %s' % name)
        self._applyAll()

    def update(self, deltaTime):
        Unit.update(self, deltaTime)

    def _applyAll(self):
        self.calc.addSource('ArmorClass.Natural', name='beastiary', calcInt=int(self.proto['armor_bonus']))
        self.calc.addSource('HitPoint', name='beastiary.expected_hp', calcInt=int(self.proto['expected_hp']))
        self.calc.addSource('HitPoint', name='beastiary.hp_fudge', calcInt=int(self.proto['hp_fudge']))

        for _,ability in enumerate(self.ctx['Abilities']):
            self.calc.addSource('Ability.'+ ability + '.Base', name='beastiary', calcInt=int(self.proto[ability]))

        feats_apply(self)
        self.__applyAttackParameters()

        self.setProp('hp', self.calc.calcPropValue('HitPoint', self, None))
        self.statistic()
        print(self.modifier)

    def __applyAttackParameters(self):
        params = json.loads(self.proto['attack_parameters'])
        if type(params) != list or len(params) == 0:
            return

        attacks = []
        weaponsCreated = {}
        weaponFirst = None
        for i, attack in enumerate(params):
            weaponName = attack[0]
            if weaponName not in weaponsCreated:
                # create a virtual weapon
                weapon = Weapon(self.ctx, {'BaseItem': weaponName,
                                           'BaseDamage': [1, attack[1], 1],
                                           'BaseCriticalThreat': [20, 20, len(attack) - 2]
                                           })
                weaponsCreated[weaponName] = weapon

                if not weaponFirst:
                    weaponFirst = weapon
            tsOffset = round(i * (self.ctx['secondsPerTurn'] / len(params)), 3)
            attacks.append((tsOffset, attack[1], 'MainHand', weaponsCreated[weaponName]))

        self.calc.addSource('Attacks', name='MainHand', calcInt=attacks)

        self.setProp('WeaponMainHand', weaponFirst)

    def statistic(self):
        print('== statistics for creature', self.getName())
        self.printProp('AttackBonus.Base')
        self.printProp('ArmorClass')
        self.printProp('HitPoint')
        print('Attacks:', self.modifier.getSource('Attacks'))
        print('== statistics end')
