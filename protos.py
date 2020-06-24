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

def apply_tuple_resource(res, unit, **kwargs):
  #print('apply resource:', res)
  if not isinstance(res, tuple):
    return

  if callable(res[0]):
    # support (_addDeityWeaponFocus, ...),
    res[0](unit)
    return

  if not isinstance(res[0], str):
    return
  if res[0] == 'Feat':
    featChoice = kwargs['featChoice'] if 'featChoice' in kwargs else kwargs
    if isinstance(res[1], str):
      # support ('Feat', 'Breath Weapon')
      featName = res[1]
      unit.addFeat(featName, featChoice.get(featName))
    elif isinstance(res[1], (tuple,list)):
      # support ('Feat', ('Natural Armor Increase', 'Draconic Ability Scores'))
      for featName in res[1]:
        unit.feats.addFeat(featName, featChoice.get(featName))
    elif isinstance(res[1], dict):
      # support ('Feat', {'Weapon Focus': 'Longsword'})
      for featName, featParam in res[1].items():
        unit.feats.addFeat(featName, featParam)

  elif res[0] == 'PropSource':
    # support ('PropSource', 'Favored Enemy', kwargs)
    unit.calc.addSource(res[1], **res[2])
  elif res[0] == 'SpellAccess':
    # support ('SpellAccess', 'Cleric', ('Magic Circle Against Evil', 'Lesser Planar Binding'))
    unit.addAccessSpell(res[1], res[2])
  elif res[0] == 'SpellType':
    # support ('SpellType', 'Divine', ...)
    unit.addAccessSpellClass(res[1])
  elif res[0] == 'Domain':
    # support ('Domain', 2)
    # provide Domain name list in kwargs['domains']
    for domainName in kwargs['domains']:
      domain = unit.ctx['Domain'].get(domainName)
      if not domain:
        warnings.warn('unknown domain:' + domainName)
        continue
      domain.apply(unit)

def is_requirements_match(requirements, unit):
  if not requirements:
    return True

  for cond in requirements:
    if not isinstance(cond, tuple) or len(cond) < 2:
      continue

    # check Ability
    if cond[0] == 'Ability':
      # support ('Ability', 'Dex', 13),
      if unit.calc.calcPropValue('Ability.' + cond[1] + '.Base', unit, None) < cond[2]:
        return False

    # check Skill
    elif cond[0] == 'Skill':
      # support ('Skill', 'Tumble', 5),
      if unit.calc.calcPropValue('Skill.' + cond[1], 'Builder') < cond[2]:
        return False

    # check Level
    elif cond[0] == 'Level':
      # support ('Level', 21)
      if unit.getClassLevel() < cond[1]:
        return False

    # check ClassLevel
    elif cond[0] == 'ClassLevel':
      if isinstance(cond[1], str) and isinstance(cond[2], int):
        # support ('ClassLevel', 'Ranger, 21)
        if unit.getClassLevel(cond[1]) < cond[2]:
          return False
      else:
        return False

    # check ClassAny
    elif cond[0] == 'ClassAny':
      clsMatched = False
      if isinstance(cond[1], tuple):
        # support ('ClassAny', ('Bard', 'Sorcerer'))
        for cls in cond[1]:
          if unit.getClassLevel(cls) > 0:
            clsMatched = True
            break
      if not clsMatched:
        return False

    # check BaseAttackBonus
    elif cond[0] == 'BaseAttackBonus':
      # support ('BaseAttackBonus', 5)
      if unit.calc.calcPropValue('AttackBonus.Base', unit) < cond[2]:
        return False

    # check Feat
    elif cond[0] == 'Feat':
      if isinstance(cond[1], tuple):
        # support ('Feat', ('Dodge', 'Mobility', 'CombatExpertise', 'SpringAttack', 'WhirlwindAttack')),
        if not unit.hasFeats(cond[1]):
          return False
      elif isinstance(cond[1], str):
        if not unit.hasFeat(cond[1]):
          return False
      else:
        return False

    # custom condition
    elif callable(cond[0]):
      if not cond[0](unit):
        # support (function, 'Weapon Focus in a melee weapon')
        return False
    else:
      warnings.warn('unknown condition ' + repr(cond))
      return False
  return True

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
    return is_requirements_match(self.prerequisite, unit)

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
        apply_tuple_resource(entry[1], unit, **choices)
      elif callable(entry[0]):
        if entry[0](level):
          apply_tuple_resource(entry[1], unit, **choices)

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
        apply_tuple_resource(entry, unit)

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
    return is_requirements_match(self.prerequisite, unit)

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
    self._proto = proto
    self.kwargs = kwargs
    if 'name' in kwargs:
      self.name = kwargs['name']
    else:
      self.name = self._proto.name
      if 'enhancement' in kwargs:
        self.name += '+' + str(kwargs['enhancement'])

  def __repr__(self):
    return self.name

  def getItemBaseName(self):
    return self._proto.name

  def apply(self, unit, hand):
    print('apply', hand, 'weapon:', self.name)
    apply_weapon_attacks(self, unit, hand)

    # weapon base damage
    weaponParams = self._proto.damageRoll
    unit.calc.addSource('Damage.' + hand, name=self.name, calcInt=lambda caster, target: ('Physical', self.name, dice_roll(1, weaponParams[1], weaponParams[0])), noCache=True)

    # weapon enhancement
    if hasattr(self, 'enhancement'):
      unit.calc.addSource('Weapon.%s.Additional' % hand, name='WeaponEnhancement', calcInt=('Magical', 'WeaponEnhancement', self.model.enhancement))
      unit.calc.addSource('AttackBonus.' + hand, name='WeaponEnhancement', calcInt=self.enhancement)

    # weapon critical parameter
    criticalParams = self._proto.criticalThreat
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
