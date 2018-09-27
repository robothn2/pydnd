#coding: utf-8

proto = {
    'name': 'DivineFavor',
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
source = proto['name']

def calcDuration(caster, metaMagics):
    return 60.0

def applyModifier(caster, targetModifier, metaMagics):
    print('apply buffer', source)
    level = caster.getCasterLevel()
    print('CasterLevel', level)
    value = max(1, min(3, int(level / 3)))
    targetModifier.updateSource(('AttackBonus', 'Additional', source), value)
    targetModifier.updateSource(('Damage', 'Additional', 'Magical', source), value)

def removeModifier(targetModifier):
    targetModifier.removeSource(('AttackBonus', 'Additional', source))
    targetModifier.removeSource(('Damage', 'Additional', 'Magical', source))