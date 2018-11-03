#coding: utf-8

class BuffManager:
    def __init__(self, unit):
        self.owner = unit
        self.buffs = []
        self.tsInMs = 0

    def addBuff(self, buffCaster, buffProto, buffMetaMagics = []):
        expired = int(1000 * (buffProto.model.buffDuration(buffCaster, buffProto))) + self.tsInMs
        buffName = buffProto.nameBuff
        if buffName not in self.buffs:
            self.buffs.append([buffCaster, expired, buffProto, buffMetaMagics])
        else:
            buffExist = self.buffs[self.buffs.index(buffName)]
            if buffExist[1] > expired:
                print('weak buff', buffName, 'cast from', repr(buffCaster))
                return False

            buffExist = [buffCaster, expired, buffProto, buffMetaMagics]

        # apply buff to owner
        buffProto.model.buffApply(buffProto, buffProto.nameBuff, buffCaster, self.owner, buffMetaMagics)
        print(repr(self.owner), 'apply buff', buffProto.nameBuff, ', cast from', repr(buffCaster))
        return True

    def update(self, deltaTime):
        self.tsInMs += int(1000 * deltaTime)
        if len(self.buffs) == 0:
            return

        # remove expired buff, one per update call
        for i, buff in enumerate(self.buffs):
            if buff[1] <= self.tsInMs:
                self.buffs.pop(i)
                buffProto = buff[2]
                buffProto.model.buffUnapply(buffProto, buffProto.nameBuff, buff[0], self.owner, [])
                print(repr(self.owner), '\'s buff', buff[2].name, 'expired, cast by', repr(buff[0]))
                break

