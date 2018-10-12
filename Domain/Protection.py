#coding: utf-8

proto = {
    'name': 'Protection',
    'desc': '''Clerics who take the Protection domain are able to shield themselves from harm using their special abilities and spells.''',
    'BonusFeats': [
        ('Feat', 'DivineProtection', '''Once per day, the cleric is able to cast an improved sanctuary spell-like ability that sets the save DC at 10 + Charisma modifier + cleric level. The effect has a duration of 1 round per caster level + the cleric's Charisma modifier.'''),
    ],
    'BonusSpells': ['LesserGlobeOfInvulnerability', 'EnergyImmunity'],
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    unit.addFeat('DivineProtection')
    unit.addAccessSpell('Cleric', ['LesserGlobeOfInvulnerability', 'EnergyImmunity'])
