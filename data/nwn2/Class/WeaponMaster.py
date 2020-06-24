#coding: utf-8

def __requireWeaponFocusOnMelee(unit):
    # check Weapon Focus on melee weapon
    weapons = unit.getFeatParams('Weapon Focus')
    for _, weaponBaseName in enumerate(weapons):
        weaponProto = unit.ctx['Weapon'].get(weaponBaseName)
        if not weaponProto:
            continue
        if not weaponProto.proto.get('Ranged'):
            return True
    return False

protos = [{
  'name': 'Weapon Master',
  'type': 'Class',
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
}]

def __applyWeaponOfChoice(feat, caster, target, **kwargs):
    weapon = kwargs.get('weapon')
    hand = kwargs.get('hand')
    params = kwargs.get('params')
    if type(params) != list or weapon.nameBase not in params:
        return

    print(feat.nameFull, 'affects weapon:', weapon.getItemBaseName(), ', params:', params)
    if 'IncreasedMultiplier' in params:
        caster.calc.addSource('Weapon.%s.CriticalMultiplier' % hand, name='Increased Multiplier', calcInt=1)
    if 'SuperiorWeaponFocus' in params:
        caster.calc.addSource('AttackBonus.' + hand, name='Superior Weapon Focus', calcInt=1)
    if 'KiCritical' in params:
        caster.calc.addSource('Weapon.%s.CriticalRange' % hand, name='Ki Critical', calcInt=2)
def __unapplyWeaponOfChoice(feat, caster, target, **kwargs):
    pass


def __castKiDamage(feat, caster, target, **kwargs):
    pass
def __decChargeKiDamage(feat, caster, target, **kwargs):
    pass

protos.extend([
  {
    'name': 'Ki Damage',
    'type': 'Feat', 'category': 'Class',
    'apply': lambda feat, caster, target, **kwargs: caster.calc.addSource('Spell.Charges', name=feat.nameFull, calcInt=feat),
    'unapply': lambda feat, caster, target, **kwargs: caster.calc.removeSource('Spell.Charges', feat.nameFull),
    'maxCharge': lambda feat, caster, target, **kwargs: caster.getClassLevel(),
    'decCharge': __decChargeKiDamage,
    'cast': __castKiDamage,
    'specifics': '''Once per day per level, a Weapon Master may use this feat to do maximum damage to their opponent.''',
  },

  {
    'name': 'Weapon of Choice', 'group': 'WeaponOfChoice',
    'type': 'Feat', 'category': 'Class',
    'forWeapon': True,
    'apply': __applyWeaponOfChoice,
    'unapply': __unapplyWeaponOfChoice,
    'specifics': '''The weapon chosen to be a weapon of choice by a Weapon Master becomes the focus for all of their special abilities.''',
  },
  {
    'name': 'Increased Multiplier', 'group': 'WeaponOfChoice',
    'type': 'Feat', 'category': 'Class',
    'specifics': '''With their weapon of choice, the multiplier is increased by x1 to all critical hits. Thus a x2 critical multiplier becomes a x3.''',
  },
  {
    'name': 'Superior Weapon Focus', 'group': 'WeaponOfChoice',
    'type': 'Feat', 'category': 'Class',
    'specifics': '''The weapon master gains a +1 bonus to all attack rolls with their weapon of choice.''',
  },
  {
    'name': 'Ki Critical', 'group': 'WeaponOfChoice',
    'type': 'Feat', 'category': 'Class',
    'specifics': '''The weapon master gains an additional +2 to the threat range of their weapon of choice.''',
  },
])
