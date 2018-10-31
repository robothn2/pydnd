#coding: utf-8
from Models import Domain

def _addDeityWeaponFocus(unit):
    deityName = unit.getProp('deity')
    deity = unit.ctx['Deity'].get(deityName)
    if not deity:
        return

    weapon = deity.model.favoredWeapon
    print('deity:', deityName, ', favored weapon:', weapon)
    if weapon == 'Unarmed Strike':
        unit.addFeat('Improved Unarmed Strike')
    else:
        unit.addFeat('Weapon Proficiency', weapon)
        unit.addFeat('Weapon Focus', weapon)

def register(protos):
    protos['Domain']['War'] = Domain(
        'War',
         desc = 'Clerics who take the War domain spend considerable time training for combat.',
         bonus = (
            (_addDeityWeaponFocus, '''The cleric receives the weapon focus feat for their deity's favored weapon. They are also proficient with that weapon even if clerics normally are not. If their deity's favored weapon is unarmed strike, they gain the improved unarmed strike feat.'''),
            ('SpellAccess', 'Cleric', ('Flame Strike', 'Power Word Stun')),
        ))
