#coding: utf-8
from utils.props import Modifier
import copy

def calc_post_mainhand_weapon(value):
  return value
def calc_post_ability_modifier(value):
  return int((value - 10) / 2)
def calc_upstream_sum(sourceValue, oldValue):
  return sourceValue + oldValue
def calc_upstream_max(sourceValue, oldValue):
  return max(sourceValue, oldValue)
def calc_upstream_extend_attacks(sourceValue, oldValue):
  oldValue.extend(sourceValue)
  oldValue.sort(key=lambda att: att[0], reverse=False)
  return oldValue
def calc_upstream_append_damage(sourceValue, oldValue):
  oldValue.append(sourceValue)
  return oldValue

class PropSource:
  def __init__(self, **kwargs):
    self.args = kwargs

class PropSourceUpstream(PropSource):
  def __init__(self, **kwargs):
    super(PropSourceUpstream, self).__init__(**kwargs)
    self.upstream = kwargs.get('upstream')
    self.name = kwargs['name'] if 'name' in kwargs else self.upstream.name
    self.calcPost = kwargs.get('calcPost')
  def __repr__(self):
    return self.name
  def __str__(self):
    return self.name
  def __call__(self, caster, target):
    if not hasattr(self.upstream, 'calcValue'):
      return 0 # unbound upstream, skip this source
    value = self.upstream.calcValue(caster, target)
    if self.calcPost:
      value = self.calcPost(value)
    return value

class PropSourceMultiUpstream(PropSource):
  def __init__(self, **kwargs):
    super(PropSourceMultiUpstream, self).__init__(**kwargs)
    self.upstreams = kwargs.get('upstreams')
    self.name = kwargs['name'] if 'name' in kwargs else self.upstreams[0].name
    self.calcMulti = kwargs.get('calcMulti')
  def __repr__(self):
    return self.name
  def __call__(self, caster, target):
    return self.calcMulti(self.upstreams, caster, target)

class PropSourceDisable(PropSource):
  def __init__(self, **kwargs):
    super(PropSourceDisable, self).__init__(**kwargs)
    self.name = kwargs['name']
    self.calcDisable = kwargs.get('calcDisable')
    self.priority = kwargs['priority'] if 'priority' in kwargs else 0
  def __repr__(self):
    return '{Disable:' + self.name + ', priority:' + repr(self.priority) + ', value:' + repr(self.calcDisable) + '}'
  def __call__(self, caster, target):
    if isinstance(self.calcDisable, bool):
      return self.calcDisable
    if callable(self.calcDisable):
      return self.calcDisable(caster, target)
    raise RuntimeError('Found invalid source Disable', self.args)

class PropSourceEnable(PropSource):
  def __init__(self, **kwargs):
    super(PropSourceEnable, self).__init__(**kwargs)
    self.name = kwargs['name']
    self.calcEnable = kwargs.get('calcEnable')
    self.priority = kwargs['priority'] if 'priority' in kwargs else 0
  def __repr__(self):
    return '{Enable:' + self.name + ', priority:' + repr(self.priority) + ', value:' + repr(self.calcEnable) + '}'
  def __call__(self, caster, target):
    if isinstance(self.calcEnable, bool):
      return self.calcEnable
    if callable(self.calcEnable):
      return self.calcEnable(caster, target)

class PropSourceInt(PropSource):
  def __init__(self, **kwargs):
    super(PropSourceInt, self).__init__(**kwargs)
    self.name = kwargs['name']
    self.calcInt = kwargs.get('calcInt')
  def __repr__(self):
    return repr(self.calcInt)
  def __call__(self, caster, target):
    if isinstance(self.calcInt, int):
      return self.calcInt
    if isinstance(self.calcInt, list):
      return self.calcInt
    if isinstance(self.calcInt, tuple):
      return list(self.calcInt)
    if callable(self.calcInt):
      return self.calcInt(caster, target)

    raise RuntimeError('Found invalid source', self.args, ', calcInt', self.calcInt)

class PropSourceIntMax(PropSource):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = kwargs['name']
    self.calcMax = kwargs.get('calcMax')
  def __repr__(self):
    return 'Max:' + repr(self.calcMax)
  def __call__(self, caster, target):
    if isinstance(self.calcMax, int):
      return self.calcMax
    if callable(self.calcMax):
      return self.calcMax(caster, target)
    raise RuntimeError('Found invalid source', self.args)

