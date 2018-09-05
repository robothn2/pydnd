#coding: utf-8

class Modifier(dict):
    def addSource(self, key, value, source = ''):
        if key not in self:
            self[key] = {source: value}
            return

        self[key][source] = value

    def addTypedSource(self, key, subtype, value, source = ''):
        if key not in self:
            self[key] = {subtype: {source: value}}
            return

        entry = self[key]
        if subtype not in entry:
            entry[subtype] = {source: value}
            return

        entrySub = entry[subtype]
        entrySub[source] = value

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

if __name__ == '__main__':
    modifier = Modifier({})
    modifier.addTypedSource('ArmorClass', 'Tumble', 1)
    print(modifier)

    modifier = Modifier({'ArmorClass': {}})
    modifier.addTypedSource('ArmorClass', 'Tumble', 2, 'Skills:Tumble')
    print(modifier)

    modifier = Modifier({'ArmorClass': {'Dodge': {'Dex': 2}}})
    modifier.addTypedSource('ArmorClass', 'Tumble', 2, 'Skills:Tumble')
    print(modifier)
