#coding: utf-8
from Dice import rollDice
from Apply import *
from common import Props

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
        if self.owner.getProp('dead'):
            return

        if len(self.enemies) == 0:
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
            print('new turn for', self.owner.getProp('name'), 'Attacks', self.owner.modifier.getSource('Attacks'))

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
                    attack[0], attack[1], attack[2], attack[3].proto['name'],
                    target.getProp('name'))
        roll = rollDice(1, 20, 1)
        info += ', roll: ' + str(roll)
        if roll == 1:
            print(info, ', missing')
            return

        dcCaster = roll + caster.getProp('ab')
        dcTarget = int(target.getProp('ac'))
        info += ', dc:{} against {}'.format(dcCaster, dcTarget)
        if roll < 20:
            if dcCaster < dcTarget:
                print(info, ', missing')
                return

        damages = self.weapon_calc_damage(caster, target, roll, attack)
        target.applyDamages(damages)

    def weapon_calc_damage(self, caster, target, roll, attack):
        damages = Props.Modifier()

        # weapon base damage
        weaponProto = attack[3].proto
        weaponParams = weaponProto['BaseDamage']['params']
        weaponDmgType = weaponProto['BaseDamageType'][0] #todo: consider multi type
        weaponName = attack[3].props['name'] #todo: use weapon name, not base name
        damages.updateSource(('Type', weaponDmgType, weaponName), rollDice(weaponParams[0], weaponParams[1], weaponParams[2]))

        # multiplier
        criticalParams = attack[3].proto['BaseCriticalThreat']['params']
        if roll >= criticalParams[0]:
            if self.criticalCheck(caster, target):
                damages.updateSource(('Multiplier', 'Weapon'), criticalParams[2])

        # additional damage
        addtionalSources = caster.modifier.getSource(['Damage', 'Additional'])
        for dmgType, dmgSources in addtionalSources.items():
            damages.mergeBranch(('Type', dmgType), dmgSources)
        return damages

    def criticalCheck(self, caster, target):
        roll = rollDice(1, 20, 1)
        if roll == 1:
            return False

        dcCaster = roll + caster.getProp('ab')
        dcTarget = int(target.getProp('ac'))
        if roll < 20:
            if dcCaster < dcTarget:
                return False
        return True
