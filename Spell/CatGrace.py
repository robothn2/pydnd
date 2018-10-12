#coding: utf-8

proto = {
    'name': 'Cat\'s Grace',
    'desc': '''The target creature's Dexterity is increased by +4.''',
    'CasterLevel': [('Druid', 2), ('Ranger', 2), ('Bard', 2), ('Wizard', 2), ('Sorcerer', 2), ('Animal', 2)],
    'InnateLevel': 2,
    'School': 'Transmutation',
    'Component': ['Verbal', 'Somatic'],
    'Target': 'Touch',
    'Range': 'Single',
    'Duration': '60 seconds / level',
    'Save': [],
    'SpellResistance': False
}
source = 'Buff:' + proto['name']

def duration(caster, metaMagics):
    return 60.0 * caster.getClassLevel()

def apply(caster, propCalc, metaMagics):
    propCalc.addSource('Ability.Dex.Buff', name=source, calcInt=4)

def unapply(propCalc):
    print('unapply buff', proto['name'])
    propCalc.removeSource('Ability.Dex.Buff', source)
