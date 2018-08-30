#coding: utf-8

import json

class Unit:
    def __init__(self, ctx):
        self.ctx = ctx

    @classmethod
    def update(self, deltaTime):
        pass

    @classmethod
    def setEnemy(self, monster):
        pass

if __name__ == '__main__':
    u = Unit()
    u.update(20)
