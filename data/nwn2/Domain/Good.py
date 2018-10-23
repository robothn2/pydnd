#coding: utf-8

proto = {
    'name': 'Good',
    'desc': '''Clerics who take the Good domain inspire their allies to heroism and are granted spells that protect against and bind evil creatures.''',
    'BonusFeats': [
        ('Feat', 'AuraOfCourage', 'The cleric is immune to fear and all allies receive a +4 saving throw bonus against fear.'),
    ],
    'BonusSpells': ['MagicCircleAgainstEvil', 'LesserPlanarBinding'],
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    unit.addFeat('AuraOfCourage')
    unit.addAccessSpell('Cleric', ['MagicCircleAgainstEvil', 'LesserPlanarBinding'])
