#coding: utf-8

from Dice import rollDice

class CombatManager:
    def __init__(self, unit):
        self.owner = unit
        self.enemies = []
        self.enemyCur = None

    def update(self, deltaTime):
        if self.owner.getProp('dead'):
            return

        # search a living enemy
        enemy = None
        if self.enemyCur and not self.enemyCur.getProp('dead'):
            enemy = self.enemyCur
        else:
            for u in self.enemies:
                if not u.getProp('dead'):
                    enemy = u
                    break

        # attack enemy
        if enemy:
            self.meleeAttack(self.owner, enemy)
        else:
            print('no enemy for', self.owner.getProp('name'))

    def addEnemy(self, enemy):
        if enemy not in self.enemies:
            self.enemies.append(enemy)

    def meleeAttackCheck(self, caster, target):
        roll = rollDice(1, 20, 1)
        if roll == 1:
            return False

        dcCaster = roll + caster.getProp('ab')
        dcTarget = int(target.getProp('ac'))
        if roll < 20:
            if dcCaster < dcTarget:
                return False
        return True

    def meleeAttack(self, caster, target):
        roll = rollDice(1, 20, 1)
        if roll == 1:
            print(caster.getProp('name'), 'melee attack', target.getProp('name'), ', roll: ', roll, ', missing')
            return

        dcCaster = roll + caster.getProp('ab')
        dcTarget = int(target.getProp('ac'))
        if roll < 20:
            if dcCaster < dcTarget:
                print(caster.getProp('name'), 'melee attack', target.getProp('name'),
                      ', dc: ', dcCaster, 'against', dcTarget,
                      ', missing')
                return

        damagesByType = self.calcMeleeDamage(caster, target, roll)
        print(caster.getProp('name'), 'melee attack', target.getProp('name'),
              ', dc: ', dcCaster, 'against', dcTarget,
              ', damage: ', damagesByType)

        damageTotal = 0
        for dmg in damagesByType.values():
            damageTotal += int(dmg)

        target.applyDamage(damageTotal)

    def calcMeleeDamage(self, caster, target, roll):
        dmgParams = caster.modifier.getSource(('MeleeDamage', 'MainHand', 'BaseDamage'), [1,4,2])
        #print(dmgParams)
        dmg = rollDice(dmgParams[0], dmgParams[1], dmgParams[2])
        dmg += caster.modifier.sumSource('MeleeDamage', ['Additional'])
        criticalParams = caster.modifier.getSource(('MeleeDamage', 'MainHand', 'CriticalThreat'), [20,20,2])
        if roll >= criticalParams[0]:
            if self.meleeAttackCheck(caster, target):
                dmg *= criticalParams[2]

        dmg *= caster.modifier.getSource(('MeleeDamage', 'FinalFactor'), 1.0)
        return {caster.modifier.getSource(('MeleeDamage', 'MainHand', 'DamageType'), 'Bludgeoning'): dmg}
