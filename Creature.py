#coding: utf-8

from Unit import Unit
from Apply import *
import warnings
import copy
class Creature(Unit):
    def __init__(self, ctx, name):
        super(Creature, self).__init__(ctx)
        if name in ctx['protosCreature']:
            self.proto = copy.deepcopy(ctx['protosCreature'][name])
            self.props.update(self.proto)
        else:
            warnings.warn('unknown create name: %s' % name)
        self._applyAll()
        self._postApplyAll()

    def update(self, deltaTime):
        Unit.update(self, deltaTime)

    def _applyAll(self):
        self.modifier.updateSource(('ArmorClass', 'beastiary', 'armor_bonus'), int(self.proto['armor_bonus']))
        self.modifier.updateSource(('HitPoint', 'beastiary', 'expected_hp'), int(self.proto['expected_hp']))
        self.modifier.updateSource(('HitPoint', 'beastiary', 'hp_fudge'), int(self.proto['hp_fudge']))

        buffs_apply(self)
        race_apply(self)
        feats_apply(self)
        abilities_apply(self)

        Unit._postApplyAll(self)
        print(self.modifier)
