#coding: utf-8
import os

def classes_apply(classes, modifier):
    for cls in classes.keys():
        clsLevel = classes[cls]['level']
        clsProto = classes[cls]['proto']

        modifier.updateUniqueSource(('HitPoint', 'Class', cls), int(clsLevel * int(clsProto.proto['HitDie'])))
        modifier.updateUniqueSource(('AttackBonus', 'Base', cls), int(clsLevel * float(clsProto.proto['BaseAttackBonus'])))
        modifier.updateUniqueSource(('SavingThrow', 'Fortitude', cls), int(clsLevel * float(clsProto.proto['FortitudePerLevel'])))
        modifier.updateUniqueSource(('SavingThrow', 'Reflex', cls), int(clsLevel * float(clsProto.proto['ReflexPerLevel'])))
        modifier.updateUniqueSource(('SavingThrow', 'Will', cls), int(clsLevel * float(clsProto.proto['WillPerLevel'])))