class PropNode:
  def __init__(self, props, name, calculator, defaultValue):
    self.name = name
    self.recalc = True # set True if need recalc
    self.noCache = False
    self.value = defaultValue
    self.defaultValue = defaultValue
    self.props = props
    self.calculator = calculator if calculator else calc_upstream_sum # default calculator is sum
    self.sourcesInt = {}
    self.sourcesUpstream = []
    self.sourcesUpstreamMulti = []
    self.sourcesDisable = []
    self.sourcesEnable = []
    self.sourceIntMax = None
    self.downstreams = [] # list of PropNode

  def __repr__(self):
    info = '{'
    if self.sourcesInt:
      info += ' Sources:' + repr(self.sourcesInt)
    if self.sourcesUpstream:
      info += ' Upstreams:' + repr(self.sourcesUpstream)
    if self.sourcesEnable:
      info += ' Enable:' + repr(self.sourcesEnable)
    if self.sourcesDisable:
      info += ' Disable:' + repr(self.sourcesDisable)
    return info + '}'

  def needRecalc(self):
    #print(self.name, 'recalc set to True')
    self.recalc = True
    for propDownstream in self.downstreams:
      propDownstream.needRecalc()

  def setNoCache(self):
    self.noCache = True
    for propDownstream in self.downstreams:
      propDownstream.setNoCache()

  def __addDownstream(self, downstreamProp):
    self.downstreams.append(downstreamProp)
    downstreamProp.needRecalc()

  def __addUpstream(self, upstreamName, upstreamDict):
    upstreamProp = self.props.get(upstreamName)
    if not upstreamProp:
      #if upstream Prop not found, create empty PropNode
      defaultValue = 0
      if 'defaultValue' in upstreamDict:
        defaultValue = upstreamDict.get('defaultValue')
      upstreamProp = PropNode(self.props, upstreamName, upstreamDict.get('calcUpstream'), defaultValue)
      self.props[upstreamName] = upstreamProp

    if upstreamProp.noCache:
      self.noCache = True
    upstreamDict['upstream'] = upstreamProp
    upstreamProp.__addDownstream(self)
    return upstreamProp

  def addSource(self, **kwargs):
    if 'upstream' in kwargs: # single upstream source, using internal calculator of upstream and do calcPost on return int value
      self.__addUpstream(kwargs.get('upstream'), kwargs)
      self.sourcesUpstream.append(PropSourceUpstream(**kwargs))

    elif 'calcMulti' in kwargs:
      upstreams = kwargs.get('upstreams')
      upstreamsProp = []
      for upstream in upstreams:
        upstreamDict = {}
        if isinstance(upstream, str):
          upstreamsProp.append(self.__addUpstream(upstream, upstreamDict))
        elif isinstance(upstream, dict):
          upstreamDict = upstream
          upstreamsProp.append(self.__addUpstream(upstream['upstream'], upstreamDict))
      kwargs['upstreams'] = upstreamsProp # replace list of str/dict to list of Prop
      self.sourcesUpstreamMulti.append(PropSourceMultiUpstream(**kwargs))

    elif 'calcEnable' in kwargs:
      self.sourcesEnable.append(PropSourceEnable(**kwargs))
      # sort switch by priority
      self.sourcesEnable.sort(key=lambda source: source.priority, reverse=False)

    elif 'calcDisable' in kwargs:
      self.sourcesDisable.append(PropSourceDisable(**kwargs))
      self.sourcesDisable.sort(key=lambda source: source.priority, reverse=False)

    else:
      name = kwargs['name']

      if 'calcMax' in kwargs:
        self.sourceIntMax = PropSourceIntMax(**kwargs)
      else:
        self.sourcesInt[name] = PropSourceInt(**kwargs)
    self.needRecalc()
    if kwargs.get('noCache'):
      self.setNoCache()

  def updateIntSource(self, sourceName, calculator):
    source = self.sourcesInt.get(sourceName)
    if source:
      source.calcInt = calculator
    else:
      self.sourcesInt[sourceName] = PropSourceInt(name=sourceName, calcInt=calculator)

  def getSource(self, sourceName):
    return self.sourcesInt.get(sourceName)

  def calcSingleSource(self, sourceName, caster, target):
    source = self.sourcesInt.get(sourceName)
    if source:
      return source(caster, target)
    return self.defaultValue

  def removeSource(self, sourceName):
    for i,source in enumerate(self.sourcesEnable):
      if source.name == sourceName:
        self.sourcesEnable.pop(i)
        self.needRecalc()
        return True

    for i,source in enumerate(self.sourcesDisable):
      if source.name == sourceName:
        self.sourcesDisable.pop(i)
        self.needRecalc()
        return True

    if sourceName in self.sourcesInt:
      self.sourcesInt.pop(sourceName)
      self.needRecalc()
      print('remove source', sourceName, 'under Prop', self.name)
      return True

    for i,source in enumerate(self.sourcesUpstream):
      if source.name == sourceName:
        self.sourcesUpstream.pop(i)
        self.needRecalc()
        return True

    if self.sourceIntMax and self.sourceIntMax.name == sourceName:
      self.sourceIntMax = None
      self.needRecalc()
      return True
    return False

  def printDownstreams(self):
    print(self.name, 'downstreams:', end=' ')
    for d in self.downstreams:
      print(d.name, end=' ')
    print('')

  def calcValue(self, caster, target):
    if not self.noCache and not self.recalc:
      return self.value

    #print('begin calc Prop:', self.name)
    self.recalc = False
    self.value = copy.deepcopy(self.defaultValue) # for list value

    sourceEnable = None
    for source in self.sourcesEnable:
      if source(caster, target):
        sourceEnable = source
        break
    for sourceDisable in self.sourcesDisable:
      if sourceEnable and sourceEnable.priority > sourceDisable.priority:
        print('  Prop %s enabled by %s' % (self.name, sourceEnable.name))
        break # highest priority disable source is lower than effecting enable source
      if sourceDisable(caster, target):
        print('  Prop %s disabled by %s' % (self.name, sourceDisable.name))
        return self.value

    for name,sourceCalculator in self.sourcesInt.items():
      sourceValueInt = sourceCalculator(caster, target)
      if sourceValueInt:
        if isinstance(sourceValueInt, tuple):
          self.value.append(sourceValueInt)
        else:
          self.value = self.calculator(sourceValueInt, self.value)

    for upstreamCalculator in self.sourcesUpstream:
      sourceValueInt = upstreamCalculator(caster, target)
      if isinstance(self.value, list):
        if isinstance(sourceValueInt, int):
          print(self.sourcesUpstream, upstreamCalculator, sourceValueInt)
        self.value.extend(sourceValueInt)
      else:
        self.value = self.calculator(sourceValueInt, self.value)

    for upstreamCalculator in self.sourcesUpstreamMulti:
      sourceValueInt = upstreamCalculator(caster, target)
      self.value = self.calculator(sourceValueInt, self.value)

    if self.sourceIntMax:
      valueNew = min(self.sourceIntMax(caster, target), self.value)
      if valueNew != self.value:
        print('  Prop %s cap by %s, %d -> %d' % (self.name, self.sourceIntMax.name, self.value, valueNew))
        self.value = valueNew
    #print('  Prop', self.name, '=', self.value)
    return self.value

  def getValueWithSource(self, caster, target):
    self.recalc = False
    self.value = 0

    result = {}
    sourceEnable = None
    for source in self.sourcesEnable:
      if source(caster, target):
        sourceEnable = source
        break
    for sourceDisable in self.sourcesDisable:
      if sourceEnable and sourceEnable.priority > sourceDisable.priority:
        result[sourceEnable.name] = True
        break # highest priority disable source is lower than effecting enable source
      if sourceDisable(caster, target):
        result[sourceDisable.name] = False
        return (0, result)

    for name,sourceEval in self.sourcesInt.items():
      sourceInt = sourceEval(caster, target)
      if sourceInt != 0:
        self.value = self.calculator(sourceInt, self.value)
        result[name] = sourceInt

    for upstreamEval in self.sourcesUpstream:
      sourceInt = upstreamEval(caster, target)
      if sourceInt != 0:
        self.value = self.calculator(sourceInt, self.value)
        result[upstreamEval.name] = sourceInt

    for upstreamMultiEval in self.sourcesUpstreamMulti:
      sourceInt = upstreamMultiEval(caster, target)
      if sourceInt != 0:
        self.value = self.calculator(sourceInt, self.value)
        result[upstreamMultiEval.name] = sourceInt

    if self.sourceIntMax:
      valueNew = min(self.sourceIntMax(caster, target), self.value)
      if valueNew != self.value:
        self.value = valueNew
        result[self.sourceIntMax.name] = 'max to ' + valueNew
    return (self.value, result)

