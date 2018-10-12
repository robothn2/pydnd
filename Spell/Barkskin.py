#coding: utf-8

proto = {
    'name': 'Barkskin',
    'desc': '''Barkskin hardens the target creature's skin, granting a natural armor bonus to Armor Class based on the caster's level: Level 1-6: +3, Level 7-12: +4, Levels 13+: +5''',
    'CasterLevel': [('Druid', 2), ('Ranger', 2), ('Plant', 2)],
    'InnateLevel': 2,
    'School': 'Transmutation',
    'Component': ['Verbal', 'Somatic'],
    'Target': 'Single',
    'Range': 'Touch',
    'Duration': '1 hour / level',
    'Save': [],
    'SpellResistance': False
}
source = 'Buff:' + proto['name']

def duration(caster, metaMagics):
    return 3600.0 * caster.getClassLevel()

def apply(caster, propCalc, metaMagics):
    level = caster.calc.calcPropValue('Caster.Level', caster, None)
    value = 3
    if level >= 13:
        value = 5
    elif level >= 7:
        value = 4
    propCalc.addSource('ArmorClass.Natural', name=source, calcInt=value)

def unapply(propCalc):
    print('unapply buff', proto['name'])
    propCalc.removeSource('ArmorClass.Natural', source)
