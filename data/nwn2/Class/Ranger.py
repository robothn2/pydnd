#coding: utf-8
from Models import Class, Feat

name = 'Ranger'

def _applyFeatFavoredEnemy(source, unit, featParams):
    bonus = max(1, int(unit.getClassLevel('Ranger') / 5))
    calcDamage = lambda caster,target: None if not target.matchRaces(featParams) else ('Divine', source, bonus)
    unit.calc.addSource('Damage.Additional', name=source, calcInt=calcDamage, noCache=True)

    calcSkill = lambda caster,target: 0 if not target.matchRaces(featParams) else max(1, int(caster.getClassLevel('Ranger') / 5))
    unit.calc.addSource('Skill.Listen', name=source, calcInt=calcSkill, noCache=True)
    unit.calc.addSource('Skill.Spot', name=source, calcInt=calcSkill, noCache=True)
    unit.calc.addSource('Skill.Taunt', name=source, calcInt=calcSkill, noCache=True)
def _unapplyFeatFavoredEnemy(source, unit):
    unit.calc.removeSource('Damage.Additional', source)

    unit.calc.addSource('Skill.Listen', source)
    unit.calc.addSource('Skill.Spot', source)
    unit.calc.addSource('Skill.Taunt', source)

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeat('Track')
        unit.addFeat('WeaponProficiency', proto['WeaponProficiency'])
        unit.addFeat('ArmorProficiency', proto['ArmorProficiency'])
    elif level == 2:
        # CombatStyle
        for _, hint in enumerate(featsHint):
            if type(hint) == list and hint[0] == 'CombatStyle':
                if hint[1] == 'TwoWeaponFighting':
                    unit.addFeat('CombatStyle', 'TwoWeaponFighting')
                    unit.addFeat('TwoWeaponFighting')
                elif hint[1] == 'TwoWeaponFighting':
                    unit.addFeat('CombatStyle', 'Archery')
                    unit.addFeat('RapidShot')
    elif level == 3:
        unit.addFeat('Toughness')
    elif level == 4:
        unit.addFeat('AnimalCompanion', featsHint)
        unit.addAccessSpellClass(proto['name'])
    elif level == 6:
        # ImprovedCombatStyle
        if 'TwoWeaponFighting' in unit.getFeatParams('CombatStyle'):
            unit.addFeat('TwoWeaponFighting', ['Improved'])
        else:
            unit.addFeat('Manyshot')
    elif level == 7:
        unit.addFeat('WoodlandStride')
    elif level == 8:
        unit.addFeat('SwiftTracker')
    elif level == 9:
        unit.addFeat('Evasion')
    elif level == 11:
        # CombatMastery
        if 'TwoWeaponFighting' in unit.getFeatParams('CombatStyle'):
            unit.addFeat('TwoWeaponFighting', ['Greater'])
        else:
            unit.addFeat('RapidShot', ['Improved'])
    elif level == 13:
        unit.addFeat('Camouflage')
    elif level == 17:
        unit.addFeat('HideInPlainSight')
    elif level == 21:
        if 'TwoWeaponFighting' in unit.getFeatParams('CombatStyle'):
            unit.addFeat('TwoWeaponFighting', ['Perfect'])

    if level % 5 == 0 or level == 1:
        unit.addFeat('FavoredEnemy', featsHint)

proto = {
    'desc': '''A ranger can use a variety of weapons and is quite capable in combat. His skills allow him to survive in the wilderness, to find his prey, and to avoid detection. He also has special knowledge about certain types of creatures, which makes it easier for him to find and defeat such foes. Finally, an experienced ranger has such a tie to nature that he can actually draw upon natural power to cast divine spells, much as a druid does.''',
    'Hit Die': 'd8',
    'Base Attack Bonus': 'High.',
    'High Saves': 'Fortitude and Reflex.',
    'Weapon Proficiencies': ('Simple', 'Martial'),
    'Armor Proficiencies': ('Light', 'Shield'),
    'SpellType': ('Divine', 4),
    'Skill Points': 6,
    'Class Skills': ['Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Heal', 'Hide', 'Listen', 'Lore', 'MoveSilently', 'Parry', 'Search', 'SetTrap', 'Spot', 'Survival'],
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'][name] = Class(name, **proto)

    protos['Feat']['FavoredEnemy'] = Feat(
        'FavoredEnemy',
        nameFull = 'Favored Enemy',
        type = 'Class',
        group = 'FavoredEnemy',
        groupMemberName = '',
        apply = _applyFeatFavoredEnemy,
        unapply = _unapplyFeatFavoredEnemy,
        prerequisite = (
            ('Class', name, 'Ranger level 1')
        ),
        specifics = '''The character gains a +1 bonus to damage rolls against their favored enemy. They also receive a +1 bonus on Listen, Spot, and Taunt checks against the favored enemy. Every 5 levels, the ranger may choose an additional Favored Enemy and all bonuses against all favored enemies increase by +1.''',
        use = 'Automatic',
    )
