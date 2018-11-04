#coding: utf-8
from Models import register_feat

def __applyGreatAbility(feat, caster, target, **kwargs):
    ability = feat.nameFull[6:9]
    propName = 'Ability.%s.Base' % ability
    prop = caster.calc.getProp(propName)
    value = prop.calcSingleSource(feat.nameFull, caster, None)
    caster.calc.addSource(propName, name=feat.nameFull, calcInt=value+1)
def __unapplyGreatAbility(feat, caster, target, **kwargs):
    pass

def register(protos):
    register_feat(protos, 'General', 'Epic Prowess',
                  type='Epic',
                  apply=lambda feat, caster, target, **kwargs: caster.calc.addSource('AttackBonus.Additional', name=feat.nameFull, calcInt=1),
                  unapply=lambda feat, caster, target, **kwargs: caster.calc.removeSource('AttackBonus.Additional', feat.nameFull),
                  prerequisite=[('Level', 21)],
                  specifics='''The character gains +1 attack bonus''',
                  )

    for _, ability in enumerate(['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']):
        register_feat(protos, 'Great' + ability, 'Great ' + ability,
                      type='Epic',
                      apply = __applyGreatAbility,
                      unapply = __unapplyGreatAbility,
                      prerequisite=[('Level', 21)],
                      specifics = '''The character gains +1 ''' + ability,
                      )
