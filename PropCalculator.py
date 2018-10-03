#coding: utf-8
from common import Props

def calc_post_mainhand_weapon(value):
    return value
def calc_post_ability_modifier(value):
    return int((value - 10) / 2)
def calc_upstream_sum(sourceValue, oldValue):
    return sourceValue + oldValue
def calc_upstream_max(sourceValue, oldValue):
    #print(sourceValue, oldValue)
    return max(sourceValue, oldValue)

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
        if hasattr(self.calcInt, '__call__'):
            return self.calcInt(caster, target)
        raise RuntimeError('Found invalid source', self.args)

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
    def __init__(self, props, name, calculator):
        self.name = name
        self.recalc = True # True if need recalc
        self.value = 0
        self.props = props
        self.calculator = calculator if calculator else calc_upstream_sum # default calculator is sum
        self.sourcesInt = {}
        self.sourcesUpstream = []
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

    def __addDownstream(self, downstreamProp):
        self.downstreams.append(downstreamProp)
        downstreamProp.needRecalc()

    def __addUpstream(self, source):
        upstream = source.get('upstream')
        if type(upstream) != str:
            return
        upstreamProp = self.props.get(upstream)
        if not upstreamProp:
            #if upstream Prop not found, create empty PropNode
            upstreamProp = PropNode(self.props, upstream, source.get('calcUpstream'))
            self.props[upstream] = upstreamProp

        source['upstream'] = upstreamProp
        sourceUpstream = PropSourceUpstream(**source)
        upstreamProp.__addDownstream(self)
        self.sourcesUpstream.append(sourceUpstream)

    def addSource(self, **kwargs):
        if 'upstream' in kwargs:
            self.__addUpstream(kwargs)
            return
        if 'calcEnable' in kwargs:
            self.sourcesEnable.append(PropSourceEnable(**kwargs))
            # sort switch by priority
            self.sourcesEnable.sort(key=lambda source: source.priority, reverse=False)
            return
        if 'calcDisable' in kwargs:
            self.sourcesDisable.append(PropSourceDisable(**kwargs))
            self.sourcesDisable.sort(key=lambda source: source.priority, reverse=False)
            return

        name = kwargs['name']

        if 'calcMax' in kwargs:
            self.sourceIntMax = PropSourceIntMax(**kwargs)
        else:
            self.sourcesInt[name] = PropSourceInt(**kwargs)

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
                print(self.downstreams)
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
        if not self.recalc:
            return self.value

        #print('begin calc Prop:', self.name)
        self.recalc = False
        self.value = 0

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
                return 0

        for name,sourceCalculator in self.sourcesInt.items():
            sourceInt = sourceCalculator(caster, target)
            self.value = self.calculator(sourceInt, self.value)

        for _,upstreamCalculator in enumerate(self.sourcesUpstream):
            sourceInt = upstreamCalculator(caster, target)
            self.value = self.calculator(sourceInt, self.value)

        if self.sourceIntMax:
            valueNew = min(self.sourceIntMax(caster, target), self.value)
            if valueNew != self.value:
                print('  Prop %s cap by %s, %d -> %d' % (self.name, self.sourceIntMax.name, self.value, valueNew))
                self.value = valueNew
        print('  Prop', self.name, '=', self.value)
        return self.value

    def getValueSource(self, caster, target):
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

        self.__addAbilitySources()
        self.__addSkillSources()

        self.addProp('ArmorClass.Dex', [
            {'upstream': 'Modifier.Dex'},
            {'name': 'ArmorDexCap', 'calcMax': 1000}, # armor can replace this cap
            {'name': 'Buff:TargetInvisible', 'calcDisable': (lambda caster, target: target.hasBuff('Invisible'))} # using normal priority 0, UncannyDodge can overwrite it
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

        self.addProp('Weapon.StrModifierMainHand', {'upstream': 'Modifier.Str', 'calcPost': calc_post_mainhand_weapon})

        self.addProp('AttackBonus.MainHand', [
            {'upstream': 'Weapon.StrModifierMainHand'},
            {'upstream': 'Modifier.Str'},
            {'name': 'ArmorDexCap', 'calcMax': 1000}, # armor can replace this max value
            {'name': 'Buff:Disarm', 'calcDisable': (lambda caster, target: caster.hasBuff('Disarm'))},
        ])
        '''
        self.addProp('HitPoint', [
            {'upstreams': ['Modifier.Con', 'Class.Level'], 'calcMulti': (
                lambda upstreams, caster, target:
                    upstreams[0].calcValue() * upstreams[1].calcValue()
            )},
        ])
        '''
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
        self.addProp('Skill.Tumble', {'upstream': 'Modifier.Dex'})
        '''
        for _,skill in enumerate(self.ctx['Skills']):
            ab = 'Skill.' + skill
            self.addProp(ab, [
                #{'name': 'Builder'},
                {'upstream': 'Modifier.' + },
                {'upstream': ab + '.Buff'}
            ])
            self.addProp('Modifier.' + ability, [
                {'upstream':  ab, 'calcPost':  calc_post_ability_modifier}
            ])
        '''

    def addProp(self, propName, sources = None, calculator = None):
        if propName in self.props:
            raise RuntimeError('found duplicate prop', propName)

        prop = PropNode(self.props, propName, calculator)
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

    def getProp(self, propName, caster, target):
        if propName not in self.props:
            return 0
        return self.props[propName]

    def printPropValueSource(self, propName, caster, target):
        if propName not in self.props:
            return
        print(self.props[propName].getValueSource(caster, target))

if __name__ == '__main__':
    ctx = __import__('Context')
    player = __import__('Character')
    p1 = player.Character(ctx.ctx)
    p2 = player.Character(ctx.ctx)
    m = p1.calc

    # test multi source
    m.addSource('Ability.Dex.Base', name='Race:Elf', calcInt=2)
    m.addSource('Ability.Dex.Base', name='Builder', calcInt=18)
    m.addSource('Ability.Dex.Base', name='LevelUp:4', calcInt=1)

    # test custom calculator calc_upstream_max() for 'Ability.Dex.Item'
    m.addSource('Ability.Dex.Item', name='Item:Boot+2', calcInt=2)
    m.addSource('Ability.Dex.Item', name='Item:RingOfDexerity+6', calcInt=6)

    m.addSource('ArmorClass.Dex', name='Feat:UncannyDodge', calcEnable = True, priority = 100)

    m.addSource('ArmorClass.Armor', name='Item:Leather+3', calcInt = 7)
    m.addSource('ArmorClass.Armor', name='Item:RingOfProtection+3', calcInt=3)

    m.addSource('Class.Level', name='Ranger', calcInt=1)
    m.addSource('Class.Level', name='Ranger', calcInt=7) # test source replaceable
    m.addSource('Class.Level', name='Cleric', calcInt=2)
    # test dynamic upstream, and custom name for upstream
    m.addSource('SpellResistance', upstream = 'Class.Level', name = 'YuantiPureBlood', calcPost = lambda value: 11 + value)

    print(m)
    m.printPropValueSource('SpellResistance', p1, p2)
    m.printPropValueSource('ArmorClass', p1, p2)
    m.printPropValueSource('ArmorClass', p1, p2) # test value cache

    # test source(Int) removable and value call needRecalc() recursively
    print(m.removeSource('Ability.Dex.Item', 'Item:RingOfDexerity+6'))
    m.printPropValueSource('ArmorClass', p1, p2)