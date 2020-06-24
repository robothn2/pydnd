#-*- coding: utf-8 -*-
import unittest


class TestPropSource(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    print ("this setupclass() method only called once.\n")

  @classmethod
  def tearDownClass(cls):
    print ("this teardownclass() method only called once too.\n")

  def setUp(self):
    print ("do something before test : prepare environment.\n")

  def tearDown(self):
    print ("do something after test : clean up.\n")

  def test_multi_source(self):
    m.addSource('Ability.Dex.Base', name='Race:Elf', calcInt=2)
    m.addSource('Ability.Dex.Base', name='Builder', calcInt=18)
    m.addSource('Ability.Str.Base', name='Builder', calcInt=14)
    m.addSource('Ability.Dex.Base', name='LevelUp:4', calcInt=1)
    self.assertEqual(m.calcPropValue('Ability.Dex.Base', p1, p2), 21)

if __name__ == '__main__':
    ctx = __import__('Context')
    player = __import__('Character')
    p1 = player.Character(ctx.ctx)
    p2 = player.Character(ctx.ctx)
    m = p1.calc

    # test multi source
    m.addSource('Ability.Dex.Base', name='Race:Elf', calcInt=2)
    m.addSource('Ability.Dex.Base', name='Builder', calcInt=18)
    m.addSource('Ability.Str.Base', name='Builder', calcInt=14)
    m.addSource('Ability.Dex.Base', name='LevelUp:4', calcInt=1)
    assert (m.calcPropValue('Ability.Dex.Base', p1, p2) == 21)

    # test custom calculator calc_upstream_max() for 'Ability.Dex.Item'
    m.addSource('Ability.Dex.Item', name='Item:Boot+2', calcInt=2)
    m.addSource('Ability.Dex.Item', name='Item:RingOfDexerity+6', calcInt=6)
    assert (m.calcPropValue('Ability.Dex.Item', p1, p2) == 6)

    m.addSource('ArmorClass.Dex', name='Feat:UncannyDodge', calcEnable = True, priority = 100)
    assert (m.calcPropValue('ArmorClass.Dex', p1, p2) == 8)

    m.addSource('ArmorClass.Armor', name='Item:Leather+3', calcInt = 7)
    m.addSource('ArmorClass.Armor', name='Item:RingOfProtection+3', calcInt=3)
    assert (m.calcPropValue('ArmorClass.Armor', p1, None) == 7)

    # test source replaceable, and optional target
    m.addSource('Class.Level', name='Ranger', calcInt=1)
    m.addSource('Class.Level', name='Ranger', calcInt=7)
    assert(m.calcPropValue('Class.Level', p1, None) == 7)

    # test cached value discarded by new source
    m.addSource('Class.Level', name='Cleric', calcInt=2)
    assert(m.calcPropValue('Class.Level', p1, None) == 9)

    # test dynamic upstream, and custom name for upstream
    m.addSource('SpellResistance', upstream = 'Class.Level', name = 'YuantiPureBlood', calcPost = lambda value: 11 + value)
    # test calcPost
    assert(m.calcPropValue('SpellResistance', p1, None) == 20)

    # test value cache
    print(m.getPropValueWithSource('ArmorClass', p1, p2))
    print(m.getPropValueWithSource('ArmorClass', p1, p2))

    # test removable source(Int) and value call needRecalc() recursively
    m.removeSource('Ability.Dex.Item', 'Item:RingOfDexerity+6')
    # test recursive call downstream.needRecalc() triggered by removing source
    print(m.getPropValueWithSource('ArmorClass', p1, p2))

    # test source calculated by multi upstream
    m.addSource('Ability.Con.Base', name='Builder', calcInt=16)
    assert (m.calcPropValue('HitPoint', p1, None) == 27)

    bab = m.calcPropValue('AttackBonus.Base')

    # noCache flag affect upstream Props recursively
    m.addSource('Damage.MainHand', name='Kukri', calcInt=lambda caster,target: rollDice(1,4,1), noCache=True)
    dmgs = []
    for i in range(10):
        dmg = m.calcPropValue('Damage.MainHand', p1, p2)
        if dmg not in dmgs:
            dmgs.append(dmg)
    assert (len(dmgs) > 1)


class TestDemo(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    print ("this setupclass() method only called once.\n")

  @classmethod
  def tearDownClass(cls):
    print ("this teardownclass() method only called once too.\n")

  def setUp(self):
    print ("do something before test : prepare environment.\n")

  def tearDown(self):
    print ("do something after test : clean up.\n")

  def test_add(self):
    """Test method add(a, b)"""
    self.assertEqual(3, 1+2)
    self.assertNotEqual(3, 2+2)

  def test_minus(self):
    """Test method minus(a, b)"""
    self.assertEqual(1, 3-2)
    self.assertNotEqual(2, 3-2)

  @unittest.skip("not ready")
  def test_skip(self):
    pass
