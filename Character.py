#coding: utf-8

import os
import json
import time
import string

from Abilities import parse_abilities
from Skills import parse_skills
from Feats import parse_feats
from Unit import Unit

class Character(Unit):
    def __init__(self, ctx):
        super(Character, self).__init__(ctx)
        self.ctx = ctx

    def buildLevel1(self, props, cls, abilities, skills, feats):
        self.props = {**self.props, **props, **parse_abilities(abilities)}
        Unit.setProp(self, 'classList', [cls])
        Unit.setProp(self, 'skills', parse_skills(skills))
        Unit.setProp(self, 'feats', parse_feats(feats, self.ctx['protosFeats']))

        self.__updateProps()

    def __updateProps(self):
        Unit.setProp(self, 'FinalAttackBonus', (self.getProp('Str') - 10)/2)
        Unit.setProp(self, 'ac', 10 + (self.getProp('Dex') - 10)/2)
        Unit.setProp(self, 'hp', 20)
        print(self.props)

