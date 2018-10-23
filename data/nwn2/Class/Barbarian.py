#coding: utf-8
from Models import Class

name = 'Barbarian'

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeats(['Rage', 'FastMovement'])
        unit.addFeat('WeaponProficiency', ['Martial', 'Simple'])
        unit.addFeat('ArmorProficiency', ['Light', 'Medium', 'Shield'])
    elif level == 2:
        unit.addFeat('UncannyDodge')
    elif level == 3:
        unit.addFeat('TrapSense')
    elif level == 7:
        unit.addFeat('DamageReduction')
    elif level == 11:
        unit.addFeat('Rage', ['Greater'])
    elif level == 14:
        unit.addFeat('Rage', ['IndomitableWill'])
    elif level == 17:
        unit.addFeat('Rage', ['Tireless'])
    elif level == 20:
        unit.addFeat('Rage', ['Mighty'])

proto = {
    'desc': '''The barbarian is an excellent warrior. Where the fighter's skill comes from training and discipline, however, the barbarian draws upon a powerful primal rage. While in this berserk fury, he becomes stronger and tougher, better able to defeat his foes and withstand their attacks. These rages leave him winded, and he has the energy for only a few such spectacular displays per day, but those few rages are usually sufficient. He is at home in the wild, and he runs at great speed.''',
    'Alignment': ['NeutralGood', 'Neutral', 'NeutralEvil', 'ChaoticGood', 'ChaoticNeutral', 'ChaoticEvil'],
    'HitDie': 12,
    'BaseAttackBonus': 1.0,
    'FortitudePerLevel': 0.5,
    'ReflexPerLevel': 0.25,
    'WillPerLevel': 0.25,
    'WeaponProficiency': ('Simple', 'Martial'),
    'ArmorProficiency': ('Light', 'Medium', 'Shield'),
    'SkillPoints': 4,
    'ClassSkills': ('CraftArmor', 'CraftTrap', 'CraftWeapon', 'Intimidate', 'Listen', 'Parry', 'Survival', 'Taunt'),
    'BonusFeats': (
        (1,['Rage','FastMovement']),
        (2,['UncannyDodge']),
        (3,['TrapSense']),
        (7,['DamageReduction']),
        (11,['GreaterRage']),
        (14,['IndomitableWill']),
        (17,['TirelessRage']),
        (20,['MightyRage'])
    ),
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'] = Class(name, **proto)
