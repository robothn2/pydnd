#coding: utf-8

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
    feats = unit.props['feats']
    protos = unit.ctx['protosFeat']
    for featName in feats.keys():
        if featName not in protos:
            continue

        proto = protos[featName]
        proto.apply(unit, feats[featName])

def abilities_modifier(unit, ability):
    return int( (unit.modifier.sumSource(('Abilities', ability), ['Base']) - 10) / 2 )
def abilities_apply(unit):
    modStr = abilities_modifier(unit, 'Str')
    modDex = abilities_modifier(unit, 'Dex')
    modCon = abilities_modifier(unit, 'Con')
    unit.modifier.updateSource(('AttackBonus', 'Str', 'Ability:Str'), modStr)
    unit.modifier.updateSource(('ArmorClass', 'Dex', 'Ability:Dex'), modDex)
    unit.modifier.updateSource(('HitPoint', 'Con', 'Ability:Con'), modCon)
    unit.modifier.updateSource(('MeleeDamage', 'Additional', 'Ability:Str'), modStr)

    # todo: apply abilities to skills
    unit.modifier.updateSource(('Skills', 'Tumble', 'Modifier', 'Ability:Dex'), modDex)

def skills_apply(unit):
    tumbleLevel = unit.modifier.sumSource(('Skills', 'Tumble'))
    spellcraftLevel = unit.modifier.sumSource(('Skills', 'Spellcraft'))
    unit.modifier.updateSource(('ArmorClass', 'Tumble', 'Skills:Tumble'), int(tumbleLevel / 10))
    unit.modifier.updateSource(('SavingThrow', 'All', 'Skills:Spellcraft'), int(spellcraftLevel / 5))

def weapon_apply(unit):
    weaponMH = unit.getProp('WeaponMainHand')
    if weaponMH:
        print(weaponMH.proto)
        unit.modifier.updateSource(('MeleeDamage', 'MainHand', 'BaseDamage'), weaponMH.proto['BaseDamage']['params'])
        unit.modifier.updateSource(('MeleeDamage', 'MainHand', 'CriticalThreat'), weaponMH.proto['BaseCriticalThreat']['params'])
        unit.modifier.updateSource(('MeleeDamage', 'MainHand', 'DamageType'), weaponMH.proto['BaseDamageType'][0])
    weaponOH = unit.getProp('WeaponOffHand')
    if weaponOH:
        unit.modifier.updateSource(('MeleeDamage', 'OffHand', 'BaseDamage'), weaponOH.proto['BaseDamage']['params'])
        unit.modifier.updateSource(('MeleeDamage', 'OffHand', 'CriticalThreat'), weaponOH.proto['BaseCriticalThreat']['params'])
        unit.modifier.updateSource(('MeleeDamage', 'OffHand', 'DamageType'), weaponOH.proto['BaseDamageType'][0])

    if weaponOH == None and weaponMH.proto['WeaponSize'] == 'Large':
        unit.modifier.updateSource(('MeleeDamage', 'FinalFactor'), 1.5)
    else:
        unit.modifier.updateSource(('MeleeDamage', 'FinalFactor'), 1.0)

    #todo: apply weapon 'Enhancement'
