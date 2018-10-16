#coding: utf-8

proto = {
    'desc': '''You gain a +1 bonus to attack and a +1 magical damage bonus for every three caster levels you have (minimum +1, maximum of +3).''',
    'CasterLevel': [('Cleric', 1), ('Paladin', 1)],
    'InnateLevel': 1,
    'School': 'Evocation',
    'Component': ['Verbal', 'Somatic'],
    'Target': 'Caster',
    'Range': 'Personal',
    'Duration': '1 minute',
    'Save': [],
    'SpellResistance': False
}
name = 'DivineFavor'
source = 'Buff:' + name

def duration(caster, metaMagics):
    return 60.0

def apply(caster, propCalc, metaMagics):
    level = caster.calc.calcPropValue('Caster.Level', caster, None)
    value = max(1, min(3, int(level / 3)))
    propCalc.addSource('AttackBonus.Additional', name=source, calcInt=value)
    propCalc.addSource('Damage.Additional', name=source, calcInt=lambda caster,target: ('Magical', source, value))

def unapply(propCalc):
    propCalc.removeSource('AttackBonus.Additional', source)
    propCalc.removeSource('Damage.Additional', source)