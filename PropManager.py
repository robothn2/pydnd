#coding: utf-8
from common import Props

def calc_post_ability_modifier(value):
    return int((value - 10) / 2)
def calc_upstream_sum(sourceValue, oldValue):
    return sourceValue + oldValue
def calc_upstream_max(sourceValue, oldValue):
    return max(sourceValue, oldValue)

class PropSource:
    def __init__(self, **kwargs):
        self.args = kwargs

class PropSourceUpstream(PropSource):
    def __init__(self, **kwargs):
        super(PropSourceUpstream, self).__init__(**kwargs)
        self.upstream = kwargs.get('upstream')
        self.calcUpstream = kwargs.get('calcUpstream')
        self.calcPost = kwargs.get('calcPost')
    def __repr__(self):
        return self.upstream.name
    def __call__(self, caster, target):
        if not hasattr(self.upstream, 'calcValue'):
            return 0 # unbound upstream, skip this source
        value = self.upstream.calcValue(caster, target, self.calcUpstream)
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
    def __init__(self, name):
        self.name = name
        self.recalc = True
        self.value = 0
        self.sourcesInt = {}
        self.sourcesUpstream = []
        self.sourcesDisable = []
        self.sourcesEnable = []
        self.sourceIntMax = None
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
        self.recalc = True

    def addSource(self, **kwargs):
        if 'upstream' in kwargs:
            self.sourcesUpstream.append(PropSourceUpstream(**kwargs))
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
        if name in self.sourcesInt:
            raise RuntimeError('Found duplicate source', name)

        if 'calcMax' in kwargs:
            self.sourceIntMax = PropSourceIntMax(**kwargs)
        else:
            self.sourcesInt[name] = PropSourceInt(**kwargs)

    def calcValue(self, caster, target, calculator = None):
        if not self.recalc:
            return self.value

        print('begin calc Prop:', self.name)
        self.recalc = True
        self.value = 0
        if not calculator:
            calculator = calc_upstream_sum #default is sum

        sourceEnable = None
        for _,source in enumerate(self.sourcesEnable):
            if source(caster, target):
                sourceEnable = source
                break
        for _,sourceDisable in enumerate(self.sourcesDisable):
            if sourceEnable and sourceEnable.priority > sourceDisable.priority:
                print('  Prop %s enabled by %s' % (self.name, sourceEnable.name))
                break
            if sourceDisable(caster, target):
                print('  Prop %s disabled by %s' % (self.name, sourceDisable.name))
                return 0

        for name,sourceCalculator in self.sourcesInt.items():
            sourceInt = sourceCalculator(caster, target)
            self.value = calculator(sourceInt, self.value)

        for _,upstreamCalculator in enumerate(self.sourcesUpstream):
            sourceInt = upstreamCalculator(caster, target)
            self.value = calculator(sourceInt, self.value)

        if self.sourceIntMax:
            valueNew = min(self.sourceIntMax(), self.value)
            if valueNew != self.value:
                print('  Prop %s cap by %s, %d -> %d' % (self.name, self.sourceIntMax.name, self.value, valueNew))
                self.value = valueNew
        print('  Prop', self.name, '=', self.value)
        return self.value

class PropManager:
    def __init__(self, ctx):
        self.ctx = ctx
        self.props = {}
        for _,ability in enumerate(['Dex']): #ctx['Abilities']
            ab = 'Ability.' + ability
            self.addProp(ab, [
                {'upstream': ab + '.Base'},
                {'upstream': ab + '.Item', 'calcUpstream': calc_upstream_max},
                {'upstream': ab + '.Buff'}
            ])
            self.addProp('Modifier.' + ability, [
                {'upstream':  ab, 'calcPost':  calc_post_ability_modifier}
            ])

        self.addProp('ArmorClass.Dex', [
            {'upstream': 'Modifier.Dex'},
            #{'name': 'ArmorDexCap', 'calcMax': 1000}, # armor can replace this cap
            #{'name': 'Buff:TargetInvisible', 'calcDisable': (lambda caster, target: target.hasBuff('Invisible'))} # using normal priority 0, UncannyDodge can overwrite it
        ])
        self.addProp('ArmorClass', [
            {'upstream': 'ArmorClass.Armor', 'calcUpstream': calc_upstream_max},
            {'upstream': 'ArmorClass.Natural'},
            {'upstream': 'ArmorClass.Luck'},
            {'upstream': 'ArmorClass.Deflection'},
            {'upstream': 'ArmorClass.Dodge'},
            {'upstream': 'ArmorClass.Dex'},
            {'upstream': 'ArmorClass.Buff'},
            {'upstream': 'ArmorClass.Aura'}
        ])

    def __repr__(self):
        return repr(self.props)

    def addProp(self, propName, sources = None):
        if propName in self.props:
            raise RuntimeError('found duplicate prop', propName)

        prop = PropNode(propName)
        if sources == None:
            pass
        elif type(sources) == dict:
            self.__replaceUpstreamField(sources)
            prop.addSource(**sources)
        elif type(sources) == list:
            for _, src in enumerate(sources):
                self.__replaceUpstreamField(src)
                prop.addSource(**src)
        self.props[propName] = prop

    def __replaceUpstreamField(self, source):
        upstream = source.get('upstream')
        if type(upstream) != str:
            return
        upstreamProp = self.props.get(upstream)
        if not upstreamProp:
            #if upstream Prop not found, create empty PropNode
            upstreamProp = PropNode(upstream)
            self.props[upstream] = upstreamProp
        source['upstream'] = upstreamProp

    def addSource(self, propName, **kwargs):
        if propName not in self.props:
            raise RuntimeError('prop not found', propName)
        self.props[propName].addSource(**kwargs)

    def getPropValue(self, propName, caster, target):
        if propName not in self.props:
            return 0
        return self.props[propName].calcValue(caster, target)

if __name__ == '__main__':
    ctx = __import__('Context')
    player = __import__('Character')
    p1 = player.Character(ctx.ctx)
    p2 = player.Character(ctx.ctx)
    m = PropManager(ctx.ctx)
    """
    """
    m.addSource('Ability.Dex.Base', name='Race:Elf', calcInt=2)
    m.addSource('Ability.Dex.Base', name='Builder', calcInt=16)
    m.addSource('Ability.Dex.Base', name='LevelUp:4', calcInt=1)
    m.addSource('Ability.Dex.Item', name='Item:Boot+4', calcInt=4)
    m.addSource('ArmorClass.Dex', name= 'Feat:UncannyDodge', calcEnable = True, priority = 100)
    m.addSource('ArmorClass.Armor', name= 'Item:Leather+3', calcInt = 6)

    print(m)
    print(m.getPropValue('Modifier.Dex', p1, p2))
    print(m.getPropValue('ArmorClass', p1, p2))
