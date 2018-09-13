#coding: utf-8

proto = {
    'name': 'Drow',
    'desc': '''Descended from the original dark-skinned elven subrace called the Illythiiri, the drow were cursed into their present appearance by the good elven deities for following the goddess Lolth down the path to evil and corruption. Also called dark elves, the drow have black skin that resembles polished obsidian and stark white or pale yellow hair. They commonly have very pale eyes in shades of lilac, silver, pink, and blue. They also tend to be smaller and slimmer than most elves.''',
    'RacialTraits': '''\
- Ability Adjustments: +2 Dexterity, +2 Intelligence, +2 Charisma, -2 Constitution.\n
- Hardiness vs. Enchantments: Immunity to magical sleep effects, +2 racial bonus to saving throws against enchantment spells or effects.\n
- Weapon Proficiency: Elves receive the Martial Weapon Proficiency feats for the longsword, rapier, longbow (including composite longbow), and shortbow (including composite shortbow) as bonus feats.\n
- Keen Senses: +2 racial bonus to Listen, Search, and Spot checks.\n
- Spell-Like Abilities:\n
1/day - Darkness as sorcerer of equal level.\n
1/day - See invisibility as sorcerer of equal level.\n
- Darkvision: Drow can see in the dark up to 120 feet. This replaces the low-light vision ability most elves receive.\n
- Spell Resistant: Spell resistance of 11+ character level.\n
- Strong Will: +2 racial bonus to Will saves against spells and spell-like abilities.\n
- Light Sensitivity: Drow suffer -2 circumstance penalty to attack rolls, saves, and checks in bright sunlight.\n
- Level Adjustment +2: Drow are more powerful and gain levels more slowly than other races. It will take more experience for a drow to reach level 2 than it would for normal races, for example.\n
- Favored Class: Wizard'''
}

def apply(unit):
    print('apply race %s' % proto['name'])
    source = 'Race:' + proto['name']
    unit.setProp('LevelAdjustment', 2)

    unit.modifier.updateSource(('Abilities', 'Dex', 'Adjustment', source), 2)
    unit.modifier.updateSource(('Abilities', 'Int', 'Adjustment', source), 2)
    unit.modifier.updateSource(('Abilities', 'Cha', 'Adjustment', source), 2)
    unit.modifier.updateSource(('Abilities', 'Con', 'Adjustment', source), -2)

    unit.modifier.updateSource(('Skills', 'Listen', source), 2)
    unit.modifier.updateSource(('Skills', 'Search', source), 2)
    unit.modifier.updateSource(('Skills', 'Spot', source), 2)

    unit.modifier.updateSource(('SavingThrow', 'Will', source), 2)

    unit.modifier.updateSource(('SpellResistance', 'Race', source), 11 + unit.getClassLevel())

    unit.addFeat('Darkvision')
    unit.addFeat('WeaponProficiency', ['longsword', 'rapier', 'longbow', 'shortbow'])
    unit.addFeat('FavoredClass', 'Wizard')
