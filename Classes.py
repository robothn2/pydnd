#coding: utf-8
import os

def classes_load(classScriptRoot):
    protos = {}
    for folder, _, fileNames in os.walk(classScriptRoot, followlinks=False):
        for fileName in fileNames:
            (name, extension) = os.path.splitext(fileName)
            if extension != '.py':
                continue
            mod = __import__('Class.' + name)
            #print(dir(mod))
            proto = eval('mod.' + name)
            #print(dir(proto))
            protos[name] = proto
    return protos

def classes_apply(classes, modifier):
    for cls in classes.keys():
        clsLevel = classes[cls]['level']
        clsProto = classes[cls]['proto']

        modifier.addTypedSource('HitPoint', 'Class', int(clsLevel * int(clsProto.proto['HitDie'])), cls)
        modifier.addTypedSource('AttackBonus', 'Base', int(clsLevel * float(clsProto.proto['BaseAttackBonus'])), cls)
        modifier.addTypedSource('SavingThrow', 'Fortitude', int(clsLevel * float(clsProto.proto['FortitudePerLevel'])), cls)
        modifier.addTypedSource('SavingThrow', 'Reflex', int(clsLevel * float(clsProto.proto['ReflexPerLevel'])), cls)
        modifier.addTypedSource('SavingThrow', 'Will', int(clsLevel * float(clsProto.proto['WillPerLevel'])), cls)

