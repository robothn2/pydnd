#coding: utf-8
from Models import Class

name = 'Cleric'

def __applyLevelUp(unit, level, levelInfo):
    featsHint = levelInfo['featsHint'] if 'featsHint' in levelInfo else []

    print('%s apply level %d, featsHint: %s' % (proto['name'], level, featsHint))
    if level == 1:
        for _, domainName in enumerate(levelInfo['clericDomains']):
            if domainName not in unit.ctx['Domain']:
                continue
            domainProto = unit.ctx['Domain'][domainName]
            domainProto.apply(unit)

        unit.addFeat('WeaponProficiency', proto['WeaponProficiency'])
        unit.addFeat('ArmorProficiency', proto['ArmorProficiency'])
        unit.addFeat('TurnUndead')
        unit.addFeat('SpontaneousCasting')
        unit.addAccessSpellClass(proto['name'])

proto = {
    'desc': '''Clerics are masters of divine magic, which is especially good at healing. Even an inexperienced cleric can bring people back from the brink of death, and an experienced cleric can bring back people who have crossed over that brink. As channelers of divine energy, clerics can affect undead creatures. A cleric can turn away or even destroy undead. Clerics have some combat training. They can use simple weapons, and they are trained in the use of armor, since armor does not interfere with divine spells the way it does with arcane spells.''',
    'Hit Die': 'd8',
    'Base Attack Bonus': 'Medium',
    'High Saves': 'Fortitude and Will.',
    'Weapon Proficiencies': 'Simple',
    'Armor Proficiencies': ('Light', 'Medium', 'Heavy', 'Shield'),
    'SpellType': 'Divine',
    'Skill Points': 2,
    'Class Skills': ('Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Diplomacy', 'Heal', 'Lore', 'Parry', 'Spellcraft'),
    'applyLevelUp': __applyLevelUp,
}

def register(protos):
    protos['Class'] = Class(name, **proto)
