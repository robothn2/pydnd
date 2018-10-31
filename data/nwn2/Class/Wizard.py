#coding: utf-8
from Models import Class

name = 'Wizard'
proto = {
    'desc': '''The wizard's strength is her spells. Everything else is secondary. She learns new spells as she experiments and grows in experience, and she can also learn them from other wizards. In addition to learning new spells, a wizard can, over time, learn to manipulate her spells so they go farther, work better, or are improved in some other way. Some wizards prefer to specialize in a certain type of magic. Specialization makes a wizard more powerful in her chosen field, but it denies her access to some of the spells that lie outside that field.''',
    'Hit Die': 'd4',
    'Base Attack Bonus': 'Low.',
    'High Saves': 'Will.',
    'Weapon Proficiencies': ('Club', 'Dagger', 'HeavyCrossbow', 'LightCrossbow', 'Quarterstaff'),
    'Armor Proficiencies': (),
    'Skill Points': 2,
    'Class Skills': ('Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftWeapon', 'Lore', 'Spellcraft'),
    'bonus': (
        (lambda level: level % 5 == 0,
            ('FeatBonus', ('MetaMagic', 'ItemCreation', 'Spell Mastery'), '''At 5th, 10th, 15th, and 20th level, a wizard gains a bonus feat. At each such opportunity, she can choose a metamagic feat, an item creation feat, or Spell Mastery. The wizard must still meet all prerequisites for a bonus feat, including caster level minimums.''')),
        (1, ('SpellType', 'Arcane', '''A wizard casts arcane spells, which are drawn from the sorcerer/wizard spell list. A wizard must choose and prepare her spells ahead of time. To learn, prepare, or cast a spell, the wizard must have an Intelligence score equal to at least 10 + the spell level (Int 10 for 0-level spells, Int 11 for 1st-level spells, and so forth).''')),
        (1, ('Feat', ('Familiar', 'Spellbook'))),
    ),
}

def register(protos):
    protos['Class'][name] = Class(name, **proto)
