#coding: utf-8

class Modifier(dict):
    def updateUniqueSource(self, pathsTuple, value):
        d = self
        cnt = len(pathsTuple)
        for i in range(cnt):
            key = pathsTuple[i]
            if i == cnt -1:
                d[key] = value
                return

            if key not in d:
                d[key] = {}
            d = d[key]

    def getSource(self, pathsTuple, defaultValue):
        cnt = len(pathsTuple)
        if cnt == 0:
            return None

        d = self
        for i in range(cnt):
            key = pathsTuple[i]
            if i == cnt -1:
                return d[key] if key in d else defaultValue

            if key not in d:
                return defaultValue
            d = d[key]

    def sumSource(self, pathsTuple, includeSourceNames = None, excludeSourceNames = None):
        branch = self.getSource(pathsTuple, {})
        sumValue = 0
        if type(includeSourceNames) == list:
            for _, name in enumerate(includeSourceNames):
                if name not in branch:
                    continue

                # sum sources under branch
                for source in branch.values():
                    sumValue += int(source)
        else:
            for key, value in branch.items():
                if type(excludeSourceNames) == list and key not in excludeSourceNames:
                    continue
                # sum sources under branch
                for source in branch.values():
                    sumValue += int(source)

        return sumValue

    def sumTypedSourceAll(self, key):
        if key not in self:
            return 0

        sumValue = 0
        for abType in self[key].values():
            for abSource in abType.values():
                sumValue += int(abSource)
        return sumValue

    def sumTypedSource(self, key, subtypes):
        if key not in self:
            return 0

        sumValue = 0
        for abType in self[key].values():
            for subtype in abType.keys():
                if subtype in subtypes:
                    sumValue += int(abType[subtype])
        return sumValue

class Props(dict):
    def incValue(self, key, value):
        if key not in self:
            self[key] = value
            return

        self[key] += value

    def hasKey(self, key, subkey):
        if key not in self:
            return False
        return subkey in self[key]

    def hasKeyList(self, key, subKeyList):
        if key not in self:
            return False

        keyEntry = self[key]
        for i, subKey in enumerate(subKeyList):
            if subKey not in keyEntry:
                return False
        return True

    def sumFieldValue(self, key, fieldName):
        if key not in self:
            return 0
        sumField = 0
        for field in self[key].values():
            if fieldName in field:
                sumField += field[fieldName]
        return sumField

if __name__ == '__main__':
    modifier = Modifier({})
    modifier.updateUniqueSource(('ArmorClass', 'Tumble'), 1)
    print(modifier)

    modifier = Modifier({'ArmorClass': {}})
    modifier.updateUniqueSource(('ArmorClass', 'Tumble', 'Skills:Tumble'), 2)
    print(modifier)

    modifier = Modifier({'ArmorClass': {'Dodge': {'Dex': 2}}})
    modifier.updateUniqueSource(('ArmorClass', 'Tumble', 'Skills:Tumble'), 3)

    modifier = Modifier({'AttackBonus': {}})
    modifier.updateUniqueSource(('AttackBonus', 'Racial', 'Undead', 'Feat:FavoredEnemy'), 3)
    print(modifier)
