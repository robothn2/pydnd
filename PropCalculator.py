#coding: utf-8
from Dice import rollDice
from common.Props import Modifier

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
        return int(value)

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
        if type(self.calcDisable) == bool:
            return self.calcDisable
        if hasattr(self.calcDisable, '__call__'):
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
        if type(self.calcEnable) == bool:
            return self.calcEnable
        if hasattr(self.calcEnable, '__call__'):
            return self.calcEnable(caster, target)

class PropSourceInt(PropSource):
    def __init__(self, **kwargs):
        super(PropSourceInt, self).__init__(**kwargs)
        self.name = kwargs['name']
        self.calcInt = kwargs.get('calcInt')
    def __repr__(self):
        return repr(self.calcInt)
    def __call__(self, caster, target):
        if type(self.calcInt) == int:
            return self.calcInt
        if type(self.calcInt) == list:
            return self.calcInt
        if hasattr(self.calcInt, '__call__'):
            return self.calcInt(caster, target)

        raise RuntimeError('Found invalid source', self.args, ', calcInt', self.calcInt)

class PropSourceIntMax(PropSource):
    def __init__(self, **kwargs):
        super(PropSourceIntMax, self).__init__(**kwargs)
        self.name = kwargs['name']
        self.calcMax = kwargs.get('calcMax')
    def __repr__(self):
        return 'Max:' + repr(self.calcMax)
    def __call__(self, caster, target):
        if type(self.calcMax) == int:
            return self.calcMax
        if hasattr(self.calcMax, '__call__'):
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
        if len(self.sourcesInt) > 0:
            info += ' Sources:' + repr(self.sourcesInt)
        if len(self.sourcesUpstream) > 0:
            info += ' Upstreams:' + repr(self.sourcesUpstream)
        if len(self.sourcesEnable) > 0:
            info += ' Enable:' + repr(self.sourcesEnable)
        if len(self.sourcesDisable) > 0:
            info += ' Disable:' + repr(self.sourcesDisable)
        return info + '}'

    def needRecalc(self):
        #print(self.name, 'recalc set to True')
        self.recalc = True
        for _,propDownstream in enumerate(self.downstreams):
            propDownstream.needRecalc()

    def setNoCache(self):
        self.noCache = True
        for _,propDownstream in enumerate(self.downstreams):
            propDownstream.setNoCache()

    def __addDownstream(self, downstreamProp):
        self.downstreams.append(downstreamProp)
        downstreamProp.needRecalc()

    def __addUpstream(self, upstreamName, upstreamDict):
        upstreamProp = self.props.get(upstreamName)
        if not upstreamProp:
            #if upstream Prop not found, create empty PropNode
            upstreamProp = PropNode(self.props, upstreamName, upstreamDict.get('calcUpstream'), 0)
            self.props[upstreamName] = upstreamProp

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
            for _,upstream in enumerate(upstreams):
                upstreamDict = {}
                if type(upstream) == str:
                    upstreamsProp.append(self.__addUpstream(upstream, upstreamDict))
                elif type(upstream) == dict:
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

    def calcSingleSource(self, sourceName, caster, target):
        source = self.sourcesInt.get(sourceName)
        if source == None:
            return self.defaultValue
        return source(caster, target)

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
        for _, d in enumerate(self.downstreams):
            print(d.name, end=' ')
        print('')

    def calcValue(self, caster, target):
        if not self.noCache and not self.recalc:
            return self.value

        #print('begin calc Prop:', self.name)
        self.recalc = False
        self.value = self.defaultValue

        sourceEnable = None
        for _,source in enumerate(self.sourcesEnable):
            if source(caster, target):
                sourceEnable = source
                break
        for _,sourceDisable in enumerate(self.sourcesDisable):
            if sourceEnable and sourceEnable.priority > sourceDisable.priority:
                print('  Prop %s enabled by %s' % (self.name, sourceEnable.name))
                break # highest priority disable source is lower than effecting enable source
            if sourceDisable(caster, target):
                print('  Prop %s disabled by %s' % (self.name, sourceDisable.name))
                return self.value

        for name,sourceCalculator in self.sourcesInt.items():
            sourceValueInt = sourceCalculator(caster, target)
            self.value = self.calculator(sourceValueInt, self.value)

        for _,upstreamCalculator in enumerate(self.sourcesUpstream):
            sourceValueInt = upstreamCalculator(caster, target)
            self.value = self.calculator(sourceValueInt, self.value)

        for _,upstreamCalculator in enumerate(self.sourcesUpstreamMulti):
            sourceValueInt = upstreamCalculator(caster, target)
            self.value = self.calculator(sourceValueInt, self.value)

        if self.sourceIntMax:
            valueNew = min(self.sourceIntMax(caster, target), self.value)
            if valueNew != self.value:
                print('  Prop %s cap by %s, %d -> %d' % (self.name, self.sourceIntMax.name, self.value, valueNew))
                self.value = valueNew
        print('  Prop', self.name, '=', self.value)
        return self.value

    def getValueWithSource(self, caster, target):
        self.recalc = False
        self.value = 0

        result = {}
        sourceEnable = None
        for _,source in enumerate(self.sourcesEnable):
            if source(caster, target):
                sourceEnable = source
                break
        for _,sourceDisable in enumerate(self.sourcesDisable):
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

        for _,upstreamEval in enumerate(self.sourcesUpstream):
            sourceInt = upstreamEval(caster, target)
            if sourceInt != 0:
                self.value = self.calculator(sourceInt, self.value)
                result[upstreamEval.name] = sourceInt

        for _,upstreamMultiEval in enumerate(self.sourcesUpstreamMulti):
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
            {'upstream': 'ArmorClass.Armor', 'calcUpstream': calc_upstream_max},
            {'upstream': 'Skill.Tumble', 'name': 'ArmorClass.Tumble', 'calcPost': (lambda value: int(value/10))},
            {'upstream': 'ArmorClass.Natural'},
            {'upstream': 'ArmorClass.Luck'},
            {'upstream': 'ArmorClass.Deflection'},
            {'upstream': 'ArmorClass.Dodge'},
            {'upstream': 'ArmorClass.Dex'},
            {'upstream': 'ArmorClass.Buff'},
            {'upstream': 'ArmorClass.Aura'}
        ])

        self.addProp('SpellResistance')
        self.addProp('BaseAttackBonus')
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

        self.addProp('Damage.MainHand', [
            #{'upstream': 'Weapon.MainHand.Base', name='Kukri', calcInt=lambda caster,target: rollDice(1,4,1), noCache=True}, # add this source on equiped mainhand weapon
            {'upstream': 'Weapon.MainHand.Additional'},
            {'upstream': 'Modifier.Str'},
            {'upstream': 'Damage.Additional'},
            #{'name': 'Buff:Disarm', 'calcDisable': (lambda caster, target: caster.hasBuff('Disarm'))},
        ])
        self.addProp('Damage.OffHand', [
            #{'upstream': 'Weapon.OffHand.Base', name='Kukri', calcInt=lambda caster,target: rollDice(1,4,1), noCache=True}, # add this source on equiped mainhand weapon
            {'upstream': 'Weapon.OffHand.Additional'},
            {'upstream': 'Modifier.Str', 'calcPost':(lambda value: int(value/2))},
            {'upstream': 'Damage.Additional'},
        ])
        self.addProp('Damage.TwoHand', [
            #{'upstream': 'Weapon.TwoHand.Base', name='Kukri', calcInt=lambda caster,target: rollDice(1,4,1), noCache=True}, # add this source on equiped mainhand weapon
            {'upstream': 'Weapon.TwoHand.Additional'},
            {'upstream': 'Modifier.Str', 'calcPost':(lambda value: int(value*3/2))},
            {'upstream': 'Damage.Additional'},
        ])

    def __repr__(self):
        return repr(self.props)

    def __addAbilitySources(self):
        for _,ability in enumerate(self.ctx['Abilities']):
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
        for skill,skillProto in self.ctx['protosSkill'].items():
            sk = 'Skill.' + skill
            self.addProp(sk, [
                {'upstream': 'Modifier.' + skillProto['Ability']},
                {'upstream': sk + '.Buff'}
            ])

        self.addProp('SavingThrow.Fortitude', {'upstream': 'Skill:Spellcraft', 'calcPost': lambda value: int(value / 5)})
        self.addProp('SavingThrow.Reflex', {'upstream': 'Skill:Spellcraft', 'calcPost': lambda value: int(value / 5)})
        self.addProp('SavingThrow.Will', {'upstream': 'Skill:Spellcraft', 'calcPost': lambda value: int(value / 5)})

    def addProp(self, propName, sources = None, calculator = None, defaultValue=0):
        if propName in self.props:
            raise RuntimeError('found duplicate prop', propName)

        prop = PropNode(self.props, propName, calculator, defaultValue)
        if sources == None:
            pass
        elif type(sources) == dict:
            src = sources
            prop.addSource(**src)
        elif type(sources) == list:
            for _, src in enumerate(sources):
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

    def getPropValue(self, propName, caster, target):
        if propName not in self.props:
            return 0
        return self.props[propName].calcValue(caster, target)

    def getProp(self, propName):
        if propName not in self.props:
            return 0
        return self.props[propName]

    def printPropValueSource(self, propName, caster, target):
        if propName not in self.props:
            return
        print(self.props[propName].getValueWithSource(caster, target))

    def updateObject(self, paths, obj):
        self.objects.updateSource(paths, obj)

    def getObject(self, paths):
        return self.objects.getSource(paths, None)

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
    assert (m.getPropValue('Ability.Dex.Base', p1, p2) == 21)

    # test custom calculator calc_upstream_max() for 'Ability.Dex.Item'
    m.addSource('Ability.Dex.Item', name='Item:Boot+2', calcInt=2)
    m.addSource('Ability.Dex.Item', name='Item:RingOfDexerity+6', calcInt=6)
    assert (m.getPropValue('Ability.Dex.Item', p1, p2) == 6)

    m.addSource('ArmorClass.Dex', name='Feat:UncannyDodge', calcEnable = True, priority = 100)
    assert (m.getPropValue('ArmorClass.Dex', p1, p2) == 8)

    m.addSource('ArmorClass.Armor', name='Item:Leather+3', calcInt = 7)
    m.addSource('ArmorClass.Armor', name='Item:RingOfProtection+3', calcInt=3)
    assert (m.getPropValue('ArmorClass.Armor', p1, None) == 7)

    # test source replaceable, and optional target
    m.addSource('Class.Level', name='Ranger', calcInt=1)
    m.addSource('Class.Level', name='Ranger', calcInt=7)
    assert(m.getPropValue('Class.Level', p1, None) == 7)

    # test cached value discarded by new source
    m.addSource('Class.Level', name='Cleric', calcInt=2)
    assert(m.getPropValue('Class.Level', p1, None) == 9)

    # test dynamic upstream, and custom name for upstream
    m.addSource('SpellResistance', upstream = 'Class.Level', name = 'YuantiPureBlood', calcPost = lambda value: 11 + value)
    # test calcPost
    assert(m.getPropValue('SpellResistance', p1, None) == 20)

    # test value cache
    m.printPropValueSource('ArmorClass', p1, p2)
    m.printPropValueSource('ArmorClass', p1, p2)

    # test removable source(Int) and value call needRecalc() recursively
    m.removeSource('Ability.Dex.Item', 'Item:RingOfDexerity+6')
    # test recursive call downstream.needRecalc() triggered by removing source
    m.printPropValueSource('ArmorClass', p1, p2)

    # test source calculated by multi upstream
    m.addSource('Ability.Con.Base', name='Builder', calcInt=16)
    assert (m.getPropValue('HitPoint', p1, None) == 27)

    bab = m.getPropValue('AttackBonus.Base')

    # noCache flag affect upstream Props recursively
    m.addSource('Damage.MainHand', name='Kukri', calcInt=lambda caster,target: rollDice(1,4,1), noCache=True)
    dmgs = []
    for i in range(10):
        dmg = m.getPropValue('Damage.MainHand', p1, p2)
        if dmg not in dmgs:
            dmgs.append(dmg)
    assert (len(dmgs) > 1)

