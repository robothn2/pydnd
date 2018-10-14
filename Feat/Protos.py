#coding: utf-8

class FeatProtoActivable:
    def __init__(self, **kwargs):
        self.funActive = kwargs.get('active')
        self.funDeactive = kwargs.get('deactive')
        self.params = kwargs.get('params')

    def activate(self, caster):
        self.funActive(caster, self.params)
    def deactivate(self, caster):
        self.funDeactive(caster)

class FeatProtoSpellLike:
    def __init__(self, **kwargs):
        self.funCast = kwargs.get('cast')
        self.params = kwargs.get('params')

