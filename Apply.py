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
                         weapon, weaponHand):
    if maxAttackTimes == 0:
        return []
    babList = calc_attackbonus_list(maxAttackTimes, baseAttackBonus, babDecValue)
    durationAttack = (secondsPerTurn - delaySecondsToFirstAttack) / len(babList)
    tsOffset = delaySecondsToFirstAttack
    attacks = []
    for _,bab in enumerate(babList):
        attacks.append((round(tsOffset,3), bab, weaponHand, weapon))
        tsOffset += durationAttack
    return attacks
