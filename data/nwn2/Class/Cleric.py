#coding: utf-8
from Models import Class

name = 'Cleric'
proto = {
    'desc': '''Clerics are masters of divine magic, which is especially good at healing. Even an inexperienced cleric can bring people back from the brink of death, and an experienced cleric can bring back people who have crossed over that brink. As channelers of divine energy, clerics can affect undead creatures. A cleric can turn away or even destroy undead. Clerics have some combat training. They can use simple weapons, and they are trained in the use of armor, since armor does not interfere with divine spells the way it does with arcane spells.''',
    'Hit Die': 'd8',
    'Base Attack Bonus': 'Medium',
    'High Saves': 'Fortitude and Will.',
    'Weapon Proficiencies': 'Simple',
    'Armor Proficiencies': ('Light', 'Medium', 'Heavy', 'Shield'),
    'Skill Points': 2,
    'Class Skills': ('Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Diplomacy', 'Heal', 'Lore', 'Parry', 'Spellcraft'),
    'bonus': (
        (1, ('Domain', 2)),
        (1, ('spellType', 'Divine', '''A cleric casts divine spells, which are drawn from the cleric spell list. A cleric must choose and prepare his spells in advance. To prepare or cast a spell, a cleric must have a Wisdom score equal to at least 10 + the spell level (Wis 10 for 0-level spells, Wis 11 for 1st-level spells, and so forth).''')),
        (1, ('Feat', ('Spontaneous Casting', 'Turn Undead'))),
    ),
}

def register(protos):
    protos['Class'][name] = Class(name, **proto)
