#coding: utf-8

class BuffManager:
  def __init__(self, unit):
    self.owner = unit
    self.buffs = []
    self.tsInMs = 0

  def addBuff(self, buffCaster, spell, **kwargs):
    calculator = spell.buffDuration
    durationSeconds = calculator if isinstance(calculator, int) else calculator(buffCaster, **kwargs)
    expired = int(1000 * durationSeconds) + self.tsInMs
    buffName = spell.nameBuff
    if buffName not in self.buffs:
      self.buffs.append((buffCaster, expired, spell, kwargs))
    else:
      buffExist = self.buffs[self.buffs.index(buffName)]
      if buffExist[1] > expired:
        print('weak buff', buffName, 'cast from', repr(buffCaster))
        return False
      buffExist = (buffCaster, expired, spell, kwargs)

    # apply buff to owner
    spell.buffApply(spell, buffCaster, self.owner, **kwargs)
    print(repr(self.owner), 'apply buff', spell.nameBuff, ', cast from', repr(buffCaster), ', duration:', durationSeconds)
    return True

  def update(self, deltaTime):
    self.tsInMs += int(1000 * deltaTime)
    if len(self.buffs) == 0:
      return

    # remove expired buff, one per update call
    for i, buffEntry in enumerate(self.buffs):
      if buffEntry[1] <= self.tsInMs:
        self.buffs.pop(i)
        caster = buffEntry[0]
        spell = buffEntry[2]
        print(repr(self.owner), '\'s buff', spell.nameBuff, 'expired, cast by', repr(caster))
        spell.buffUnapply(spell, caster, self.owner)
        break

