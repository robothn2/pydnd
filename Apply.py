#coding: utf-8
from Dice import rollDice

def race_apply(unit, raceName):
    if not raceName:
        return
    protosRace = unit.ctx['protosRace']
    if raceName not in protosRace:
        return
    proto = protosRace[raceName]
    proto.apply(unit)

def buffs_apply(unit):
    pass

def feats_apply(unit):
    feats = unit.modifier.getSource('Feats')
    protos = unit.ctx['protosFeat']
    for featName in feats.keys():
        if featName not in protos:
            continue

        proto = protos[featName]
        proto.apply(unit, feats[featName])

def calc_attackbonus_list(baseAttackBonus, babDecValue):
    bab = int(baseAttackBonus)
    abList = []
    while 1:
        abList.append(bab)
        bab -= babDecValue
        if bab <= 0:
            break
    return abList

def calc_attacks_in_turn(baseAttackBonus, babDecValue, secondsPerTurn, delaySecondsToFirstAttack,
                         weapon, hasHasteBuff, isMainhand):
    babList = calc_attackbonus_list(baseAttackBonus, babDecValue)
    if hasHasteBuff:
        babList.insert(0, babList[0])

    durationAttack = (secondsPerTurn - delaySecondsToFirstAttack) / len(babList)
    tsOffset = delaySecondsToFirstAttack
    attacks = []
    for _,bab in enumerate(babList):
        attacks.append((round(tsOffset,3), bab, isMainhand, weapon))
        tsOffset += durationAttack
    return attacks

def weapon_apply(unit):
    conditions = unit.modifier.getSource(['Conditional', 'Weapon'])

    attacks = []
    bab = unit.modifier.sumSource(('AttackBonus', 'Base'))
    #print(calc_attackbonus_list(bab, 5))
    weaponMH = unit.getProp('WeaponMainHand')
    if weaponMH:
        attacks.extend(calc_attacks_in_turn(bab, 5, unit.ctx['secondsPerTurn'], 0.0,
                                       weaponMH, unit.hasBuff('Haste'), True))

        # apply weapon based conditions
        for sourceName, cond in conditions.items():
            condition, featParams = cond  # @see Feat/WeaponFocus.py
            condition(unit, weaponMH, featParams)

    #if unit.hasFeats(['TwoWeaponFighting']):
    weaponOH = unit.getProp('WeaponOffHand')
    if weaponOH:
        attacks.extend(calc_attacks_in_turn(bab, 5, unit.ctx['secondsPerTurn'], 0.3, weaponOH, False, False))

        # apply weapon based conditions
        for sourceName, cond in conditions.items():
            condition, featParams = cond
            condition(unit, weaponOH, featParams)

    #print(attacks)
    attacks.sort(key=lambda att: att[0], reverse=False)
    unit.modifier.updateSource(['Attacks'], attacks)
