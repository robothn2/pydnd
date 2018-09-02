#coding: utf-8
import warnings

def feats_parse(feats, featPrototypes):
    d = {}
    if type(feats) is list:
        for featName in feats:
            if featName in featPrototypes:
                d[featName] = featPrototypes[featName]
            else:
                warnings.warn('unknown feat: %s' % featName)

def feats_apply(feats, props):
    for feat in feats.keys():
        if feat == 'Dodge':
            props.addTypedSource('ArmorClass', 'dodge', 1, 'Feat:Dodge')
        elif feat == 'FavoredEnemy:Undead':
            props.addTypedSource('AttackBonus', 'racial:undead', 1, 'Feat:FavoredEnemy:Undead')
