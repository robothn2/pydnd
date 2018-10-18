#coding: utf-8

proto = {
    'name': 'NaturalArmorIncrease',
    'Type': 'Class',
    'Specifics': '''At 1st level, the red dragon disciple's skin toughens and begins to grow scaly, granting him a +1 natural armor bonus to AC. This bonus improves to +2 at 4th level, +3 at 7th level, and +4 at 10th level.''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def apply(unit, featParams):
    level = unit.getClassLevel('RedDragonDisciple')
    value = int((level + 2) / 3)
    unit.calc.updatePropIntSource('ArmorClass.Natural', source, value)
