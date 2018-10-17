#coding: utf-8

proto = {
    'name': 'Wizard',
    'desc': '''The wizard's strength is her spells. Everything else is secondary. She learns new spells as she experiments and grows in experience, and she can also learn them from other wizards. In addition to learning new spells, a wizard can, over time, learn to manipulate her spells so they go farther, work better, or are improved in some other way. Some wizards prefer to specialize in a certain type of magic. Specialization makes a wizard more powerful in her chosen field, but it denies her access to some of the spells that lie outside that field.''',
    'HitDie': 4,
    'BaseAttackBonus': 0.5,
    'FortitudePerLevel': 0.25,
    'ReflexPerLevel': 0.25,
    'WillPerLevel': 0.5,
    'WeaponProficiency': ['Club', 'Dagger', 'HeavyCrossbow', 'LightCrossbow', 'Quarterstaff'],
    'ArmorProficiency': [],
    'SpellType': 'Arcane',
    'SkillPoints': 2,
    'ClassSkills': ['Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftWeapon', 'Lore', 'Spellcraft'],
    'BonusFeats': (
        (1, ['Familiar', 'Spellbook']),
    )
}

def applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeat('Familiar', featsHint)
        unit.addFeat('Spellbook')
        unit.addFeat('WeaponProficiency', proto['WeaponProficiency'])
        unit.addFeat('ArmorProficiency', proto['ArmorProficiency'])

    if level == 5 or level == 10 or level == 15 or level == 20:
        pass # todo: add bonus feat
