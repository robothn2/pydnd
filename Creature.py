#coding: utf-8

from Unit import Unit
from Apply import *
from Item import *
import warnings, copy, json

class Creature(Unit):
    def __init__(self, ctx, name):
        super(Creature, self).__init__(ctx)
        if name in ctx['protosCreature']:
            self.proto = copy.deepcopy(ctx['protosCreature'][name])
            self.props.update(self.proto)
        else:
            warnings.warn('unknown create name: %s' % name)
        self._applyAll()

    def update(self, deltaTime):
        Unit.update(self, deltaTime)

    def _applyAll(self):
        self.modifier.updateSource(('ArmorClass', 'beastiary', 'armor_bonus'), int(self.proto['armor_bonus']))
        self.modifier.updateSource(('HitPoint', 'beastiary', 'expected_hp'), int(self.proto['expected_hp']))
        self.modifier.updateSource(('HitPoint', 'beastiary', 'hp_fudge'), int(self.proto['hp_fudge']))

        for _,ability in enumerate(['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']):
            self.modifier.updateSource(('Abilities', ability, 'Base', 'beastiary'), int(self.proto[ability]))

        buffs_apply(self)
        #race_apply(self)
        #feats_apply(self)
        abilities_apply(self)
        self.__applyAttackParameters()

        self.setProp('ac', self.modifier.sumSource(('ArmorClass')))
        self.setProp('ab', self.modifier.sumSource(('AttackBonus')))
        self.setProp('hp', self.modifier.sumSource(('HitPoint')))

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
                weapon = Weapon(self.ctx, {'BaseItem': weaponName,
                                           'BaseDamage': [1, attack[1], 1],
                                           'BaseCriticalThreat': [20, 20, len(attack) - 2]
                                           })
                weaponsCreated[weaponName] = weapon
                #print(self.getProp('name'), 'create a virtual weapon', self.proto)

                if not weaponFirst:
                    weaponFirst = weapon
            tsOffset = round(i * (self.ctx['secondsPerTurn'] / len(params)), 3)
            attacks.append((tsOffset, attack[1], True, weaponsCreated[weaponName]))

        self.modifier.updateSource(['Attacks'], attacks)

        self.setProp('WeaponMainHand', weaponFirst)

    def statistic(self):
        print('== statistics for creature', self.getProp('name'))
        print('AttackBonus', self.props['ab'])
        print('ArmorClass', self.props['ac'])
        print('HitPoint', self.props['hp'])
        print('Attacks:', self.modifier.getSource('Attacks'))
