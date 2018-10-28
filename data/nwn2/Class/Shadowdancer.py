#coding: utf-8
from Models import Class

name = 'Shadowdancer'

proto = {
    'desc': '''Operating in the border between light and darkness, shadowdancers are nimble artists of deception. They are mysterious and unknown, never completely trusted but always inducing wonder when met. Rogues, bards, and monks make excellent shadowdancers. Fighters, barbarians, rangers, and paladins also find that shadowdancer abilities allow them to strike at their opponents with surprise and skill. Wizard, sorcerer, cleric, and druid shadowdancers employ the defensive capabilities inherent in the prestige class to allow them to cast their spells from safety and move away quickly. Despite their link with shadows and trickery, shadowdancers are as often good as evil.''',
    'Hit Die': 'd8',
    'Base Attack Bonus': 'Medium.',
    'High Saves': 'Reflex.',
    'Weapon Proficiencies': ('Simple'),
    'Armor Proficiencies': ('Light'),
    'Skill Points': 6,
    'Class Skills': ('Bluff', 'CraftTrap', 'Diplomacy', 'Hide', 'Listen', 'MoveSilently', 'Parry', 'Search', 'SleightOfHand', 'Spot', 'Tumble'),
    'requirements': (
        ('Skill', 'Move Silently', 8),
        ('Skill', 'Hide', 10),
        ('Skill', 'Tumble', 5),
        ('Feat', ('Dodge', 'Mobility'))
    ),
    'bonus': (
        (1, ('Feat', 'Hide in Plain Sight')),
        (2, ('Feat', ('Darkvision', 'Evasion', 'Uncanny Dodge'))),
        (3, ('Feat', ('Summon Shadow', 'Shadow Daze'))),
        (4, ('Feat', 'Shadow Evade')),
        (5, ('Feat', ('Defensive Roll', 'Improved Uncanny Dodge'))),
        (7, ('Feat', 'Slippery Mind')),
        (10, ('Feat', 'Improved Evasion')),
    ),
}

def register(protos):
    protos['Class'][name] = Class(name, **proto)
