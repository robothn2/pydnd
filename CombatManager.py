#coding: utf-8
from Dice import rollDice
from Apply import *
from common import Props
import CalcResult

class CombatManager:
    def __init__(self, unit):
        self.owner = unit
        self.enemies = []
        self.enemyCur = None
        self.deltaInTurn = 0.0

    def addEnemy(self, enemy):
        if enemy not in self.enemies:
            self.enemies.append(enemy)

    def update(self, deltaTime):
        if len(self.enemies) == 0:
            return
        # search a living enemy
        enemy = None
        if self.enemyCur and not self.enemyCur.isDead():
            enemy = self.enemyCur
        else:
            for u in self.enemies:
                if not u.isDead():
                    enemy = u
                    break
        if not enemy:
            self.deltaInTurn = 0.0
            self.enemies = []
            print('no living enemy for', self.owner.getName())
            return

        tsBegin = self.deltaInTurn
        tsEnd = tsBegin + deltaTime
        self.deltaInTurn += deltaTime
        attacks = self.owner.calc.getPropValue('Attacks', self.owner, enemy)
        if self.deltaInTurn >= self.owner.ctx['secondsPerTurn']:
            self.deltaInTurn -= self.owner.ctx['secondsPerTurn']
            print('new turn for', self.owner.getName(), ', Attacks', attacks)

        # attack enemy
        for _, attack in enumerate(attacks):
            if attack[0] < tsBegin:
                continue
            if attack[0] > tsEnd:
                break
            self.meleeAttack(self.owner, enemy, attack)

    def meleeAttack(self, caster, target, attack):
        info = '{} attack:turnOffset({}) bab({}) {} weapon({}) {}'\
            .format(caster.getName(),
                    round(attack[0], 3), attack[1], attack[2], attack[3].getName(),
                    target.getName())
        roll = rollDice(1, 20, 1)
        info += ', roll: ' + str(roll)
        if roll == 1:
            print(info, ', missing')
            return False

        abFinal = attack[1] # bab from attack
        abFinal += caster.getAttackBonus(target) # ab from caster's Buff, Feats, Str
        dcCaster = roll + abFinal
        dcTarget = int(target.getArmorClass(caster))
        info += ', dc:{} against {}'.format(dcCaster, dcTarget)
        if roll < 20:
            if dcCaster < dcTarget:
                print(info, ', missing')
                return False

        print(info, ', hit', end=' ')
        damages = self.weapon_calc_damage(caster, target, roll, attack)
        target.applyDamages(damages)
        if target.isDead() and 'proto' in dir(target):
            xp = int(target.proto['xp'])
            # todo: XP penalty
            caster.addXP(xp)
        return True

    def weapon_calc_damage(self, caster, target, roll, attack):
        damages = CalcResult.Damages()

        hand = attack[2]
        dmgsCalc = caster.calc.getPropValue('Damage.' + hand, caster, target)
        print(dmgsCalc)
        for _,dmg in enumerate(dmgsCalc):
            damages.addSingleSource(dmg[0], dmg[1], dmg[2])

        # multiplier
        weapon = attack[3]
        rangeDiff, multipliers = weapon.getCriticalThreat()
        #print(rangeDiff, multipliers)
        if roll >= 20 - rangeDiff:
            if self.criticalCheck(caster, target, attack[0]):
                damages.addMultipliers(multipliers)
        return damages

    def criticalCheck(self, caster, target, bab):
        roll = rollDice(1, 20, 1)
        if roll == 1:
            return False

        dcCaster = roll + bab + caster.getAttackBonus(target)
        dcTarget = target.getArmorClass(caster)
        if roll < 20:
            if dcCaster < dcTarget:
                return False
        return True

    def castSpell(self, spellName, target):
        # spell failure check

        # spell concentration check

        # spell resistence check

        # instant spell, or spell channeling
        # apply spell effects
        #   spell dc against target saving throw
        #   effect immunity
        #   damage reduction

        # decrease spell charges

        pass
