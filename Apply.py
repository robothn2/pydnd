#coding: utf-8

def race_apply(unit, raceName):
    if not raceName in unit.ctx['Race']:
        return
    unit.ctx['Race'][raceName].model.apply(unit)

def feats_apply(unit):
    feats = unit.modifier.getSource('Feats')
    protos = unit.ctx['Feat']
    for featName in feats.keys():
        if featName not in protos:
            continue

        proto = protos[featName]
        if hasattr(proto, 'apply'):
            print('apply feat', proto.proto['name'], ', params', feats[featName])
            proto.apply(unit, feats[featName])

def calc_attackbonus_list(maxAttackTimes, baseAttackBonus, babDecValue):
    bab = int(baseAttackBonus)
    abList = []
    while maxAttackTimes > 0:
        maxAttackTimes -= 1
        abList.append(bab)
        bab -= babDecValue
        if bab <= 0:
            break
    return abList

def calc_attacks_in_turn(maxAttackTimes, baseAttackBonus, babDecValue, secondsPerTurn, delaySecondsToFirstAttack,
                         weapon, hand):
    if maxAttackTimes == 0:
        return []
    babList = calc_attackbonus_list(maxAttackTimes, baseAttackBonus, babDecValue)
    durationAttack = (secondsPerTurn - delaySecondsToFirstAttack) / len(babList)
    tsOffset = delaySecondsToFirstAttack
    attacks = []
    for _,bab in enumerate(babList):
        attacks.append((round(tsOffset,3), bab, hand, weapon))
        tsOffset += durationAttack
    return attacks

def apply_weapon_attacks(weapon, unit, hand, maxAttackTimes = 10):
    tsOffset = 0.5 if hand == 'OffHand' else 0.0
    bab = unit.calc.calcPropValue('AttackBonus.Base', weapon, None)
    babDec = 5

    if weapon.proto['name'] == 'Kama' and unit.getClassLevel('Monk') > 0:
        babDec = 3
    if hand == 'OffHand':
        if not unit.hasFeat('TwoWeaponFighting'):
            maxAttackTimes = 0
        else:
            featParams = unit.getFeatParams('TwoWeaponFighting')
            if 'Perfect' in featParams:
                maxAttackTimes = 10
            elif 'Improved' in featParams:
                maxAttackTimes = 2
            else:
                maxAttackTimes = 1

    # attacks
    unit.calc.addSource('Attacks', name=hand, calcInt=lambda caster, target: \
        calc_attacks_in_turn(maxAttackTimes, bab, babDec, unit.ctx['secondsPerTurn'], tsOffset, weapon, hand))