class PropCalculator:
  def __init__(self, ctx):
    self.ctx = ctx
    self.props = {}
    self.objects = Modifier()

    self.__addAbilitySources()
    self.__addSkillSources()

    self.addProp('ArmorClass.Dex', [
      {'upstream': 'Modifier.Dex'},
      {'name': 'ArmorDexCap', 'calcMax': 1000}, # armor can replace this cap
      {'name': 'Buff:TargetInvisible', 'calcDisable': (lambda caster, target: target and target.hasBuff('Invisible'))} # using normal priority 0, UncannyDodge can overwrite it
    ])
    self.addProp('ArmorClass', [
      {'name': 'ArmorClass.Base', 'calcInt': 10},
      {'upstream': 'ArmorClass.Armor', 'calcUpstream': calc_upstream_max},
      {'upstream': 'Skill.Tumble', 'name': 'ArmorClass.Tumble', 'calcPost': (lambda value: int(value/10))},
      {'upstream': 'ArmorClass.Natural', 'calcUpstream': calc_upstream_max},
      {'upstream': 'ArmorClass.Luck'},
      {'upstream': 'ArmorClass.Deflection', 'calcUpstream': calc_upstream_max},
      {'upstream': 'ArmorClass.Dodge'},
      {'upstream': 'ArmorClass.Dex'},
      {'upstream': 'ArmorClass.Buff'},
      {'upstream': 'ArmorClass.Aura'}
    ])

    self.addProp('Class.Level')
    self.addProp('Level.Adjustment')

    self.addProp('HitPoint', [
      {'name': 'ModifierCon_x_Level', 'upstreams': ['Modifier.Con', 'Class.Level'], 'calcMulti': (
        lambda upstreams, caster, target:
          upstreams[0].calcValue(caster, target) * upstreams[1].calcValue(caster, target)
      )},
    ])

    self.addProp('AttackBonus.Base')
    self.addProp('AttackBonus.Additional', [
      {'name': 'RaceSize', 'calcInt': 0}, # gnome = 1, others = 0
    ])
    self.addProp('AttackBonus.MainHand', [
      {'upstream': 'Modifier.Str'},
      {'upstream': 'AttackBonus.Additional'},
    ])
    self.addProp('AttackBonus.OffHand', [
      {'upstream': 'Modifier.Str'},
      {'upstream': 'AttackBonus.Additional'},
    ])
    self.addProp('AttackBonus.TwoHand', [
      {'upstream': 'Modifier.Str'},
      {'upstream': 'AttackBonus.Additional'},
    ])
    self.addProp('Attacks', None, calc_upstream_extend_attacks, [])

    self.addProp('Damage.Additional', None, calc_upstream_append_damage, [])
    self.addProp('Damage.MainHand', [
      {'upstream': 'Weapon.MainHand.Additional', 'defaultValue':[]},
      {'upstream': 'Modifier.Str', 'calcPost':lambda value: [('Physical', 'Modifier.Str', value)]},
      {'upstream': 'Damage.Additional'},
      #{'name': 'Buff:Disarm', 'calcDisable': (lambda caster, target: caster.hasBuff('Disarm'))},
    ], None, [])
    self.addProp('Damage.OffHand', [
      {'upstream': 'Weapon.OffHand.Additional', 'defaultValue':[]},
      {'upstream': 'Modifier.Str', 'calcPost':lambda value: [('Physical', 'Modifier.Str', int(value/2))]},
      {'upstream': 'Damage.Additional'},
    ], None, [])
    self.addProp('Damage.TwoHand', [
      {'upstream': 'Weapon.TwoHand.Additional', 'defaultValue':[]},
      {'upstream': 'Modifier.Str', 'calcPost':lambda value: [('Physical', 'Modifier.Str', int(value*3/2))]},
      {'upstream': 'Damage.Additional'},
    ], None, [])

    self.addProp('Weapon.MainHand.CriticalRange')
    self.addProp('Weapon.OffHand.CriticalRange')
    self.addProp('Weapon.TwoHand.CriticalRange')
    self.addProp('Weapon.MainHand.CriticalMultiplier')
    self.addProp('Weapon.OffHand.CriticalMultiplier')
    self.addProp('Weapon.TwoHand.CriticalMultiplier')

    self.addProp('Caster.Level')
    self.addProp('Spell.Charges')
    self.addProp('Spell.Activable')

    self.addProp('Vision.Dark')
    self.addProp('Vision.LowLight')

    self.addProp('SpellResistance')

    self.addProp('SavingThrow.Fortitude', [
      {'upstream': 'Modifier.Con'},
      {'upstream': 'SavingThrow.All'},
    ])
    self.addProp('SavingThrow.Reflex', [
      {'upstream': 'Modifier.Dex'},
      {'upstream': 'SavingThrow.All'},
    ])
    self.addProp('SavingThrow.Will', [
      {'upstream': 'Modifier.Wis'},
      {'upstream': 'SavingThrow.All'},
    ])

    self.addProp('Reduction.Fire')

    self.addProp('Immunity.Sleep')
    self.addProp('Immunity.Paralysis')
    self.addProp('Immunity.Poison')
    self.addProp('Immunity.Disease')

  def __repr__(self):
    return repr(self.props)

  def __addAbilitySources(self):
    for ability in self.ctx['Abilities']:
      ab = 'Ability.' + ability
      self.addProp(ab, [
        {'upstream': ab + '.Base'},
        {'upstream': ab + '.Item', 'calcUpstream': calc_upstream_max},
        {'upstream': ab + '.Buff'}
      ])
      self.addProp('Modifier.' + ability, [
        {'upstream':  ab, 'calcPost':  calc_post_ability_modifier}
      ])
  def __addSkillSources(self):
    for skill,skillProto in self.ctx['Skill'].items():
      sk = 'Skill.' + skill
      self.addProp(sk, [
        {'upstream': 'Modifier.' + skillProto['Ability']},
        {'upstream': sk + '.Buff'}
      ])

    self.addProp('SavingThrow.All', {'upstream': 'Skill:Spellcraft', 'calcPost': lambda value: int(value / 5)})

  def addProp(self, propName, sources = None, calculator = None, defaultValue=0):
    if propName in self.props:
      raise RuntimeError('found duplicate prop', propName)

    prop = PropNode(self.props, propName, calculator, defaultValue)
    if not sources:
      pass
    elif isinstance(sources, dict):
      src = sources
      prop.addSource(**src)
    elif isinstance(sources, (list, tuple)):
      for src in sources:
        prop.addSource(**src)
    self.props[propName] = prop

  def addSource(self, propName, **kwargs):
    prop = self.props.get(propName)
    if not prop:
      raise RuntimeError('prop not found', propName)
    prop.addSource(**kwargs)

  def removeSource(self, propName, sourceName):
    prop = self.props.get(propName)
    if not prop:
      raise RuntimeError('prop not found', propName)
    return prop.removeSource(sourceName)

  def calcPropValue(self, propName, caster, target = None):
    if propName not in self.props:
      return 0
    return self.props[propName].calcValue(caster, target)

  def updatePropIntSource(self, propName, sourceName, calculator):
    prop = self.props.get(propName)
    if not prop:
      raise RuntimeError('prop not found', propName)
    prop.updateIntSource(sourceName, calculator)

  def getProp(self, propName):
    if propName not in self.props:
      return 0
    return self.props[propName]

  def getPropSource(self, propName, sourceName):
    prop = self.props.get(propName)
    if not prop:
      return None
    return prop.getSource(sourceName)

  def getPropValueWithSource(self, propName, caster, target = None):
    prop = self.props.get(propName)
    if not prop:
      return (0, {})
    return prop.getValueWithSource(caster, target)

  def updateObject(self, paths, obj):
    self.objects.updateSource(paths, obj)

  def getObject(self, paths):
    return self.objects.getSource(paths, None)
