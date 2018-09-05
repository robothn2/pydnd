#coding: utf-8
import os

def feats_load(scriptRoot):
    protos = {}
    for folder, _, fileNames in os.walk(scriptRoot, followlinks=False):
        for fileName in fileNames:
            (name, extension) = os.path.splitext(fileName)
            if extension != '.py':
                continue
            mod = __import__('Feat.' + name)
            protos[name] = eval('mod.' + name)
    return protos

def feats_apply(unit):
    feats = unit.props['feats']
    protos = unit.ctx['protosFeat']
    for featName in feats.keys():
        if featName not in protos:
            continue

        proto = protos[featName]
        proto.apply(unit)
