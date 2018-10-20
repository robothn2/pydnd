#coding: utf-8

proto = {
    'name': 'Shadowdancer',
    'desc': '''Operating in the border between light and darkness, shadowdancers are nimble artists of deception. They are mysterious and unknown, never completely trusted but always inducing wonder when met. Rogues, bards, and monks make excellent shadowdancers. Fighters, barbarians, rangers, and paladins also find that shadowdancer abilities allow them to strike at their opponents with surprise and skill. Wizard, sorcerer, cleric, and druid shadowdancers employ the defensive capabilities inherent in the prestige class to allow them to cast their spells from safety and move away quickly. Despite their link with shadows and trickery, shadowdancers are as often good as evil.''',
    'Requirements': '''Skills: Move Silently 8 ranks, Hide 10 ranks, Tumble 5 ranks.\nFeats: Dodge, Mobility''',
    'HitDie': 8,
    'BaseAttackBonus': 0.75,
    'FortitudePerLevel': 0.25,
    'ReflexPerLevel': 0.5,
    'WillPerLevel': 0.25,
    'WeaponProficiency': ['Simple'],
    'ArmorProficiency': ['Light'],
    'SpellType': '',
    'SkillPoints': 6,
    'ClassSkills': ['Bluff', 'CraftTrap', 'Diplomacy', 'Hide', 'Listen', 'MoveSilently', 'Parry', 'Search', 'SleightOfHand', 'Spot', 'Tumble']
}

def matchRequirements(unit):
    # skills check
    if unit.modifier.sumSource(('Skills', 'MoveSilently'), ['Base']) < 8\
            or unit.modifier.sumSource(('Skills', 'Hide'), ['Base']) < 10\
            or unit.modifier.sumSource(('Skills', 'Tumble'), ['Base']) < 5:
        return False

    # feats check
    if not unit.hasFeats(['Dodge', 'Mobility']):
        return False
    return True

def applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeat('HideInPlainSight')
        unit.addFeat('WeaponProficiency', ['Simple'])
        unit.addFeat('ArmorProficiency', ['Light'])
    elif level == 2:
        unit.addFeat('Darkvision')
        unit.addFeat('Evasion')
        unit.addFeat('UncannyDodge')
    elif level == 3:
        unit.addFeat('SummonShadow')
        unit.addFeat('ShadowDaze')
    elif level == 4:
        unit.addFeat('ShadowEvade')
    elif level == 5:
        unit.addFeat('DefensiveRoll')
        unit.addFeat('ImprovedUncannyDodge')
    elif level == 7:
        unit.addFeat('SlipperyMind')
    elif level == 10:
        unit.addFeat('ImprovedEvasion')
