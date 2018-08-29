#coding: utf-8

import json
from common import CsvLoader

class CreaturePrototypes:
    def __init__(self):
        self.prototypes = CsvLoader.CsvLoader(r'data/beastiary.csv')

    def __contains__(self, creatureName):
        return creatureName in self.d
    def __getattr__(self, name):
        return self.prototypes.__getattr__(name)

class Creature:
    def __init__(self, proto):
        self.d = proto

if __name__ == '__main__':
    protos = CreaturePrototypes()
    mob = Creature(protos.zombie)
    print(mob.d)