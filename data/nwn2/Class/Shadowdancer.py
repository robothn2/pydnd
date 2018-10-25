#coding: utf-8
from Models import Class

name = 'Shadowdancer'

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeat('HideInPlainSight')
        unit.addFeat('WeaponProficiency', ['Simple'])
        unit.addFeat('ArmorProficiency', ['Light'])
    elif level == 2:
        unit.addFeat('Darkvision')
        unit.addFeat('Evasion')
        unit.addFeat('UncannyDodge')
    elif level == 3:
        unit.addFeat('SummonShadow')
        unit.addFeat('ShadowDaze')
    elif level == 4:
        unit.addFeat('ShadowEvade')
    elif level == 5:
        unit.addFeat('DefensiveRoll')
        unit.addFeat('ImprovedUncannyDodge')
    elif level == 7:
        unit.addFeat('SlipperyMind')
    elif level == 10:
        unit.addFeat('ImprovedEvasion')

proto = {
    'desc': '''Operating in the border between light and darkness, shadowdancers are nimble artists of deception. They are mysterious and unknown, never completely trusted but always inducing wonder when met. Rogues, bards, and monks make excellent shadowdancers. Fighters, barbarians, rangers, and paladins also find that shadowdancer abilities allow them to strike at their opponents with surprise and skill. Wizard, sorcerer, cleric, and druid shadowdancers employ the defensive capabilities inherent in the prestige class to allow them to cast their spells from safety and move away quickly. Despite their link with shadows and trickery, shadowdancers are as often good as evil.''',
    'Requirements': (
        ('Skill', 'Move Silently', 8),
        ('Skill', 'Hide', 10),
        ('Skill', 'Tumble', 5),
        ('Feat', ('Dodge', 'Mobility'))
    ),
    'Hit Die': 'd8',
    'Base Attack Bonus': 'Medium.',
    'High Saves': 'Reflex.',
    'Weapon Proficiencies': ('Simple'),
    'Armor Proficiencies': ('Light'),
    'Skill Points': 6,
    'Class Skills': ('Bluff', 'CraftTrap', 'Diplomacy', 'Hide', 'Listen', 'MoveSilently', 'Parry', 'Search', 'SleightOfHand', 'Spot', 'Tumble'),
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'] = Class(name, **proto)
