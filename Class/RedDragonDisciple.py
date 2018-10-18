#coding: utf-8

proto = {
    'name': 'RedDragonDisciple',
    'desc': '''It is known that certain dragons can take humanoid form and even have humanoid lovers. Sometimes a child is born of this union, and every child of that child unto the thousandth generation claims a bit of dragon blood, be it ever so small. Usually, little comes of it, though mighty sorcerers occasionally credit their powers to draconic heritage. For some, however, dragon blood beckons irresistibly. These characters become dragon disciples, who use their magical power as a catalyst to ignite their dragon blood, realizing its fullest potential. Members of this prestige class draw on the potent blood of red dragons coursing in their veins. Though red dragons are among the most cruel and evil creatures on Faerûn, red dragon disciples may be of any alignment.''',
    'Requirements': '''Skills: Lore 8 ranks.\nClass: Bard or Sorcerer.''',
    'HitDie': 12,
    'BaseAttackBonus': 0.75,
    'FortitudePerLevel': 0.5,
    'ReflexPerLevel': 0.25,
    'WillPerLevel': 0.5,
    'WeaponProficiencies': [],
    'ArmorProficiencies': [],
    'SpellType': '',
    'SkillPoints': 2,
    'ClassSkills': ['Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Diplomacy', 'Listen', 'Lore', 'Parry', 'Search', 'Spellcraft', 'Spot'],
    'BonusFeats': (
        (1, ['NaturalArmorIncrease', 'DraconicAbilityScores']),
        (3, ['BreathWeapon']),
        (5, ['BlindFight']),
        (10, ['HalfDragon'])
    )
}

def matchRequirements(unit):
    # skills check
    if unit.calc.calcPropValue('Skill.Lore', 'Builder') < 8:
        return False

    # classes check
    if unit.getClassLevel('Sorcerer') == 0 and unit.getClassLevel('Wizard') == 0:
        return False
    return True

def applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeats(['NaturalArmorIncrease', 'DraconicAbilityScores'])
    elif level == 3:
        unit.addFeat('BreathWeapon')
    elif level == 5:
        unit.addFeat('BlindFight')
    elif level == 10:
        unit.addFeat('HalfDragon')
