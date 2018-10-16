#coding: utf-8

class SpellProtoBufferSelf:
    def __init__(self, bufferName, **kwargs):
        self.name = bufferName
        self.funCastToTarget = kwargs.get('castToTarget')
        self.funFillCharge = kwargs.get('fillCharge')
        self.funDecCharge = kwargs.get('decCharge')
        self.funBuffDuration = kwargs.get('buffDuration')
        self.funBuffApply = kwargs.get('buffApply')
        self.funBuffUnapply = kwargs.get('buffUnapply')
        self.params = kwargs.get('params')

    def activate(self, caster):
        self.funCastToTarget(caster, None, self.params)

    def duration(self, caster, metaMagics):
        return self.funBuffDuration(caster, metaMagics)

    def apply(self, caster, propCalc, metaMagics):
        return self.funBuffApply(caster, caster.calc, metaMagics)

    def unapply(self, propCalc):
        return self.funBuffUnapply(propCalc)