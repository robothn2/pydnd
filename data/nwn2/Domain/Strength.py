#coding: utf-8

proto = {
    'name': 'Strength',
    'desc': '''Clerics who take the Strength domain are able to boost their Strength with divine energy, and gain access to spells that make them stronger and more resilient.''',
    'BonusFeats': [
        ('Feat', 'DivineStrength', '''Once per day, the cleric may gain a bonus to Strength equal to 2 + 1 per 3 class levels. This effect has a duration of 5 rounds + the cleric's Charisma modifier.'''),
    ],
    'BonusSpells': ['BullStrength', 'DivinePower'],
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    unit.addFeat('DivineStrength')
    unit.addAccessSpell('Cleric', ['BullStrength', 'DivinePower'])
