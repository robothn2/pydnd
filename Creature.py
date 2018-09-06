#coding: utf-8

from Unit import Unit
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
        self.modifier.addTypedSource('ArmorClass', 'beastiary', int(self.proto['armor_bonus']), 'armor_bonus')
        self.modifier.addTypedSource('HitPoint', 'beastiary', int(self.proto['expected_hp']), 'expected_hp')
        self.modifier.addTypedSource('HitPoint', 'beastiary', int(self.proto['hp_fudge']), 'hp_fudge')
        Unit._applyAll(self)
        Unit._postApplyAll(self)
        print(self.modifier)
