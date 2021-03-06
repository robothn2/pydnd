#coding: utf-8

def __apply(feat, caster, target, **kwargs):
    caster.calc.addSource('SavingThrow.All', name=feat.name, calcInt=1)
    caster.calc.addSource('ArmorClass.Luck', name=feat.name, calcInt=1)
def __unapply(feat, caster, target, **kwargs):
    caster.calc.removeSource('SavingThrow.All', feat.name)
    caster.calc.removeSource('ArmorClass.Luck', feat.name)

protos = [
  {
    'name': 'Luck of Heroes',
    'type': 'Feat', 'category': 'Background',
    'apply': __apply,
    'unapply': __unapply,
    'specifics': '''Character gains a +1 bonus on all saving throws as well as a +1 luck bonus to Armor Class.''',
  },
]
