#coding: utf-8
from Models import register_feat

def __applyGreatAbility(source, unit, feat, params):
    ability = source[5:]
    propName = 'Ability.%s.Base' % ability
    prop = unit.calc.getProp(propName)
    value = prop.calcSingleSource(source, unit, None)
    unit.calc.addSource(propName, name=source, calcInt=value+1)
def __unapplyGreatAbility(source, unit, feat, params):
    pass

def register(protos):
    register_feat(protos, 'General', 'Epic Prowess',
                  type='Epic',
                  apply=lambda source, unit, feat, params: unit.calc.addSource('AttackBonus.Additional', name=source, calcInt=1),
                  unapply=lambda source, unit, feat, params: unit.calc.removeSource('AttackBonus.Additional', source),
                  prerequisite=[('Level', 21)],
                  specifics='''The character gains +1 attack bonus''',
                  )

    for _, ability in enumerate(protos['Abilities']):
        register_feat(protos, 'Great' + ability, 'Great ' + ability,
                      type='Epic',
                      apply = __applyGreatAbility,
                      unapply = __unapplyGreatAbility,
                      prerequisite=[('Level', 21)],
                      specifics = '''The character gains +1 attack bonus''',
                      )