#coding: utf-8

proto = {
    'desc': '''This spell strengthens your animal companion, giving its attacks a +1 enhancement bonus to attack and damage for every three caster levels you have (maximum of +5).''',
    'CasterLevel': [('Druid', 3), ('Ranger', 3)],
    'InnateLevel': 3,
    'School': 'Transmutation',
    'Component': ['Verbal', 'Somatic'],
    'Target': 'Personal',
    'Range': 'Caster',
    'Duration': '60 seconds / level',
    'Save': [],
    'SpellResistance': False
}
name = 'GreaterMagicFang'
source = 'Buff:' + name

def duration(caster, metaMagics):
    return 60.0 * caster.getClassLevel()

def apply(caster, target, metaMagics):
    level = caster.calc.calcPropValue('Caster.Level', caster, None)
    value = min(5, int((level + 2) / 3))
    target.calc.addSource('AttackBonus.Additional', name=source, calcInt=value)
    target.calc.addSource('Damage.Additional', name=source, calcInt=value)

def unapply(target):
    target.calc.removeSource('AttackBonus.Additional', source)
    target.calc.removeSource('Damage.Additional', source)
