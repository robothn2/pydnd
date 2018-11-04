#coding: utf-8
from Models import register_feat

def __apply(feat, caster, target, **kwargs):
    caster.calc.addSource('SavingThrow.All', name=feat.nameFull, calcInt=1)
    caster.calc.addSource('ArmorClass.Luck', name=feat.nameFull, calcInt=1)
def __unapply(feat, caster, target, **kwargs):
    caster.calc.removeSource('SavingThrow.All', feat.nameFull)
    caster.calc.removeSource('ArmorClass.Luck', feat.nameFull)

def register(protos):
    register_feat(protos, 'General', 'Luck of Heroes',
        type = 'Background',
        apply = __apply,
        unapply = __unapply,
        specifics = '''Character gains a +1 bonus on all saving throws as well as a +1 luck bonus to Armor Class.''',
    )
