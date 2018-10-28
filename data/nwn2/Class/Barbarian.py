#coding: utf-8
from Models import Class

name = 'Barbarian'
proto = {
    'desc': '''The barbarian is an excellent warrior. Where the fighter's skill comes from training and discipline, however, the barbarian draws upon a powerful primal rage. While in this berserk fury, he becomes stronger and tougher, better able to defeat his foes and withstand their attacks. These rages leave him winded, and he has the energy for only a few such spectacular displays per day, but those few rages are usually sufficient. He is at home in the wild, and he runs at great speed.''',
    'Alignment': ('NeutralGood', 'Neutral', 'NeutralEvil', 'ChaoticGood', 'ChaoticNeutral', 'ChaoticEvil'),
    'Hit Die': 'd12',
    'Base Attack Bonus': 'High.',
    'High Saves': 'Fortitude.',
    'Weapon Proficiencies': ('Simple', 'Martial'),
    'Armor Proficiencies': ('Light', 'Medium', 'Shield'),
    'Skill Points': 4,
    'Class Skills': ('CraftArmor', 'CraftTrap', 'CraftWeapon', 'Intimidate', 'Listen', 'Parry', 'Survival', 'Taunt'),
    'bonus': (
        (1, ('Feat', ('Rage', 'Fast Movement'))),
        (2, ('Feat', 'Uncanny Dodge')),
        (3, ('Feat', 'Trap Sense')),
        (7, ('Feat', 'Damage Reduction')),
        (11, ('Feat', 'Greater Rage')),
        (14, ('Feat', 'Indomitable Will')),
        (17, ('Feat', 'Tireless Rage')),
        (20, ('Feat', 'Mighty Rage')),
    ),
}

def register(protos):
    protos['Class'][name] = Class(name, **proto)
