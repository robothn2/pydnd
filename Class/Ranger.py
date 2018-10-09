#coding: utf-8

proto = {
    'name': 'Ranger',
    'desc': '''A ranger can use a variety of weapons and is quite capable in combat. His skills allow him to survive in the wilderness, to find his prey, and to avoid detection. He also has special knowledge about certain types of creatures, which makes it easier for him to find and defeat such foes. Finally, an experienced ranger has such a tie to nature that he can actually draw upon natural power to cast divine spells, much as a druid does.''',
    'HitDie': 8,
    'BaseAttackBonus': 1.0,
    'FortitudePerLevel': 0.5,
    'ReflexPerLevel': 0.5,
    'WillPerLevel': 0.25,
    'WeaponProficiency': ['Simple', 'Martial'],
    'ArmorProficiency': ['Light', 'Shield'],
    'SpellType': 'Divine',
    'SkillPoints': 6,
    'ClassSkills': ['Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Heal', 'Hide', 'Listen', 'Lore', 'MoveSilently', 'Parry', 'Search', 'SetTrap', 'Spot', 'Survival']
}

def applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeat('Track')
        unit.addFeat('WeaponProficiency', proto['WeaponProficiency'])
        unit.addFeat('ArmorProficiency', proto['ArmorProficiency'])
    elif level == 2:
        # CombatStyle
        if 'TwoWeaponFighting' in featsHint:
            unit.addFeat('TwoWeaponFighting')
        else:
            pass
    elif level == 3:
        unit.addFeat('Toughness')
    elif level == 4:
        unit.addFeat('AnimalCompanion', featsHint)
        unit.grantSpellClass('Divine', proto['name'])
    elif level == 6:
        # ImprovedCombatStyle
        if 'TwoWeaponFighting' in unit.getFeatParams('CombatStyle'):
            unit.addFeat('TwoWeaponFighting', ['Improved'])
        else:
            pass
    elif level == 7:
        unit.addFeat('WoodlandStride')
    elif level == 8:
        unit.addFeat('SwiftTracker')
    elif level == 9:
        unit.addFeat('Evasion')
    elif level == 11:
        # CombatMastery
        if 'TwoWeaponFighting' in unit.getFeatParams('CombatStyle'):
            unit.addFeat('TwoWeaponFighting', ['Perfect'])
        else:
            pass
    elif level == 13:
        unit.addFeat('Camouflage')
    elif level == 17:
        unit.addFeat('HideInPlainSight')

    if level % 5 == 0 or level == 1:
        unit.addFeat('FavoredEnemy', featsHint)
