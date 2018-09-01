#coding: utf-8

from Unit import Unit
import warnings

class Creature(Unit):
    def __init__(self, ctx, name):
        super(Creature, self).__init__(ctx)
        if name in ctx['protosCreatures']:
            self.props.update(ctx['protosCreatures'][name])
        else:
            warnings.warn('unknown create name: %s' % name)
        Unit.setProp(self, 'FinalAttackBonus', 0)

    def update(self, deltaTime):
        Unit.update(self, deltaTime)