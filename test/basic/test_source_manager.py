#-*- coding: utf-8 -*-
from utils.source_manager import SourceManager
#from rule.nwn2 import RuleFactory
import unittest


class TestSourceManager(unittest.TestCase):
  def setUp(self):
    pass
    #self._manager = SourceManager()
    #factory = RuleFactory()
    #rule = factory.get('UnitSourceManager')
    #rule.fill_source_manager(self._manager, factory)

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
    '''
    ab.str (sum)
      ab.str.base (sum)
        builder = 12
        race = 2
        levelup:4 = 1
      ab.str.item (max)
        ring = 5
        kama = 2
        belt = 6
      ab.str.buff (max)
        bull strength = 4
    '''

    sm.addCalculator('ab.str.base', 'sum')
    sm.addSource('ab.str.base', 'builder', 12)
    sm.addSource('ab.str.base', 'race', 2)
    sm.addSource('ab.str.base', 'levelup:4', 1)
    sm.addCalculator('ab.str.item', 'max')
    sm.addSource('ab.str.item', 'ring', 5)
    sm.addSource('ab.str.item', 'kama', 2)
    sm.addSource('ab.str.item', 'belt', 6)
    sm.addCalculator('ab.str.buff', 'max')
    sm.addSource('ab.str.buff', 'bull strength', 4)
    sm.addCalculator('ab.str', 'sum')
    sm.linkCalculator('ab.str.base', 'ab.str')
    sm.linkCalculator('ab.str.item', 'ab.str')
    sm.linkCalculator('ab.str.buff', 'ab.str')
    self.assertEqual(sm.calcResult('ab.str'), 25)

    sm.addCalculator('mod.str', 'sum', 'modifier')
    sm.linkCalculator('ab.str', 'mod.str')
    self.assertEqual(sm.calcResult('mod.str'), 7)

    sm.addCalculator('attackbonus.mod', 'sum')
    sm.linkCalculator('mod.str', 'attackbonus.mod')
    self.assertEqual(sm.calcResult('attackbonus.mod'), 7)

    sm.removeSource('ab.str.buff', 'bull strength')
    self.assertEqual(sm.calcResult('attackbonus.mod'), 5)

  def test_calculator_negative_source(self):
    sm = SourceManager()

    sm.addCalculator('ab.str.base', 'sum')
    sm.addSource('ab.str.base', 'builder', 12)
    sm.addCalculator('ab.str.item', 'max')
    sm.addSource('ab.str.item', 'belt', 6)
    sm.addCalculator('ab.str.buff', 'max')
    sm.addSource('ab.str.buff', 'weakness', -4)
    sm.addCalculator('ab.str', 'sum')
    sm.linkCalculator('ab.str.base', 'ab.str')
    sm.linkCalculator('ab.str.item', 'ab.str')
    sm.linkCalculator('ab.str.buff', 'ab.str')

    sm.addCalculator('mod.str', 'sum', 'modifier')
    sm.linkCalculator('ab.str', 'mod.str')
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
    sm.addCalculator('sr.race', 'max', lambda value: value + 11)
    sm.linkCalculator('level.class', 'sr.race')
    sm.addCalculator('sr', 'max')
    sm.linkCalculator('sr.race', 'sr')
    sm.addSource('level.class', 'ranger', 5)
    self.assertEqual(sm.calcResult('sr'), 16)
    sm.addSource('level.class', 'cleric', 5)
    self.assertEqual(sm.calcResult('sr'), 21)
    sm.addSource('level.class', 'fighter', 5)
    self.assertEqual(sm.calcResult('sr'), 26)

  def test_calculator_tuple_result(self):
    sm = SourceManager()

    sm.addCalculator('dmg.additional', 'sum')
    sm.addCalculator('dmg.mainhand', 'sum')
    sm.linkCalculator('dmg.additional', 'dmg.mainhand')
    sm.addSource('dmg.mainhand', 'dagger', {'physical': 4})
    self.assertEqual(sm.calcResult('dmg.mainhand'), {'physical': 4})
    sm.addSource('dmg.additional', 'powerattack', {'physical': 3})
    self.assertEqual(sm.calcResult('dmg.mainhand'), {'physical': 7})
    sm.addSource('dmg.additional', 'divinemight', {'divine': 2})
    self.assertEqual(sm.calcResult('dmg.mainhand'), {'physical': 7, 'divine': 2})

  def test_calculator_sum_dict_result(self):
    sm = SourceManager()

    sm.addCalculator('dmg.additional')
    sm.addCalculator('dmg.mainhand')
    sm.linkCalculator('dmg.additional', 'dmg.mainhand')
    sm.addCalculator('dmg', methodSource='sum_dict')
    sm.linkCalculator('dmg.mainhand', 'dmg')
    sm.addSource('dmg.mainhand', 'dagger', {'physical': 4})
    sm.addSource('dmg.additional', 'divinemight', {'divine': 2})
    sm.addSource('dmg.additional', 'powerattack', {'physical': 3})
    self.assertEqual(sm.calcResult('dmg'), 9)

  def test_calculator_add_and_link(self):
    sm = SourceManager()

    sm.addCalculator('dmg.additional')
    sm.addCalculator('dmg.mainhand', upstream='dmg.additional')
    sm.addCalculator('dmg', methodSource='sum_dict', upstream='dmg.mainhand')
    sm.addSource('dmg.mainhand', 'dagger', {'physical': 4})
    sm.addSource('dmg.additional', 'divinemight', {'divine': 2})
    sm.addSource('dmg.additional', 'powerattack', {'physical': 3})
    self.assertEqual(sm.calcResult('dmg'), 9)
