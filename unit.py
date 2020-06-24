#coding: utf-8

from utils.props import Props
from combat_manager import CombatManager
from buff_manager import BuffManager
from feat_manager import FeatManager
from prop_calculator import PropCalculator

class Unit:
  def __init__(self, ctx):
    self.ctx = ctx
    self.calc = PropCalculator(ctx)
    self.props = Props({'dead': False, 'hp': 0, 'xp': 0})
    self.combat = CombatManager(self)
    self.buffs = BuffManager(self)
    self.feats = FeatManager(self)

  def __repr__(self):
    return self.getName()

  def update(self, deltaTime):
    if self.isDead():
      return

    self.buffs.update(deltaTime)
    self.combat.update(deltaTime)

  def getName(self):
    return self.props.get('name')

  def setProp(self, key, value):
    self.props[key] = value

  def getProp(self, key):
    if key in self.props:
      return self.props[key]
    return None
  def isDead(self):
    return self.props['dead']

  def addAccessSpellClass(self, className):
    pass

  def addAccessSpell(self, className, spells = []):
    pass

  def addFeat(self, featName, featParam = []):
    self.feats.addFeat(featName, featParam)

  def hasFeats(self, feats):
    for featFullName in feats:
      if not self.feats.hasFeat(featFullName):
        return False
    return True
  def hasFeat(self, featFullName):
    return self.feats.hasFeat(featFullName)

  def getFeatParams(self, featFullName):
    return self.feats.getFeatParams(featFullName)

  def matchRaces(self, races):
    race = self.getProp('race')
    return race in races

  def getClassLevel(self, className = None):
    classLevels = self.calc.getProp('Class.Level')
    if isinstance(className, str):
      return classLevels.calcSingleSource(className, self, None)
    return classLevels.calcValue(self, None)

  def printProp(self, key):
    print(key, ':', self.calc.getPropValueWithSource(key, self))

  def getAttackBonus(self, target, hand):
    return self.calc.calcPropValue('AttackBonus.Additional', self, target) \
       + self.calc.calcPropValue('AttackBonus.' + hand, self, target)

  def getArmorClass(self, target):
    return self.calc.calcPropValue('ArmorClass', self, target)

  def addBuff(self, caster, buffProto, **kwargs):
    self.buffs.addBuff(caster, buffProto, **kwargs)
    return True

  def hasBuff(self, buffName):
    return False

  def active(self, name, **kwargs):
    source = self.calc.getPropSource('Spell.Activable', name)
    if not source:
      print('No activable ability found:', name)
      return
    print('Activate ability:', name)
    spell = source.calcInt
    spell.model.active(spell, self, self)
  def deactive(self, name):
    activableAbility = self.calc.getPropSource('Spell.Activable', name)
    if not activableAbility:
      print('No activable ability found:', name)
      return
    print('Deactivate ability:', name)
    activableAbility.calcInt.deactive(self)

  def castSpell(self, name, target, **kwargs):
    source = self.calc.getPropSource('Spell.Charges', name)
    if not source:
      print('Spell not found:', name)
      return
    print('Cast spell', name, 'to', target.getName())
    spell = source.calcInt
    spell.model.cast(spell, self, target, params=self.feats.getFeatParams(spell.nameFull), **kwargs)


  def addEnemy(self, enemy):
    self.combat.addEnemy(enemy)

  def applyDamages(self, damages):
    damageTotal = damages.calcTotal()
    print(self.getName(), ', damage', damageTotal, ' info', damages)
    # todo: damage reduction
    self._applyDamage(damageTotal)

  def _applyDamage(self, damageTotal):
    hpOld = int(self.getProp('hp'))
    hpNew = hpOld - damageTotal
    if hpNew < 0:
      hpNew = 0
    print(self.getName(), 'hp changed:', hpOld, '->', hpNew)
    self.setProp('hp', hpNew)
    if hpNew == 0:
      self.setProp('dead', True)
      print(self.getName(), 'die')
