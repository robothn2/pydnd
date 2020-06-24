#coding: utf-8

from unit import Unit
from abilities import abilities_parse
from models import apply_tuple_resource
import json,warnings

def load_json_file(builderJsonFile):
  with open(builderJsonFile, encoding='utf-8') as f:
    builder = json.load(f)
    if len(builder) == 0:
      warnings.warn('fail to read builder file: %s' % builderJsonFile)
      return None
    return builder

class Player(Unit):
  def __init__(self, ctx):
    super(Player, self).__init__(ctx)
    self.ctx = ctx
    self.builder = {'name': '', **abilities_parse(8, 8, 8, 8, 8, 8)}

  def getName(self):
    return self.builder['name']

  def buildByBuilder(self, builder, levelRequest):
    if not isinstance(builder, dict):
      return False
    if levelRequest < 1:
      return False

    self.builder = builder
    print('loading builder:', builder['builderName'])
    '''
    'name': 'Lora',
    'race': 'Yuan-ti Pureblood',
    'gender': 'female',
    'age': 20,
    'deity': 'Leira',
    'alignment': 'ChaoticNeutral',
    'background': 'WildChild',
    'abilities': {'Str': 16, 'Dex': 12, 'Con': 10, 'Int': 14, 'Wis': 8, 'Cha': 16},
     '''
    for key in builder.keys():
      if key in ['race', 'gender', 'age', 'deity', 'alignment', 'background']:
        self.props[key] = builder[key]

    # apply race
    raceName = builder['race']
    race = self.ctx['Race'].get(raceName)
    if not race:
      warnings.warn('unknown race:' + raceName)
      return False
    race.model.apply(self)

    # apply initial abilities
    for k, v in builder['abilities'].items():
      self.calc.addSource('Ability.%s.Base' % k, name='Builder', calcInt=int(v))

    """ apply builder details per level
    'levels': [
      {"level": 1, "class": "Ranger",	"feats": "Dodge", "featChoice": {"Favored Enemy": "Dragons"}, "skills": {"CraftWeapon": 4, "Heal": 4, "Hide": 4, "Intimidate": 2, "MoveSilently": 4, "Spellcraft": 1, "Spot": 4, "Tumble": 2, "UseMagicDevice": 2}},
      ...
      ]
    """
    classLevels = self.calc.getProp('Class.Level')
    for i, levelEntry in enumerate(builder['levels']):
      level = levelEntry.pop('level')
      if level > levelRequest:
        break

      # check class name existence
      cls = levelEntry.pop('class')
      if cls not in self.ctx['Class']:
        warnings.warn('unknown character class: %s at level %d' % (cls, level))
        return False
      clsProto = self.ctx['Class'][cls]

      # add ability
      if 'ability' in levelEntry:
        self.calc.addSource('Ability.%s.Base' % levelEntry.pop('ability'), name='LevelUp:%d'%level, calcInt=1)

      # update Class.Level, bab, SavingThrows, HitPoint
      clsLevel = classLevels.calcSingleSource(cls, self, None)
      clsLevel += 1
      self.calc.addSource('Class.Level', name=cls, calcInt=clsLevel)
      if type(clsProto.spellType) is tuple:
        self.calc.addSource('Caster.Level', name='SpellGrantLevel', calcInt=1 - clsProto.spellType[1])
        self.calc.addSource('Caster.Level', name=cls, calcInt=clsLevel)
      self.calc.addSource('AttackBonus.Base', name=cls, calcInt=int(clsLevel * float(clsProto.bab)))

      self.calc.addSource('SavingThrow.Fortitude', name=cls, calcInt=clsProto.calcSaveThrow('Fortitude', clsLevel))
      self.calc.addSource('SavingThrow.Reflex', name=cls, calcInt=clsProto.calcSaveThrow('Reflex', clsLevel))
      self.calc.addSource('SavingThrow.Will', name=cls, calcInt=clsProto.calcSaveThrow('Will', clsLevel))
      self.calc.addSource('HitPoint', name=cls, calcInt=clsLevel*int(clsProto.hd))

      # apply class feats/abilities by level
      clsProto.levelUp(self, clsLevel, **levelEntry)

      # add feats
      feats = levelEntry.get('feats')
      if feats:
        #print('found builder feats:', feats)
        featChoice = levelEntry['featChoice'] if 'featChoice' in levelEntry else {}
        apply_tuple_resource(('Feat', feats), self, **featChoice)

      # update skills
      for skillName,skillLevel in levelEntry['skills'].items():
        self.calc.addSource('Skill.%s'% skillName, name='Builder', calcInt=skillLevel)

    return True

  def equipWeapon(self, hand, weapon):
    if hand == 'TwoHand':
      self.unequipWeapon('TwoHand')
      self.unequipWeapon('MainHand')
      self.unequipWeapon('OffHand')
    elif hand == 'MainHand':
      self.unequipWeapon('TwoHand')
      self.unequipWeapon('MainHand')
    else:
      self.unequipWeapon('TwoHand')
      self.unequipWeapon('OffHand')

    self.calc.updateObject(('Weapon', hand), weapon)

  def unequipWeapon(self, hand):
    weaponExist = self.calc.getObject(('Weapon', hand))
    if weaponExist:
      weaponExist.unapply(self, hand)

  def __applyWeaponHand(self, hand):
    weaponExist = self.calc.getObject(('Weapon', hand))
    if weaponExist:
      weaponExist.apply(self, hand)

  def applyAll(self):
    self.feats.apply()
    self.__applyWeaponHand('TwoHand')
    self.__applyWeaponHand('MainHand')
    self.__applyWeaponHand('OffHand')

    self.setProp('hp', self.calc.calcPropValue('HitPoint', self, None))

  def statistic(self):
    self.applyAll()
    print('== statistics for character', self.getName())
    print('Feats:', repr(self.feats))
    self.printProp('AttackBonus.Base')
    self.printProp('ArmorClass')
    self.printProp('HitPoint')
    self.printProp('SpellResistance')
    self.printProp('SavingThrow.Fortitude')
    self.printProp('SavingThrow.Reflex')
    self.printProp('SavingThrow.Will')
    #self.printProp('Reduction')
    print('Attacks:', self.calc.calcPropValue('Attacks', self))
    print('== statistics end')

  def addXP(self, xp):
    xpOld = self.getProp('xp')
    xpNew = xpOld + xp
    self.setProp('xp', xpNew)
    print(self.getName(), 'received xp', xp, ',total', xpNew)
