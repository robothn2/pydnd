#-*- coding: utf-8 -*-
from utils.source_manager import SourceManager
#from rule.nwn2 import RuleFactory
import unittest
from collections import defaultdict


class TestSourceManager(unittest.TestCase):
  def setUp(self):
    pass
    #self._manager = SourceManager()
    #factory = RuleFactory()
    #rule = factory.get('UnitSourceManager')
    #rule.fill_source_manager(self._manager, factory)

  def test_calculator_default_result(self):
    sm = SourceManager()
    # defaultResult is 0 if not set
    sm.addCalculator('a1')
    self.assertEqual(sm.calcResult('a1'), 0)
    sm.addSource('a1', 'b', 2)
    self.assertEqual(sm.calcResult('a1'), 2)
    sm.removeSource('a1', 'b')
    self.assertEqual(sm.calcResult('a1'), 0)

    sm.addCalculator('a2', defaultResult=5)
    self.assertEqual(sm.calcResult('a2'), 5)
    sm.addSource('a2', 'b', 2)
    self.assertEqual(sm.calcResult('a2'), 2)
    sm.removeSource('a2', 'b')
    self.assertEqual(sm.calcResult('a2'), 5)

  def test_calculator_add_remove_source(self):
    sm = SourceManager()
    sm.addCalculator('ab.str.base', 'sum')
    self.assertEqual(sm.calcResult('ab.str.base'), 0)
    sm.addSource('ab.str.base', 'builder', 12)
    self.assertEqual(sm.calcResult('ab.str.base'), 12)
    sm.addSource('ab.str.base', 'race', 2)
    self.assertEqual(sm.calcResult('ab.str.base'), 14)
    sm.addSource('ab.str.base', 'levelup:4', 1)
    self.assertEqual(sm.calcResult('ab.str.base'), 15)
    sm.removeSource('ab.str.base', 'levelup:4')
    self.assertEqual(sm.calcResult('ab.str.base'), 14)
    sm.removeSource('ab.str.base', 'race')
    self.assertEqual(sm.calcResult('ab.str.base'), 12)
    sm.removeSource('ab.str.base', 'builder')
    self.assertEqual(sm.calcResult('ab.str.base'), 0)

  def test_calculator_sum(self):
    sm = SourceManager()
    sm.addCalculator('ab.str.base', 'sum')
    sm.addSource('ab.str.base', 'builder', 12)
    sm.addSource('ab.str.base', 'race', 2)
    sm.addSource('ab.str.base', 'levelup:4', 1)
    self.assertEqual(sm.calcResult('ab.str.base'), 15)
    sm.removeSource('ab.str.base', 'levelup:4')
    self.assertEqual(sm.calcResult('ab.str.base'), 14)
    sm.removeSource('ab.str.base', 'race')
    self.assertEqual(sm.calcResult('ab.str.base'), 12)

  def test_calculator_max(self):
    sm = SourceManager()
    sm.addCalculator('ab.str.item', 'max')
    sm.addSource('ab.str.item', 'ring', 5)
    sm.addSource('ab.str.item', 'kama', 2)
    sm.addSource('ab.str.item', 'belt', 6)
    self.assertEqual(sm.calcResult('ab.str.item'), 6)
    sm.removeSource('ab.str.item', 'belt')
    self.assertEqual(sm.calcResult('ab.str.item'), 5)
    sm.removeSource('ab.str.item', 'ring')
    self.assertEqual(sm.calcResult('ab.str.item'), 2)

  def test_calculator_min(self):
    sm = SourceManager()
    sm.addCalculator('ac.mod_cap', 'min')
    sm.addSource('ac.mod_cap', 'mod.dex', 4)
    self.assertEqual(sm.calcResult('ac.mod_cap'), 4)
    sm.addSource('ac.mod_cap', 'armor.cap', 3)
    self.assertEqual(sm.calcResult('ac.mod_cap'), 3)
    sm.removeSource('ac.mod_cap', 'armor.cap')
    self.assertEqual(sm.calcResult('ac.mod_cap'), 4)

  def test_calculator_upstreams(self):
    sm = SourceManager()

    sm.addCalculator('ab.str.base', 'sum')
    sm.addCalculator('ab.str.item', 'max')
    sm.addCalculator('ab.str.buff', 'max')
    sm.addCalculator('ab.str', 'sum', upstream=('ab.str.base', 'ab.str.item', 'ab.str.buff'))
    sm.addSource('ab.str.base', 'builder', 12)
    sm.addSource('ab.str.base', 'race', 2)
    sm.addSource('ab.str.base', 'levelup:4', 1)
    sm.addSource('ab.str.item', 'ring', 5)
    sm.addSource('ab.str.item', 'kama', 2)
    sm.addSource('ab.str.item', 'belt', 6)
    sm.addSource('ab.str.buff', 'bull strength', 4)
    self.assertEqual(sm.calcResult('ab.str'), 25)

    sm.addCalculator('mod.str', 'sum', 'modifier', upstream='ab.str')
    self.assertEqual(sm.calcResult('mod.str'), 7)

    sm.addCalculator('attackbonus.mod', 'sum', upstream='mod.str')
    self.assertEqual(sm.calcResult('attackbonus.mod'), 7)

    sm.removeSource('ab.str.buff', 'bull strength')
    self.assertEqual(sm.calcResult('attackbonus.mod'), 5)

  def test_calculator_negative_source(self):
    sm = SourceManager()

    sm.addCalculator('ab.str.base', 'sum')
    sm.addCalculator('ab.str.item', 'max')
    sm.addCalculator('ab.str.buff', 'max')
    sm.addCalculator('ab.str', 'sum', upstream=('ab.str.base', 'ab.str.item', 'ab.str.buff'))
    sm.addCalculator('mod.str', 'sum', 'modifier', upstream='ab.str')
    sm.addSource('ab.str.base', 'builder', 12)
    sm.addSource('ab.str.item', 'belt', 6)
    sm.addSource('ab.str.buff', 'weakness', -4)
    self.assertEqual(sm.calcResult('mod.str'), 2) # ((12 + 6 + -4) - 10) / 2

    sm.removeSource('ab.str.base', 'builder')
    self.assertEqual(sm.calcResult('mod.str'), -4)

  def test_calculator_lambda_source(self):
    sm = SourceManager()

    sm.addCalculator('c', 'sum', noCache=True)
    sm.addSource('c', 's1', lambda kwargs: 5)
    self.assertEqual(sm.calcResult('c'), 5)
    sm.addSource('c', 's2', lambda kwargs: kwargs.get('p', 2))
    self.assertEqual(sm.calcResult('c'), 7)
    self.assertEqual(sm.calcResult('c', p=3), 8)

    sm.removeSource('c', 's1')
    self.assertEqual(sm.calcResult('c', p=-5), -5)

  def test_calculator_replace_source(self):
    sm = SourceManager()

    sm.addCalculator('level.class', 'sum')
    sm.addSource('level.class', 'ranger', 1)
    sm.addSource('level.class', 'ranger', 7)
    self.assertEqual(sm.calcResult('level.class'), 7)

  def test_calculator_discard_cache_value(self):
    sm = SourceManager()

    sm.addCalculator('level.class', 'sum')
    sm.addSource('level.class', 'ranger', 7)
    self.assertEqual(sm.calcResult('level.class'), 7)
    sm.addSource('level.class', 'cleric', 2)
    self.assertEqual(sm.calcResult('level.class'), 9)

  def test_calculator_lambda_level(self):
    sm = SourceManager()

    sm.addCalculator('level.class', 'sum')
    sm.addCalculator('sr.race', 'max', lambda value: value + 11, upstream='level.class')
    sm.addCalculator('sr', 'max', upstream='sr.race')
    sm.addSource('level.class', 'ranger', 5)
    self.assertEqual(sm.calcResult('sr'), 16)
    sm.addSource('level.class', 'cleric', 5)
    self.assertEqual(sm.calcResult('sr'), 21)
    sm.addSource('level.class', 'fighter', 5)
    self.assertEqual(sm.calcResult('sr'), 26)

  def test_calculator_tuple_result(self):
    sm = SourceManager()

    sm.addCalculator('dmg.additional', 'sum')
    sm.addCalculator('dmg.mainhand', 'sum', upstream='dmg.additional')
    sm.addSource('dmg.mainhand', 'dagger', ('physical', 4))
    self.assertEqual(sm.calcResult('dmg.mainhand'), {'physical': 4})
    sm.addSource('dmg.additional', 'powerattack', ('physical', 3))
    self.assertEqual(sm.calcResult('dmg.mainhand'), {'physical': 7})
    sm.addSource('dmg.additional', 'divinemight', ('divine', 2))
    self.assertEqual(sm.calcResult('dmg.mainhand'), {'physical': 7, 'divine': 2})

  def test_calculator_sum_dict_result(self):
    sm = SourceManager()

    sm.addCalculator('dmg.additional')
    sm.addCalculator('dmg.mainhand', upstream='dmg.additional')
    sm.addCalculator('dmg', methodSource='sum_dict', upstream='dmg.mainhand')
    sm.addSource('dmg.mainhand', 'dagger', ('physical', 4))
    sm.addSource('dmg.additional', 'divinemight', ('divine', 2))
    sm.addSource('dmg.additional', 'powerattack', ('physical', 3))
    self.assertEqual(sm.calcResult('dmg'), 9)

  def test_calculator_roll_dice(self):
    sm = SourceManager()

    sm.addCalculator('dmg.mainhand.variable', noCache=True)
    sm.addCalculator('dmg.mainhand', upstream='dmg.mainhand.variable')
    sm.addCalculator('dmg', methodSource='sum_dict', upstream='dmg.mainhand')
    # A dagger with 1d4 base damage and a +2d6 sonic
    sm.addSource('dmg.mainhand.variable', 'dagger:base', ('physical', (1,4,1)))
    sm.addSource('dmg.mainhand.variable', 'dagger:element', ('sonic', (1,6,2)))
    results = defaultdict(int)
    for i in range(500):
      results[sm.calcResult('dmg')] += 1
    self.assertEqual(len(results), 6*2+4 + 1 - 3)

  def test_calculator_source_enabler(self):
    sm = SourceManager()

    sm.addCalculator('ac.dex_mod')
    sm.addCalculator('ac.dex_mod_control', sourceAsEnabler=True, upstream='ac.dex_mod')
    sm.addCalculator('ac', upstream='ac.dex_mod_control')
    # player will lost his dex modifier ac if he has footflat buff, until he has
    # UncannyDodge feat
    self.assertEqual(sm.calcResult('ac'), 0)
    sm.addSource('ac.dex_mod', 'builder', 4)
    self.assertEqual(sm.calcResult('ac'), 4)
    sm.addSource('ac.dex_mod_control', 'foot_flat', (5, False))
    self.assertEqual(sm.calcResult('ac'), 0)
    sm.addSource('ac.dex_mod_control', 'uncanny_dodge', (10, True))
    self.assertEqual(sm.calcResult('ac'), 4)
    sm.removeSource('ac.dex_mod_control', 'uncanny_dodge')
    self.assertEqual(sm.calcResult('ac'), 0)
    sm.removeSource('ac.dex_mod_control', 'foot_flat')
    self.assertEqual(sm.calcResult('ac'), 4)
