#coding: utf-8
from Models import Class

name = 'RedDragonDisciple'

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeats(['Natural Armor Increase', 'Draconic Ability Scores'])
    elif level == 3:
        unit.addFeat('Breath Weapon')
    elif level == 5:
        unit.addFeat('Blind-Fight')
    elif level == 10:
        unit.addFeat('Half-Dragon')

proto = {
    'desc': '''It is known that certain dragons can take humanoid form and even have humanoid lovers. Sometimes a child is born of this union, and every child of that child unto the thousandth generation claims a bit of dragon blood, be it ever so small. Usually, little comes of it, though mighty sorcerers occasionally credit their powers to draconic heritage. For some, however, dragon blood beckons irresistibly. These characters become dragon disciples, who use their magical power as a catalyst to ignite their dragon blood, realizing its fullest potential. Members of this prestige class draw on the potent blood of red dragons coursing in their veins. Though red dragons are among the most cruel and evil creatures on Faerûn, red dragon disciples may be of any alignment.''',
    'Requirements': (('Skill', 'Lore', 8), ('Class', ('Bard', 'Sorcerer'))),
    'Hit Die': 'd12',
    'Base Attack Bonus': 'Medium.',
    'High Saves': 'Fortitude and Will.',
    'Weapon Proficiencies': 'None.',
    'Armor Proficiencies': 'None.',
    'Skill Points': '2 + Int modifier.',
    'Class Skills': ['Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Diplomacy', 'Listen', 'Lore', 'Parry', 'Search', 'Spellcraft', 'Spot'],
    'BonusFeats': (
        (1, ['NaturalArmorIncrease', 'DraconicAbilityScores']),
        (3, ['BreathWeapon']),
        (5, ['BlindFight']),
        (10, ['HalfDragon'])
    ),
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'] = Class(name, **proto)
