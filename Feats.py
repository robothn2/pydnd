#coding: utf-8
import os

def feats_apply(unit):
    feats = unit.props['feats']
    protos = unit.ctx['protosFeat']
    for featName in feats.keys():
        if featName not in protos:
            continue

        proto = protos[featName]
        proto.apply(unit, feats[featName])
