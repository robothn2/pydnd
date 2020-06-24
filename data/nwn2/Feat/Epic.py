#coding: utf-8

protos = [
  {
    'name': 'Epic Prowess',
    'type': 'Feat', 'category': 'Epic',
    'apply': lambda feat, caster, target, **kwargs: caster.calc.addSource('AttackBonus.Additional', name=feat.nameFull, calcInt=1),
    'unapply': lambda feat, caster, target, **kwargs: caster.calc.removeSource('AttackBonus.Additional', feat.nameFull),
    'prerequisite': [('Level', 21)],
    'specifics': '''The character gains +1 attack bonus''',
  },
]

def __applyGreatAbility(feat, caster, target, **kwargs):
    ability = feat.nameFull[6:9]
    propName = 'Ability.%s.Base' % ability
    prop = caster.calc.getProp(propName)
    value = prop.calcSingleSource(feat.nameFull, caster, None)
    caster.calc.addSource(propName, name=feat.nameFull, calcInt=value+1)
def __unapplyGreatAbility(feat, caster, target, **kwargs):
    pass

for ability in ('Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'):
  proto = {
    'name': 'Great ' + ability,
    'type': 'Feat', 'category': 'Epic',
    'apply': __applyGreatAbility,
    'unapply': __unapplyGreatAbility,
    'prerequisite': [('Level', 21)],
    'specifics': 'The character gains +1 ' + ability,
  }
  protos.append(proto)