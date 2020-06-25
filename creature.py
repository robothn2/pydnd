#coding: utf-8

from unit import Unit
from protos import create_weapon
import warnings, copy, json

class Creature(Unit):
  def __init__(self, ctx, name):
    super(Creature, self).__init__(ctx)
    if name in ctx['Creature']:
      self.proto = copy.deepcopy(ctx['Creature'][name])
      self.props.update(self.proto)
    else:
      warnings.warn('unknown create name: %s' % name)
    self._applyAll()

  def update(self, deltaTime):
    Unit.update(self, deltaTime)

  def _applyAll(self):
    self.calc.addSource('ArmorClass.Natural', name='beastiary', calcInt=int(self.proto['armor_bonus']))
    self.calc.addSource('HitPoint', name='beastiary.expected_hp', calcInt=int(self.proto['expected_hp']))
    self.calc.addSource('HitPoint', name='beastiary.hp_fudge', calcInt=int(self.proto['hp_fudge']))

    for ability in self.ctx['Abilities']:
      self.calc.addSource('Ability.'+ ability + '.Base', name='beastiary', calcInt=int(self.proto[ability]))

    self.feats.apply()
    self.__applyAttackParameters()

    self.setProp('hp', self.calc.calcPropValue('HitPoint', self, None))
    self.statistic()

  def __applyAttackParameters(self):
    params = json.loads(self.proto['attack_parameters'])
    if not isinstance(params, list) or not params:
      return

    attacks = []
    weaponsCreated = {}
    weaponFirst = None
    for i, attack in enumerate(params):
      weaponName = attack[0]
      if weaponName not in weaponsCreated:
        # create a virtual weapon
        weapon = create_weapon(self.ctx, weaponName,
                damageRoll=(1, attack[1]),
                criticalThreat=(1, len(attack) - 2))

        weaponsCreated[weaponName] = weapon

        if not weaponFirst:
          weaponFirst = weapon
      tsOffset = round(i * (self.ctx['secondsPerTurn'] / len(params)), 3)
      attacks.append((tsOffset, attack[1], 'MainHand', weaponsCreated[weaponName]))

    self.calc.addSource('Attacks', name='MainHand', calcInt=attacks)

    self.setProp('WeaponMainHand', weaponFirst)

  def statistic(self):
    print('== statistics for creature', self.getName())
    self.printProp('AttackBonus.Base')
    self.printProp('ArmorClass')
    self.printProp('HitPoint')
    print('Attacks:', self.calc.calcPropValue('Attacks', self))
    print('== statistics end')
