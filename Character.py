#coding: utf-8

import os
import json
import time
import string

import Abilities
import Skills
import Feats
import CombatManager

class Character():
    def __init__(self, ctx):
        self.ctx = ctx
        self.combat = CombatManager.CombatManager(self)

    def BuildLevel1(self, race, gender, age, nameFirst, nameLast, align, cls, deity, abilities, skills, feats):
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
