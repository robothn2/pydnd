#coding: utf-8

def classes_apply(classes, modifier):
    for cls in classes.keys():
        clsLevel = classes[cls]['level']
        clsProto = classes[cls]['proto']

        modifier.addSource('HitPoint', int(clsLevel * int(clsProto['HitDie'])), cls)
        modifier.addTypedSource('AttackBonus', 'base', int(clsLevel * float(clsProto['BaseAttackBonus'])), cls)
        modifier.addTypedSource('SavingThrow', 'fortitude', int(clsLevel * float(clsProto['FortitudePerLevel'])), cls)
        modifier.addTypedSource('SavingThrow', 'reflex', int(clsLevel * float(clsProto['ReflexPerLevel'])), cls)
        modifier.addTypedSource('SavingThrow', 'will', int(clsLevel * float(clsProto['WillPerLevel'])), cls)
