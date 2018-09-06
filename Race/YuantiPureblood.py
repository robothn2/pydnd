#coding: utf-8

proto = {
    'name': 'YuantiPureblood',
    'desc': '''The yuan-ti are descended from humans whose bloodlines have been mingled with those of snakes. Their evilness, cunning, and ruthlessness are legendary. Yuan-ti constantly scheme to advance their own dark agendas. They are calculating and suave enough to form alliances with other evil creatures when necessary, but they always put their own interests first.\nYuan-ti that can pass for humans with suitable clothing, cosmetics, and magic are known as Purebloods. These creatures are usually charged with infiltrating humanoid societies and managing covert operations that require direct contact with humanoids.''',
    'RacialTraits': '''
- Ability Adjustments: +2 Dexterity, +2 Intelligence, +2 Charisma\n
- Darkvision: Yuan-ti purebloods can see in the dark up to 60 feet.\n
- Scaled Skin: +1 Natural Armor Bonus.\n
- Spell Resistant: Spell resistance of 11+ character level.\n
- Snake Senses: You gain the feats Alertness (+2 to Spot and Listen skills) and Blind-Fight (bonuses to fighting while blind or against invisible creatures) for free.\n
- Spell-Like Abilities (1/day): Animal Trance, Cause Fear, Charm Person, Darkness, Entangle\n
- Level adjustment: +2\n
- Favored Class: Ranger'''
}

def apply(unit):
    print('apply race %s' % proto['name'])
    unit.setProp('LevelAdjustment', 2)
    unit.modifier.addTypedSource('Dex', 'Adjustment', 2, 'Race:' + proto['name'])
    unit.modifier.addTypedSource('Int', 'Adjustment', 2, 'Race:' + proto['name'])
    unit.modifier.addTypedSource('Cha', 'Adjustment', 2, 'Race:' + proto['name'])
    unit.modifier.addTypedSource('ArmorClass', 'Natural', 1, 'Race:' + proto['name'])
    totalLevel = unit.props.sumFieldValue('classes', 'level')
    unit.modifier.addTypedSource('SpellResistant', 'Race', 11 + totalLevel, 'Race:' + proto['name'])
    unit.addFeat(['Darkvision', 'Alertness', 'BlindFight', 'FavoredClass(Ranger)'])
