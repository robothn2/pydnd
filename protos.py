#coding: utf-8
from dice import dice_roll
import re
import warnings

def _parseHighSaves(text):
  if text.find('All') >= 0:
    return ['Fortitude', 'Reflex', 'Will']
  ret = []
  if text.find('Fortitude') >= 0:
    ret.append('Fortitude')
  if text.find('Reflex') >= 0:
    ret.append('Reflex')
  if text.find('Will') >= 0:
    ret.append('Will')
  return ret
def _parseBaseAttackBonus(text):
  if text.find('High') >= 0:
    return 1.0
  return 0.75 if text.find('Medium') >= 0 else 0.5
def _parseHitDie(text):
  return int(re.match(r"d(\d+)", text).groups()[0])
def _parseWeaponProficiencies(text):
  return text
def _parseArmorProficiencies(text):
  return text
def _parseSkillPoints(text):
  return text
def _parseClassSkills(text):
  return text
def _parse(kwargs, key, func):
  if key not in kwargs:
    return None
  return func(kwargs.pop(key))

def _name_canonical(name):
  name_new = name.replace('\'s', '').replace('-', ' ')
  words = name_new.split(' ')
  return ''.join(list(map(lambda word: word.capitalize(), words)))

class ProtoBase:
  def __init__(self, **kwargs):
    self.name = kwargs.pop('name')
    self.nameCanonical = _name_canonical(self.name)
    self._proto = kwargs
  def __getattr__(self, attr):
    if attr in self._proto:
      return self._proto[attr]

class ProtoRace(ProtoBase):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

class ProtoDeity(ProtoBase):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

class ProtoClass(ProtoBase):
  def __init__(self, **kwargs):
    self.bab = _parse(kwargs, 'Base Attack Bonus', _parseBaseAttackBonus)
    self.hd = _parse(kwargs, 'Hit Die', _parseHitDie)
    self.highSaves = _parse(kwargs, 'High Saves', _parseHighSaves)
    self.weapons = _parse(kwargs, 'Weapon Proficiencies', _parseWeaponProficiencies)
    self.armors = _parse(kwargs, 'Armor Proficiencies', _parseArmorProficiencies)
    self.skillPoints = _parse(kwargs, 'Skill Points', _parseSkillPoints)
    self.classSkills = _parse(kwargs, 'Class Skills', _parseClassSkills)
    super().__init__(**kwargs)
    self.spellType = None
    for bonus in kwargs['bonus']:
      # (1, ('SpellType', 'Arcane', ...))
      if bonus[1][0] == 'SpellType':
        self.spellType = (bonus[1][1], bonus[0])

    # todo: parse bonus and merge prerequisite entry

  def isAvailable(self, unit):
    return unit.matchPrerequisite(self.prerequisite)

  def levelUp(self, unit, level, **choices):
    print('apply', self.name, 'level', level)
    if level == 1:
      unit.addFeat('Weapon Proficiency', self.weapons)
      unit.addFeat('Armor Proficiency', self.armors)

    if not isinstance(self.bonus, tuple):
      return
    for entry in self.bonus:
      #print(entry)
      if not isinstance(entry, tuple):
        continue
      if entry[0] == level:
        unit.applyTupleResource(entry[1], **choices)
      elif callable(entry[0]):
        if entry[0](level):
          unit.applyTupleResource(entry[1], **choices)

  def calcSaveThrow(self, savingName, classLevel):
    if savingName in self.highSaves:
      return classLevel // 2 + 2
    return classLevel // 3

class ProtoDomain(ProtoBase):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def apply(self, unit):
    print('apply cleric domain %s' % self.name)
    if hasattr(self, 'bonus'):
      for entry in self.bonus:
        print('apply resource %s cleric domain %s' % (str(entry), self.name))
        unit.applyTupleResource(entry)

class ProtoFeat(ProtoBase):
  def __init__(self, **kwargs):
    if 'category' not in kwargs:
      kwargs['category'] = 'General'
    super().__init__(**kwargs)
    #todo: group and nameMember
    self.group = kwargs.get('group', self.nameCanonical)
    self.nameMember = kwargs.get('nameMember')
    if hasattr(self, 'buffDuration'):
      self.nameBuff = self.name

  def isAvailable(self, unit):
    return unit.matchPrerequisite(self.prerequisite)

class ProtoSpell(ProtoBase):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.nameBuff = kwargs.pop('buffName') if 'buffName' in kwargs else self.name

def __calc_attackbonus_list(maxAttackTimes, baseAttackBonus, babDecValue):
  bab = int(baseAttackBonus)
  abList = []
  while maxAttackTimes > 0:
    maxAttackTimes -= 1
    abList.append(bab)
    bab -= babDecValue
    if bab <= 0:
      break
  return abList
def __calc_attacks_in_turn(maxAttackTimes, baseAttackBonus, babDecValue,
                           secondsPerTurn, delaySecondsToFirstAttack, weapon,
                           hand):
  if maxAttackTimes == 0:
    return []
  babList = __calc_attackbonus_list(maxAttackTimes, baseAttackBonus, babDecValue)
  durationAttack = (secondsPerTurn - delaySecondsToFirstAttack) / len(babList)
  tsOffset = delaySecondsToFirstAttack
  attacks = []
  for bab in babList:
    attacks.append((round(tsOffset,3), bab, hand, weapon))
    tsOffset += durationAttack
  return attacks
