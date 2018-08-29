#coding: utf-8

import json

class Unit:
    def __init__(self, proto):
        self.d = proto

    @classmethod
    def update(self, deltaTime):
        pass

if __name__ == '__main__':
    u = Unit()
    u.update(20)
