#coding: utf-8
import warnings

class FeatProto:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.name = kwargs.get('name')
        self.nameFull = kwargs.get('nameFull')
        self.group = kwargs.get('group')
        self.groupMemberName = kwargs.get('groupMemberName')
        self.apply = kwargs.get('apply')
        self.unapply = kwargs.get('unapply')
        self.prerequisite = kwargs.get('prerequisite')

    def apply(self, type, caster):
        if type == 'active':
            caster.calc.addSource('Spell.Activable', name=self.nameFull, calcInt=self)
        elif type == 'spell':
            assert 'spell group not impl'
        elif type == 'chargedSpell':
            caster.calc.addSource('Spell.Charges', name=self.nameFull, calcInt=self)
        else:
            self.apply(caster)

    def unapply(self, target = None):
        pass

    def active(self, caster):
        active = self.kwargs.get('active')
        active(caster)
    def deactive(self, caster):
        deactive = self.kwargs.get('deactive')
        deactive(caster)

class FeatGroupProto:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.caster = kwargs.get('caster')
        self.members = {}
    def addMember(self, featProto, featParams):
        self.members[featProto.nameFull] = featProto
        featProto.apply(self.type, self.caster)

    def unapplyMember(self, target = None):
        pass

class FeatManager:
    def __init__(self, unit):
        self.owner = unit
        self.featGroups = [
            FeatGroupProto(name='Self', type='applySelf', caster=unit),
            FeatGroupProto(name='Weapon', type='applySelf', caster=unit), # apply on weapon switching
            FeatGroupProto(name='Target', type='applySelf', caster=unit),
            FeatGroupProto(name='Active', type='active', caster=unit),
            FeatGroupProto(name='Spell', type='spell', caster=unit),
            FeatGroupProto(name='ChargedSpell', type='chargedSpell', caster=unit),
        ]

    def addFeat(self, featNameFull, featParams):
        featProto = self.owner.ctx['protosFeat'].get(featNameFull)
        if not featProto:
            warnings.warn('unknown feat ' + featNameFull)
            return False

        for _, group in enumerate(self.featGroups):
            if group.name != featProto.group:
                continue

            print(repr(self.owner), 'add feat', featProto.nameFull, 'to group', group.name)
            group.addMember(featProto, featParams)
            return True

        assert 'unknown feat group ' + featProto.group + ' for feat ' + featProto.nameFull
        return False

    def removeFeat(self, featNameFull):
        pass

    def getAvailableFeats(self):
        pass