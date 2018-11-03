#coding: utf-8
from Models import register_feat

def __applyToWeapon(source, unit, feat, params, **kwargs):
    weapon = kwargs.get('weapon')
    hand = kwargs.get('hand')
    if params is not list or weapon.getItemBaseName() not in params:
        return

    print(source, 'affects weapon:', weapon.getItemBaseName(), ', params:', params)
    unit.calc.addSource('Damage.'+ hand, name='WeaponSpecialization', calcInt=('Physical', 'WeaponSpecialization', 2))
    if 'Greater' in params:
        unit.calc.addSource('Damage.'+ hand, name='GreaterWeaponSpecialization', calcInt=('Physical', 'GreaterWeaponSpecialization', 2))
    if 'Epic' in params:
        unit.calc.addSource('Damage.'+ hand, name='EpicWeaponSpecialization', calcInt=('Physical', 'EpicWeaponSpecialization', 2))
def __unapply(source, unit, feat, params):
    unit.calc.removeSource('AttackBonus.TwoHand', feat.nameMember)
    unit.calc.removeSource('AttackBonus.MainHand', feat.nameMember)
    unit.calc.removeSource('AttackBonus.OffHand', feat.nameMember)

def register(protos):
    register_feat(protos, 'WeaponSpecialization', 'Weapon Specialization',
                  type='Special',
                  applyToWeapon=__applyToWeapon,
                  unapply=__unapply,
                  prerequisite=[('ClassLevel', 'Fighter', 1), ('BaseAttackBonus', 4), ('Feat', 'Weapon Focus')],
                  specifics='''A character with this feat has trained especially hard with a specific weapon group, and gains a +2 damage bonus when using these weapons in combat.''',
                  )
    register_feat(protos, 'WeaponSpecialization', 'Greater Weapon Specialization',
                  type='Special',
                  prerequisite=[('ClassLevel', 'Fighter', 12), ('Feat', ('Greater Weapon Focus', 'Weapon Specialization'))],
                  specifics='''This feat grants an additional +1 to hit bonus with the selected weapon. This stacks with all other bonuses to attack roll (including Weapon Focus). This feat can be taken multiple times, but each time the effect applies to a new type of weapon.''',
                  )
    register_feat(protos, 'WeaponSpecialization', 'Epic Weapon Specialization',
                  type='Epic',
                  prerequisite=[('Level', 21), ('Feat', ('Epic Weapon Focus', 'Greater Weapon Specialization'))],
                  specifics='''The character gains +6 to all damage dealt using the selected weapon. This feat can be taken multiple times, but applies to a different weapon each time. This bonus replaces that of Weapon Specialization and Greater Weapon Specialization.''',
                  )
