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
