#coding: utf-8
import json
from enum import Enum
Skill = Enum('Skill', ('Appraise', 'Bluff', 'Concentration', 'DisableTrap', 'Heal', 'Hide', 'Intimidate',
                       'Listen', 'Lore', 'MoveSilent', 'Spot', 'Spellcraft', 'Taunt', 'Tumble',
                       'UseMagicDevice'))

class Skills:
    def __init__(self, skills):
        self.d = [0] * len(Skill)

        if type(skills) is dict:
            for k,v in skills.items():
                if Skill[k]:
                    self.d[Skill[k].value - 1] = int(v)
                else:
                    print('  unknown skill:', k, v)

        print('  skills:', str(self))

    def __str__(self):
        ret = ''
        for name, member in Skill.__members__.items():
            skillLevel = self.d[member.value - 1]
            if skillLevel > 0:
                ret += name + ':' + str(skillLevel) + ','
        return ret

if __name__ == '__main__':
    ab = Skills({'Concentration': 4, 'SpellCraft': 1, 'Tumble': 3, 'Lore': 4})
