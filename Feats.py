#coding: utf-8
import json
import warnings

class Feats:
    def __init__(self, feats, featPrototypes):
        self.d = {}
        if type(feats) is list:
            for featName in feats:
                if featName in featPrototypes:
                    self.d[featName] = featPrototypes[featName]
                else:
                    warnings.warn('unknown feat: %s' % featName)

        #print('  feats:', str(self))

    def __str__(self):
        return json.dumps(self.d, indent=4)
