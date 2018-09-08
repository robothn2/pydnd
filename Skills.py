#coding: utf-8

from enum import Enum
Skill = Enum('Skill', ('Appraise', 'Bluff', 'Concentration', 'DisableTrap', 'Heal', 'Hide', 'Intimidate',
                       'Listen', 'Lore', 'MoveSilent', 'Spot', 'Spellcraft', 'Taunt', 'Tumble',
                       'UseMagicDevice'))

#     sk = skills_parse({'Concentration': 4, 'SpellCraft': 1, 'Tumble': 3, 'Lore': 4})
def skills_parse(skills):
    d = [0] * len(Skill)

    if type(skills) is dict:
        for k,v in skills.items():
            if Skill[k]:
                d[Skill[k].value - 1] = int(v)
            else:
                print('  unknown skill:', k, v)
    return d
