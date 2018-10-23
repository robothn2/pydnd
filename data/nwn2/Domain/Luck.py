#coding: utf-8

proto = {
    'name': 'Luck',
    'desc': '''Clerics who take the Luck domain are gifted with incredible fortune.''',
    'BonusFeats': [
        ('Feat', 'LuckOfHeroes'),
    ],
    'BonusSpells': ['FreedomOfMovement', 'GreaterSpellMantle'],
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    unit.addFeat('LuckOfHeroes')
    unit.addAccessSpell('Cleric', ['FreedomOfMovement', 'GreaterSpellMantle'])
