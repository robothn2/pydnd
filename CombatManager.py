#coding: utf-8
from Dice import rollDice
from Apply import *
from common import Props
import Damages

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
        if self.owner.isDead():
            return

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
            print('no living enemy for', self.owner.getProp('name'))
            return

        tsBegin = self.deltaInTurn
        tsEnd = tsBegin + deltaTime
        self.deltaInTurn += deltaTime
        if self.deltaInTurn >= self.owner.ctx['secondsPerTurn']:
            self.deltaInTurn -= self.owner.ctx['secondsPerTurn']
            print('new turn for', self.owner.getProp('name'), ', Attacks', self.owner.modifier.getSource('Attacks'))

        # attack enemy
        attacks = self.owner.modifier.getSource('Attacks')
        for _, attack in enumerate(attacks):
            if attack[0] < tsBegin:
                continue
            if attack[0] > tsEnd:
                break
            self.meleeAttack(self.owner, enemy, attack)

    def meleeAttack(self, caster, target, attack):
        info = '{} attack:turnOffset({}) bab({}) mainhand({}) weapon({}) {}'\
            .format(caster.getProp('name'),
                    round(attack[0], 3), attack[1], attack[2], attack[3].proto['name'],
                    target.getProp('name'))
        roll = rollDice(1, 20, 1)
        info += ', roll: ' + str(roll)
        if roll == 1:
            print(info, ', missing')
            return

        abFinal = attack[1] # bab from attack
        abFinal += caster.getAttackBonus(target) # ab from caster's Buff, Feats, Str
        weapon = attack[3]
        abFinal += weapon.getAttackBonus(target) # ab from weapon's Buff(MagicWeapon etc.), VS alignment, Enhancement
        dcCaster = roll + abFinal
        dcTarget = int(target.getArmorClass(caster))
        info += ', dc:{} against {}'.format(dcCaster, dcTarget)
        if roll < 20:
            if dcCaster < dcTarget:
                print(info, ', missing')
                return

        damages = self.weapon_calc_damage(caster, target, roll, attack)
        target.applyDamages(damages)
        if target.isDead() and 'proto' in dir(target):
            xp = int(target.proto['xp'])
            # todo: XP penalty
            caster.addXP(xp)

    def weapon_calc_damage(self, caster, target, roll, attack):
        damages = Damages.Damages()

        # weapon base damage
        weapon = attack[3]
        weaponProto = weapon.proto
        weaponParams = weaponProto['BaseDamage']['params']
        weaponDmgType = weaponProto['BaseDamageType'][0] #todo: consider multi damage type
        weaponName = weapon.props['name']
        damages.addSingleSource(weaponDmgType, weaponName, rollDice(weaponParams[0], weaponParams[1], weaponParams[2]))

        # multiplier
        rangeDiff, multipliers = weapon.getCriticalThreat()
        #print(rangeDiff, multipliers)
        if roll >= 20 - rangeDiff:
            if self.criticalCheck(caster, target, attack[0]):
                damages.addMultipliers(multipliers)

        # additional damage
        damages.addModifierSources(caster.modifier, ['Damage', 'Additional'])
        # conditional damage
        damages.addConditionalTargetSources(caster.modifier, caster, target)
        return damages

    def criticalCheck(self, caster, target, bab):
        roll = rollDice(1, 20, 1)
        if roll == 1:
            return False

        dcCaster = roll + bab + caster.getAttackBonus(target)
        dcTarget = target.getArmorClass(target)
        if roll < 20:
            if dcCaster < dcTarget:
                return False
        return True
