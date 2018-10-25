#coding: utf-8
from Models import Class

name = 'Bard'

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeats(['BardicKnowledge', 'Inspiration', 'InspireCourage', 'BardicMusic', 'Countersong', 'Fascinate'])
    elif level == 2:
        unit.addFeat('InspireCompetence')
    elif level == 3:
        unit.addFeat('HavenSong')
    elif level == 5:
        unit.addFeat('InspireDefense')
    elif level == 6:
        unit.addFeat('CloudMind')
    elif level == 7:
        unit.addFeat('InspireRegeneration')
    elif level == 8:
        unit.addFeat('InspireToughness')
    elif level == 9:
        unit.addFeat('IronskinChant')
    elif level == 11:
        unit.addFeat('InspireSlowing')
    elif level == 12:
        unit.addFeat('SongOfFreedom')
    elif level == 14:
        unit.addFeat('InspireJarring')
    elif level == 15:
        unit.addFeat('SongOfHeroism')
    elif level == 18:
        unit.addFeat('LegionnaireMarch')

proto = {
    'desc': '''A bard brings forth magic from his soul, not from a book. He can cast only a small number of spells, but he can do so without selecting or preparing them in advance. His magic emphasizes charms and illusions over the more dramatic evocation spells that wizards and sorcerers often use. In addition to spells, a bard works magic with his music and poetry. He can encourage allies, hold his audiences rapt, and counter magical effects that rely on speech or sound. Bards have some of the skills that rogues have, although bards are not as focused on skill mastery as rogues are. A bard listens to stories as well as telling them, of course, so he has a vast knowledge of local events and noteworthy items.''',
    'Alignment': ('NeutralGood', 'Neutral', 'NeutralEvil', 'ChaoticGood', 'ChaoticNeutral', 'ChaoticEvil'),
    'Hit Die': 'd6',
    'Base Attack Bonus': 'Medium',
    'High Saves': 'Reflex and Will.',
    'Weapon Proficiencies': ('Simple', 'Longsword', 'Rapier', 'Shortsword', 'Shortbow'),
    'Armor Proficiencies': ('Light', 'Shield'),
    'SpellType': 'Arcane',
    'Skill Points': 6,
    'Class Skills': ('Appraise', 'Bluff', 'Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Diplomacy', 'Hide', 'Listen', 'Lore', 'MoveSilently', 'Parry', 'Perform', 'SleightOfHand', 'Spellcraft', 'Taunt', 'Tumble', 'UseMagicDevice'),
    'BonusFeats': (
        (1, ['BardicKnowledge', 'Inspiration', 'InspireCourage', 'BardicMusic', 'Countersong', 'Fascinate']),
        (2, ['InspireCompetence']),
        (3, ['HavenSong']),
        (5, ['InspireDefense']),
        (6, ['CloudMind']),
        (7, ['InspireRegeneration']),
        (8, ['InspireToughness']),
        (9, ['IronskinChant']),
        (11, ['InspireSlowing']),
        (12, ['SongOfFreedom']),
        (14, ['InspireJarring']),
        (15, ['SongOfHeroism']),
        (18, ['LegionnaireMarch']),
    ),
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'] = Class(name, **proto)

