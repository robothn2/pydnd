#coding: utf-8

proto = {
    'name': 'Ranger',
    'desc': '''A ranger can use a variety of weapons and is quite capable in combat. His skills allow him to survive in the wilderness, to find his prey, and to avoid detection. He also has special knowledge about certain types of creatures, which makes it easier for him to find and defeat such foes. Finally, an experienced ranger has such a tie to nature that he can actually draw upon natural power to cast divine spells, much as a druid does.''',
    'HitDie': 8,
    'BaseAttackBonus': 1.0,
    'FortitudePerLevel': 0.5,
    'ReflexPerLevel': 0.5,
    'WillPerLevel': 0.25,
    'WeaponProficiencies': ['simple', 'martial'],
    'ArmorProficiencies': ['light', 'shields(except tower shields)'],
    'SkillPoints': 6,
    'ClassSkills': ['Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Heal', 'Hide', 'Listen', 'Lore', 'MoveSilently', 'Parry', 'Search', 'SetTrap', 'Spot', 'Survival']
}

def applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('ranger apply level %d' % level, featsHint)
    if level == 1:
        unit.addFeat(['Track'])
        unit.addFeat(['FavoredEnemy'], featsHint)
    elif level == 2:
        unit.addFeat(['CombatStyle'], featsHint)
    elif level == 3:
        unit.addFeat(['Toughness'])
    elif level == 4:
        unit.addFeat(['AnimalCompanion'], featsHint)
        # todo: Spells: Beginning at 4th level, a ranger gains the ability to cast a small number of divine spells, which are drawn from the ranger spell list. A ranger must choose and prepare his spells in advance. To prepare or cast a spell, a ranger must have a Wisdom score equal to at least 10 + the spell level (Wis 10 for 0-level spells, Wis 11 for 1st-level spells, and so forth).
    elif level == 6:
        unit.addFeat(['ImprovedCombatStyle'], featsHint)
    elif level == 7:
        unit.addFeat(['WoodlandStride'])
    elif level == 8:
        unit.addFeat(['SwiftTracker'])
    elif level == 9:
        unit.addFeat(['Evasion'])
    elif level == 11:
        unit.addFeat(['CombatMastery'])
    elif level == 13:
        unit.addFeat(['Camouflage'])
    elif level == 17:
        unit.addFeat(['HideInPlainSight'])