def apply_weapon_attacks(weapon, unit, hand, maxAttackTimes = 10):
  tsOffset = 0.5 if hand == 'OffHand' else 0.0
  bab = unit.calc.calcPropValue('AttackBonus.Base', weapon, None)
  babDec = 5

  if weapon.getItemBaseName() == 'Kama' and unit.getClassLevel('Monk') > 0:
    babDec = 3
  if hand == 'OffHand':
    if not unit.hasFeat('Two-Weapon Fighting'):
      maxAttackTimes = 0
    else:
      featParams = unit.getFeatParams('Two-Weapon Fighting')
      if 'Perfect' in featParams:
        maxAttackTimes = 10
      elif 'Improved' in featParams:
        maxAttackTimes = 2
      else:
        maxAttackTimes = 1

  # attacks
  unit.calc.addSource('Attacks', name=hand, calcInt=lambda caster, target: \
      __calc_attacks_in_turn(maxAttackTimes, bab, babDec, unit.ctx['secondsPerTurn'], tsOffset, weapon, hand))

class ProtoWeapon(ProtoBase):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

class Weapon:
  def __init__(self, proto, **kwargs):
    self.proto = proto
    self.kwargs = kwargs
    if 'name' in kwargs:
      self.name = kwargs['name']
    else:
      self.name = self.proto.name
      if 'enhancement' in kwargs:
        self.name += '+' + str(kwargs['enhancement'])

  def __repr__(self):
    return self.name

  def getItemBaseName(self):
    return self.proto.name

  def apply(self, unit, hand):
    print('apply', hand, 'weapon:', self.name)
    apply_weapon_attacks(self, unit, hand)

    # weapon base damage
    weaponParams = self.proto.damageRoll
    unit.calc.addSource('Damage.' + hand, name=self.name, calcInt=lambda caster, target: ('Physical', self.name, dice_roll(1, weaponParams[1], weaponParams[0])), noCache=True)

    # weapon enhancement
    if hasattr(self, 'enhancement'):
      unit.calc.addSource('Weapon.%s.Additional' % hand, name='WeaponEnhancement', calcInt=('Magical', 'WeaponEnhancement', self.model.enhancement))
      unit.calc.addSource('AttackBonus.' + hand, name='WeaponEnhancement', calcInt=self.enhancement)

    # weapon critical parameter
    criticalParams = self.proto.criticalThreat
    unit.calc.addSource('Weapon.%s.CriticalRange' % hand, name='WeaponBase', calcInt=criticalParams[0])
    unit.calc.addSource('Weapon.%s.CriticalMultiplier' % hand, name='WeaponBase', calcInt=criticalParams[1])

    # weapon related feats
    unit.feats.apply(weapon=self, hand=hand)

  def unapply(self, unit, hand):
    unit.calc.removeSource('Attacks', hand)

    unit.calc.removeSource('Damage.' + hand, self.name)

    unit.calc.removeSource('Weapon.%s.Additional' % hand, 'WeaponEnhancement')
    unit.calc.removeSource('Damage.' + hand, 'WeaponEnhancement')

    unit.calc.removeSource('Weapon.%s.CriticalRange' % hand, 'WeaponBase')
    unit.calc.removeSource('Weapon.%s.CriticalMultiplier' % hand, 'WeaponBase')


def create_weapon(protos, protoName, **kwargs):
  if protoName in protos['Weapon']:
    proto = protos['Weapon'][protoName]
  else:
    # for a natural weapon, we need following keys in |props|:
    #   damageRoll, default is [1,4,1], also named as 1d4
    #   BaseCriticalThreat, default is [1, 2], also named as 20/x2
    #   BaseDamageType, default is ['Bludgeoning']
    damageRoll = kwargs.get('damageRoll', (1, 4, 1))
    criticalThreat = kwargs.get('criticalThreat', (1, 2))
    weaponSize = kwargs.get('size', 'Small')
    damageType = kwargs.get('damageType', 'Bludgeoning')
    specifics = kwargs.get('specifics', 'Natural weapon: ' + protoName)
    proto = ProtoWeapon(name=protoName, damageRoll=damageRoll,
                        criticalThreat=criticalThreat, damageType=damageType,
                        size=weaponSize, specifics=specifics)

  return Weapon(proto, **kwargs)

def register_proto(proto, protos):
  if 'type' not in proto:
    return False

  t = proto.get('type')
  if not t or not isinstance(t, str):
    return False
  if t == 'Feat':
    p = ProtoFeat(**proto)
  elif t == 'Spell':
    p = ProtoSpell(**proto)
    #support buff with the same name as the spell that generate it
    if hasattr(proto, 'buffDuration'):
      protos['Buff'][p.name] = p
  elif t == 'Weapon':
    p = ProtoWeapon(**proto)
  elif t == 'Race':
    p = ProtoRace(**proto)
  elif t == 'Class':
    p = ProtoClass(**proto)
  elif t == 'Deity':
    p = ProtoDeity(**proto)
  elif t == 'Domain':
    p = ProtoDomain(**proto)
  else:
    return False
  protos[t][p.name] = p
  return True
