#coding: utf-8
from Models import Class

name = 'WeaponMaster'

def __requireWeaponFocusOnMelee(unit):
    # check Weapon Focus on melee weapon
    weapons = unit.getFeatParams('WeaponFocus')
    for _, weaponBaseName in enumerate(weapons):
        weaponProto = unit.ctx['protosWeapon'].get(weaponBaseName)
        if not weaponProto:
            continue
        if not weaponProto.proto.get('Ranged'):
            return True
    return False

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeat('WeaponOfChoice', featsHint)
        unit.addFeat('WeaponOfChoice', 'KiDamage')
    elif level == 5:
        unit.addFeat('WeaponOfChoice', ['IncreasedMultiplier', 'SuperiorWeaponFocus'])
    elif level == 7:
        unit.addFeat('WeaponOfChoice', 'KiCritical')

proto = {
    'desc': '''For a weapon master, perfection is found in the mastery of a single melee weapon. A weapon master seeks to unite this weapon of choice with the body, to make them one and to use the weapon as naturally and without thought as any other limb. Weapon Masters may not choose Unarmed Strike as their Weapon of Choice.''',
    'Requirements': (
        ('BaseAttackBonus', 5),
        ('Skill', 'Hide', 10),
        ('Skill', 'Tumble', 5),
        ('Feat', ('Dodge', 'Mobility', 'CombatExpertise', 'SpringAttack', 'WhirlwindAttack')),
        ('Feat', __requireWeaponFocusOnMelee, 'Weapon Focus in a melee weapon')
    ),
    'Hit Die': 'd10',
    'Base Attack Bonus': 'High.',
    'High Saves': 'Reflex.',
    'Skill Points': '2 + Int modifier.',
    'Class Skills': ('CraftWeapon', 'Intimidate', 'Lore', 'Parry', 'Taunt'),
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'] = Class(name, **proto)
