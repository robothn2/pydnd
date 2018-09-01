#coding: utf-8

import os
import json
import time
import string

import Abilities
import Skills
import Feats
import Unit

class Character(Unit.Unit):
    def __init__(self, ctx):
        super(Character, self).__init__(ctx)
        self.ctx = ctx

    def buildLevel1(self, race, gender, age, nameFirst, nameLast, align, cls, deity, abilities, skills, feats):
        self.race = race
        self.gender = gender
        self.age = age
        self.nameFirst = nameFirst
        self.nameLast = nameLast
        self.cls = cls
        self.deity = deity
        self.abilities = Abilities.Abilities(abilities)
        self.skills = Skills.Skills(skills)
        self.feats = Feats.Feats(feats, self.ctx['protosFeats'])
        self.__updateProps()

    def __updateProps(self):
        pass

