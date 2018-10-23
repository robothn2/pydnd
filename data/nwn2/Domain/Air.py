#coding: utf-8

proto = {
    'name': 'Air',
    'desc': '''Clerics of the Air domain move with the subtlety of the breeze and gain the ability to cast electrical damage spells.''',
    'BonusFeats': [
        ('Feat', 'UncannyDodge',
         '''The cleric receives the weapon focus feat for their deity's favored weapon. They are also proficient with that weapon even if clerics normally are not. If their deity's favored weapon is unarmed strike, they gain the improved unarmed strike feat.'''),
    ],
    'BonusSpells': ['CallLightning', 'ChainLightning'],
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    unit.addFeat('UncannyDodge')
    unit.addAccessSpell('Cleric', ['CallLightning', 'ChainLightning'])
