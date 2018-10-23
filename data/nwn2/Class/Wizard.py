#coding: utf-8
from Models import Class

name = 'Wizard'

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        unit.addFeat('Familiar', featsHint)
        unit.addFeat('Spellbook')
        unit.addFeat('WeaponProficiency', proto['WeaponProficiency'])
        unit.addFeat('ArmorProficiency', proto['ArmorProficiency'])

    if level == 5 or level == 10 or level == 15 or level == 20:
        pass # todo: add bonus feat

proto = {
    'desc': '''The wizard's strength is her spells. Everything else is secondary. She learns new spells as she experiments and grows in experience, and she can also learn them from other wizards. In addition to learning new spells, a wizard can, over time, learn to manipulate her spells so they go farther, work better, or are improved in some other way. Some wizards prefer to specialize in a certain type of magic. Specialization makes a wizard more powerful in her chosen field, but it denies her access to some of the spells that lie outside that field.''',
    'Hit Die': 'd4',
    'Base Attack Bonus': 'Low.',
    'High Saves': 'Will.',
    'Skill Points': '2 + Int modifier.',
    'Weapon Proficiencies': ['Club', 'Dagger', 'HeavyCrossbow', 'LightCrossbow', 'Quarterstaff'],
    'Armor Proficiencies': [],
    'Spell Type': 'Arcane',
    'Class Skills': ['Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftWeapon', 'Lore', 'Spellcraft'],
    'BonusFeats': (
        (1, ['Familiar', 'Spellbook']),
    ),
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'] = Class(name, **proto)
