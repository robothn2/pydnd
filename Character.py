#coding: utf-8

from Skills import *
from Feats import *
from Unit import *
from Classes import *

class Character(Unit):
    def __init__(self, ctx):
        super(Character, self).__init__(ctx)
        self.ctx = ctx

    def buildLevel1(self, props, cls, abilities, skills, feats):
        if cls not in self.ctx['protosClass']:
            return False
        self.props = {**self.props, **props, **abilities_parse(abilities)}
        Unit.setProp(self, 'classes', {cls: {'level': 1, 'proto': self.ctx['protosClass'][cls]}})
        Unit.setProp(self, 'skills', skills_parse(skills))
        Unit.setProp(self, 'feats', feats_parse(feats, self.ctx['protosFeat']))
        Unit.setProp(self, 'buffs', {})

        self._applyAll()
        return True

    def _applyAll(self):
        classes_apply(self.getProp('classes'), self.modifier)
        Unit._applyAll(self)
        Unit._postApplyAll(self)
        print(self.modifier)
        print(self.props)
