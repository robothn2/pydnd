#coding: utf-8
from Models import Feat, register_feat

def __active(feat, caster, target, **kwargs):
    params = kwargs.get('params')
    value = 6 if params and 'Improved' in params else 3
    caster.calc.addSource('AttackBonus.Additional', name=feat.nameFull, calcInt=-value)
    caster.calc.addSource('Damage.Additional', name=feat.nameFull, calcInt=lambda caster, target: ('Physical', feat.nameFull, value))

def __deactive(feat, caster):
    caster.calc.removeSource('AttackBonus.Additional', feat.nameFull)
    caster.calc.removeSource('Damage.Additional', feat.nameFull)

def register(protos):
    # register main feat
    register_feat(protos, 'PowerAttack', 'Power Attack',
                  apply=lambda feat, caster, target, **kwargs: caster.calc.addSource('Spell.Activable', name=feat.nameFull, calcInt=feat),
                  unapply=lambda feat, caster, target, **kwargs: caster.calc.removeSource('Spell.Activable', feat.nameFull),
                  active=__active,
                  deactive=__deactive,
                  prerequisite=[('Ability', 'Str', 13)],
                  specifics='''A character with this feat can make powerful but ungainly attacks. When Power Attack is selected, it grants a +3 bonus to the damage roll, but at the cost of -3 to the attack roll.''',
                  )

    #register member feats
    register_feat(protos, 'PowerAttack', 'Improved Power Attack',
                  nameMember='Improved',
                  prerequisite=[('Feat', 'PowerAttack'), ('BaseAttackBonus', 6)],
                  specifics='''This feat allows the character to trade a -6 penalty on his attack roll to gain a +6 bonus on his damage roll. It is very useful when fighting tough, easy-to-hit opponents.''',
                  )

    register_feat(protos, 'FavoredEnemy', 'Favored Power Attack',
                  prerequisite=[('Feat', 'FavoredEnemy'), ('Feat', 'PowerAttack'), ('BaseAttackBonus', 4)],
                  specifics='''When you use the Power Attack or Improved Power Attack feat with a one-handed weapon against a favored enemy, your Power Attack damage bonus is doubled. With a two-handed weapon against a favored enemy, your Power Attack damage bonus is tripled.''',
                  )
