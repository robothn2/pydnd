#coding: utf-8

proto = {
    'name': 'WeaponMaster',
    'desc': '''For a weapon master, perfection is found in the mastery of a single melee weapon. A weapon master seeks to unite this weapon of choice with the body, to make them one and to use the weapon as naturally and without thought as any other limb. Weapon Masters may not choose Unarmed Strike as their Weapon of Choice.''',
    'Requirements': '''Base Attack Bonus: +5\nFeats: Weapon Focus in a melee weapon, Dodge, Mobility, Combat Expertise, Spring Attack and Whirlwind Attack.\nSkills: Intimidate 4 or more ranks.''',
    'HitDie': 10,
    'BaseAttackBonus': 1.0,
    'FortitudePerLevel': 0.25,
    'ReflexPerLevel': 0.5,
    'WillPerLevel': 0.25,
    'WeaponProficiencies': [],
    'ArmorProficiencies': [],
    'SkillPoints': 2,
    'ClassSkills': ['CraftWeapon', 'Intimidate', 'Lore', 'Parry', 'Taunt']
}

def matchRequirements(unit):
    # skills check
    if unit.modifier.sumSource(('Skills', 'Intimidate'), ['Base']) < 4:
        return False

    # bab check
    if unit.modifier.sumSource('AttackBonus', ['Base']) < 5:
        return False

    # feats check
    if not unit.props.hasKeyList(['WeaponFocus', 'Dodge', 'Mobility', 'CombatExpertise', 'SpringAttack', 'WhirlwindAttack']):
        return False

    #todo: check Weapon Focus on melee weapon
    return True

def applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeat(['WeaponOfChoice'], featsHint)
        unit.addFeat(['KiDamage'])
    elif level == 5:
        unit.addFeat(['IncreaseMultiplier', 'SuperiorWeaponFocus'])
    elif level == 7:
        unit.addFeat(['Ki Critical'])
