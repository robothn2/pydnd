#coding: utf-8
from Models import register_feat

def __apply(source, unit, feat, params):
    unit.calc.addSource('SavingThrow.All', name=source, calcInt=1)
    unit.calc.addSource('ArmorClass.Luck', name=source, calcInt=1)
def __unapply(source, unit, feat, params):
    unit.calc.removeSource('SavingThrow.All', source)
    unit.calc.removeSource('ArmorClass.Luck', source)

def register(protos):
    register_feat(protos, 'General', 'Luck of Heroes',
        type = 'Background',
        apply = __apply,
        unapply = __unapply,
        specifics = '''Character gains a +1 bonus on all saving throws as well as a +1 luck bonus to Armor Class.''',
    )
