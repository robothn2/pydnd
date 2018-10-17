#coding: utf-8

proto = {
    'name': 'Monk',
    'desc': '''The key feature of the monk is her ability to fight unarmed and unarmored. Thanks to her rigorous training, she can strike as hard as if she were armed and strike faster than a warrior with a sword. Though a monk casts no spells, she has a magic of her own. She channels a subtle energy, called ki, which allows her to perform amazing feats. The monk's best-known feat is her ability to stun an opponent with an unarmed blow. A monk also has a preternatural awareness that allows her to dodge an attack even if she is not consciously aware of it. As a monk gains experience and power, her mundane and ki-oriented abilities grow, giving her more and more power over herself and, sometimes, over others.''',
    'Alignment': ['LawfulGood', 'LawfulNeural', 'LawfulEvil'],
    'HitDie': 8,
    'BaseAttackBonus': 0.75,
    'FortitudePerLevel': 0.5,
    'ReflexPerLevel': 0.5,
    'WillPerLevel': 0.5,
    'WeaponProficiency': ('Club', 'LightCrossbow',  'HeavyCrossbow', 'Dagger', 'Handaxe', 'Javelin', 'Kama', 'Quarterstaff', 'Shuriken', 'Sling'),
    'ArmorProficiency': (),
    'SpellType': '',
    'SkillPoints': 4,
    'ClassSkills': ('Concentration', 'CraftAlchemy', 'CraftTrap', 'Diplomacy', 'Hide', 'Listen', 'Lore', 'MoveSilently', 'Parry', 'Spot', 'Tumble'),
    'BonusFeats': (
        (1,['MonkACBonus','FlurryOfBlows','ImprovedUnarmStrike']),
        (2,['Evasion']),
        (3,['FastMovement','StillMind']),
        (4,['KiStrike']),
        (5,['PurityOfBody']),
        (7,['WholenessOfBody']),
        (9,['ImprovedEvasion']),
        (11,['DiamondBody']),
        (13,['DiamondSoul']),
        (15,['QuiveringPalm']),
        (19,['EmptyBody']),
        (20,['PerfectSelf'])
    )
}

def applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeats(['MonkACBonus','FlurryOfBlows','ImprovedUnarmStrike'])
        unit.addFeat('WeaponProficiency', ['Martial', 'Simple'])
        unit.addFeat('ArmorProficiency', ['Light', 'Shield'])
    elif level == 2:
        unit.addFeat('Evasion')
    elif level == 3:
        unit.addFeats(['FastMovement','StillMind'])
    elif level == 4:
        unit.addFeat('KiStrike')
    elif level == 5:
        unit.addFeat('PurityOfBody')
    elif level == 7:
        unit.addFeat('WholenessOfBody')
    elif level == 9:
        unit.addFeat('ImprovedEvasion')
    elif level == 11:
        unit.addFeat('DiamondBody')
    elif level == 13:
        unit.addFeat('DiamondSoul')
    elif level == 15:
        unit.addFeat('QuiveringPalm')
    elif level == 19:
        unit.addFeat('EmptyBody')
    elif level == 20:
        unit.addFeat('PerfectSelf')
