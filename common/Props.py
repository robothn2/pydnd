#coding: utf-8

def sumIntValue(value):
    sumValue = 0
    if type(value) == int:
        sumValue += value
    elif type(value) == dict:
        for subValue in value.values():
            sumValue += int(subValue)
    return sumValue

class Modifier(dict):
    def updateSource(self, paths, value):
        d = self
        cnt = len(paths)
        for i in range(cnt):
            key = paths[i]
            if i == cnt -1:
                d[key] = value
                return

            if key not in d:
                d[key] = {}
            d = d[key]

    def getSource(self, paths, defaultValue = {}):
        d = self
        if type(paths) == str:
            return d[paths] if paths in d else defaultValue
        if (type(paths) != list and type(paths) != tuple):
            return defaultValue

        cnt = len(paths)
        if cnt == 0:
            return defaultValue

        for i in range(cnt):
            key = paths[i]
            if i == cnt -1:
                return d[key] if key in d else defaultValue

            if key not in d:
                return defaultValue
            d = d[key]

    def sumSource(self, pathsList, includeBranchNames = None, excludeBranchNames = None):
        branch = self.getSource(pathsList, {})
        #print('got branch:', branch)
        sumValue = 0
        if type(includeBranchNames) == list:
            for _, name in enumerate(includeBranchNames):
                if name not in branch:
                    continue
                # sum sources under branch[name]
                for v in branch[name].values():
                    sumValue += sumIntValue(v)
        else:
            for key, branchSub in branch.items():
                if type(excludeBranchNames) == list and key not in excludeBranchNames:
                    continue
                # sum sources under branch
                if type(branchSub) == int:
                    sumValue += branchSub
                    continue
                for v in branchSub.values():
                    sumValue += sumIntValue(v)

        return sumValue

    def updateListParam(self, paths, params):
        d = self
        cnt = len(paths)
        for i in range(cnt):
            key = paths[i]
            if i == cnt -1:
                if key not in d:
                    d[key] = params
                else:
                    #merge params and d[key]
                    for _, param in params:
                        if param not in d[key]:
                            d[key].append(param)
                return

            if key not in d:
                d[key] = {}
            d = d[key]

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
    modifier.updateSource(('ArmorClass', 'Tumble'), 1)
    print(modifier)

    modifier = Modifier({'ArmorClass': {}})
    modifier.updateSource(('ArmorClass', 'Tumble', 'Skills:Tumble'), 2)
    print(modifier)

    modifier = Modifier({'ArmorClass': {'Dodge': {'Dex': 2}}})
    modifier.updateSource(('ArmorClass', 'Tumble', 'Skills:Tumble'), 3)

    modifier.updateSource(('AttackBonus', 'Racial', 'Undead', 'Feat:FavoredEnemy'), 3)

    modifier.updateSource(('Str', 'Race', 'Orc'), 2)
    print(modifier.getSource(['Str'], {}))
    print(modifier.getSource(('Str'), {}))
    print(modifier.getSource([], {}))
    print(modifier.getSource(['Str', 'Race'], {}))
    print(modifier.getSource(['Str', 'NotExist'], {}))
    print(modifier.getSource(['NotExist', 'NotExist'], {}))

    modifier = Modifier({'ArmorClass': {'Natural': {'BaseArmor': 10, 'Race:YuantiPureblood': 1}, 'Dodge': {'Feat:Dodge': 1}, 'Dex': {'Ability:Dex': 3}, 'Tumble': {'Skills:Tumble': 3}}})
    print(modifier.sumSource('ArmorClass', {}))
