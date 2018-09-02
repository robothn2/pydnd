#coding: utf-8
import random

def rollDice(minValue = 1, maxValue = 20, multiTimes = 1):
    result = 0
    cnt = 0
    while (cnt < multiTimes):
        result += random.randint(minValue, maxValue)
        cnt += 1
    return result
