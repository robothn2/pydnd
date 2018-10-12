#coding: utf-8

proto = {
    'name': 'Time',
    'desc': '''Clerics who take the Time domain are quick to act.''',
    'BonusFeats': [
        ('Feat', 'ImprovedInitiative', 'The cleric receives a bonus to initiative rolls'),
    ],
    'BonusSpells': ['Haste', 'Premonition'],
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    unit.addFeat('ImprovedInitiative')
    unit.addAccessSpell('Cleric', ['Haste', 'Premonition'])
