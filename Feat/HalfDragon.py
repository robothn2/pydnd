#coding: utf-8

proto = {
    'name': 'HalfDragon',
    'Type': 'Class',
    'Specifics': '''At 10th level, the red dragon disciple's transformation is complete. He becomes a half-dragon, and gains darkvision as well as immunity to sleep, paralysis, and fire.''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def apply(unit, featParams):
    unit.calc.addSource('Vision.Dark', name=source, calcInt=60)
    unit.calc.addSource('Immunity.Sleep', name=source, calcInt=1)
    unit.calc.addSource('Immunity.Paralysis', name=source, calcInt=1)
    unit.calc.addSource('Reduction.Fire', name=source, calcInt=-1)
