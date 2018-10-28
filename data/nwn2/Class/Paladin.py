#coding: utf-8
from Models import Class

name = 'Paladin'
proto = {
    'desc': '''Divine power protects the paladin and gives her special powers. It wards off harm, protects her from disease, lets her heal herself, and guards her heart against fear. A paladin can also direct this power to help others, healing their wounds or curing diseases. Finally, a paladin can use this power to destroy evil. Even a novice paladin can detect evil, and more experienced paladins can smite evil foes and turn away undead.''',
    'Alignment': ('LawfulGood'),
    'Hit Die': 'd10',
    'Base Attack Bonus': 'High.',
    'High Saves': 'Fortitude.',
    'Weapon Proficiencies': ('Simple', 'Martial'),
    'Armor Proficiencies': ('Light', 'Medium', 'Heavy', 'Shield'),
    'SpellType': ('Divine', 4),
    'Skill Points': 2,
    'Class Skills': ('Concentration', 'CraftArmor', 'CraftWeapon', 'Diplomacy', 'Heal', 'Lore', 'Parry'),
    'bonus': (
        (1, ('Feat', 'Smite Evil')),
        (2, ('Feat', ('DivineGrace', 'LayOnHands'))),
        (3, ('Feat', ('AuraOfCourage', 'DivineHealth'))),
        (4, ('Feat', 'TurnUndead')),
        (4, ('SpellType', 'Divine', '''Beginning at 4th level, a paladin gains the ability to cast a small number of divine spells, which are drawn from the paladin spell list. A paladin must choose and prepare her spells in advance. To prepare or cast a spell, a paladin must have a Wisdom score equal to at least 10 + the spell level (Wis 10 for 0-level spells, Wis 11 for 1st-level spells, and so forth).''')),
        (6, ('Feat', 'RemoveDisease')),
    ),
}

def register(protos):
    protos['Class'][name] = Class(name, **proto)
