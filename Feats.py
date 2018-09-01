#coding: utf-8
import json
import warnings

def parse_feats(feats, featPrototypes):
    d = {}
    if type(feats) is list:
        for featName in feats:
            if featName in featPrototypes:
                d[featName] = featPrototypes[featName]
            else:
                warnings.warn('unknown feat: %s' % featName)
    print(d)