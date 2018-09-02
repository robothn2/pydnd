#coding: utf-8

from Unit import Unit
import warnings

class Creature(Unit):
    def __init__(self, ctx, name):
        super(Creature, self).__init__(ctx)
        if name in ctx['protosCreature']:
            self.props.update(ctx['protosCreature'][name])
        else:
            warnings.warn('unknown create name: %s' % name)
        self._applyAll()
        self._postApplyAll()

    def update(self, deltaTime):
        Unit.update(self, deltaTime)
