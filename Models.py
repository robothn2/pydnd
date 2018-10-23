#coding: utf-8

class ModelBase:
    def __init__(self, name, **kwargs):
        self.model = type(name, (), kwargs)
        print(self.model)

class Rase(ModelBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

class Class(ModelBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def isAvailable(self, unit):
        if not hasattr(self.model, 'Requirements'):
            return True

        for _,cond in enumerate(self.model.Requirements):
            if cond is not tuple or len(cond) < 2:
                continue

            # check Skill
            if cond[0] == 'Skill':
                if unit.calc.calcPropValue('Skill.' + cond[1], 'Builder') < cond[2]:
                    return False

            # check Class
            elif cond[0] == 'Class':
                clsMatched = False
                if cond[1] is tuple:
                    for _1,cls in enumerate(cond[1]):
                        if unit.getClassLevel('Sorcerer') > 0:
                            clsMatched = True
                            break
                elif cond[1] is str:
                    if unit.getClassLevel('Sorcerer') > 0:
                        clsMatched = True
                if not clsMatched:
                    return False

            # check BaseAttackBonus
            elif cond[0] == 'BaseAttackBonus':
                if unit.calc.calcPropValue('AttackBonus.Base', unit) < cond[2]:
                    return False

            # check Feat
            elif cond[0] == 'Feat':
                if cond[1] is tuple:
                    if not unit.hasFeats(cond[1]):
                        return False
                elif cond[1] is str:
                    if not unit.hasFeat(cond[1]):
                        return False
                elif cond[1] is function:
                    if not cond[1](unit):
                        return False

            # custom condition
            elif cond[1] is function:
                if not cond[1](unit):
                    return False

        return True