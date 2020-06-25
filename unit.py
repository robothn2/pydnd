#coding: utf-8
from utils.props import Props
from combat_manager import CombatManager
from buff_manager import BuffManager
from feat_manager import FeatManager
from prop_calculator import PropCalculator
import warnings

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


  def applyTupleResource(self, res, **kwargs):
    #print('apply resource:', res)
    if not isinstance(res, tuple):
      return

    if callable(res[0]):
      # support (_addDeityWeaponFocus, ...),
      res[0](self)
      return

    if not isinstance(res[0], str):
      return
    if res[0] == 'Feat':
      featChoice = kwargs['featChoice'] if 'featChoice' in kwargs else kwargs
      if isinstance(res[1], str):
        # support ('Feat', 'Breath Weapon')
        featName = res[1]
        self.addFeat(featName, featChoice.get(featName))
      elif isinstance(res[1], (tuple,list)):
        # support ('Feat', ('Natural Armor Increase', 'Draconic Ability Scores'))
        for featName in res[1]:
          self.feats.addFeat(featName, featChoice.get(featName))
      elif isinstance(res[1], dict):
        # support ('Feat', {'Weapon Focus': 'Longsword'})
        for featName, featParam in res[1].items():
          self.feats.addFeat(featName, featParam)

    elif res[0] == 'PropSource':
      # support ('PropSource', 'Favored Enemy', kwargs)
      self.calc.addSource(res[1], **res[2])
    elif res[0] == 'SpellAccess':
      # support ('SpellAccess', 'Cleric', ('Magic Circle Against Evil', 'Lesser Planar Binding'))
      self.addAccessSpell(res[1], res[2])
    elif res[0] == 'SpellType':
      # support ('SpellType', 'Divine', ...)
      self.addAccessSpellClass(res[1])
    elif res[0] == 'Domain':
      # support ('Domain', 2)
      # provide Domain name list in kwargs['domains']
      for domainName in kwargs['domains']:
        domain = self.ctx['Domain'].get(domainName)
        if not domain:
          warnings.warn('unknown domain:' + domainName)
          continue
        domain.apply(self)

  def matchPrerequisite(self, requirements):
    if not requirements:
      return True

    for cond in requirements:
      if not isinstance(cond, tuple) or len(cond) < 2:
        continue

      # check Ability
      if cond[0] == 'Ability':
        # support ('Ability', 'Dex', 13),
        if self.calc.calcPropValue('Ability.' + cond[1] + '.Base', self, None) < cond[2]:
          return False

      # check Skill
      elif cond[0] == 'Skill':
        # support ('Skill', 'Tumble', 5),
        if self.calc.calcPropValue('Skill.' + cond[1], 'Builder') < cond[2]:
          return False

      # check Level
      elif cond[0] == 'Level':
        # support ('Level', 21)
        if self.getClassLevel() < cond[1]:
          return False

      # check ClassLevel
      elif cond[0] == 'ClassLevel':
        if isinstance(cond[1], str) and isinstance(cond[2], int):
          # support ('ClassLevel', 'Ranger, 21)
          if self.getClassLevel(cond[1]) < cond[2]:
            return False
        else:
          return False

      # check ClassAny
      elif cond[0] == 'ClassAny':
        clsMatched = False
        if isinstance(cond[1], tuple):
          # support ('ClassAny', ('Bard', 'Sorcerer'))
          for cls in cond[1]:
            if self.getClassLevel(cls) > 0:
              clsMatched = True
              break
        if not clsMatched:
          return False

      # check BaseAttackBonus
      elif cond[0] == 'BaseAttackBonus':
        # support ('BaseAttackBonus', 5)
        if self.calc.calcPropValue('AttackBonus.Base', self) < cond[2]:
          return False

      # check Feat
      elif cond[0] == 'Feat':
        if isinstance(cond[1], tuple):
          # support ('Feat', ('Dodge', 'Mobility', 'CombatExpertise', 'SpringAttack', 'WhirlwindAttack')),
          if not self.hasFeats(cond[1]):
            return False
        elif isinstance(cond[1], str):
          if not self.hasFeat(cond[1]):
            return False
        else:
          return False

      # custom condition
      elif callable(cond[0]):
        if not cond[0](self):
          # support (function, 'Weapon Focus in a melee weapon')
          return False
      else:
        warnings.warn('unknown condition ' + repr(cond))
        return False
    return True

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
    spell.active(spell, self, self)
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
    spell.cast(spell, self, target, params=self.feats.getFeatParams(spell.name), **kwargs)


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
