#coding: utf-8
from Models import Class

name = 'Paladin'

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeats(['SmiteEvil'])
        unit.addFeat('WeaponProficiency', ['Martial', 'Simple'])
        unit.addFeat('ArmorProficiency', ['Light', 'Medium', 'Heavy', 'Shield'])
    elif level == 2:
        unit.addFeats(['DivineGrace', 'LayOnHands'])
    elif level == 3:
        unit.addFeats(['AuraOfCourage', 'DivineHealth'])
    elif level == 4:
        unit.addFeat('TurnUndead')
        unit.addAccessSpellClass(proto['name'])
    elif level == 11:
        unit.addFeat('RemoveDisease')

proto = {
    'desc': '''Divine power protects the paladin and gives her special powers. It wards off harm, protects her from disease, lets her heal herself, and guards her heart against fear. A paladin can also direct this power to help others, healing their wounds or curing diseases. Finally, a paladin can use this power to destroy evil. Even a novice paladin can detect evil, and more experienced paladins can smite evil foes and turn away undead.''',
    'Alignment': ['LawfulGood'],
    'HitDie': 10,
    'BaseAttackBonus': 1.0,
    'FortitudePerLevel': 0.5,
    'ReflexPerLevel': 0.25,
    'WillPerLevel': 0.25,
    'WeaponProficiency': ('Simple', 'Martial'),
    'ArmorProficiency': ('Light', 'Medium', 'Heavy', 'Shield'),
    'SpellType': 'Divine',
    'SkillPoints': 2,
    'ClassSkills': ('Concentration', 'CraftArmor', 'CraftWeapon', 'Diplomacy', 'Heal', 'Lore', 'Parry'),
    'BonusFeats': (
        (1,['SmiteEvil']),
        (2,['DivineGrace', 'LayOnHands']),
        (3,['AuraOfCourage', 'DivineHealth']),
        (4,['TurnUndead']),
        (6,['RemoveDisease']),
    ),
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'] = Class(name, **proto)
