#coding: utf-8
from Models import Class

name = 'Bard'
proto = {
    'desc': '''A bard brings forth magic from his soul, not from a book. He can cast only a small number of spells, but he can do so without selecting or preparing them in advance. His magic emphasizes charms and illusions over the more dramatic evocation spells that wizards and sorcerers often use. In addition to spells, a bard works magic with his music and poetry. He can encourage allies, hold his audiences rapt, and counter magical effects that rely on speech or sound. Bards have some of the skills that rogues have, although bards are not as focused on skill mastery as rogues are. A bard listens to stories as well as telling them, of course, so he has a vast knowledge of local events and noteworthy items.''',
    'Alignment': ('NeutralGood', 'Neutral', 'NeutralEvil', 'ChaoticGood', 'ChaoticNeutral', 'ChaoticEvil'),
    'Hit Die': 'd6',
    'Base Attack Bonus': 'Medium',
    'High Saves': 'Reflex and Will.',
    'Weapon Proficiencies': ('Simple', 'Longsword', 'Rapier', 'Shortsword', 'Shortbow'),
    'Armor Proficiencies': ('Light', 'Shield'),
    'Skill Points': 6,
    'Class Skills': ('Appraise', 'Bluff', 'Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Diplomacy', 'Hide', 'Listen', 'Lore', 'MoveSilently', 'Parry', 'Perform', 'SleightOfHand', 'Spellcraft', 'Taunt', 'Tumble', 'UseMagicDevice'),
    'bonus': (
        (1, ('SpellType', 'Arcane', '''A bard casts arcane spells, which are drawn from the bard spell list. He can cast any spell he knows without preparing it ahead of time. To learn or cast a spell, a bard must have a Charisma score equal to at least 10 + the spell level (Cha 10 for 0-level spells, Cha 11 for 1st-level spells, and so forth). Starting at 8th level, and every three levels after, bards can replace one known spell with a new spell of the same level. The spell that can be replaced must be two spell levels below what the bard can currently cast (1st level spell at 8, 1st or 2nd level spell at 11, 1st or 2nd or 3rd level spell at 14, and so forth). Bards do not suffer from arcane spell failure when wearing light armor; medium and heavy armors, and shields still incur the normal failure chance.''')),
        (1, ('Feat', ('Bardic Knowledge', 'Inspiration', 'Inspire Courage', 'Bardic Music', 'Countersong', 'Fascinate'))),
        (2, ('Feat', 'Inspire Competence')),
        (3, ('Feat', 'Haven Song')),
        (5, ('Feat', 'Inspire Defense')),
        (6, ('Feat', 'Cloud Mind')),
        (7, ('Feat', 'Inspire Regeneration')),
        (8, ('Feat', 'Inspire Toughness')),
        (9, ('Feat', 'Ironskin Chant')),
        (11, ('Feat', 'Inspire Slowing')),
        (12, ('Feat', 'Song of Freedom')),
        (14, ('Feat', 'Inspire Jarring')),
        (15, ('Feat', 'Song of Heroism')),
        (18, ('Feat', 'Legionnaire March')),
    ),
}

def register(protos):
    protos['Class'][name] = Class(name, **proto)
