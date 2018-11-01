#coding: utf-8
from Models import Class, register_feat

name = 'Weapon Master'

def __requireWeaponFocusOnMelee(unit):
    # check Weapon Focus on melee weapon
    weapons = unit.getFeatParams('WeaponFocus')
    for _, weaponBaseName in enumerate(weapons):
        weaponProto = unit.ctx['Weapon'].get(weaponBaseName)
        if not weaponProto:
            continue
        if not weaponProto.proto.get('Ranged'):
            return True
    return False

proto = {
    'desc': '''For a weapon master, perfection is found in the mastery of a single melee weapon. A weapon master seeks to unite this weapon of choice with the body, to make them one and to use the weapon as naturally and without thought as any other limb. Weapon Masters may not choose Unarmed Strike as their Weapon of Choice.''',
    'Hit Die': 'd10',
    'Base Attack Bonus': 'High.',
    'High Saves': 'Reflex.',
    'Skill Points': 2,
    'Class Skills': ('CraftWeapon', 'Intimidate', 'Lore', 'Parry', 'Taunt'),
    'requirements': (
        ('BaseAttackBonus', 5),
        ('Skill', 'Hide', 10),
        ('Skill', 'Tumble', 5),
        ('Feat', ('Dodge', 'Mobility', 'CombatExpertise', 'SpringAttack', 'WhirlwindAttack')),
        (__requireWeaponFocusOnMelee, 'Weapon Focus in a melee weapon')
    ),
    'bonus': (
        (1, ('Feat', 'Weapon of Choice')),
        (1, ('Feat', 'Ki Damage')),
        (5, ('Feat', ('Increased Multiplier', 'Superior Weapon Focus'))),
        (7, ('Feat', 'Ki Critical')),
    ),
}

def __applyToWeapon(source, unit, feat, params, **kwargs):
    weapon = kwargs.get('weapon')
    hand = kwargs.get('hand')
    if params is not list or weapon.getItemBaseName() not in params:
        return

    print(source, 'affects weapon:', weapon.getItemBaseName(), ', params:', params)
    if 'IncreasedMultiplier' in params:
        unit.calc.addSource('Weapon.%s.CriticalMultiplier' % hand, name='IncreasedMultiplier', calcInt=1)
    if 'SuperiorWeaponFocus' in params:
        unit.calc.addSource('AttackBonus.' + hand, name='SuperiorWeaponFocus', calcInt=1)
    if 'KiCritical' in params:
        unit.calc.addSource('Weapon.%s.CriticalRange' % hand, name='KiCritical', calcInt=2)
def __unapply(source, unit, feat, params):
    pass

def register(protos):
    protos['Class'][name] = Class(name, **proto)

    register_feat(protos, 'WeaponOfChoice', 'Weapon of Choice',
                  apply=__applyToWeapon,
                  unapply=__unapply,
                  specifics='''The weapon chosen to be a weapon of choice by a Weapon Master becomes the focus for all of their special abilities.''',
                  )
    register_feat(protos, 'WeaponOfChoice', 'Increased Multiplier',
                  prerequisite=[('ClassLevel', name, 5)],
                  specifics='''With their weapon of choice, the multiplier is increased by x1 to all critical hits. Thus a x2 critical multiplier becomes a x3.''',
                  )
    register_feat(protos, 'WeaponOfChoice', 'Superior Weapon Focus',
                  prerequisite=[('ClassLevel', name, 5)],
                  specifics='''The weapon master gains a +1 bonus to all attack rolls with their weapon of choice.''',
                  )
    register_feat(protos, 'WeaponOfChoice', 'Ki Critical',
                  prerequisite=[('ClassLevel', name, 7)],
                  specifics='''The weapon master gains an additional +2 to the threat range of their weapon of choice.''',
                  )
