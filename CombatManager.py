#coding: utf-8

from Dice import rollDice
#from Character import Character
#from Creature import Creature

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

    def meleeAttack(self, caster, target):
        roll = rollDice(1, 20, 1)
        if roll == 1:
            print(caster.getProp('name'), 'melee attack', target.getProp('name'), ', roll: ', roll, ', missing')
            return

        dcCaster = roll + caster.getProp('FinalAttackBonus')
        dcTarget = int(target.getProp('ac'))
        if roll < 20:
            if dcCaster < dcTarget:
                print(caster.getProp('name'), 'melee attack', target.getProp('name'),
                      ', dc: ', dcCaster, 'against', dcTarget,
                      ', missing')
                return

        damagesByType = self.calcMeleeDamage(caster, target)
        print(caster.getProp('name'), 'melee attack', target.getProp('name'),
              ', dc: ', dcCaster, 'against', dcTarget,
              ', damage: ', damagesByType)

        damageTotal = 0
        for dmg in damagesByType.values():
            damageTotal += int(dmg)

        target.applyDamage(damageTotal)

    def calcMeleeDamage(self, caster, target):
        #if isinstance(caster, Character):
            return {'Piercing': 0, 'Slashing': 8, 'Bludgeoning': 0}
        #return {'Bludgeoning': 4}