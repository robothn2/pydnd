#coding: utf-8
import json
from common import CsvLoader

class FeatPrototypes(CsvLoader.CsvLoader):
    def __init__(self):
        self.prototypes = CsvLoader.CsvLoader(r'data/feats.csv', False)

    def __contains__(self, featName):
        return featName in self.prototypes
    def __getattr__(self, name):
        return self.prototypes.__getattr__(name)

class Feats:
    def __init__(self, feats, featPrototypes):
        self.d = {}
        if type(feats) is list:
            for featName in feats:
                if featName in featPrototypes:
                    self.d[featName] = featPrototypes.__getattr__(featName)
                else:
                    print('  unknown feat:', featName)

        #print('  feats:', str(self))

    def __str__(self):
        return json.dumps(self.d, indent=4)

if __name__ == '__main__':
    protos = FeatPrototypes()
    print(protos.Dodge)
    feats = Feats(['Dodge', 'Mobility', 'PowerAttack', 'SpringAttack'], protos)
    print(feats)
    #feats = Feats(protos.Dodge, protos.Mobility, protos.PowerAttack, protos.SprintAttack)
