#coding: utf-8
from Dice import rollDice

def race_apply(unit):
    if 'race' not in unit.props:
        return
    race = unit.props['race']
    protosRace = unit.ctx['protosRace']
    if race not in protosRace:
        return
    proto = protosRace[race]
    proto.apply(unit)

def classes_apply(unit):
    classes = unit.getProp('classes')
    for cls in classes.keys():
        clsLevel = classes[cls]['level']
        clsProto = classes[cls]['proto']

        unit.modifier.updateSource(('HitPoint', 'Class', cls), int(clsLevel * int(clsProto.proto['HitDie'])))
        unit.modifier.updateSource(('AttackBonus', 'Base', cls), int(clsLevel * float(clsProto.proto['BaseAttackBonus'])))
        unit.modifier.updateSource(('SavingThrow', 'Fortitude', cls), int(clsLevel * float(clsProto.proto['FortitudePerLevel'])))
        unit.modifier.updateSource(('SavingThrow', 'Reflex', cls), int(clsLevel * float(clsProto.proto['ReflexPerLevel'])))
        unit.modifier.updateSource(('SavingThrow', 'Will', cls), int(clsLevel * float(clsProto.proto['WillPerLevel'])))

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

def abilities_modifier(unit, ability):
    return int( (unit.modifier.sumSource(('Abilities', ability)) - 10) / 2 )
def abilities_apply(unit):
    modStr = abilities_modifier(unit, 'Str')
    modDex = abilities_modifier(unit, 'Dex')
    modCon = abilities_modifier(unit, 'Con')
    unit.modifier.updateSource(('AttackBonus', 'Str', 'Ability:Str'), modStr)
    unit.modifier.updateSource(('ArmorClass', 'Dex', 'Ability:Dex'), modDex)
    unit.modifier.updateSource(('HitPoint', 'Con', 'Ability:Con'), modCon)
    unit.modifier.updateSource(('Damage', 'Additional', 'Physical', 'Ability:Str'), modStr)

    # todo: apply abilities to skills
    unit.modifier.updateSource(('Skills', 'Tumble', 'Modifier', 'Ability:Dex'), modDex)

def skills_apply(unit):
    tumbleLevel = unit.modifier.sumSource(('Skills', 'Tumble'))
    spellcraftLevel = unit.modifier.sumSource(('Skills', 'Spellcraft'))
    unit.modifier.updateSource(('ArmorClass', 'Tumble', 'Skills:Tumble'), int(tumbleLevel / 10))
    unit.modifier.updateSource(('SavingThrow', 'All', 'Skills:Spellcraft'), int(spellcraftLevel / 5))

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
