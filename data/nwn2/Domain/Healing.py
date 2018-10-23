#coding: utf-8

proto = {
    'name': 'Healing',
    'desc': '''Clerics who take the Healing domain are able to cure wounds more effectively than their brethren, and they gain access to cure spells at a faster rate.''',
    'BonusFeats': [
        ('Feat', 'EmpowerHealing', 'The following healing spells are cast as if with the Empower Spell feat: CureMinorWounds, CureLightWounds, CureModerateWounds, CureSeriousWounds, and CureCriticalWounds.'),
    ],
    'BonusSpells': ['CureSeriousWounds', 'Heal'],
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    unit.addFeat('EmpowerHealing')
    unit.addAccessSpell('Cleric', ['CureSeriousWounds', 'Heal'])
